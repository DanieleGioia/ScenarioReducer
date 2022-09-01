from abc import abstractmethod
'''
@author: Daniele Giovanni Gioia
@date:3/06/2022
@copyright: Copyright 2022, Politecnico di Torino, IT
'''
class Scenario_reducer():
    '''
    Abstract class for a scenario reducer that,
    given a fixed n, reduces an original set of scenarios
    with cardinality N to a smaller one of cardinality n.

    Different strategies can vary, for example, w.r.t.:
    -The statistical distance.
    -The selection order (Fast forward, backward, simultaneous backward, ...).

    For further details, please refer to:
    [1] Heitsch, Holger, and Werner Römisch. "Scenario reduction algorithms in stochastic programming." Computational optimization and applications 24.2-3 (2003): 187-206.
    '''
    @abstractmethod
    def __init__(self, initialSet, initProbs):
        """
        The initial set is assumed to have a dimension d x N,
        where N is the number of the initial set of scenarios
        """    
    @abstractmethod
    def reduce(self,distance, n_scenarios: int = 1):
        """
        reduces the initial set of scenarios

        distances allowed so far: 1,2,np.inf
        """   
        pass
