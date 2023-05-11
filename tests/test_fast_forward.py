from typing import Any
import numpy as np
import pytest
from scipy.stats import norm
from statsmodels.stats.weightstats import DescrStatsW
from scenarioReducer import Fast_forward

'''
@author: pdb567
@date:11/05/2022

Run from cmd with print option: pytest -s test_fast_forward.py
'''

class NormalScenarioGenerator:
    def __init__(self, loc=0, scale=1, seed=47):
        self.loc = loc
        self.scale = scale
        self.seed = seed

    def make_scenarios(self, n_scenarios=500, seed=None):
        if seed is None:
            seed = self.seed
        rng = np.random.default_rng(seed)
        y = rng.normal(self.loc, self.scale, (1, n_scenarios))
        return y
    
    @property
    def rv(self):
        return norm(self.loc, self.scale)
    
    def __getattr__(self, __name: str) -> Any:
        # Forward other attributes to rv
        return self.rv.__getattribute__(__name)


@pytest.fixture(scope="module")
def scenario_generator():
    gen = NormalScenarioGenerator()
    return gen


def test_fast_forward_stats(scenario_generator):
    """
    Verify that reduced scenario set has similar statistical properties to
    the original scenario set.
    """
    n_scenarios_original = 1000
    scenario_reduction_factor = 5

    y = scenario_generator.make_scenarios(n_scenarios_original)
    FFreducer = Fast_forward(y, np.ones(y.shape[1])/y.shape[1])
    y_reduced, y_reduced_probs = FFreducer.reduce(np.inf, n_scenarios_original // scenario_reduction_factor)
    
    d_original = DescrStatsW(data=y.T)
    d_reduced = DescrStatsW(data=y_reduced.T, weights=y_reduced_probs)

    print_comparative_stats(d_original, d_reduced)

    # Since we are dealing with random samples, tolerances cannot be too tight.
    # Using larger scenario sets will be more accurate, but then the test takes a long time.
    np.testing.assert_allclose(d_original.mean, d_reduced.mean, rtol=1e-3, atol=1e-2)
    np.testing.assert_allclose(d_original.std, d_reduced.std, rtol=1e-2, atol=1e-4)
    q = [0.05, 0.5, 0.95]
    np.testing.assert_allclose(d_original.quantile(q), d_reduced.quantile(q), rtol=1e-2, atol=1e-3)


def print_comparative_stats(d1, d2):
    compare_list = {
        'd1': d1,
        'd2': d2,
    }

    stats = [
        ('mean',),
        ('std',),
        ('quantile', 0.05),
        ('quantile', 0.5),
        ('quantile', 0.95),
    ]

    for s in stats:
        if len(s) == 1:
            s_txt = s[0]
            for descr, d in compare_list.items():
                print(f'{descr:10} {s_txt} = {d.__getattribute__(s[0]).item():.5f}')
        else:
            s_txt = f'{s[0]}({s[1]})'
            for descr, d in compare_list.items():
                print(f'{descr:10} {s_txt} = {d.__getattribute__(s[0])(s[1], return_pandas=False).item():.5f}')