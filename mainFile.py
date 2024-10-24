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




# print_row_of_cards(cards, sections): print 4 cards lying next to eachother, one half (upper/lower) at a time
# parameter explanation:
#
# cards[4] (different types of elements):
#   (suit, rank)    - tuple representing a card denoted by suit and rank (same as those in deck[])
#   int             - if 0: empty outline of a card, if non-zero: outline of a card with specified value, denoting hidden cards
#   None            - empty, print whitespace
#
# bool sections[4]:
#   True    - print upper part of corresponding card (same index) in cards[]
#   False   - print lower part
def print_row_of_cards(cards, sections):
    red = "\033[31m"
    default = "\033[0m"

    white = "    "
    upper_line = "\u256D\u2500\u2500\u256E"
    lower_line = "\u2570\u2500\u2500\u256F"
    pipe = '\u2502'

    colors = [default, default, default, default]    # terminal color
    symbols = ["", "", "", ""]   # suit unicode symbol
    values = ["", "", "", ""]    # rank character (A, 1...9, T, J, Q, K)

    # rows to print
    row1 = ""
    row2 = ""

    if len(cards) != 4:
        print("invalid set of cards passed to print_card_row()")
        exit()


    for i in range(4):
        if cards[i] == None:    # empty (no card), print whitespace (handled later by checking cards[i])
            continue


        if type(cards[i]) is int:   # print card outline with or without additional game state information
            colors[i] = default
            if cards[i]:    # print card outline with with number indicating hidden cards
                values[i] = str(cards[i])
                symbols[i] = '+'

            else:   # only card outline
                values[i] = ' '
                symbols[i] = ' '

            continue


        # else, print a card
        #TODO put in a separate fn?

        suit = cards[i][0]
        rank = cards[i][1]

        if suit == 'S':
            symbols[i] = '\u2660'
            colors[i] = default

        elif suit == 'H':
            symbols[i] = '\u2665'
            colors[i] = red;

        elif suit == 'D':
            symbols[i] = '\u2666'
            colors[i] = red;

        elif suit == 'C':
            symbols[i] = '\u2663'
            colors[i] = default


        # change ace (14), (10), jack (11), queen (12), king (13) to A, T, J, Q, K respectively
        if rank == 1 or rank == 14:
            values[i] = 'A'

        elif rank == 10:   # '10' is two characters and therefore looks skewed when printed
            values[i] = 'T'

        elif rank == 11:
            values[i] = 'J'

        elif rank == 12:
            values[i] = 'Q'

        elif rank == 13:
            values[i] = 'K'

        else:
            values[i] = str(rank)
        

    # build row1, row2
    for i in range(4):
        if cards[i] == None:    # print whitespace (no card)
            row1 += white
            row2 += white

        elif sections[i]:   # print upper part of card
            row1 += upper_line
            row2 += pipe + colors[i] + values[i] + symbols[i] + default + pipe

        else:   # print lower part of card
            row1 += pipe + colors[i] + symbols[i] + values[i] + default + pipe
            row2 += lower_line


    print(row1)
    print(row2)


initCards()

#example
print_row_of_cards([2, 2, 2, 2], [True, True, True, True])
print_row_of_cards([('S', 14), ('H', 11), ('C', 3), 0], [True, True, True, True])
print_row_of_cards([('S', 14), ('H', 11), ('C', 3), 0], [True, True, False, False])
print_row_of_cards([('S', 14), ('H', 11), None, None], [False, False, False, False])


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

