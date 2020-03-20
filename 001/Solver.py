from DiscretePongMDP import *
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit


NumEpisodes = 5000
MaxTimeSteps = 50000
tracker = np.zeros((int(NumEpisodes/100)+1,2))


qTable = np.zeros((18,17,18,9,9,2)) #p, x, y, x., y., a
learningRate = 0.05
explorationRate = 0.05
discountFactor = 0.99

stepBuffer = 0

def epsilonGreedy(epsilon, s):
    if (np.random.rand() > epsilon):
        actions = qTable[s][:]
        return np.argmax(actions)
    else:
        return randint(0,1)

def getLearningRate(episode):
    return np.max([0.8 * np.power(0.9992, episode), 0.02])
    #return 0.05 + 0.5 * (0.5 - 0.05) * (1 + np.cos(np.mod(episode, 1000) / 1000 * np.pi))
    return 0.1

def getExplorationRate(episode):
    return np.max([0.5 * np.power(0.9992, episode), 0.02])
    #return 0.05 + 0.5 * (0.4 - 0.05) * (1 + np.cos(np.mod(episode, 1000) / 1000 * np.pi))
    return 0.1
hits = 0
best = 500
for episode in range(0, NumEpisodes+1):
    #Begin Episode
    step = 0
    MDP = DiscretePongMDP(qTable.shape[0], qTable.shape[1], qTable.shape[2], qTable.shape[3], qTable.shape[4], 20, 20)
    s, r, running, temp = MDP.update(2)
    learningRate = getLearningRate(episode)
    explorationRate = getExplorationRate(episode)
    while(running and step < MaxTimeSteps):
        step = step + 1  
        #Action Selection
        a = epsilonGreedy(explorationRate, s)
        #Exicute Action
        ns, r, running, hit = MDP.update(a)
        hits += hit 
        #Update Equation       
        qTable[s][a] = qTable[s][a] + learningRate * (r + discountFactor * np.max(qTable[ns][:]) - qTable[s][a])           
        #Update State
        s = ns

    if (step > best):
        np.save('q_table.npy', qTable)
        best = step
        print("New best: " + str(best))

    stepBuffer = stepBuffer + step
    if (np.mod(episode, 100) == 0):
        tracker[int(episode/100), 0] = hits/100
        tracker[int(episode/100), 1] = episode
        print("Average for previous 100 episodes = " + str(stepBuffer/100) + "  -  " + str(hits/100) + "  -  " + str(episode))
        stepBuffer = 0
        hits = 0

#np.save('q_table.npy', qTable)

sns.set_style("darkgrid")

plt.figure()
df = pd.DataFrame({'Avg Rally': tracker[:, 0], 'Episodes': tracker[:, 1]})


ax = sns.lineplot(x="Episodes", y="Avg Rally", data=df).set_title("Q-Learning Agent Training")

plt.show()

        


    