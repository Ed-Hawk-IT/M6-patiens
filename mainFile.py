import random

deck = []
pile1 = []
pile2 = []
pile3 = []
pile4 = []



def initCards():
    suits = ["S","H","C","D"]
    ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]    # ace == 14
    for suit in suits:
        for rank in ranks:
            deck.append ((suit, rank))
    random.shuffle(deck) # shuffle deck 

def viewdict (ls):
    for i in ls:
        print (f"{i}: {ls[i]}")
    print ()

def print_card(suit, rank, halfcard):
    red = "\033[31m"
    default = "\033[0m"

    color = default     # terminal color
    symbol = "ERR"      # suit unicode symbol, ERR if suit is invalid
    value = str(rank)   # rank character (A, 1...10, J, Q, K)


    if suit == 'S':
        symbol = '\u2660'
        color = default

    elif suit == 'H':
        symbol = '\u2665'
        color = red;

    elif suit == 'D':
        symbol = '\u2666'
        color = red;

    elif suit == 'C':
        symbol = '\u2663'
        color = default


    # change ace (14), jack (11), queen (12), king (13) to A, J, Q, K respectively
    # change 10 to T because other wise that card is wider then the others//ed
    if value == '1' or value == '14':
        value = 'A'

    elif value == '11':
        value = 'J'

    elif value == '12':
        value = 'Q'

    elif value == '13':
        value = 'K'
        

    print("\u256D\u2500\u2500\u256E")
    print('\u2502' + color + value + symbol + default + '\u2502')
    if not halfcard:    # print lower part of card
        print('\u2502' + color + symbol + value + default + '\u2502')
        print("\u2570\u2500\u2500\u256F")


initCards()
print_card(deck[0][0], deck[0][1], True)
print_card(deck[1][0], deck[1][1], False)

print_card(deck[13][0], deck[13][1], True)
print_card(deck[14][0], deck[14][1], False)

print_card(deck[26][0], deck[26][1], True)
print_card(deck[27][0], deck[27][1], False)

print_card(deck[39][0], deck[39][1], True)
print_card(deck[40][0], deck[40][1], False)

#good don´t you have to explain in person what what does /ed

#func below are acctions, but not rules

def moveCard(fromPile1, toPile1):  #move a card from index 0 to index 0
    card = fromPile1[-1]
    fromPile1.pop()
    toPile1.append(card)

def discardCard(fromPile2): #discard a card
    fromPile2.pop()

def addCards(): #add four card in all piles
    moveCard(deck,pile1)
    moveCard(deck,pile2)
    moveCard(deck,pile3)
    moveCard(deck,pile4)

#func below are Rules,

def moveCardRules(fromPile3,topile3):
    if len(topile3) != 0:
        print("Error: Targeted pile not empty")
    elif len(fromPile3) == 0:
        print("Error: Source pile is empty")
    else:
        moveCard(fromPile3,topile3)

def discardCardRules(formPile4): #är nummer nu?
    status = False
    topCards = []
    cardPiles = [pile1, pile2, pile3, pile4]
    for p in cardPiles:
        if len (p) == 0:
            p.append(("Joker",0))
        pCard = p[-1]
        topCards.append(pCard)
    discarded = formPile4[-1] #kan nu vara tom
    for c in topCards:
        if c[0] == discarded[0]:
            if c[1] > discarded[1]:
                status = True
    for p in cardPiles:
        if len (p) == 1:
            p.pop()
    return (status)


#func below are player actions,

def callAction():
    choice = {"n": "New Cards", "m": "Move", "d": "discard"}
    viewdict(choice)
    action = input("choose action: ")
    if action == "n":
        addCards()
    elif action == "m":
        x = input("From: ")
        y = input("To: ")
        moveCardRules(x,y)
    elif action == "d":
        x = input("From: ")
        discardCard(x)

