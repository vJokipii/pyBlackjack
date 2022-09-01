import random
import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QPainter
from PyQt5.QtCore import QTimer
import classes
import functions as f

credits = 500
bank = 10000
bet = 0

GameRunning = False
PlayerTurn = False
DealerTurn = False

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
    "*:hover{background: '#483D8B';" +
    "color: '#FFD700'}"
    )
    if layout == maingrid:
        layout.addWidget(button, row, col)
    else:
        layout.addWidget(button, col)

def Toggle_PlayerTurn():
    global PlayerTurn
    global lbl_gameinfo
    PlayerTurn = not PlayerTurn
    # debug
    print(PlayerTurn) 
    if PlayerTurn == True: lbl_gameinfo.setText("Your turn. Choose an action.")

def Toggle_GameRunning():
    global GameRunning
    GameRunning = not GameRunning

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
    layout.addWidget(newcard, 0)

def Hit():
    global PlayerTurn
    if not PlayerTurn: return
    global lbl_gameinfo
    timer = QTimer()
    lbl_gameinfo.setText("The dealer is dealing you a card...")
    timer.singleShot(2000, DealCard_Player)
    timer.singleShot(2100, Check)

def Forfeit():
    global PlayerTurn
    if not PlayerTurn: return
    global lbl_gameinfo
    global bet
    global bank
    global credits
    timer = QTimer()
    lbl_gameinfo.setText(f"You forfeit this round. You get half your bet ({int(bet / 2)}) back.")
    bank -= int(bet/2)
    credits += int(bet/2)
    timer.singleShot(2000, ResetGame)

def Stand():
    global PlayerTurn
    global DealerTurn
    global lbl_gameinfo
    if not PlayerTurn: return
    lbl_gameinfo.setText("You ended your turn.")
    PlayerTurn = False
    timer = QTimer()
    timer.singleShot(2000, Dealer_Turn)
    DealerTurn = True

def Double():
    global PlayerTurn
    global bet
    global bank
    global credits
    global lbl_gameinfo
    global lbl_bet
    global lbl_bank
    global lbl_credits
    timer = QTimer()
    if not PlayerTurn: return
    if bank < (bet * 2) or credits < bet:
        lbl_gameinfo.setText("You cannot double your bet right now.")
        return
    credits -= bet
    bank += bet
    bet *= 2
    UpdateEconomy()
    lbl_gameinfo.setText("You doubled your bet.")
    #Laitetaan playerturn pois päältä odotuksen ajaksi, ja takaisin päälle vähän ennen Hit funktiota
    timer.singleShot(2000, Hit)

def Dealer_Turn():
    global lbl_gameinfo
    global dealer
    global dealercards
    lbl_gameinfo.setText("The dealer is drawing cards...")
    timer = QTimer()
    timer.singleShot(700, DealCard_Dealer)
    timer.singleShot(1300, Check)

def BetPlusFifty():
    global GameRunning
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    if GameRunning == True: return
    bet = f.BetPlusFifty(bet, lbl_gameinfo, lbl_bet)

def BetPlusTen():
    global GameRunning
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    if GameRunning == True: return
    bet = f.BetPlusTen(bet,lbl_gameinfo, lbl_bet)

def BetMinusTen():
    global GameRunning
    global bet
    global lbl_bet
    global lbl_gameinfo
    if GameRunning == True: return
    bet = f.BetMinusTen(bet,lbl_gameinfo, lbl_bet)

def BetMinusFifty():
    global GameRunning
    global bet
    global lbl_bet
    global lbl_gameinfo
    if GameRunning == True: return
    bet = f.BetMinusFifty(bet,lbl_gameinfo, lbl_bet)

def UpdateEconomy():
    global credits
    global bank
    global bet
    lbl_credits.setText(f"Credits: {credits}")
    lbl_bank.setText(f"Bank: {bank}")
    lbl_bet.setText(f"Bet: {bet}")

def PlaceBet():
    global GameRunning
    global credits
    global bank
    global bet
    global lbl_bet
    global lbl_gameinfo
    global lbl_bank
    global lbl_credits
    if GameRunning == True: return
    if credits < bet:
        lbl_gameinfo.setText("You do not have enough credits! Lower your bet.")
        return
    elif bank < bet:
        lbl_gameinfo.setText("The dealer does not have enough credits! Lower your bet.")
        return
    elif bet < 10:
        lbl_gameinfo.setText("The minimum bet is 10 credits.")
        return
    else:pass
    credits -= bet
    bank += bet
    timer = QTimer()
    f.PlaceBet(bet, credits, bank, lbl_gameinfo, lbl_bet, lbl_bank, lbl_credits)
    f.PrepLabelUpdate(lbl_gameinfo, "The dealer is dealing cards...")
    timer.singleShot(3000, f.UpdateLabel)
    timer.singleShot(3200, InitialDeal)
    Toggle_GameRunning()

