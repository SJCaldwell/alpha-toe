import numpy as np
from builtins import input

"""
Random and Human-interacting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanTicTacToePlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        print("Available moves (row,column):")
        for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i%self.game.n))
        while True: 
            
            print("Enter your move in the form (x,y) (no parentheses): ")
            
            # Python 3.x
            a = input()

            x,y = [int(x) for x in a.split(',')]
            
            a = self.game.n * x + y if x!= -1 else self.game.n ** 2
            
            if valid[a]:
                break
            else:
                print('Invalid')

        return a
