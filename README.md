# ScenarioReducer

This library implements several approximate scenario reduction algorithms. Given a probability distribution with finite support, they aim to determine a probability measure with support of reduced and fixed cardinality by selecting the closest to the original one in terms of a selected statistical distance.

For further details, please refer to:

```Bibtex
@article{Heitsch2003,
author = {Heitsch, Holger and R{\"o}misch, Werner},
date = {2003/02/01},
doi = {10.1023/A:1021805924152},
isbn = {1573-2894},
journal = {Computational Optimization and Applications},
number = {2},
pages = {187--206},
title = {Scenario Reduction Algorithms in Stochastic Programming},
url = {https://doi.org/10.1023/A:1021805924152},
volume = {24},
year = {2003}
}
```

## Code structure

```Bash
|____main_example.py
|____scenarioReducer
|____setup.py
| |____scenario_reducer.py
| |______init__.py
| |____fast_forward.py
|____tests
| |____test_fast_forward.py
```

### ScenarioReducer Class

It is an abstract class for a scenario reducer that suggests the methods that a scenario reducer should possess. The main method **reduce**,  given a fixed n, must reduce an original set of scenarios with cardinality N to a smaller one of cardinality n.

Different strategies can vary, for example, w.r.t.:

- The statistical distance.
- The selection order (Fast Forward, Backward, Simultaneous Backward, ...).

### Fast_forward class

This class implements a scenario reducer that follows a *Fast Forward* (FF) technique from:

[1] Heitsch, Holger, and Werner Römisch. "Scenario reduction algorithms in stochastic programming." Computational optimization and applications 24.2-3 (2003): 187-206.

FF is preferred for $n\le \frac{N}{4}$ , where $n$  is the new reduced cardinality of the support and $N$ is the original one.

### Example

An easy example to familiarize yourself with the library is provided in **main_example.py**

### Available tests

1. *test_fast_forward* creates a starting set of one-dimensional Gaussian distributed scenarios of known mean and variance. The test then uses the *Fast_Forward* class to reduce the number of scenarios. Mean, standard deviation, and 0.05, 0.5, and 0.95 quantiles are eventually compared between the original scenario set and the reduced scenario set to confirm that such statistical measures are close.
