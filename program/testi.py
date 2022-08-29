import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QLineEdit
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor, QPixmap, QPainter, QPaintDevice, QPaintEngine, QPainterPath

#Initialize window and layouts
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Blackjack")
window.setFixedWidth(800)
window.setFixedHeight(800)
window.setStyleSheet("background: #161219;")

cardlayout = QHBoxLayout()
window.setLayout(cardlayout)

def CreateLabel(label, layout): #Funktio joka asettaa label elementin tyyliasetukset
    label.setStyleSheet(
    "color: 'white';" +
    "font: 'Helvetica';" +
    "font-size: 35pc;" +
    "font-weight: bold;"
    )
    layout.addWidget(label)

class GuiCard(QtWidgets.QWidget):
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

        rect = QtCore.QRect(0,0,80,120)
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
        if self.name == 10: painter.drawText(25,70,(f"{self.name}")) #keskusta jos 10
        elif isinstance(self.name, str): painter.drawText(33,70,(f"{self.name}")) #keskusta jos kirjain
        else: painter.drawText(30,70,(f"{self.name}")) #keskusta jos 2 - 9
        painter.drawText(55,115,(f"{self.symbols[self.suit]}")) #alakulma

        painter.end()

card = GuiCard("D", 10)
card2 = GuiCard("S", 5)
card3 = GuiCard("H", "J")

cardlayout.addWidget(card)
cardlayout.addWidget(card2)
cardlayout.addWidget(card3)

#Display window
window.show()
sys.exit(app.exec())