import time
from AKQJ10Game import KuhnGame
from AKQJ10Trainer import train, continueTrain
import matplotlib.pyplot as plt
import numpy as np

# Train a game tree from scratch
train(iterations=10 ** 6, saveName="kt-10M")


# Play against trained game tree
game = KuhnGame()
game.read("kt-10M")

p1_hrhr = [1, 0, 0, 1, 1]
p2_hrhr = [0, 1, 1, 1, 1]

iterations = 10**6

print("Number of Games: " + str(iterations))
print("==========================================")
print("Player 1: Strategy: High Risk High Reward")
win1 = game.playAI(iterations=iterations, go_first=True, probability=p1_hrhr)
print("Player 2: Strategy: High Risk High Reward")
win2 = game.playAI(iterations=iterations, go_first=False, probability=p2_hrhr)

p1_safe = [0, 0, 1, 1, 1]
p2_safe = [0, 0, 0, 1, 1]

print("Player 1: Strategy: Playing It Safe")
win3 = game.playAI(iterations=iterations, go_first=True, probability=p1_safe)
print("Player 2: Strategy: Playing It Safe")
win4 = game.playAI(iterations=iterations, go_first=False, probability=p2_safe)

print("Strategy: HRHR vs HRHR")
win5 = game.playStrats(iterations=iterations, probability1=p1_hrhr, probability2=p2_hrhr)
print("Strategy: SAFE vs SAFE")
win6 = game.playStrats(iterations=iterations, probability1=p1_safe, probability2=p2_safe)
print("Strategy: HRHR vs SAFE")
win7 = game.playStrats(iterations=iterations, probability1=p1_hrhr, probability2=p2_safe)
print("Strategy: SAFE vs HRHR")
win8 = game.playStrats(iterations=iterations, probability1=p1_safe, probability2=p2_hrhr)


X = ['HRHR vs AI','AI vs HRHR','SAFE vs AI','AI vs SAFE'] 
Ygirls = [win1[0],win2[0],win3[0],win4[0]] 
Zboys = [win1[1],win2[1],win3[1],win4[1]] 
  
X_axis = np.arange(len(X)) 
  
plt.figure(1)
plt.bar(X_axis - 0.2, Ygirls, 0.4, label = 'Win%') 
plt.bar(X_axis + 0.2, Zboys, 0.4, label = 'Loss%') 
  
plt.xticks(X_axis, X) 
plt.xlabel("Strategy") 

plt.ylabel("Percentage") 
plt.title("Strategy Performance vs AI") 
plt.legend() 
plt.show() 

X = ['HRHR vs HRHR','SAFE vs SAFE','HRHR vs SAFE','SAFE vs HRHR'] 
Ygirls = [win5[0],win6[0],win7[0],win8[0]] 
Zboys = [win5[1],win6[1],win7[1],win8[1]] 
 
X_axis = np.arange(len(X)) 
plt.figure(2)
plt.bar(X_axis - 0.2, Ygirls, 0.4, label = 'Win% P1') 
plt.bar(X_axis + 0.2, Zboys, 0.4, label = 'Loss% P1') 
  
plt.xticks(X_axis, X) 
plt.xlabel("Strategy") 

plt.ylabel("Percentage") 
plt.title("Strategy vs Strategy") 
plt.legend() 
plt.show() 