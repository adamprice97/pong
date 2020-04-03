
from AdverseDiscretePongMDP import *
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime

NumEpisodes = 50000
MaxTimeSteps = 50000

qTable1 = np.zeros((19,36,10,10,2)) #x, y, x., y., a = 64,800‬ (9.5x smaller)
qTable2 = np.zeros((19,36,10,10,2)) #high res 26,48,16,16  low res 18,36,10,10
MaxSpeed = 20
buffer = 2
learningRate = 0.05
explorationRate = 0.05
discountFactor = 0.99
messageBuff = 100

tracker = np.zeros(int(NumEpisodes/messageBuff)+1)
wintracker = np.zeros(int(NumEpisodes/messageBuff)+1)

stepBuffer = 0

print(str(datetime.datetime.now()))

def epsilonGreedy(epsilon, s, agent):
    if (np.random.rand() > epsilon):
        if (agent == 1):
            actions = qTable1[s][:]
        else:
            actions = qTable2[s][:]
        return np.argmax(actions)
    else:
        return randint(0,1)

def getLearningRate(episode):
    return 0.05 + 0.5 * (0.15 - 0.05) * (1 + np.cos(np.mod(episode, NumEpisodes) / NumEpisodes * np.pi))

def getExplorationRate(episode):
    return 0.01 + 0.5 * (0.2 - 0.01) * (1 + np.cos(np.mod(episode, NumEpisodes) / NumEpisodes * np.pi))
   
hits = 0
best = 1500
winBuffer = [0,0]
MDP = AdverseDiscretePongMDP(qTable1.shape[0], qTable1.shape[1], qTable1.shape[2], qTable1.shape[3], MaxSpeed, MaxSpeed)
for episode in range(0, NumEpisodes+1):
    #Begin Episode
    step = 0
    s, running = MDP.reset()
    learningRate = getLearningRate(episode)
    explorationRate = getExplorationRate(episode)
    while(running and step < MaxTimeSteps):
        step += buffer
        #Action Selection
        a1 = epsilonGreedy(explorationRate, s[0], 1)
        a2 = epsilonGreedy(explorationRate, s[1], 2)
        #Exicute Action
        ns, r, w, running, hit = MDP.update(a1, a2, buffer)
        hits += hit 
        #Update Equation       
        qTable1[s[0]][a1] = qTable1[s[0]][a1] + learningRate * (r[0] + discountFactor * np.max(qTable1[ns[0]][:]) - qTable1[s[0]][a1])  
        qTable2[s[1]][a2] = qTable2[s[1]][a2] + learningRate * (r[1] + discountFactor * np.max(qTable2[ns[1]][:]) - qTable2[s[1]][a2])  
        #Update States
        s = ns

    winBuffer[0] += w[0]
    winBuffer[1] += w[1]
    if (step > best):
        np.save('q_table1_best002.npy', qTable1)
        np.save('q_table2_best002.npy', qTable2)
        best = step
        print("New best: " + str(best))

    stepBuffer = stepBuffer + step
    if (np.mod(episode, messageBuff) == 0 and episode != 0):
        tracker[int(episode/messageBuff)] = hits/messageBuff
        wintracker[int(episode/messageBuff)] = winBuffer[0]
        print("Average for previous 100 episodes = " + str(stepBuffer/messageBuff) + "  -  " + str(hits/messageBuff) + "  -  " + str(episode) + "  -  " + str(winBuffer[0]) + "|" + str(winBuffer[1]))
        stepBuffer = 0
        hits = 0
        winBuffer = [0,0]

np.save('q_table1_end002.npy', qTable1)
np.save('q_table2_end002.npy', qTable2)
np.save('data_1_002.npy', tracker)
np.save('windata_1_002.npy', wintracker)

sns.set_style("darkgrid")
plt.plot(tracker)
plt.plot(wintracker)
plt.show()


        


    