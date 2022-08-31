from .scenario_reducer import Scenario_reducer
import numpy as np
'''
@author: Daniele Giovanni Gioia
@date:3/06/2022
@copyright: Copyright 2022, Politecnico of Turin, IT
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
        dist_mtrx = np.zeros((self.N,self.N))
        #check on the mtrx
        if not distance in [1,2,np.inf]:
            raise ValueError('distance not allowed')
        for i in range(self.N):
            for j in range(self.N):
                dist_mtrx[i,j] = np.linalg.norm( self.initialSet[:,i] - self.initialSet[:,j],distance )
        #### 
        J_set = np.arange(self.N)
        ##Step 1
        zeta = np.zeros(self.N)
        for u in J_set:
            tmpProb = probs_initial[u]
            probs_initial[u] = 0 #set zero that element
            zeta[u] = probs_initial @ dist_mtrx[:,u]
            probs_initial[u] = tmpProb #restore the element
        ##first indx
        indxR.append(np.nanargmin(zeta))
        ####
        ##Step i
        for it in range(n_scenarios-1): #we already did the first
            zeta = np.zeros(self.N) #new zeta
            probs_initial[indxR] = 0 #set zero chosen elements
            #new J_set
            J_set = np.setdiff1d(J_set,indxR[-1]) # remove the last selected item
            for u in J_set:
                tmpProb = probs_initial[u]
                probs_initial[u] = 0 #set zero that element
                zeta[u] = probs_initial @ dist_mtrx[:,u]
                probs_initial[u] = tmpProb #restore the element
            #new selection
            zeta[indxR] = np.nan #eliminated indx
            indxR.append(np.nanargmin(zeta))
        J_set = np.setdiff1d(J_set,indxR[-1])#last removed
        #### 
        ##Probabilities redistribution
        probs_initial = self.initProbs.copy()  #re_int
        probs_reduced = probs_initial[indxR] #probabilities in the reduced set
        #closest scenario selection
        #set diag NaN oth it would be the minimum
        dist_mtrx[np.arange(self.N),np.arange(self.N)] = np.nan
        indx_closest = lambda x: np.nanargmin(dist_mtrx[x,indxR])
        for toDelete in J_set:
            probs_reduced[indx_closest(toDelete)] += probs_initial[toDelete]
        #new probs check
        if round(np.sum(probs_reduced),2) != 1:
            raise ValueError('new Probs must sum to one')
        #returns the reduced set and the respective probabilities
        return self.initialSet[:,indxR],probs_reduced
