# coding=UTF8

# Python TicTacToe game with Tk GUI and minimax AI
# Author: Maurits van der Schee <maurits@vdschee.nl>
# Repo: https://github.com/mevdschee/python-tictactoe

"""
Run this file to play manually with any agent.
"""

from Tkinter import Tk, Button, PhotoImage
from PIL import ImageTk, Image
from tkFont import Font
from copy import deepcopy


import numpy as np

from MCTS import MCTS

from utils import *

from tictactoe.TicTacToeGame import TicTacToeGame, display
from tictactoe.TicTacToePlayers import *
from tictactoe.tensorflow.NNet import NNetWrapper as NNet


BOARD_SIZE = 3

g = TicTacToeGame(BOARD_SIZE)

# nnet players
nn = NNet(g)
nn.load_checkpoint('./temp/', 'best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, nn, args1)
nnp = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

'''
class Board:

  def __init__(self,other=None):
    self.player = 'X'
    self.opponent = 'O'
    self.empty = '.'
    self.size = 3
    self.fields = {}
    for y in range(self.size):
      for x in range(self.size):
        self.fields[x,y] = self.empty
    # copy constructor
    if other:
      self.__dict__ = deepcopy(other.__dict__)

  def move(self,x,y):
    board = Board(self)
    board.fields[x,y] = board.player
    (board.player,board.opponent) = (board.opponent,board.player)
    return board

  def __minimax(self, player):
    if self.won():
      if player:
        return (-1,None)
      else:
        return (+1,None)
    elif self.tied():
      return (0,None)
    elif player:
      best = (-2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value>best[0]:
            best = (value,(x,y))
      return best
    else:
      best = (+2,None)
      for x,y in self.fields:
        if self.fields[x,y]==self.empty:
          value = self.move(x,y).__minimax(not player)[0]
          if value<best[0]:
            best = (value,(x,y))
      return best

  def best(self):
    return self.__minimax(True)[1]

  def tied(self):
    for (x,y) in self.fields:
      if self.fields[x,y]==self.empty:
        return False
    return True

  def won(self):
    # horizontal
    for y in range(self.size):
      winning = []
      for x in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # vertical
    for x in range(self.size):
      winning = []
      for y in range(self.size):
        if self.fields[x,y] == self.opponent:
          winning.append((x,y))
      if len(winning) == self.size:
        return winning
    # diagonal
    winning = []
    for y in range(self.size):
      x = y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # other diagonal
    winning = []
    for y in range(self.size):
      x = self.size-1-y
      if self.fields[x,y] == self.opponent:
        winning.append((x,y))
    if len(winning) == self.size:
      return winning
    # default
    return None

  def __str__(self):
    string = ''
    for y in range(self.size):
      for x in range(self.size):
        string+=self.fields[x,y]
      string+="\n"
    return string
'''

class GUI:

  def __init__(self):
    self.app = Tk()
    self.app.title('TicTacToe')
    self.app.resizable(width=False, height=False)
    self.board = g.getInitBoard()
    self.curPlayer = 1
    self.Lagann = ImageTk.PhotoImage(Image.open("mecha.jpg"))
    self.Killmanovich = ImageTk.PhotoImage(Image.open("killmanovich.png"))
    self.blankSquare = ImageTk.PhotoImage(Image.open("white square.png"))
    self.font = Font(family="Helvetica", size=32)
    self.buttons = {}
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
          handler = lambda x=x,y=y: self.move(x,y)
          button = Button(self.app, command=handler, width=300, height=300)
          button.grid(row=y, column=x)
          self.buttons[x,y] = button
    handler = lambda: self.reset()
    button = Button(self.app, text='reset', command=handler)
    button.grid(row=self.board.size+1, column=0, columnspan=self.board.size, sticky="WE")
    self.update()

  def reset(self):
    self.board = g.getInitBoard()
    self.curPlayer = 1
    self.update()

  def move(self,x,y):
    self.app.config(cursor="watch")
    self.app.update()
    print x, y
    self.board, self.curPlayer = g.getNextState(self.board, self.curPlayer, BOARD_SIZE*x + y)
    #self.board = self.board.move(x,y)
    self.update()
    move = nnp(g.getCanonicalForm(self.board, self.curPlayer))
    print move
    if move:
      self.board, self.curPlayer = g.getNextState(self.board, self.curPlayer, move)
      #self.board = self.board.move(*move)
      self.update()
    self.app.config(cursor="")

  def update(self):
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
          piece = self.board[x,y]
          img = self.blankSquare
          if piece == -1:
            img = self.Lagann
          if piece == 1:
            img = self.Killmanovich
          self.buttons[x,y].config(image = img)
          #self.buttons[x,y]['disabledforeground'] = 'black'
          if piece == 0:
            self.buttons[x,y]['state'] = 'normal'
          else:
            self.buttons[x,y]['command'] = 0  # this disables the callback
            self.buttons[x,y]['relief'] = 'sunken'  # makes the button fixed
            #self.buttons[x,y]['state'] = 'disabled'
    winning = g.getGameEnded(self.board, self.curPlayer)  #self.board.won()
    if winning:
      for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
          #self.buttons[x,y]['disabledforeground'] = 'red'
          self.buttons[x,y]['fg'] = 'red'
          self.buttons[x,y]['command'] = 0  # this disables the callback
          self.buttons[x,y]['relief'] = 'sunken'  # makes the button fixed
          #self.buttons[x,y]['state'] = 'disabled'
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
          self.buttons[x,y].update()

  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  GUI().mainloop()
