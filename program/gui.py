import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QLineEdit
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

credits = 300
bank = 600
bet = 0

#Initialize window and layouts
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Blackjack")
window.setFixedWidth(800)
window.setFixedHeight(800)
window.setStyleSheet("background: #161219;")

class guiCard():
    def __init__(self, suit, name, layout):
        self.suit = suit
        self.name = name
        self.symbols = {"D" : "♦", "C" : "♣", "H" : "♥", "S" : "♠"}
        cardLayout = QVBoxLayout()
        layout.addLayout(cardLayout)
    
    def initLabels(self):
        topLabel = QLabel(f"{self.name}{self.symbols[self.suit]}")
        CreateLabel(topLabel, self.cardLayout)
        


############# Funktioita #########################

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


def CreateLabel(label, layout): #Funktio joka asettaa label elementin tyyliasetukset
    label.setStyleSheet(
    "color: 'green';" +
    "font: 'Helvetica';" +
    "font-size: 35pc;" +
    "font-weight: bold;"
    )
    layout.addWidget(label)

def UpdateLabel(label, text, value): #Funktio joka asettaa tekstin ja arvot label elementtiin
    label.setText(f"{text}: {value}")

###################################################

#Layout hierarkia

#maingrid sisältää kaikki laatikot
maingrid = QGridLayout()
window.setLayout(maingrid)
maingrid.setRowStretch(0, 3) #dealercards
maingrid.setRowStretch(1, 3) #playercards
maingrid.setRowStretch(2, 2) #padding
maingrid.setRowStretch(3, 0) #economy
maingrid.setRowStretch(4, 0) #actions
maingrid.setRowStretch(5, 0) #betting
maingrid.setRowStretch(7, 1) #quit nappi

#dealercards laatikko johon laitetaan jakajan kortit
dealercards = QHBoxLayout()
maingrid.addLayout(dealercards,0,0)

#playercards laatikko johon laitetaan pelaajan kortit
playercards = QHBoxLayout()
maingrid.addLayout(playercards,1,0)

#economy laatikko johon laitetaan bet, credits ja bank labelit
economy = QHBoxLayout()
maingrid.addLayout(economy,3,0, alignment=QtCore.Qt.AlignCenter)
economy.setSpacing(50)

lbl_credits = QLabel()
UpdateLabel(lbl_credits, "Credits", credits)
CreateLabel(lbl_credits, economy)

lbl_bank = QLabel()
UpdateLabel(lbl_bank, "Bank", bank)
CreateLabel(lbl_bank, economy)

lbl_bet = QLabel()
UpdateLabel(lbl_bet, "Bet", bet)
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
CreateButton(btn_plusfifty, betting, 50)
btn_plusten = QPushButton("+10")
CreateButton(btn_plusten, betting, 50)
btn_minusten = QPushButton("-10")
CreateButton(btn_minusten, betting, 50)
btn_minusfifty = QPushButton("-50")
CreateButton(btn_minusfifty, betting, 50)
btn_bet = QPushButton("Place Bet")
CreateButton(btn_bet, betting, 75)

#quit nappi johonki
btn_quit = QPushButton("Quit")
btn_quit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
btn_quit.setFixedWidth(350)
btn_quit.setFixedHeight(45)
btn_quit.setStyleSheet(
"*{border: 3px solid '#DAA520';" +
"border-radius: 45px;" +
"font-size: 35pc;" +
"font-weight: bold;" +
"color: 'white'}" +
"*:hover{background: '#483D8B';}"
)
maingrid.addWidget(btn_quit, 7,0, alignment=QtCore.Qt.AlignBottom)


#Display window
window.show()
sys.exit(app.exec())