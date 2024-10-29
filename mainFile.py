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
    shortest = -1
    for pile in piles:
        if len(pile) > depth:
            depth = len(pile)
        if len(pile) < shortest or shortest == -1:
            shortest = len(pile)

    depth += 1
    if depth == 1:
        depth = 2

    hidden = 0
    if shortest >= 4:
        hidden = shortest - 2
        if hidden > 9:
            hidden = 9
    
    # depth is the number of rows to print
    # depth is atleast 2, as printing empty card outlines requires 2 rows

    print(" 1   2   3   4")

    # one call to print_row_at_cards() per iteration
    i = 0
    row = 0 # purely used by generate_pre_post_strings() as i does not necessarily correspond to row (happens if there are hidden cards)
    while i < depth:    # no "for in range()" as i might require modification
        cards = []
        sections = []

        for pile in piles:
            # hidden cards
            if i < hidden:
                cards.append(hidden)    # will print: |{hidden}+|
                sections.append(True)
                i = hidden-1   # i == hidden next iteration

            # empty pile and first 2 rows -> print empty card outline
            elif len(pile) == 0 and i < 2:    
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

        prestr, poststr = generate_pre_post_strings(row)
        print_row_of_cards(prestr, cards, sections, poststr)
        row += 1
        i += 1


# generate valid prestr and poststr
# desired pre/post strings/visuals are defined in this function
def generate_pre_post_strings(halfcard_row):
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
    
    if halfcard_row == 0:
        prestr = [whitespace[0], whitespace[0]]
        poststr = [post[0], post[1]]
    elif halfcard_row == 1:
        prestr = [whitespace[0], whitespace[0]]
        poststr = [post[2], post[3]]
    else:
        prestr = [whitespace[0], whitespace[0]]
        poststr = [whitespace[1], whitespace[1]]

    return prestr, poststr




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
        symbols[i], colors[i], values[i] = get_card_visuals(cards[i], red, default)


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


def get_card_visuals(card, red, default):
    suit = card[0]
    rank = card[1]

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


    # change ace (14), (10), jack (11), queen (12), king (13) to A, T, J, Q, K respectively
    if rank == 1 or rank == 14:
        value = 'A'

    elif rank == 10:   # '10' is two characters and therefore looks skewed when printed
        value = 'T'

    elif rank == 11:
        value = 'J'

    elif rank == 12:
        value = 'Q'

    elif rank == 13:
        value = 'K'

    else:
        value = str(rank)


    return symbol, color, value




#func below are acctions, not rule

def moveCard(src, dst):  # move top card in src to dst, assumes src to be non-empty
    card = src[-1]
    src.pop()
    dst.append(card)

def discardCard(fromPile2): #discard a card
    fromPile2.pop()

def addCards(): #add four cards in all piles
    if len(deck) != 0:
        moveCard(deck, pile1)
        moveCard(deck, pile2)
        moveCard(deck, pile3)
        moveCard(deck, pile4)
        return 0

    return 1

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
# if flag test is set, no card will actually be discarded and cards_discarded
# will remain unchanged (this is used to test whether or not the player can discard any cards)
#return:
#   0 success
#   1 operation not permitted
#   2 invalid input
#   3 source empty (no card to discard)
def discardCardRules(pile_n, test): # number between 1 and 4
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
        if not test:    # not a test, player wants to discard
            discardCard(cardPiles[srcpile])
            cards_discarded += 1
        return 0    #success

    if discarded[0] == "Joker":
        return 3    #src empty
    
    return 1    # card not discardable


# check whether or not game is over
def gameover():
    if deck:    # still cards in the deck
        return False

    piles = [pile1, pile2, pile3, pile4]
    for pile in piles:
        if not pile:    # empty pile, player can still move cards
            return False

    for i in range(len(piles)):
        if discardCardRules(i+1, True) == 0:    # player can still discard card(s)
            return False

    return True # game over, player cannot do anything



#func below are player actions

# get input from user and perform operations
#   True    - conclude current session/finish
#   False   - continue (print cards and call callAction() again)
def callAction():
    choice = {"n": "deal cards", "m": "move card", "d": "discard card", "f": "finish"}
    viewdict(choice)

    action = input("choose action: ")
    if action == "n":
        if addCards():
            print ("no more cards to deal")

    elif action == "m":
        try:
            src = int(input("from: "))
            dst = int(input("to: "))
        except ValueError:
            print("Error: invalid input\n")
            return False
        except KeyboardInterrupt:
            print()
            exit()
        except EOFError:
            print()
            exit()

        status = moveCardRules(src, dst)

        if status == 1:
            print("source pile is empty")
        elif status == 2:
            print("targeted pile isn't empty")
        elif status == 3:
            print("Error: invalid input")

        print()


    elif action == "d":
        try:
            p = int(input("from: "))
        except ValueError:
            print("Error: invalid input\n")
            return False
        except KeyboardInterrupt:
            print()
            exit()
        except EOFError:
            print()
            exit()

        status = discardCardRules(p, False)

        if status == 1:
            print("targeted card isn't discardable")
        elif status == 2:
            print("Error: invalid input")
        elif status == 3:
            print("source pile is empty")

        print()


    elif action == "f":
        return True

    return False


def gameLoop():
    scorelist = []
    while True:
        deck.clear()
        pile1.clear()
        pile2.clear()
        pile3.clear()
        pile4.clear()
        initCards()

        print("\033[32mPatiens Idioten\033[0m\n")
        game = {"n":"new game", "s":"score", "q":"quit"}
        viewdict(game)

        try:
            opt = input("choose option: ")
        except KeyboardInterrupt:
            print()
            exit()
        except EOFError:
            print()
            exit()

        if opt == "n":
            while True:
                print_cards()
                if gameover():
                    print("\033[31mGame Over!\033[0m")
                    break

                if callAction():
                    break

            score = 48 - cards_discarded
            scorelist.append(score)
            print (f"your score was: {score}\n")

        elif opt == "s":
            print("your scores:")
            print("game: score")
            x = 0
            for i in range(len(scorelist)):
                print(f"{i+1}:    {scorelist[i]}")
                x += scorelist[i]

            if len(scorelist):
                average = round((x) / (len(scorelist)),2 )
                print(f"average: {average}")

            print('\n')

        elif opt == "q":
            break


gameLoop()
