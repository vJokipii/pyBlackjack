import random

suits = ["S", "H", "C", "D"]
names = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

class Card:
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
        self.symbols = {"D" : "♦", "C" : "♣", "H" : "♥", "S" : "♠"}

    def show(self):
        print(f"{self.name}{self.symbols[self.suit]}")

######################################################################

class Deck:
    def __init__(self):
        self.cards = []

        for name in names:
            for suit in suits:
                card = Card(name, suit)
                self.cards.append(card)
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def resetDeck(self):
        self.cards = []
        for name in names:
            for suit in suits:
                card = Card(name, suit)
                self.cards.append(card)
        self.shuffle()