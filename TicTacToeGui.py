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

class GUI:

  def __init__(self):
    self.app = Tk()
    self.app.title('TicTacToe')
    self.app.resizable(width=False, height=False)
    self.board = g.getInitBoard()
    self.curPlayer = 1
    self.Lagann = ImageTk.PhotoImage(Image.open("mecha.jpg"))
    self.LagannWin = ImageTk.PhotoImage(Image.open("mechawin.jpg")) # NN will never lose
    self.Killmanovich = ImageTk.PhotoImage(Image.open("killmanovich.png"))
    self.KillmanovichLose = ImageTk.PhotoImage(Image.open("killmanovichlose.png"))
    self.blankSquare = ImageTk.PhotoImage(Image.open("white square.png"))
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
    #print x, y
    self.board, self.curPlayer = g.getNextState(self.board, self.curPlayer, BOARD_SIZE*x + y)
    #self.board = self.board.move(x,y)
    self.update()
    move = nnp(g.getCanonicalForm(self.board, self.curPlayer))
    #print move
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
          if piece == 1:
            img = self.Killmanovich
          if piece == -1:
            img = self.Lagann
          self.buttons[x,y].config(image = img)
          if piece == 0:  # enable button
            self.buttons[x,y]['state'] = 'normal'
            self.buttons[x,y]['command'] = lambda x=x,y=y: self.move(x,y)
          else: # disable button
            self.buttons[x,y]['command'] = 0  # this disables the callback
            self.buttons[x,y]['relief'] = 'sunken'  # makes the button fixed

    winning = g.getGameEnded(self.board, self.curPlayer)  #self.board.won()
    if winning:
      if winning == 1:
          print("I LOSE? ERROR DOES NOT COMPUTE I CANNOT LOSE")
      elif winning > 0:
          print("DRAW DRAW DRAW DRAW DRAW DRAW DRAW DRAW DRAW DRAW DRAW DRAW")
      else:
        print("I WIN! HAHA YOU CANNOT DEFEAT ME!")
        for x in range(BOARD_SIZE):
          for y in range(BOARD_SIZE):
            piece = self.board[x,y]
            img = self.blankSquare
            if piece == -1:
              img = self.LagannWin
            if piece == 1:
              img = self.KillmanovichLose
            self.buttons[x,y].config(image = img)

            self.buttons[x,y]['command'] = 0  # this disables the callback
            self.buttons[x,y]['relief'] = 'sunken'  # makes the button fixed

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
          self.buttons[x,y].update()

  def mainloop(self):
    self.app.mainloop()

if __name__ == '__main__':
  GUI().mainloop()
