import random

deck = []
pile1 = []
pile2 = []
pile3 = []
pile4 = []
cards_discarded = 0



def initCards(): #makes tuples of cards that are put in a deck.
    suits = ["S","H","C","D"]
    ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]    # ace == 14
    for suit in suits:
        for rank in ranks:
            deck.append ((suit, rank))
    random.shuffle(deck) # shuffle deck 

def viewdict (ls): #will print a dictonary
    for i in ls:
        print (f"{i}: {ls[i]}")
    print ()



# print_cards(): prints out current cards on (pile1, pile2, pile3, pile4), calls print_row_of_cards()
def print_cards():
    piles = [pile1, pile2, pile3, pile4]

    depth = 0
    for pile in piles:
        if len(pile) > depth:
            depth = len(pile)

    depth += 1
    if depth == 1:
        depth = 2
    
    # depth is the number of rows to print
    # depth is atleast 2, as printing empty card outlines requires 2 rows

    # one call to print_row_at_cards() per iteration
    for i in range(depth):
        cards = []
        sections = []

        for pile in piles:

            # empty pile and first 2 rows -> print empty card outline
            if len(pile) == 0 and i < 2:    
                cards.append(0)
                if i == 0:  # print upper part of empty card outline
                    sections.append(True)
                else:   # print lower part of empty card outline
                    sections.append(False)

            # deeper than current pile -> print whitespace
            elif i > len(pile): 
                cards.append(None)
                sections.append(True)   # as card is None this bool has no effect, but something has to be there for indexes to match

            # reached top of current pile -> print lower part of top card
            elif i == len(pile):    
                cards.append(pile[i-1])
                sections.append(False)

            # print upper part of current card
            else:  
                cards.append(pile[i])
                sections.append(True)



        upper_line = "\u256D\u2500\u2500\u256E"
        lower_line = "\u2570\u2500\u2500\u256F"
        pipe = '\u2502'
        
        cards_discarded_str = ""
        cards_left_str = ""

        if cards_discarded < 10:
            cards_discarded_str += "0"
        if len(deck) < 10:
            cards_left_str += "0"
    
        cards_discarded_str += str(cards_discarded)
        cards_left_str += str(len(deck))


        post = [
            "    " + upper_line,
            "    " + pipe + cards_left_str + pipe,
            "    " + pipe + cards_discarded_str + pipe,
            "    " + lower_line 
        ]
        whitespace = ["", "        "]

        if i == 0:
            prestr = [whitespace[0], whitespace[0]]
            poststr = [post[0], post[1]]
        elif i == 1:
            prestr = [whitespace[0], whitespace[0]]
            poststr = [post[2], post[3]]
        else:
            prestr = [whitespace[0], whitespace[0]]
            poststr = [whitespace[1], whitespace[1]]

        print_row_of_cards(prestr, cards, sections, poststr)



# print_row_of_cards(cards, sections): print 4 cards lying next to eachother, one half (upper/lower) at a time
# parameter explanation:
#
# pre_strings[2]:
#   [row1, row2]    - strings to be printed before row of cards (2 terminal rows)
#   None
#
# cards[4] (different types of elements):
#   (suit, rank)    - tuple representing a card denoted by suit and rank (same as those in deck[])
#   int             - if 0: empty outline of a card, if non-zero: outline of a card with specified value, denoting hidden cards
#   None            - empty, print whitespace
#
# bool sections[4]:
#   True    - print upper part of corresponding card (same index) in cards[]
#   False   - print lower part
#
# post_strings[2]:
#   [row1, row2]    - strings to be printed after row of cards
#   None
#
def print_row_of_cards(pre_strings, cards, sections, post_strings):
    red = "\033[31m"
    default = "\033[0m"
    #red = "\033[31m\033[107m" #inverted
    #default = "\033[30m\033[107m" #inverted

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
    if pre_strings:
        row1 += pre_strings[0]
        row2 += pre_strings[1]

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

    if post_strings:
        row1 += post_strings[0]
        row2 += post_strings[1]

    print(row1)
    print(row2)