def InitialDeal():
    timer = QTimer()
    timer.singleShot(500, DealCard_Player)
    timer.singleShot(1000, DealCard_Player)
    timer.singleShot(1500, DealCard_Dealer)
    timer.singleShot(2000, Check)
    timer.singleShot(2000, Toggle_PlayerTurn)

def Check():
    global dealer
    global player
    playervalue = f.checkHand(player)
    dealervalue = f.checkHand(dealer)
    global lbl_gameinfo
    global PlayerTurn
    global DealerTurn
    timer = QTimer()

    if len(player) == 2 and playervalue == 21: PlayerWin(True) #Blackjack
    
    if playervalue > 21:
        lbl_gameinfo.setText("You got a bust! The dealer wins this round.")
        PlayerTurn = False
        timer.singleShot(3000, ResetGame)
    elif playervalue <= 21 and PlayerTurn: lbl_gameinfo.setText("Your turn. Choose an action.")
    
    if DealerTurn and dealervalue < 17:
        Dealer_Turn()
        return
    elif DealerTurn and dealervalue >= 17:
        if dealervalue >= 17:
            if dealervalue > 21:
                lbl_gameinfo.setText("The dealer got a bust!")
                timer.singleShot(4000, PlayerWin)
            else:
                if dealervalue > playervalue:
                    lbl_gameinfo.setText("The dealer's hand beats yours! The dealer wins this round.")
                    timer.singleShot(4000, ResetGame)
                else:
                    if dealervalue == playervalue: Tie()
                    else:
                        lbl_gameinfo.setText("Your hand beats the dealer's!")
                        timer.singleShot(4000, PlayerWin)


def DealCard_Player():
    global lbl_gameinfo
    card = random.choice(deck.cards)
    player.append(card)
    AddCard(card, playercards)
    deck.cards.remove(card)

def DealCard_Dealer():
    card = random.choice(deck.cards)
    dealer.append(card)
    AddCard(card, dealercards)
    deck.cards.remove(card)

def PlayerWin(blackjack = False):
    global bet
    global bank
    global credits
    global lbl_gameinfo
    timer = QTimer()
    payout = 0
    if blackjack:
        payout = int(bet + (bet * 1.5))
        lbl_gameinfo.setText(f"You got a blackjack! You win {payout} (3:2) credits.")
    else:
        payout = int(bet * 2)
        lbl_gameinfo.setText(f"You beat the dealer! You win {payout} (1:1) credits.")
    credits += payout
    bank -= payout
    timer.singleShot(3000, ResetGame)

def Tie():
    global bet
    global bank
    global credits
    global lbl_gameinfo
    timer = QTimer()
    lbl_gameinfo.setText(f"It's a tie! You get your bet ({bet}) back.")
    credits += bet
    bank -= bet
    timer.singleShot(3000, ResetGame())

def ResetGame():
    global bet
    global lbl_gameinfo
    global GameRunning
    global PlayerTurn
    global DealerTurn
    global dealer
    global player
    global deck
    global dealercards
    global playercards
    global credits
    global bank
    timer = QTimer()
    deck.resetDeck()
    dealer.clear()
    player.clear()
    for i in reversed(range(dealercards.count())): dealercards.itemAt(i).widget().deleteLater()
    for i in reversed(range(playercards.count())): playercards.itemAt(i).widget().deleteLater()
    bet = 0
    UpdateEconomy()
    if credits < 10:
        lbl_gameinfo.setText("You are out of credits! Closing blackjack.")
        timer.singleShot(3000, Quit)
        return
    elif bank < 10:
        lbl_gameinfo.setText("The dealer is out of credits! Closing blackjack.")
        timer.singleShot(3000, Quit)
        return
    lbl_gameinfo.setText("If you would like to play another round, place a bet.")
    GameRunning = False
    PlayerTurn = False
    DealerTurn = False


def Quit():
    sys.exit(app.exec())

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
btn_hit.clicked.connect(Hit)
CreateButton(btn_hit, actions)
btn_double = QPushButton("Double")
btn_double.clicked.connect(Double)
CreateButton(btn_double, actions)
btn_stand = QPushButton("Stand")
btn_stand.clicked.connect(Stand)
CreateButton(btn_stand, actions)
btn_forfeit = QPushButton("Forfeit")
btn_forfeit.clicked.connect(Forfeit)
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
"font-size: 45pc;" +
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
"*:hover{background: '#483D8B';" +
"color: '#FFD700'}"
)
maingrid.addWidget(btn_quit, 8,0, alignment=QtCore.Qt.AlignCenter)
btn_quit.clicked.connect(Quit)

#Display window
window.show()
sys.exit(app.exec())