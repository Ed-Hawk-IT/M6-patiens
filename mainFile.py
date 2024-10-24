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

def moveCard(fromPile, toPile):  #move a card from index 0 to index 0
    card = fromPile[0]
    del fromPile[0]
    toPile.insert(0,card)
    print (toPile)

def discardCard(fromPile): #discard a card
    discard = [] 
    moveCard(fromPile, discard)
    discard = []

def addCards(DECK,PILE1,PILE2,PILE3,PILE4): #add four card in all piles
    moveCard(DECK,PILE1)
    moveCard(DECK,PILE2)
    moveCard(DECK,PILE3)
    moveCard(DECK,PILE4)

