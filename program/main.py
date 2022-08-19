import random
import time
import classes

credits = 300
bank = 600
bet = 0

gameRunning = False
playerAction = False
dealerAction = False
replayQuery = False

#Luodaan korttipakka & kädet

deck = classes.Deck()
player = []
dealer = []

#Funktioita

def dealCard(hand):
    card = random.choice(deck.cards)
    hand.append(card)
    deck.cards.remove(card)

def checkHand(hand):
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

def playerWin(blackjack):
    global credits
    global bet
    global bank

    if blackjack == False:
        payout = bet*2
        bank -= payout
        credits += payout
        print(f"Congratulations, you beat the dealer! You received {payout} credits (1:1) and now have {credits} in total.")
    else:
        payout = bet + (bet * 1.5)
        bank -= payout
        credits += payout
        print(f"Congratulations, you got a blackjack! You received {payout} credits (3:2) and now have {credits} in total.")

def tie():
    global credits
    global bet
    global bank

    credits += bet
    bank -= bet
    print(f"The round resulted in a tie. You get your bet back.")

def startGame():
    global credits
    global bet
    global bank
    global deck
    global player
    global dealer

    player = []
    dealer = []

    deck.resetDeck()
    credits -= bet
    bank += bet
    print(f"You placed a bet for {bet} credits. You now have {credits} credits and the dealer has {bank} credits. Good luck!")
    time.sleep(2)
    print("The dealer is dealing the cards...")

def showHand(hand):
    for i in range(len(hand)):
        hand[i].show()

################# GAME LOOP #############################

print("<| BLACKJACK |>")
print("")
gameRunning = True

while gameRunning:
    bet = int(input(f"You have {credits} credits and the dealer has {bank} credits. Place a bet to start the game. "))
    if bet > credits:
        print("You do not have that many credits!")
        continue
    elif bet < 10:
        print("The minimum bet is 10 credits!")
        continue
    elif bet > bank:
        print("The dealer does not have that many credits!")
        continue
    else:
        pass

    time.sleep(1)
    startGame()
    time.sleep(4)

    #Jaetaan kortit
    dealCard(player)
    dealCard(player)
    dealCard(dealer)
    dealCard(dealer)

    print(" \nYour hand: ")
    showHand(player)
    print(" \nDealer's card:")
    dealer[0].show()

    #Tarkistetaan saiko pelaaja blackjackin
    if checkHand(player) == 21:
        playerWin(bet,credits,bank, True)
        playerAction = False
        replayQuery = True

    time.sleep(3)

    playerAction = True

    while playerAction: #Pelaaja valitsee
        print(" \nPLAYER ACTIONS")
        print("hit --> take another card. \nstand --> pass this turn. \ndouble down --> double your bet and take another card. \nforfeit --> lose half of your bet and quit playing this round. \n  ")
        choice = input("What would you like to do? --> ")
        if choice == "hit":
            time.sleep(1)
            print("Dealer is dealing you a card...")
            dealCard(player)
            time.sleep(2)

        elif choice == "stand":
            time.sleep(1)
            dealerAction = True
            break

        elif choice == "double down" and credits >= bet:
            time.sleep(1)
            credits -= bet
            bank += bet
            bet *= 2 #Tuplataan panos jotta osataan maksaa oikea määrä takaisin voitosta
            print(f"You doubled your bet. Your credits are now at {credits} and the dealer has {bank} credits.")
            print("Dealer is dealing you a card...")
            dealCard(player)
            time.sleep(2)

        elif choice == "double down" and credits < bet:
            print("You do not have enough credits to double your bet!")
            continue

        else: #forfeit
            credits += (bet * 0.5)
            bank -= (bet * 0.5)
            replayQuery = True
            playerAction = False
            break

        #Tarkistetaan tuliko bust, jos ei ja pelaaja ei valinnut forfeit tai stand, palataan valintoihin

        if checkHand(player) > 21:
            print("Your hand:")
            showHand(player)
            time.sleep(1)
            print("You got a bust!")
            time.sleep(1)
            replayQuery = True
            break
        else:
            print("Your hand:")
            showHand(player)
            time.sleep(1)
            continue

    while dealerAction:
        #Jakajan käsi paljastetaan, jos jakajan käsi on alle 17, jakaja nostaa kortteja niin kauan että peli ratkeaa
        print("Dealer's hand:")
        showHand(dealer)
        time.sleep(1)
        dealerhand = checkHand(dealer)
        playerhand = checkHand(player)
        if dealerhand > 21:
            print("Dealer got a bust!")
            playerWin(False)
            time.sleep(3)
            replayQuery = True
        elif dealerhand >= 17 and dealerhand == playerhand:
            tie()
            time.sleep(3)
            replayQuery = True
        elif dealerhand >= 17 and dealerhand < playerhand:
            playerWin(False)
            time.sleep(3)
            replayQuery = True
        elif dealerhand < 17:
            print("Dealer draws a card...")
            dealCard(dealer)
            time.sleep(1)
            continue
        else:
            pass

        break

    while replayQuery:
        if credits < 10:
            print("You do not have enough credits left to keep playing. Closing blackjack.")
            break
        elif bank < 10:
            print("You cleaned out the dealer! Closing blackjack.")
            break
        else:
            pass

        replay = input(f"Would you like to play again? (YES / NO) -> ")

        if replay == "YES":
            replayQuery = False
            continue
        elif replay == "NO":
            print("Closing blacjack")
            time.sleep(1)
            break
        else:
            print("Invalid command")
            continue