#func below are acctions, not rule

def moveCard(src, dst):  # move top card in src to dst, assumes src to be non-empty
    card = src[-1]
    src.pop()
    dst.append(card)

def discardCard(fromPile2): #discard a card
    fromPile2.pop()

def addCards(): #add four card in all piles
    moveCard(deck,pile1)
    moveCard(deck,pile2)
    moveCard(deck,pile3)
    moveCard(deck,pile4)

#func below are Rules


# moves top card in src to dst, if such operation is permitted (dst empty)
# return:
#   3 invalid input
#   2 dst is not empty
#   1 src is empty
#   0 success
def moveCardRules(src, dst):
    piles = [pile1, pile2, pile3, pile4]
    srcpile = src-1
    dstpile = dst-1

    if srcpile < 0 or dstpile < 0 or srcpile >= len(piles) or dstpile >= len(piles):
        return 3

    if len(piles[srcpile]) == 0:
        return 1

    if len(piles[dstpile]):
        return 2

    moveCard(piles[srcpile], piles[dstpile])
    return 0


# discard a card, if such operation is permitted
# updates global variable cards_discarded
#return:
#   0 succes
#   1 operation not permitted
#   2 invalid input
#   3 source empty (no card to discard)
def discardCardRules(pile_n): # number between 1 and 4
    cardPiles = [pile1, pile2, pile3, pile4]
    status = False
    topCards = []
    global cards_discarded

    srcpile = pile_n - 1;
    if srcpile < 0 or srcpile >= len(cardPiles):
        return 2    # invalid input

    for p in cardPiles:
        if len (p) == 0:
            p.append(("Joker",0))
        topCards.append(p[-1])

    discarded = cardPiles[srcpile][-1]
    for c in topCards:
        if c[0] == discarded[0]:
            if c[1] > discarded[1]:
                status = True

    for p in cardPiles:
        if len(p) == 1 and p[0][0] == "Joker":
            p.pop()

    if status == True:
        discardCard(cardPiles[srcpile])
        cards_discarded += 1
        return 0    #success

    if discarded[0] == "Joker":
        return 3    #src empty
    
    return 1    # card not discardable

    #alt.ver. without jokers:
    #srcpile = pile_n - 1;
    #if srcpile < 0 or srcpile >= len(cardPiles):
    #    return 2
    #if not len(cardPiles[srcpile]):
    #    return 3
    #srccard = cardPiles[srcpile][-1]
    #for i in range(len(cardPiles)):
    #    if srcpile == i or not len(cardPiles[i]):
    #        continue
    #    cmpcard = cardPiles[i][-1] 
    #    if cmpcard[0] == srccard[0] and cmpcard[1] > srccard[1]:
    #        cardPiles[srcpile].pop()
    #        return 0
    #return 1



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
        y = discardCardRules(x)
        

#game loop
def gameLoop():
    print("#do this together//ed")


initCards()

#TEMP prototype
while True:
    print_cards()

    inp = input()
    if inp == 'd':
        if len(deck) >= 4:
            addCards()

    elif len(inp) >= 2 and inp[1] == 'd':
        discardCardRules(int(inp[0]))

    elif len(inp) >= 2:
        moveCardRules(int(inp[0]), int(inp[1]))


#example


# moveCard(deck, pile1)
# moveCard(deck, pile1)
# moveCard(deck, pile1)
# moveCard(deck, pile2)
# moveCard(deck, pile2)
# moveCard(deck, pile4)
# moveCard(deck, pile4)
# pile1 = [("S", 4), ("H", 13)]
# pile2 = [("C", 14)]
# pile3 = [("H", 11), ("C", 5)]
# pile4 = [("H", 12)]
# print_cards()
# print(discardCardRules(4))
# print_cards()
# print(discardCardRules(3))
# print_cards()
