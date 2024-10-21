deck = []
def makeCard():
    suits = ["S","H","C","D"]
    ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    for suit in suits:
        for rank in ranks:
            deck.append ((suit, rank))


makeCard()