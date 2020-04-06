'''A collection of static methods used by both the environemnt and players to use'''


''' STATIC FUNCTIONS FOR CARD NAME FORMATTING'''
def returnCardNumberText(id):
    num = id % 13
    if num == 0: return "Two"
    if num == 1: return "Three"
    if num == 2: return "Four"
    if num == 3: return "Five"
    if num == 4: return "Six"
    if num == 5: return "Seven"
    if num == 6: return "Eight"
    if num == 7: return "Nine"
    if num == 8: return "Ten"
    if num == 9: return "Jack"
    if num == 10: return "Queen"
    if num == 11: return "King"
    if num == 12: return "Ace"

def returnCardNumberLetter(id):
    num = id % 13
    if num == 0: return "2"
    if num == 1: return "3"
    if num == 2: return "4"
    if num == 3: return "5"
    if num == 4: return "6"
    if num == 5: return "7"
    if num == 6: return "8"
    if num == 7: return "9"
    if num == 8: return "10"
    if num == 9: return "J"
    if num == 10: return "Q"
    if num == 11: return "K"
    if num == 12: return "A"

def returnCardSuit(id):
    suit = id // 13
    if suit == 0: return '\u2660' #"Spades"
    if suit == 1: return '\u2665' #"Hearts"
    if suit == 2: return '\u2663' #"Clubs"
    if suit == 3: return '\u2666' #"Diamonds"

def returnCardString(id):
    result = []
    for i in id:
        result.append("%s of %s" % (returnCardNumberText(i),returnCardSuit(i)))
    return result

def returnCardStringShort(id):
    result = []
    for i in id:
        result.append("%s%s" % (returnCardSuit(i)[0],returnCardNumberLetter(i)))
    return result

def returnHandName(hand, score):
    if score == 0:
        return ("High Card")
    elif score == 1:
        return ("Pair")
    elif score == 2:
        return ("Two Pairs")
    elif score == 3:
        return ("Three of A Kind")
    elif score == 4:
        return ("Straight")
    elif score == 5:
        return ("Flush")
    elif score == 6:
        return ("Full House")
    elif score == 7:
        return ("Four of a Kind")
    elif score == 8:
        if hand[0] % 13 == 12: return ('Royal Flush')
        return ("Straight Flush")

'''STATIC functions for checking hands'''
def returnHighCard(hand, num):

    newHand = list(map(lambda x: x % 13,hand))
    popped = []
    out = []
    for i in range(num):
        index = newHand.index(max(newHand))
        if not index in popped:
            out.append(hand[index])
            newHand[index] = -10
            popped.append(index)

    return out

def returnPair(hand):
    newHand = list(map(lambda x: x % 13,hand))
    for i in newHand:
        if newHand.count(i) >= 2: return (True,list(filter(lambda x: x%13 == i, hand)))

    return (False,0)

def returnTwoPairs(hand):
    newHand = list(map(lambda x: x % 13,hand))
    pairs = []
    for i in newHand:
        for j in newHand:
            if i!=j and newHand.count(i) >= 2 and newHand.count(j) >= 2:
                if not i in pairs: pairs.append(i)
    if len(pairs) >= 2:
        pairs.sort(reverse=True)
        h1 = list(filter(lambda x: x%13 == pairs[0], hand))[:2]
        h2 = list(filter(lambda x: x%13 == pairs[1], hand))[:2]
        return (True, (h1+h2))
    return (False,0)

def returnThreeOfAKind(hand):
    newHand = list(map(lambda x: x % 13,hand))
    newHand.sort(reverse=True)
    for i in newHand:
        if newHand.count(i) >= 3: return (True,list(filter(lambda x: x%13 == i, hand)))

    return (False,0)

def returnFullHouse(hand):
    if returnTwoPairs(hand)[0] and returnThreeOfAKind(hand)[0]:
        pair = list(set(returnTwoPairs(hand)[1]) - set(returnThreeOfAKind(hand)[1]))

        return (True, (returnThreeOfAKind(hand)[1] + pair))

    return (False,0)

