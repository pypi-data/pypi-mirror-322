# CSMHP
This package is an implementation of:<br />
Cluster-based Superposed Marked Hawkes Process (CIBer)  <br />



The `CSMHP` package implements a novel Hawkes process model in PyTorch for modeling event sequence with high dimension of covariates, especially categorical ones. This model is useful in various fields such as finance, healthcare, and cyber-risk analysis, where temporal event sequences need to be modeled and analyzed. The package allows training a Hawkes process with clustering-based probability estimates.

## Features

- **Hawkes Process Model**: A self-exciting point process that models events whose intensity is influenced by prior events.
- **Clustering Model Integration**: Integrates clustering algorithms to infer event type probabilities.
- **Parameter Optimization**: Supports optimization of the model parameters (`mu`, `gamma`, `alpha_kernel`, `beta_kernel`) using gradient-based methods.
- **Event Simulation**: Implements the thinning algorithm for simulating future event times based on the trained model.
- **Mini-batch Optimization**: Option for mini-batch optimization to handle large datasets efficiently.

## Installation

To install the `CSMHP` package, you can use `pip`:

```bash
pip install CSMHP

```python
import torch
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from CSMHP import CSM_Hawkes

# Initialize parameters
T = 1000  # Length of observation window
num_clusters = 3  # Number of event clusters
params = None  # Optionally provide initial parameters
X_train = np.random.rand(100, 5)  # Example training data with 100 events and 5 features
y_train = np.random.randint(0, num_clusters, size=100)

# Define a clustering model (e.g., KMeans)
cluster_model = RandomForestClassifier(n_estimators=50, max_depth=2)
cluster_model.fit(X_train, y_train)
probability = cluster_model.predict(X_train)

# Initialize CSM_Hawkes model
hawkes_model = CSMHP(T=T, num_clusters=num_clusters, params=params, 
                          model=cluster_model, X_train=X_train, step=0.01, unit='Week')

# Fit the model (train the probability and parameters)
event_times = np.random.rand(100) * T  # Example event times
hawkes_model.fit_param(event_times, probability epoch=20)
hawkes_model.fit_prob(event_times, probability, step=0.5, epoch=5)
hawkes_model.fit_param(event_times, None, epoch=20)
hawkes_model.fit_prob(event_times, None, step=0.5, epoch=5)
hawkes_model.fit_param(event_times, None, epoch=10)

