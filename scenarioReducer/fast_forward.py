from .scenario_reducer import Scenario_reducer
import numpy as np
# Use numba if available
try:
    from numba import njit
except ImportError:
    def njit(*args, **kwargs):
        return lambda f: f

'''
@author: Daniele Giovanni Gioia
@date:3/06/2022
@copyright: Copyright 2022, Politecnico di Torino, IT
'''
class Fast_forward(Scenario_reducer):
    '''
    This class implements a scenario reducer that follows
    a Fast Forward (FF) technique.

    For further details, please refer to:
    [1] Heitsch, Holger, and Werner Römisch. "Scenario reduction algorithms in stochastic programming." Computational optimization and applications 24.2-3 (2003): 187-206.

    Please notice that FF is preferred for n<N/4, where n is the
    new reduced cardinality and N is the original one.
    '''
    def __init__(self, initialSet, initProbs):
        self.initialSet = initialSet
        self.N = initialSet.shape[1]
        self.initProbs = initProbs #room for generalization
        ###
        ###checks probs
        if initProbs.size != self.N:
            raise ValueError(' Probs and scenario must match')
        if round(np.sum(initProbs),2) != 1:
            raise ValueError('Probs must sum to one')

    def reduce(self,distance,n_scenarios: int = 1):
        """
        reduces the initial set of scenarios
        """
        indxR = [] #indeces of the reduced set
        probs_initial = self.initProbs.copy() 
        #### computation of the distance matrix
        #check on the mtrx
        if not distance in [1,2,np.inf]:
            raise ValueError('distance not allowed')
        dist_mtrx = compute_distance_matrix(self.initialSet, distance)
        dist_mtrx_original = dist_mtrx.copy()
        #### 
        J_set = np.arange(self.N)
        ##Step 1
        zeta = calculate_zeta(J_set, dist_mtrx, probs_initial)
        ##first indx
        u = np.nanargmin(zeta)
        indxR.append(u)
        ####
        ##Step i
        for it in range(n_scenarios-1): #we already did the first
            dist_mtrx = np.minimum(dist_mtrx, dist_mtrx[u, :])
            probs_initial[indxR] = 0 #set zero chosen elements
            #new J_set
            J_set = np.setdiff1d(J_set,indxR[-1]) # remove the last selected item
            zeta = calculate_zeta(J_set, dist_mtrx, probs_initial)
            #new selection
            u = np.argmin(zeta)
            indxR.append(u)
        J_set = np.setdiff1d(J_set,indxR[-1])#last removed
        #### 
        ##Probabilities redistribution
        probs_initial = self.initProbs.copy()  #re_int
        probs_reduced = redistribute_probs(np.array(indxR), probs_initial, dist_mtrx_original, J_set)
        # Alternate probability calculation, vectorized

        #new probs check
        if round(np.sum(probs_reduced),2) != 1:
            raise ValueError('new Probs must sum to one')
        #returns the reduced set and the respective probabilities
        return self.initialSet[:,indxR],probs_reduced


@njit(cache=True)
def compute_distance_matrix(initialSet, distance):
    N = initialSet.shape[1]
    dist_mtrx = np.zeros((N, N))
    for i in range(N): #sym matrix
            for j in range(i+1):
                dist_mtrx[i,j] = np.linalg.norm(initialSet[:,i] - initialSet[:,j],distance )
                dist_mtrx[j,i] = dist_mtrx[i,j]
    return dist_mtrx


@njit(cache=True)
def calculate_zeta(J_set, dist_mtrx, probs_initial):
    N = probs_initial.shape[0]
    zeta = np.ones(N)*np.inf
    for u in J_set:
        tmpProb = probs_initial[u]
        probs_initial[u] = 0  # set zero that element
        zeta[u] = probs_initial @ dist_mtrx[u, :]
        probs_initial[u] = tmpProb  # restore the element
    return zeta


# numba doesn't help this one since it spends its time in numpy vectorized functions
def redistribute_probs(indxR, probs_initial, dist_mtrx_original, J_set):
    N = probs_initial.shape[0]
    probs_reduced = np.zeros(len(indxR))
    #closest scenario selection

    dist_mtrx = dist_mtrx_original[:, indxR]
    indx_closest = np.argmin(dist_mtrx, axis=1)
    for u in range(len(indxR)):
        probs_reduced[u] += np.sum(probs_initial[indx_closest == u])
    return probs_reduced
