import random
import sys
from telnetlib import GA
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QLineEdit
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QPainter
from PyQt5.QtCore import QTimer
import classes
import functions as f
from enum import Enum

credits = 500
bank = 10000
bet = 0

GameState = Enum("GameState", "Betting Dealing PlayerAction DealerAction Results")
GameState = GameState.Betting

#Luodaan korttipakka & kädet
deck = classes.Deck()
player = []
dealer = []

#Initialisoidaan ikkuna
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Blackjack")
window.setFixedWidth(700)
window.setFixedHeight(650)
window.setStyleSheet("background: #161219;")

#Layout hierarkia
#maingrid sisältää kaikki laatikot
maingrid = QGridLayout()
window.setLayout(maingrid)
maingrid.setRowStretch(0, 2) #dealercards
maingrid.setRowStretch(1, 2) #playercards
maingrid.setRowStretch(2, 1) #padding
maingrid.setRowStretch(3, 0) #economy
maingrid.setRowStretch(4, 0) #actions
maingrid.setRowStretch(5, 0) #betting
maingrid.setRowStretch(6, 0) #padding
maingrid.setRowStretch(7, 0) #gameinfo
maingrid.setRowStretch(8, 0) #quit nappi

#Oma custom widget luokka jolla voidaan piirtää pelaajien kortit widget elementtinä näytölle ja lisätä ne laatikoihin
class GuiCard(QWidget):
    def __init__(self, suit, name):
        super(GuiCard, self).__init__()
        self.suit = suit
        self.name = name
        self.symbols = {"D" : "♦", "C" : "♣", "H" : "♥", "S" : "♠"}
        layout = QVBoxLayout()
        self.setLayout(layout)

    def paintEvent(self, e):
        painter = QPainter(self)
        font = painter.font()
        font.setFamily('Impact')
        font.setPointSize(24)
        painter.setFont(font)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QtCore.QRect(0,0,70,110)
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor('#FFF8DC'))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRoundedRect(rect, 5, 5)
        if self.suit == "D" or self.suit == "H": painter.setPen(QtGui.QColor("red"))
        else: painter.setPen(QtGui.QColor("black"))
        painter.drawText(3,25,(f"{self.symbols[self.suit]}")) #yläkulma
        if self.name == 10: painter.drawText(20,70,(f"{self.name}")) #keskusta jos 10
        elif isinstance(self.name, str): painter.drawText(25,70,(f"{self.name}")) #keskusta jos kirjain
        else: painter.drawText(27,70,(f"{self.name}")) #keskusta jos 2 - 9
        painter.drawText(45,105,(f"{self.symbols[self.suit]}")) #alakulma
        painter.end()

##############################################################################################################################################
############################################### FUNKTIOT #####################################################################################
##############################################################################################################################################

def CreateButton(button, layout, width = 70, row = 0, col = 0): #Funktio jolla luodaan nappi haluttuun paikkaan halutuilla asetuksilla, ja säätää tyyliasetukset
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(width)
    button.setFixedHeight(25)
    button.setStyleSheet(
    "*{border: 3px solid '#DAA520';" +
    "border-radius: 45px;" +
    "font-size: 35pc;" +
    "font-weight: bold;" +
    "color: 'white'}" +
    "*:hover{background: '#483D8B';}"
    )
    if layout == maingrid:
        layout.addWidget(button, row, col)
    else:
        layout.addWidget(button, col)

def CreateLabel(label, layout): #Funktio jolla luodaan economy labelit
    label.setStyleSheet(
    "color: '#7CFC00';" +
    "font: 'Helvetica';" +
    "font-size: 35pc;" +
    "font-weight: bold;"
    )
    layout.addWidget(label)


def AddCard(card, layout):
    newcard = GuiCard(card.suit, card.name)
    if layout == player: playercards.addWidget(newcard, 1)
    else: dealercards.addWidget(newcard, 1)


def BetPlusFifty():
    if GameState != GameState.Betting: return
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    bet = f.BetPlusFifty(bet, lbl_gameinfo, lbl_bet)

def BetPlusTen():
    if GameState != GameState.Betting: return
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    bet = f.BetPlusTen(bet,lbl_gameinfo, lbl_bet)

def BetMinusTen():
    if GameState != GameState.Betting: return
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    bet = f.BetMinusTen(bet,lbl_gameinfo, lbl_bet)

def BetMinusFifty():
    if GameState != GameState.Betting: return
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    bet = f.BetMinusFifty(bet,lbl_gameinfo, lbl_bet)

