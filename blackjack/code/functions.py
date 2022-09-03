from enum import Enum
import random
from PyQt5 import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal


# Ylimääräinen moduuli puhtaasti koodin luettavuussyistä
# Tänne on heitetty vähän apufunktioita joiden ei ole pakko olla päämoduulissa -
# ja siellä vain sotkisivat koodia ja häiritsisivät luettavuutta entisestään.

labeltext = ""
label = None

def BetPlusFifty(bet, lbl_info, lbl_bet):
    bet += 50
    lbl_info.setText(f"You are about to bet {bet} credits.")
    lbl_bet.setText(f"Bet: {bet}")
    return bet

def BetPlusTen(bet, lbl_info, lbl_bet):
    bet += 10
    lbl_info.setText(f"You are about to bet {bet} credits.")
    lbl_bet.setText(f"Bet: {bet}")
    return bet

def BetMinusFifty(bet,lbl_info, lbl_bet):
    if bet >= 50: bet -= 50
    elif bet < 50 and bet > 0: bet -= bet
    if bet > 0 : lbl_info.setText(f"You are about to bet {bet} credits.")
    else : lbl_info.setText(f"Welcome To Blackjack! Place a bet in order to begin.")
    lbl_bet.setText(f"Bet: {bet}")
    return bet

def BetMinusTen(bet,lbl_info, lbl_bet):
    if bet >= 10: bet -= 10
    if bet > 0 : lbl_info.setText(f"You are about to bet {bet} credits.")
    else : lbl_info.setText(f"Welcome To Blackjack! Place a bet in order to begin.")
    lbl_bet.setText(f"Bet: {bet}")
    return bet

def PlaceBet(bet, credits, bank, lbl_info, lbl_bet, lbl_bank, lbl_credits):
    lbl_info.setText(f"You placed a bet for {bet} credits. Good luck!")
    lbl_credits.setText(f"Credits: {credits}")
    lbl_bank.setText(f"Bank: {bank}")
    lbl_bet.setText(f"Bet: {bet}")

def PrepLabelUpdate(lbl, value):
    global label
    global labeltext
    label = lbl
    labeltext = value

def UpdateLabel():
    global label
    global labeltext
    if label != None and labeltext != "": label.setText(labeltext)
    else: pass
    label = None
    labeltext = ""

def checkHand(hand): #Tarkistetaan käden x korttien arvo, ässä antaa 11 jos voi, jos ei niin 1
    value = 0
    ace = 0
    faces = ["J","Q","K"]
    for card in hand:
        if card.name in range(11):
            value += card.name
        elif card.name in faces:
            value += 10
        else:
            value += 11
            ace += 1
        while ace and value > 21:
            value -= 10
            ace -= 1
    return value