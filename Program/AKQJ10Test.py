import pickle, random
from GameNode import KuhnNode

class KuhnTest():
    nodeMap: dict

    def read(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.nodeMap = pickle.load(f)

    # Plays the game against the strategy testNodeMap from a given history,
    # returns the utility of playing the simulated game.
    def test_play(self, testNodeMap: dict, history: str):
        cards = [1, 2, 3, 4, 5]
        random.shuffle(cards)
        plays = len(history)
        curr_player = plays % 2
        opponent = 1 - curr_player

        # Return payoff for terminal states
        if plays >= 1:
            terminalPass = history[plays-1] == 'p'
            doubleBet = history[plays - 2: plays] == 'bb'
            isPlayerCardHigher = cards[curr_player] > cards[opponent]
            if terminalPass:
                if history == 'p':
                    return 0
                else:
                    if isPlayerCardHigher:
                        return 0
                    else:
                        return 1
            elif doubleBet:
                if isPlayerCardHigher:
                    return 1
                else:
                    return -1

        # Keep playing if not terminal state
        infoSet = str(cards[curr_player]) + history
        if curr_player == 0:
            curr_strategy = self.nodeMap.get(infoSet).getAverageStrategy()
        else:
            curr_strategy = testNodeMap.get(infoSet).getAverageStrategy()
        r = random.random()
        if r < curr_strategy[0]:
            return -self.test_play(testNodeMap, history + 'p')
        else:
            return -self.test_play(testNodeMap, history + 'b')