def PlaceBet():
    if GameState != GameState.Betting: return
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    global lbl_bank
    global lbl_credits
    credits -= bet
    bank += bet
    timer = QTimer()
    f.PlaceBet(bet, credits, bank, lbl_gameinfo, lbl_bet, lbl_bank, lbl_credits)
    f.PrepLabelUpdate(lbl_gameinfo, "The dealer is dealing cards...")
    timer.singleShot(3000, f.UpdateLabel)
    timer.singleShot(3200, InitialDeal)

def InitialDeal():
    global GameState
    GameState = GameState.Dealing
    timer = QTimer()
    f.PrepLabelUpdate(lbl_gameinfo, "Your turn. Choose an action.")
    timer.singleShot(500, DealPlayer)
    timer.singleShot(1000, DealPlayer)
    timer.singleShot(1500, DealDealer)
    timer.singleShot(2000, f.UpdateLabel)

def DealPlayer():
    card = random.choice(deck.cards)
    player.append(card)
    AddCard(card, player)
    deck.cards.remove(card)

def DealDealer():
    card = random.choice(deck.cards)
    dealer.append(card)
    AddCard(card, dealer)
    deck.cards.remove(card)

##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################

#dealercards laatikko johon laitetaan jakajan kortit
dealercards = QHBoxLayout()
maingrid.addLayout(dealercards, 0,0)

#playercards laatikko johon laitetaan pelaajan kortit
playercards = QHBoxLayout()
maingrid.addLayout(playercards, 1,0)

#economy laatikko johon laitetaan bet, credits ja bank labelit
economy = QHBoxLayout()
maingrid.addLayout(economy,3,0, alignment=QtCore.Qt.AlignCenter)
economy.setSpacing(50)

lbl_credits = QLabel(text=(f"Credits: {credits}"))
CreateLabel(lbl_credits, economy)

lbl_bank = QLabel(text=(f"Bank: {bank}"))
CreateLabel(lbl_bank, economy)

lbl_bet = QLabel(text=(f"Bet: {bet}"))
CreateLabel(lbl_bet, economy)

#actions laatikko johon laitetaan pelaajan napit
actions = QHBoxLayout()
maingrid.addLayout(actions, 4, 0, alignment=QtCore.Qt.AlignCenter)
btn_hit = QPushButton("Hit")
CreateButton(btn_hit, actions)
btn_double = QPushButton("Double")
CreateButton(btn_double, actions)
btn_stand = QPushButton("Stand")
CreateButton(btn_stand, actions)
btn_forfeit = QPushButton("Forfeit")
CreateButton(btn_forfeit, actions)

#betting laatikko johon laitetaan napit joilla nostetaan tai lasketaan panosta
betting = QHBoxLayout()
maingrid.addLayout(betting,5,0, alignment=QtCore.Qt.AlignCenter)
btn_plusfifty = QPushButton("+50")
btn_plusfifty.clicked.connect(BetPlusFifty)
CreateButton(btn_plusfifty, betting, 50)

btn_plusten = QPushButton("+10")
btn_plusten.clicked.connect(BetPlusTen)
CreateButton(btn_plusten, betting, 50)

btn_minusten = QPushButton("-10")
btn_minusten.clicked.connect(BetMinusTen)
CreateButton(btn_minusten, betting, 50)

btn_minusfifty = QPushButton("-50")
btn_minusfifty.clicked.connect(BetMinusFifty)
CreateButton(btn_minusfifty, betting, 50)

btn_bet = QPushButton("Place Bet")
btn_bet.clicked.connect(PlaceBet)
CreateButton(btn_bet, betting, 75)

#tyhjä label padding syistä
lbl_padding = QLabel(text=" ")
maingrid.addWidget(lbl_padding, 7,0,alignment=QtCore.Qt.AlignCenter)

#gameinfo label joka näyttää pelaajalle tärkeää tietoa
lbl_gameinfo = QLabel(text="Welcome To Blackjack! Place a bet in order to begin.")
lbl_gameinfo.setStyleSheet(
"color: 'white';" +
"font: 'Helvetica';" +
"font-size: 35pc;" +
"font-weight: bold;"
)
maingrid.addWidget(lbl_gameinfo, 6,0, alignment=QtCore.Qt.AlignCenter)

#quit nappi johonki :)
btn_quit = QPushButton("Quit")
btn_quit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
btn_quit.setFixedWidth(60)
btn_quit.setFixedHeight(25)
btn_quit.setStyleSheet(
"*{border: 3px solid '#DAA520';" +
"border-radius: 45px;" +
"font-size: 35pc;" +
"font-weight: bold;" +
"color: 'white'}" +
"*:hover{background: '#483D8B';}"
)
maingrid.addWidget(btn_quit, 8,0, alignment=QtCore.Qt.AlignCenter)

#Display window
window.show()
sys.exit(app.exec())