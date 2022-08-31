from scenarioReducer import *
import numpy as np

#generate a scenario
initialScenario = np.random.rand(10,400) # dim 10, 400 scenarios
initialProbs = (1/400)*np.ones(400) #mass uniformly distr
#Class instance
FFreducer = Fast_forward(initialScenario,initialProbs)
#scenario reduction
newScenario,newProbs = FFreducer.reduce(2,5) #2norm, 5scenarios
print('W2_red')
print(newScenario)
print(newProbs)
#
newScenario,newProbs = FFreducer.reduce(np.inf,5) #Infnorm, 5scenarios
print('Winf_red')
print(newScenario)
print(newProbs)