import random
from typing import *
from GameNode import KuhnNode
import pickle, time
from AKQJ10Test import KuhnTest

NUM_ACTIONS = 2

nodeMap = {}

def continueTrain(file, iterations: int, saveName):
    kt = KuhnTest()
    kt.read(file)
    global nodeMap
    nodeMap = kt.nodeMap
    train(iterations, saveName)

def train(iterations: int, saveName):
    t1 = time.time()
    # We represent cards[0] as player 1 and cards[1] as player 2
    cards = [1, 2, 3, 4, 5]
    util = 0
    for i in range(1, iterations):
        # Shuffle Cards. Note that cards are shuffled before call to cfr,
        # chance node outcomes are pre-sampled.
        # This form of Monte Carlo CFR is called chance-sampling.
        random.shuffle(cards)
        util += cfr(cards, '', 1, 1)
        # Progress
        freq_print = 100000
        if i % (freq_print) == 0:
            if time.time() - t1 != 0.:
                print(f"Kuhn trained {i} iterations. {str(freq_print / (time.time() - t1))} iterations per second.")
            my = KuhnTest()
            my.nodeMap = nodeMap
            t1 = time.time()
    my = KuhnTest()
    my.nodeMap = nodeMap
    print("Strategy: ")

    for node in sorted(nodeMap.values()):
        print(node)

    # Save the trained algorithm
    with open(saveName, 'wb') as f:
        pickle.dump(nodeMap, f)

def cfr(cards: List[int], history: str, p0: float, p1: float) -> float:
    plays = len(history)
    curr_player = plays % 2

    infoSet = str(cards[curr_player]) + history

    curr_node = KuhnNode()
    curr_node.infoSet = infoSet
    payoff = curr_node.returnPayoff(cards)
    terminalNode = payoff is not None

    # Return payoff for terminal states
    if terminalNode:
        return payoff

    # Get information set node or create it if nonexistent
    curr_node = nodeMap.get(infoSet)
    if curr_node is None:
        curr_node = KuhnNode()
        curr_node.infoSet = infoSet
        nodeMap[infoSet] = curr_node

    # For each action, recursively call cfr with additional history and probability
    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)
    util = [0] * NUM_ACTIONS

    # nodeUtil is the weighted average of the cfr of each branch,
    # weighted by the probability of traversing down a branch
    nodeUtil = 0
    for a in range(NUM_ACTIONS):
        nextHistory = history + ('p' if a == 0 else 'b')
        # The first probability is player 1's counterfactual probability
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        # Current player is 1
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    # For each action, compute and accumulate counterfactual regret
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil

if __name__ == '__main__':
    import time
    start_time = time.time()
    train(10 ** 6, "kt-10")
    # continueTrain('kt-30Mp', 170*10**6, 'kt-200M')
    print("--- %s seconds ---" % (time.time() - start_time))
