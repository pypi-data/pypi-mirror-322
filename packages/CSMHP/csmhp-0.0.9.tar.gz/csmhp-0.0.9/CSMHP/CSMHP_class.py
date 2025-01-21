import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .optimize_wrapper import MinimizeWrapper


class CSMHP(torch.nn.Module):
    
    def __init__(self, T, num_clusters, params, model, X_train, step=3, unit='Week', mini_batch = False, batch_input = False, printer = False):
        super(CSMHP, self).__init__()
        """
        Args:
            T: Scalar
                length of the observation window
            num_classes: Scalar
                number of event types
            params: Dict
                parameters for the Hawkes process
            step: Scalar
                step size for optimization
            model: Object
                clustering model, machine learning models for cluster inference
            X_train: Tensor of shape (num_events, num_features)
                training data, used for cluster inference
            step: Scalar
                step size for optimization (Probability)
            unit: String
                the unit of time, default is 'Week'
            mini_batch: Boolean
                whether to use mini-batch optimization
        """
        self.T = T
        self.unit_name = unit
        if self.unit_name == 'Week':
            self.unit = 7
        self.num_classes = num_clusters
        self.printer = printer

        if params is None:
            # Initialize parameters randomly
            if batch_input:
                self.mu = torch.ones(num_clusters)/num_clusters#torch.rand(num_clusters)
                self.gamma = torch.rand(num_clusters)/10
                self.alpha_kernel = torch.abs(torch.ones(num_clusters))/5 + torch.rand(num_clusters)/100
                  #torch.abs(torch.ones(num_clusters))     #
                self.beta_kernel =  torch.abs(torch.ones(num_clusters))/15 + torch.rand(num_clusters)/100  #torch.rand(num_clusters)
        
            else:
                self.mu = torch.rand(num_clusters)
                self.gamma = torch.rand(num_clusters)
                self.alpha_kernel = torch.rand(num_clusters) 
                self.beta_kernel = torch.rand(num_clusters)

        else:
            # Initialize parameters with given values
            # In this class, to ensure the positivity of the parameters, we use softplus function
            # Hence, if the parameters are inherented from the previous model, we need to transform them first
            # by using the inverse of softplus function: log(exp(x)-1)
            if isinstance(params['mu'], np.ndarray):
                #self.mu = torch.log(torch.exp(torch.from_numpy(params['mu']))-1)
                self.mu = torch.from_numpy(params['mu'])
                self.gamma = torch.from_numpy(params['gamma'])
                self.alpha_kernel = torch.from_numpy(params['alpha_kernel'])
                self.beta_kernel = torch.from_numpy(params['beta_kernel'])
                #self.alpha_kernel = torch.log(torch.exp(torch.from_numpy(params['alpha_kernel']))-1)
                #self.beta_kernel = torch.log(torch.exp(torch.from_numpy(params['beta_kernel']))-1)
            elif isinstance(params['mu'], torch.Tensor):
                #self.mu = torch.log(torch.exp(params['mu'])-1)
                self.mu = params['mu']  
                self.gamma = params['gamma']
                self.alpha_kernel = params['alpha_kernel']
                self.beta_kernel = params['beta_kernel']
                #self.alpha_kernel = torch.log(torch.exp(params['alpha_kernel'])-1)
                #self.beta_kernel = torch.log(torch.exp(params['beta_kernel'])-1)
            else:
                print('Invalid parameters')
                print('Please provide the parameters in the form of numpy array or torch tensor')

        # Initialize parameters as learnable parameters
        self.mu = torch.nn.Parameter(self.mu.double())
        self.gamma =  torch.nn.Parameter(self.gamma.double())
        self.alpha_kernel = torch.nn.Parameter(self.alpha_kernel.double())
        self.beta_kernel = torch.nn.Parameter(self.beta_kernel.double())

        # Initialize the cluster model, X_train, labels, device
        self.cluster_model = model
        self.batch_input = batch_input
        if batch_input:
            self.X_train = np.concatenate(X_train)
        else:
            self.X_train = X_train
        self.labels = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Initialize probability as a parameter with softmax to ensure it sums to 1
        # self.probabilities = torch.nn.Parameter(torch.rand(batch_size, num_classes))
        self.probability = None
        self.logits = None

        # Initialize the training status, training events, step size, epoch, mini_batch, trace
        self.is_trained = False
        self.train_events = None
        self.step = step
        self.epoch = None
        self.mini_batch = mini_batch
        self.trace = []
        print('The training way of probabliliy: mini_batch: ', self.mini_batch)

    def intensity_function(self, probability, t, event_times, is_test=False):

        """
        Args:
            probability: Tensor of shape (num_events, num_classes)
            t: Scalar or Tensor of shape (num_events, )
            event_times: Tensor of shape (num_events, )
        """
        probability = probability.to(self.device)
        # if is_test and self.is_trained:
        #     self.T = event_times[-1]

        def fill_triu(A, value):
            A = torch.tril(A, diagonal=-1)
            # Mask for the upper triangular part (excluding diagonal)
            A = A + torch.triu(torch.ones_like(A)) * value
            # Apply the value to the upper triangular elementse
            return A   

        if is_test and self.is_trained:
            event_times = torch.concatenate([self.train_events, event_times])

        intensity = 0
        # Transform the parameters to ensure the positivity by softplus function
        #mu = F.softplus(self.mu)
        #alpha_kernel = F.softplus(self.alpha_kernel)
        #beta_kernel = F.softplus(self.beta_kernel)

        # Allow for different input cases: single time, multiple times, and test case
        
        # Single time case
        if t.shape == torch.Size([]) and probability.shape == torch.Size([self.num_classes]):
            intensity = 0
            #baseline = torch.exp(self.mu + self.gamma * (t / self.T))
            baseline = self.mu + self.gamma * (t / self.T)
            excitation = torch.sum(self.alpha_kernel[:, None]  * torch.exp(-self.beta_kernel[:, None] * (t - event_times[event_times < t])), dim=1)
            intensity = (baseline + excitation) @ probability
        
        # Multiple times case (Training)
        elif len(t) > 1 and probability.shape[0]==len(t) and is_test==False:

            dt = event_times[:, None] - event_times[None, :]
            dt = fill_triu(-dt * self.beta_kernel[:, None, None], -1e20)
            lamb_c = torch.exp(torch.logsumexp(dt, dim=-1)) * self.alpha_kernel[:, None] + self.mu[:,None] + self.gamma[:, None] * t/self.T  # (N, T)
            intensity = torch.sum(lamb_c * probability.T, dim=0)

            if any(intensity < 0):
                print('error: negative intensity')
                #print(stop)
                
        # Multiple times case (Testing)
        elif len(t) > 1 and probability.shape[0]==len(t) and is_test:
            
            dt = event_times[:, None] - event_times[None, :]
            dt = fill_triu(-dt * self.beta_kernel[:, None, None], -1e20)
            lamb_c = (torch.exp(torch.logsumexp(dt, dim=-1)) * self.alpha_kernel[:, None])[:,-len(t):] + self.mu[:,None] + self.gamma[:, None] * t/self.T  # (N, T)
            intensity = torch.sum(lamb_c * probability.T, dim=0)

            if any(intensity < 0):
                print('error: negative intensity')
                #print(stop)
        return intensity
    
    def log_likelihood(self, probability, event_times, is_test=False):
        """
        ------------------------------------------------------------------------------------
        This function is used to calculate the negative log-likelihood of the Hawkes process
        ------------------------------------------------------------------------------------
        Args:
            self.batch_input: Boolean
                whether the input is batch input or not
                if True:
                    probability: List of Tensors of shape num_seq * (num_events, num_classes)
                    event_times: List of Tensors of shape num_seq * (num_events,)
                else:
                    probability: Tensor of shape (num_events, num_classes)
                    event_times: Tensor of shape (num_events,)    
            is_test: Boolean
                whether the input is test data or not
        Returns:
            Negative log-likelihood
        """
        #probability = probability.to(self.device)
        ll_total = 0
        idx = 0
        if self.batch_input:
            for i, event_time in enumerate(event_times):
                if len(event_time) == 0:
                    print('empty sequence')
                else:
                    n = len(event_time)
                    #print(Stop)
                    # Initialize the log likelihood
                    ll = torch.log(self.intensity_function(probability[idx:idx+n,:], event_time, event_time, is_test=is_test)).sum()

                    # Calculate time differences
                    t_diff = event_time[-1] - event_time[0]
                    t_squared_diff = event_time[-1]**2 - event_time[0]**2

                    #base_terms = torch.outer(t_diff, self.mu) + torch.outer(t_squared_diff, (self.gamma / 2 / self.T))
                    base_terms = t_diff * self.mu + t_squared_diff * (self.gamma / 2 / self.T)
                    # Calculate base term base_terms[j] = t_diff[j] * mu_c + t_squared_diff[j] * gamma_c / 2 / T

                    diff_j = event_time[-1] - event_time[:-1] 
                    exp_j = torch.exp(-self.beta_kernel[:, None]*diff_j) *(self.alpha_kernel/self.beta_kernel)[:, None]
                    exp_term = (-exp_j + (self.alpha_kernel/self.beta_kernel)[:, None]).sum(dim=1)

                    integral_part = (probability[i] @ (exp_term + base_terms)).sum() * (1.0/(len(event_time)))
                    #print('integral part: ', integral_part.item(), 'sum part: ', ll.item())

                    if integral_part.item() < 0:
                        print('invalid integral part', 'negative value')
                        print(stop)
                    idx += n
                    #print('integral part: ', integral_part.item(), 'sum part: ', ll.item(), 'total: ', -ll.item() + integral_part.item())
                    ll -= integral_part
                    ll_total += ll

            print('Negative log likelihood: ', ll_total.item())
            return ll_total    
          
        else:
            probability = probability.double().to(self.device)

            # Initialize the log likelihood
            ll = torch.log(self.intensity_function(probability, event_times, event_times, is_test=is_test)).sum()

            # Calculate time differences
            t_diff = event_times[-1] - event_times[0]
            t_squared_diff = event_times[-1]**2 - event_times[0]**2

            #base_terms = torch.outer(t_diff, self.mu) + torch.outer(t_squared_diff, (self.gamma / 2 / self.T))
            base_terms = t_diff * self.mu + t_squared_diff * (self.gamma / 2 / self.T)
            # Calculate base term base_terms[j] = t_diff[j] * mu_c + t_squared_diff[j] * gamma_c / 2 / T
            diff_j = event_times[-1] - event_times[:-1] 
            exp_j = torch.exp(-self.beta_kernel[:, None]*diff_j) *(self.alpha_kernel/self.beta_kernel)[:, None]
            exp_term = (-exp_j + (self.alpha_kernel/self.beta_kernel)[:, None]).sum(dim=1)

            integral_part = (probability@ (exp_term + base_terms)).sum() * (1.0/(len(event_times)))
            #print('integral part: ', integral_part.item(), 'sum part: ', ll.item())

            if integral_part.item() < 0:
                print('invalid integral part', 'negative value')
                print(stop)
            
            if self.printer:
                print('integral part: ', integral_part.item(), 'sum part: ', ll.item(), 'total: ', -ll.item() + integral_part.item())
            else:
                print('Negative log likelihood: ', -ll.item() + integral_part.item())
            
            ll -= integral_part
            
            return -ll  
    
    def fit_prob(self, event_times, probability=None, step=1, epoch=20):
        """
        --------------------------------------------------------------
        This function is used to train the probability of the Hawkes process
        The probability is equivalent trained through the logit, and then softmax to output the probability
        --------------------------------------------------------------
        Args:
            probability: Tensor of shape (num_events, num_classes)
            event_times: Tensor of shape (num_events,)

        Returns:
            None
        """   
        self.mu.requires_grad = False
        self.gamma.requires_grad = False
        self.alpha_kernel.requires_grad = False
        self.beta_kernel.requires_grad = False
        if self.logits is not None:
            self.logits.requires_grad = True

        if isinstance(probability, np.ndarray):
            probability = torch.from_numpy(probability)

        if isinstance(event_times, np.ndarray):
            event_times = torch.from_numpy(event_times)
        elif isinstance(event_times, list):
            if self.batch_input:
                None
            else:
                event_times = torch.tensor(event_times)
        elif isinstance(event_times, pd.Series):
            event_times = torch.tensor(event_times.values)

        if probability is not None:
            # logits = torch.log(probability)
            # self.logits =  torch.nn.Parameter(logits).to(self.device)
            if self.batch_input:
                logits = torch.log(torch.concatenate(probability))
            else:
                logits = torch.log(probability)
            self.logits =  torch.nn.Parameter(logits).to(self.device)            

        elif self.probability is None and probability is None:
            self.probability = torch.rand(len(event_times), self.num_classes)
            logits = torch.log(probability) 

        new_probability = torch.softmax(self.logits, dim = 1).to(self.device)
    
        # To implement mini-batch optimization: each time we only optimize partial logits variable
        #optimizer = torch.optim.Adam(self.parameters(), lr=self.step)
        optimizer = torch.optim.SGD(self.parameters(), lr=step)
        #optimizer = torch.optim.LBFGS(model.parameters(), lr=0.1, max_iter=20)

        batch_size = 32
        records = []
        #records.append(self.log_likelihood(new_probability, event_times).item())
        if self.batch_input:
            for epoch in range(epoch):  # Number of optimization steps
                # print(stop)
                optimizer.zero_grad()
                if self.mini_batch:
                    self.logits.requires_grad = True
                    # Disable gradient computation for the part we don't want to optimize
                    idx = torch.randint(0, len(self.logits), (len(self.logits)-batch_size,))
                    self.logits[idx].detach_()

                new_probability = torch.softmax(self.logits, dim = 1).to(self.device)
                loss = self.log_likelihood(new_probability, event_times)
                loss.backward()
                self.logits.grad[idx] = 0
                records.append(loss.item())
        
                optimizer.step()
                print(f'Epoch {epoch + 1}, Loss: {loss.item()}') 

        else:
            for epoch in range(epoch):  # Number of optimization steps
                # print(stop)

                if self.mini_batch:
                    self.logits.requires_grad = True
                    # Disable gradient computation for the part we don't want to optimize
                    idx = torch.randint(0, len(self.logits), (len(self.logits)-batch_size,))
                    self.logits[idx].detach_()

                optimizer.zero_grad()
                new_probability = torch.softmax(self.logits, dim = 1).to(self.device)
                loss = self.log_likelihood(new_probability, event_times)
                loss.backward()
                self.logits.grad[idx] = 0   
                records.append(loss.item())
                optimizer.step()
                print(f'Epoch {epoch + 1}, Loss: {loss.item()}') 

        new_probability = torch.softmax(self.logits, dim = 1).to(self.device)
        records.append(self.log_likelihood(new_probability, event_times).item())
        self.trace.append(records)
        new_probability = torch.softmax(self.logits,dim=1).detach().clone()
        new_label = torch.argmax(new_probability, dim=1)
        self.labels = new_label.to('cpu').numpy()
        self.cluster_model.fit(self.X_train, new_label.to('cpu').numpy())
        self.probability = torch.from_numpy(self.cluster_model.predict_proba(self.X_train))
        self.probability.to(self.device)
        logits = torch.log(self.probability+1e-6)
        self.logits =  torch.nn.Parameter(logits)#.to(self.device)
        self.logits.to(self.device)

        print("New Labels: ", np.unique(new_label.numpy(), return_counts=True))

    def project_parameters(self):
        # Ensure a + b * 1.3 > 0 element-wise using vectorized operations
        with torch.no_grad():
            mask = (self.mu + self.gamma * 1.3 < 0)  # Find where the constraint is violated
            self.gamma[mask] = (1e-6 - self.mu[mask]) / 1.3 

    def fit_param(self, event_times, probability= None, epoch=150):
        """
        --------------------------------------------------------------
        This function is used to train the parameters of the Hawkes process
        The parameters:
            mu: Tensor of shape (num_classes,)
            gamma: Tensor of shape (num_classes,)
            alpha_kernel: Tensor of shape (num_classes,)
            beta_kernel: Tensor of shape (num_classes,)
        --------------------------------------------------------------
        Args:
            event_times: Tensor of shape (num_events,)

        Returns:
            None
        """
        if isinstance(probability, np.ndarray):
            probability = torch.from_numpy(probability)

        if isinstance(event_times, np.ndarray):
            event_times = torch.from_numpy(event_times)
        elif isinstance(event_times, list):
            if self.batch_input:
                None
            else:
                event_times = torch.tensor(event_times)            
            #event_times = torch.tensor(event_times)
        elif isinstance(event_times, pd.Series):
            event_times = torch.tensor(event_times.values)

        if self.probability is None and probability is not None:
            if self.batch_input:
                self.probability = torch.concatenate(probability)  
            else:
                self.probability = probability

                    
        # set the parameters as the parameters to be optimized
        # I want each time to optimize hawkes parameters or probability exclusively
        # So I need to set the requires_grad to True or False
        self.mu.requires_grad = True
        self.gamma.requires_grad = True
        self.alpha_kernel.requires_grad = True
        self.beta_kernel.requires_grad = True
        if self.logits is not None:
            self.logits.requires_grad = False        
        #self.logits.requires_grad = False

        parameter_to_optimize = [param for param in self.parameters() if param.requires_grad]
        #optimizer = torch.optim.Adam(parameter_to_optimize, lr=0.01)
        bounds = [(0, None) for _ in range(self.num_classes)] + [(None, None) for _ in range(self.num_classes)] + [(0, None) for _ in range(self.num_classes)] + [(0, None) for _ in range(self.num_classes)]
        minimizer_args = dict(method='Nelder-Mead', bounds=bounds, options={'maxiter':10})
        minimizer_args['jac'] = False
        optimizer =MinimizeWrapper(parameter_to_optimize, minimizer_args)
        #optimizer = torch.optim.LBFGS(parameter_to_optimize, lr=0.1, history_size=10)
        records = []

        def closure():
            optimizer.zero_grad()
            loss = self.log_likelihood(self.probability, event_times)
            loss.backward()
            self.project_parameters()
            #records.append(loss.item())
            return loss
        # loss = self.log_likelihood(self.probability, event_times)
        # loss.backward()
        # records.append(loss.item())
        # optimizer.step(closure)

        for epoch in range(epoch):
            optimizer.zero_grad()
            loss = self.log_likelihood(self.probability, event_times)
            loss.backward()
            records.append(loss.item())
            #optimizer.step(closure)
            optimizer.step(closure)
            self.project_parameters()
            print(f'Epoch {epoch + 1}, Loss: {loss.item()}')
        # optimizer.step(closure)
        records.append(self.log_likelihood(self.probability, event_times).item())
        self.trace.append(records)

        print("Fitted Parameters:")
        print("Mu:",  self.mu.data)
        print("Gamma:", self.gamma.data)
        print("Alpha kernels:", self.alpha_kernel.data)
        print("Beta kernels:", self.beta_kernel.data)   
        print("logits exist: ", self.logits is not None)

    def predict_integrated(self, probability, event_times, interval):
        probability = probability.to(self.device)
        # Calculate the integrated intensity function
        n = len(event_times)
        
        # Calculate time differences t_diff[j] = t_{j+1} - t_j 
        t_diff = interval[1] - interval[0]
        t_squared_diff = interval[1]**2 - interval[0]**2
        


        base_terms = t_diff * self.mu + t_squared_diff * (self.gamma / 2 / self.T)
        # Calculate base term base_terms[j] = t_diff[j] * mu_c + t_squared_diff[j] * gamma_c / 2 / T
        exp_sum = torch.sum(-torch.exp(torch.outer((interval[1] - event_times), -self.beta_kernel))*(self.alpha_kernel/self.beta_kernel) + torch.exp(torch.outer((interval[0] - event_times), -self.beta_kernel))*(self.alpha_kernel/self.beta_kernel),axis=0)
        # Calculate the sum of the exponential terms, exp_sum[j] = sum_{i=1}^{j} alpha_c * exp(-beta_c * (t_{j+1} - t_i)) - alpha_c * exp(-beta_c * (t_j - t_i))
        n = probability.shape[0]
        
        if n == 0:
            integral_term = (exp_sum + base_terms).mean()
        else:
            integral_term = torch.sum(probability @ (exp_sum + base_terms)) * (1.0/n)

        if torch.isnan(integral_term):
            print(stop)
        if integral_term == 0.0:
            print(stop)

        return integral_term.item()
    
    def predict_error_ins(self, weekly_frequency):
        if self.is_trained == False:
            print("Please train the model first")
            return None
    
        # we divide the time into intervals uniformly, with equal length, if the self.unit is week, then we divide the time into weeks
        t_interval = [0.0 + 1 * i for i in range(len(weekly_frequency) + 1)]
        interval_num = len(weekly_frequency)

        predicted_counts = np.zeros(interval_num)
        collected_events = self.train_events
        collected_probability = self.probability

        for i in range(interval_num):
            collected_events = self.train_events[self.train_events < t_interval[i]]
            collected_probability =  self.probability #[self.train_events < t_interval[i]]
            predicted_counts[i] = self.predict_integrated(collected_probability, collected_events, [t_interval[i], t_interval[i+1]])

        true_count = weekly_frequency.iloc[:,1].to_numpy() 
        # plt.plot(true_count, label='True Count')
        # plt.plot(predicted_counts, label='Predicted Count')
        return np.mean((true_count - predicted_counts)**2), true_count, predicted_counts
    
    def predict_error_oos(self, weekly_frequency, test_probability, test_events):
        if self.is_trained == False:
            print("Please train the model first")
            return None
        if isinstance(test_probability, np.ndarray):
            test_probability = torch.from_numpy(test_probability)
    
        start = self.train_events[-1].item()
        # we divide the time into intervals uniformly, with equal length, if the self.unit is week, then we divide the time into weeks
        t_interval = [start + 1 * i for i in range(len(weekly_frequency)+1)]
        interval_num = len(weekly_frequency)

        predicted_counts = np.zeros(interval_num)
        collected_events = self.train_events.to(self.device)
        collected_probability = self.probability.to(self.device)
        self.probability = self.probability.to(self.device)
        self.train_events = self.train_events.to(self.device)
        test_events = test_events.to(self.device)
        test_probability = test_probability.to(self.device)

        for i in range(interval_num):
            # new collected events should be train + test[time<t_interval[i]], it should be torch tensor
            collected_events = torch.cat([self.train_events, test_events[test_events < t_interval[i]]])
            collected_probability =  torch.cat([self.probability, test_probability[test_events < t_interval[i]]], axis=0)
            predicted_counts[i] = self.predict_integrated(collected_probability, collected_events, [t_interval[i], t_interval[i+1]])

        true_count = weekly_frequency.iloc[:,1].to_numpy() 
        return np.mean((true_count[:40] - predicted_counts[:40])**2), true_count, predicted_counts
    
    def thinning_algorithm(self, X_train, end_time, start_time = None):

        """
        ---------------------------------------------------------------------------
        Modified thinning algorithm to simulate future events
        two stages process:
        1. Generate feature x from the training data
        2. Generate candidate event time based on the intensity function given x
        3. Calculate the actual intensity at the candidate time, probability for x and the probability of acceptance
        4. Accept/reject the candidate event
        5. Repeat the process until the end time is reached
        ---------------------------------------------------------------------------
        Args:   
            X_train: (pd.DataFrame)
                dataframe containing the features of training data 
            model: (object)
                trained model object (ML models)
            end_time: (float)
                time horizon
            max_marked_intensity: (float)
                maximum intensity of the marked process
            max_temp_intensity: (float)
                maximum intensity of the temporary process
            start_time: (float)
                starting time of the simulation
        Returns:
            future_events: (list)
                list containing the future event times
        """

        # t_space = np.linspace(0, end_time, 1000)
        # max_temp_intensity = 0
        # for t in t_space:
        #     candidate = self.intensity_function(t, self.cluster_model, X_train)
        #     max_temp_intensity = max(max_temp_intensity, candidate)
        
        max_temp_intensity = max(self.intensity_function(self.probability, self.train_events, self.train_events)).item()
        X_prob = torch.tensor([X_train.value_counts(normalize=True)[tuple(X_train.values[i])] for i in range(len(X_train))]).to(self.device)
        max_marked_intensity = max(self.intensity_function(self.probability, self.train_events, self.train_events)*X_prob).item()
            
        # print('max_intensity: ', max_marked_intensity)
        # print('max_temp_intensity: ', max_temp_intensity)
        
        empirical_prob = X_train.value_counts(normalize=True)
        # Empirical probability of each x
        
        idx_x = np.random.choice(len(X_train), size=10000, replace=True)
        x = X_train.iloc[idx_x]
        # First step: random select x

        sample_probability = torch.tensor(self.cluster_model.predict_proba(x.to_numpy())).to(self.device)
        # sample_probability is the corresponding conditional probability

        X_prob = np.zeros((10000))
        # X_prob save each of the probability(emipirical) for selecting x
        for i in range(10000):
            X_prob[i] = empirical_prob.loc[tuple(x.values[i])]
        
        self.simulate_event = self.train_events

        future_events = []
        if start_time is None:  
            current_time = self.train_events[-1]
        else:
            current_time = start_time

        i = 0
        while current_time < end_time:
            # Generate candidate event time
            i += 1
            u = np.random.uniform()
            inter_event_time = -np.log(u) / max_temp_intensity
            candidate_time = current_time + inter_event_time
            # sample possible candidate time interval for next arrival
            
            # Calculate the actual intensity at the candidate time, probability for x and the probability of acceptance
            intensity = self.intensity_function(sample_probability[i], candidate_time, self.simulate_event)
            acceptance_prob = intensity * X_prob[i] / (max_marked_intensity*1.2)
            # print(stop)
            # Accept/reject the candidate event
            if np.random.uniform() <= acceptance_prob:
                future_events.append(candidate_time.item())
                self.simulate_event = torch.cat((self.simulate_event, candidate_time.unsqueeze(0)))
                current_time = candidate_time
                
            if candidate_time > end_time:
                break

        return future_events

                

    def simulation_plot(self, X_train, t_test):
    
        occurs = []
        for i in range(1000):
            future_event_times = self.thinning_algorithm(X_train=X_train, end_time=t_test[-1])
            occurs.append(len(future_event_times))
        
        
        plt.hist(occurs, bins=10, edgecolor='black')
        # Adding title and labels
        plt.title('Histogram of Float Numbers')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.axvline(x = len(t_test), color = 'b', label = 'axvline - full height')
        # Display the plot
        plt.show()