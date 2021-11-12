'''A collection of static methods used by both the environemnt and players to use'''

POKER_SCORE_HIGH_CARD = 0
POKER_SCORE_PAIR = 1
POKER_SCORE_TWO_PAIRS = 2
POKER_SCORE_THREE_OF_A_KIND = 3
POKER_SCORE_STRAIGHT = 4
POKER_SCORE_FLUSH = 5
POKER_SCORE_FULL_HOUSE = 6
POKER_SCORE_FOUR_OF_A_KIND = 7
POKER_SCORE_STRAIGHT_FLUSH = 8

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
    if suit == 0: return '\u2660 Spades'
    if suit == 1: return '\u2665 Hearts'
    if suit == 2: return '\u2663 Clubs'
    if suit == 3: return '\u2666 Diamonds'

def returnCardString(id):
    return ["%s of %s" % (returnCardNumberText(i),returnCardSuit(i)) for i in id]

def returnCardStringShort(id):
    return ["%s%s" % (returnCardSuit(i)[0],returnCardNumberLetter(i)) for i in id]

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
def returnHighCard(hand):
    '''
    Return cards in descending true value.
    '''

    # No need to consider duplicate keys because context, argument will never have pairs.
    hand_dict = {x % 13: x for x in hand}
    reversed_list = sorted(hand_dict.keys(), reverse=True)

    return [hand_dict[x] for x in reversed_list]

def returnPair(hand):
    new_hand = [x % 13 for x in hand]
    for i in new_hand:
        if new_hand.count(i) >= 2: return (True, [x for x in hand if x % 13 == i])

    return (False, [])

def returnTwoPairs(hand):
    new_hand = [x % 13 for x in hand]
    pairs = []
    for i in new_hand:
        for j in new_hand:
            if i!=j and new_hand.count(i) >= 2 and new_hand.count(j) >= 2:
                if i not in pairs: pairs.append(i)
    if len(pairs) >= 2:
        pairs.sort(reverse=True)
        h1 = [x for x in hand if x % 13 == pairs[0]][:2]
        h2 = [x for x in hand if x % 13 == pairs[1]][:2]
        return (True, (h1 + h2))
    return (False, [])

def returnThreeOfAKind(hand):
    new_hand = [x % 13 for x in hand]
    new_hand.sort(reverse=True)
    for i in new_hand:
        if new_hand.count(i) >= 3: return (True, [x for x in hand if x % 13 == i])

    return (False, [])

def returnFullHouse(hand):
    if returnTwoPairs(hand)[0] and returnThreeOfAKind(hand)[0]:
        pair = list(set(returnTwoPairs(hand)[1]) - set(returnThreeOfAKind(hand)[1]))

        return (True, (returnThreeOfAKind(hand)[1] + pair))

    return (False, [])

def returnFourOfAKind(hand):
    new_hand = [x % 13 for x in hand]
    for i in new_hand:
        if new_hand.count(i) >= 4: return (True, [x for x in hand if x % 13 == i])

    return (False, [])

def returnFlush(hand):
    new_hand = [x // 13 for x in hand]
    out = []
    for i in new_hand:
        if new_hand.count(i) >= 5:
            for index, value in enumerate(new_hand):
                if value == i:
                    out.append(hand[index])
            out.sort(reverse=True)
            return (True, out)

    return (False, [])

def returnStraight(hand):
    new_hand = []
    for h in hand:
        new_hand.append((h%13,h))
        if (h%13 == 12): new_hand.append((-1,h))

    new_hand.sort(key=lambda x:x[0])
    out = [new_hand[0]]
    for i in range(len(new_hand) -1):
        if (new_hand[i+1][0] - new_hand[i][0] != 0):
            if(new_hand[i+1][0] - new_hand[i][0] == 1):
                out.append(new_hand[i+1])
            else:
                if len(out) >= 5:
                    out.sort(key=lambda x:x[0], reverse=True)
                    return (True, [i[1] for i in out][:5])
                out = [new_hand[i+1]]
    if len(out) >= 5:
        out.sort(key=lambda x:x[0], reverse=True)
        return (True, [i[1] for i in out][:5])

    return (False, [])

def returnStraightFlush(hand):
    valid, hand = returnFlush(hand)
    if valid: return returnStraight(hand)
    return (valid, hand)
    
def returnHandScore(total_hand):
    '''
    Returns top cards (max. 5) and hand score.
    '''
    score = 0
    hand = []

    evaluation_list = [returnStraightFlush, returnFourOfAKind, returnFullHouse, returnFlush, returnStraight, returnThreeOfAKind, returnTwoPairs, returnPair]

    for i, fn in enumerate(evaluation_list):
        valid, hand = fn(total_hand)
        if valid:
            score = len(evaluation_list) - i
            break
    remain = list(set(total_hand) - set(hand))
    hand += returnHighCard(remain)
    return hand[:5], score

def returnTieBreakScore(hand, score):
    '''
    Return a tiebreak score to each hand.
    '''
    add_card_sum_hand = [
        4, 5, 7, 8
    ]
    if score in add_card_sum_hand: return sum([x % 13 for x in hand])
    if score == 1: return sum([x % 13 for x in hand[2:]]) + 100 * (hand[0] % 13) 
    if score == 2: return hand[4] + 500 * (hand[0] % 13) + 12 * (hand[2] % 13)
    if score == 3: return sum(x % 13 for x in hand[3:]) + 100 * (hand[0] % 13) 
    if score == 6: return 100 * (hand[0] % 13) + (hand[3] % 13)
    if score == 0: return sum([x ** i for i, x in enumerate(hand)])
