deck = []
pile1 = []
pile2 = []
pile3 = []
pile4 = []



def initCards():
    suits = ["S","H","C","D"]
    ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]	# ace == 14
    for suit in suits:
        for rank in ranks:
            deck.append ((suit, rank))


def print_card(suit, rank):
	red = "\033[31m"
	default = "\033[0m"

	color = default		# terminal color
	symbol = "ERR"		# suit unicode symbol
	value = str(rank)	# rank unicode symbol (A, 1...10, J, Q, K)


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
	print('\u2502' + color + symbol + value + default + '\u2502')
	print("\u2570\u2500\u2500\u256F")


initCards()
print_card(deck[0][0], deck[0][1])
print_card(deck[13][0], deck[13][1])
print_card(deck[26][0], deck[26][1])
print_card(deck[39][0], deck[39][1])