def returnFourOfAKind(hand):
    newHand = list(map(lambda x: x % 13,hand))
    for i in newHand:
        if newHand.count(i) >= 4: return (True,list(filter(lambda x: x%13 == i, hand)))

    return (False,0)

def returnFlush(hand):
    newHand = list(map(lambda x: x // 13,hand))
    out = []
    for i in newHand:
        if newHand.count(i) >= 5:
            for j in range(len(newHand)):
                if newHand[j] == i:
                    out.append(hand[j])
            out.sort(reverse=True)
            return (True,out)

    return (False,0)

def returnStraight(hand):
    newHand = []
    for h in hand:
        newHand.append((h%13,h))
        if (h%13 == 12): newHand.append((-1,h))

    newHand.sort(key=lambda x:x[0])
    out = [newHand[0]]
    for i in range(len(newHand) -1):
        if (newHand[i+1][0] - newHand[i][0] != 0):
            if(newHand[i+1][0] - newHand[i][0] == 1):
                out.append(newHand[i+1])
            else:
                if len(out) >= 5:
                    out.sort(key=lambda x:x[0],reverse=True)
                    return (True,[i[1] for i in out][:5])
                out = [newHand[i+1]]
    if len(out) >= 5:
        out.sort(key=lambda x:x[0],reverse=True)
        return (True,[i[1] for i in out][:5])

    return (False,0)

def returnStraightFlush(hand):
    newHand = hand
    spades = []
    hearts = []
    clubs = []
    diamonds = []

    for i in newHand:
        if (i//13 == 0): spades.append(i)
        if (i//13 == 1): hearts.append(i)
        if (i//13 == 2): clubs.append(i)
        if (i//13 == 3): diamonds.append(i)

    if len(spades) >= 5: return returnStraight(spades)
    if len(hearts) >= 5: return returnStraight(hearts)
    if len(clubs) >= 5: return returnStraight(clubs)
    if len(diamonds) >= 5: return returnStraight(diamonds)

    return (False, 0)

def returnHandScore(totalHand):
    '''Returns best 5 cards and hand score'''
    score = 0
    hand = []
    if returnStraightFlush(totalHand)[0] :
        score = 8
        hand = returnStraightFlush(totalHand)[1]
    elif returnFourOfAKind(totalHand)[0]:
        score = 7
        hand = returnFourOfAKind(totalHand)[1]
    elif returnFullHouse(totalHand)[0]:
        score = 6
        hand = returnFullHouse(totalHand)[1]
    elif returnFlush(totalHand)[0]:
        score = 5
        hand = returnFlush(totalHand)[1]
    elif returnStraight(totalHand)[0]:
        score = 4
        hand = returnStraight(totalHand)[1]
    elif returnThreeOfAKind(totalHand)[0]:
        score = 3
        hand = returnThreeOfAKind(totalHand)[1]
    elif returnTwoPairs(totalHand)[0]:
        score = 2
        hand = returnTwoPairs(totalHand)[1]
    elif returnPair(totalHand)[0]:
        score = 1
        hand = returnPair(totalHand)[1]
    remain = list(set(totalHand) - set(hand))
    hand += returnHighCard(remain, 5-len(hand))
    return hand, score

def returnHandDigitSum(hand, score):
    add_card_sum_hand = [
        4, 5, 7, 8
    ]
    if score in add_card_sum_hand: return sum([x % 13 for x in hand])
    if score == 1: return sum([x % 13 for x in hand[2:]]) + 100 * (hand[0] % 13) 
    if score == 2: return hand[4] + 100 * ((hand[0] % 13) + (hand[2] % 13))
    if score == 3: return sum(x % 13 for x in hand[3:]) + 100 * (hand[0] % 13) 
    if score == 6: return 100 * (hand[0] % 13) + (hand[3] % 13)
    if score == 0: return sum([x ** i for i, x in enumerate(hand)])