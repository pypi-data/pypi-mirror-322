import torch
import numpy as np
from scipy.optimize import (
        minimize, 
        basinhopping, 
        brute, 
        differential_evolution, 
        shgo,
        dual_annealing
        )
import functools
from copy import deepcopy


# thanks to https://stackoverflow.com/a/31174427/6937913
# recursively set attributes
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

def rdelattr(obj, attr):
    pre, _, post = attr.rpartition('.')
    return delattr(rgetattr(obj, pre) if pre else obj, post)

# generic float casting
def floatX(x, np_to, torch_to):
    if isinstance(x, np.ndarray):
        return x.astype(np_to)
    elif isinstance(x, torch.Tensor):
        return x.to(torch_to)
    elif isinstance(x, float):
        return np_to(x)
    else:
        raise ValueError('Only numpy arrays and torch tensors can be cast to'
                f'float, not {x} of type {type(x)}')

float32 = functools.partial(floatX, np_to=np.float32, torch_to=torch.float32)
float64 = functools.partial(floatX, np_to=np.float64, torch_to=torch.float64)


class MinimizeWrapper(torch.optim.Optimizer):
    def __init__(self, params, minimizer_args):
        assert type(minimizer_args) is dict
        if 'jac' not in minimizer_args:
            minimizer_args['jac'] = True
        assert minimizer_args['jac'] in [True, False], \
                "separate jac function not supported"
        params = self.set_floatX(params)
        self.jac_methods = ["CG", "BFGS", "L-BFGS-B", "TNC", "SLSQP"]
        self.hess_methods = ["Newton-CG", "dogleg", "trust-ncg",
                             "trust-krylov", "trust-exact", "trust-constr"]
        self.gradfree_methods = ["Nelder-Mead", "Powell", "COBYLA"]
        method = minimizer_args['method']
        if method in self.jac_methods:
            self.use_hess = False
        elif method in self.hess_methods:
            self.use_hess = True
        elif method in self.gradfree_methods:
            self.use_hess = False
            assert minimizer_args['jac'] == False, \
                "set minimizer_args['jac']=False to use gradient free algorithms"
        else:
            raise ValueError(f"Method {method} not supported or does not exist")
        self.minimizer_args = minimizer_args
        if 'options' not in self.minimizer_args:
            self.minimizer_args.update({'options':{}})
        if 'maxiter' not in self.minimizer_args['options']:
            self.minimizer_args['options'].update({'maxiter':2})
        super(MinimizeWrapper, self).__init__(params, self.minimizer_args)
        assert len(self.param_groups) == 1, "only supports one group"

    def set_floatX(self, params):
        params = [p for p in params]
        if all(p.dtype == torch.float32 for p in params):
            self.floatX = float32
        elif all(p.dtype == torch.float64 for p in params):
            self.floatX = float64
        else:
            raise ValueError('Only float or double parameters permitted')
        return params

    def ravel_pack(self, tensors):
        # pack tensors into a numpy array
        def numpyify(tensor):
            if tensor.device != torch.device('cpu'):
                tensor = tensor.cpu()
            return tensor.detach().numpy()
        x = np.concatenate([numpyify(tensor).ravel() for tensor in tensors], 0)
        x = self.floatX(x)
        return x

    def np_unravel_unpack(self, x):
        x = torch.from_numpy(self.floatX(x))
        return self.unravel_unpack(x)

    def unravel_unpack(self, x):
        # unpack parameters from a numpy array
        _group = next(iter(self.param_groups))
        _params = _group['params'] # use params as shape reference
        i = 0
        params = []
        for _p in _params:
            j = _p.numel()
            p = x[i:i+j].view(_p.size())
            p = p.to(_p.device)
            params.append(p)
            i += j
        return params

    def minimize(self, func, x0, **minimizer_args):
        return minimize(func, x0, **minimizer_args)

    @torch.no_grad()
    def step(self, closure):

        group = next(iter(self.param_groups))
        params = group['params']

        def torch_wrapper(x, return_grad=False, *args):
            # monkey patch set parameter values
            _params = self.np_unravel_unpack(x)
            for p, _p in zip(params, _params):
                p.data = _p
            with torch.enable_grad():
                loss = closure()
                loss = self.floatX(loss.item())
            if return_grad:
                grads = self.ravel_pack([p.grad for p in params])
                return loss, grads
            else:
                return loss
        if self.minimizer_args['jac']:
            torch_wrapper = functools.partial(torch_wrapper, return_grad=True)

        if hasattr(closure, 'model') and self.use_hess:
            def hess(x):
                model = deepcopy(closure.model)
                with torch.enable_grad():
                    x = self.floatX(torch.tensor(x)).requires_grad_()
                    def f(x):
                        _params = self.unravel_unpack(x)
                        # monkey patch substitute variables
                        named_params = list(model.named_parameters())
                        for _p, (n, _) in zip(_params, named_params):
                            rdelattr(model, n)
                            rsetattr(model, n, _p)
                        return closure.loss(model)
                    def numpyify(x):
                        if x.device != torch.device('cpu'):
                            x = x.cpu()
                        #return x.numpy().astype(np.float64)
                        return self.floatX(x.numpy())
                    return numpyify(torch.autograd.functional.hessian(f, x))
        else:
            hess = None

        # run the minimizer
        x0 = self.ravel_pack(params)
    
        self.res = self.minimize(torch_wrapper, x0, hess=hess, **self.minimizer_args)

        # set the final parameters
        _params = self.np_unravel_unpack(self.res.x)
        for p, _p in zip(params, _params):
            p.data = _p


class BasinHoppingWrapper(MinimizeWrapper):
    def __init__(self, params, minimizer_args, basinhopping_kwargs):
        self.basinhopping_kwargs = basinhopping_kwargs
        super().__init__(params, minimizer_args)

    def minimize(self, func, x0, **minimizer_args):
        return basinhopping(func, x0, minimizer_kwargs=minimizer_args,
                **self.basinhopping_kwargs)


class DifferentialEvolutionWrapper(MinimizeWrapper):
    def __init__(self, params, de_kwargs):
        self.minimizer_args = {'jac': False}
        self.de_kwargs = de_kwargs
        params = self.set_floatX(params)
        super(MinimizeWrapper, self).__init__(params, self.minimizer_args)

    def minimize(self, func, x0, hess, **kwargs):
        return differential_evolution(func, **self.de_kwargs)


class SHGOWrapper(MinimizeWrapper):
    def __init__(self, params, minimizer_args, shgo_kwargs):
        minimizer_args.update({'jac': False})
        self.shgo_kwargs = shgo_kwargs
        super().__init__(params, minimizer_args)

    def minimize(self, func, x0, **minimizer_args):
        def jac_fun(x, *args):
            return func(x, True)[1]
        def obj_fun(x, *args):
            return func(x, False)
        minimizer_args['jac'] = jac_fun
        return shgo(obj_fun, minimizer_kwargs=minimizer_args,
                    args=[False],
                    **self.shgo_kwargs)


class DualAnnealingWrapper(MinimizeWrapper):
    def __init__(self, params, minimizer_args, da_kwargs):
        minimizer_args.update({'jac': False})
        self.da_kwargs = da_kwargs 
        super().__init__(params, minimizer_args)

    def minimize(self, func, x0, **minimizer_args):
        jac_fun = lambda x: func(x, True)[1]
        minimizer_args['jac'] = jac_fun
        return dual_annealing(func, local_search_options=minimizer_args,
                args=[False],
                **self.da_kwargs)