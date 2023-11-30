from typing import Dict
import pickle, random
from GameNode import KuhnNode

class KuhnGame():
    AI: Dict

    def read(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.AI = pickle.load(f)

    def playStrats(self, iterations:int, probability1: list, probability2: list):
        winsP1 = 0
        lossP1 = 0
                      
        print("==========================================")
        for idx in range(0, iterations):
            cards = [1, 2, 3, 4, 5]

            random.shuffle(cards)
            # print(" Your card is: " + (str(cards[0]) if go_first else str(cards[1])))

            val = self.gameStrats(cards, '', probability1, probability2)
            
            if val>0:
                winsP1 = winsP1+1    
            elif val<0:
                lossP1 = lossP1+1

        print("Win%: " + str(round(winsP1/iterations*100,2)) + "%\nLoss%: " + str(round(lossP1/iterations*100,2)) + "%")
        print("==========================================")

        return [round(winsP1/iterations*100,2), round(lossP1/iterations*100,2)]

    def gameStrats(self, cards, history: str, probability1, probability2):
        while True:
            players = ["You", "AI"]
            plays = len(history)
            AI_turn = (plays % 2 == 1)
            curr_player = plays % 2
            opponent = 1 - curr_player
            
            if plays >= 1:
                terminal_pass = history[plays - 1] == 'p'
                double_bet = history[plays - 2: plays] == 'bb'
                is_player_card_higher = cards[curr_player] > cards[opponent]
                if terminal_pass:
                    if history == "p":
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #             (players[1] if AI_turn else players[0]) + " did not place any bets.")
                        return 0
                    else:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #             (players[1] if AI_turn else players[0]) + " did not place any bets.")
                        return 1 if not is_player_card_higher else 0
                
                elif double_bet:
                    if is_player_card_higher:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #     (players[1] if AI_turn else players[0]) + " won.")
                        return -1 if AI_turn else 1
                    else:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #     (players[0] if AI_turn else players[1]) + " won.")
                        return 1 if AI_turn else -1

            # Keep playing if not terminal state
            if AI_turn:
                bp = self.passOrBet(cards[0], probability1)

                if bp == 'p':
                    # print("You passed.\n")
                    history = history + 'p'
                elif bp == 'b':
                    # print("You bet $1.\n")
                    history = history + 'b'
                else:
                    history = history

            else:
                # bp = input("Your turn, enter 'b' for bet or 'p' for pass:\n")
                bp = self.passOrBet(cards[1], probability2)

                if bp == 'p':
                    # print("You passed.\n")
                    history = history + 'p'
                elif bp == 'b':
                    # print("You bet $1.\n")
                    history = history + 'b'
                else:
                    history = history

    def playAI(self, iterations:int, go_first: bool, probability: list):

        import numpy as np
        import matplotlib.pyplot as plt
        
        data = np.zeros((6 , 6))
        
        # freq_print = 100000
        # if i % (freq_print) == 0:
        wins = 0
        loss = 0              
        print("==========================================")
        for idx in range(0, iterations):
            cards = [1, 2, 3, 4, 5]

            random.shuffle(cards)
            # print(" Your card is: " + (str(cards[0]) if go_first else str(cards[1])))

            val = self.gameRecursive(cards, '', go_first, probability)
            data[cards[0]][cards[1]] =  data[cards[0]][cards[1]] + val
            
            if val>0:
                wins = wins+1    
            elif val<0:
                loss = loss+1

        print("Win%: " + str(round(wins/iterations*100,2)) + "%\nLoss%: " + str(round(loss/iterations*100,2)) + "%")
        print("==========================================")

        plt.colorbar()
        plt.title( "2-D Heat Map" )

        plt.imshow( data , interpolation='nearest', extent=[1, 5, 1, 5])
        
        plt.show()
        return [round(wins/iterations*100,2), round(loss/iterations*100,2)]

    def passOrBet(self, card, probability):
        p = probability[card-1]
        moveSet = ["b", "p"]

        return random.choices(moveSet, weights=(p*100, 100-p*100), k=1)[0]

    def gameRecursive(self, cards, history: str, goFirst: bool, probability):
        while True:
            players = ["You", "AI"]
            plays = len(history)
            AI_turn = (plays % 2 == 1) if goFirst else plays % 2 == 0
            curr_player = plays % 2
            opponent = 1 - curr_player
            AI_card = str(cards[1]) if goFirst else str(cards[0])
            
            if plays >= 1:
                terminal_pass = history[plays - 1] == 'p'
                double_bet = history[plays - 2: plays] == 'bb'
                is_player_card_higher = cards[curr_player] > cards[opponent]
                if terminal_pass:
                    if history == "p":
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #             (players[1] if AI_turn else players[0]) + " did not place any bets.")
                        return 0
                    else:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #             (players[1] if AI_turn else players[0]) + " did not place any bets.")
                        return 1 if not is_player_card_higher else 0
                
                elif double_bet:
                    if is_player_card_higher:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #     (players[1] if AI_turn else players[0]) + " won.")
                        return -1 if AI_turn else 1
                    else:
                        # print("AI had card " + AI_card + ". Game ended with history: " + history + ".\n" +
                        #     (players[0] if AI_turn else players[1]) + " won.")
                        return 1 if AI_turn else -1

            info_set = str(cards[curr_player]) + history
            # Keep playing if not terminal state
            if AI_turn:
                AIStrategy = self.AI[info_set].getAverageStrategy()
                r = random.random()

                if r < AIStrategy[0]:
                    # print("AI checked/passed.\n")
                    history = history + 'p'
                else:
                    # print("AI bet $1.\n")
                    history = history + 'b'

            else:
                # bp = input("Your turn, enter 'b' for bet or 'p' for pass:\n")
                bp = self.passOrBet(cards[0] if goFirst else cards[1], probability)

                if bp == 'p':
                    # print("You passed.\n")
                    history = history + 'p'
                elif bp == 'b':
                    # print("You bet $1.\n")
                    history = history + 'b'
                else:
                    history = history

if __name__ == '__main__':
    game = KuhnGame()
    game.read('kt-200Mp')
    game.playAI(False, 0)
