import random,math
import poker


class Player():
    def __init__(self,name="Bot",alwaysFold=False):
        self.name = name
        self.cards = []
        self.tableCards = []
        self.chips = 0
        self.alwaysFold = alwaysFold

    def returnName(self):
        return self.name

    def returnChips(self):
        return self.chips

    def setBlinds(self,blinds):
        self.blinds = blinds

    def setCards(self,card):
        self.cards.append(card)

    def setTableCards(self,cards):
        self.tableCards = cards

    def setAvailableChips(self,amount):
        self.chips = amount

    def printCard(self):
        print(env.returnCardStringShort(self.cards))

    def returnBet(self,curBet,record=[]):
        r = random.randint(0,100)
        bet = 0
        if self.alwaysFold:return -1
        if curBet == 0:
            bet = 0
        elif self.chips >= curBet:
            bet = curBet
        else:
            bet = -1
        return bet

def printRecord(record,printAll=True,roundNo=0):
    if printAll:
        for rounds in record:
            for line in rounds:
                action = "betted £%d" % (line[1])
                if line[1] == 0: action = "checked"
                if line[1] == -1: action = "folded"
                if line[1] == -2: action = "won\n--End Of Round--"
                print("%s %s" % (line[0], action))


# TODO: Refine odds to multiplier conversion and when to fold
class StatsPlayer(Player):
    '''A Player Object that returns bet based on simple probabilities to win.'''

    def __init__(self,name,threshold = 0.1):
        super(StatsPlayer, self).__init__()
        self.name = name
        self.threshold = {}

    '''Probabilities are calculated by only considering outs for this player. More complex ideas
    such as half outs and hidden outs are not yet implemented. 5/6/2019'''
    def returnBet(self,curBet,record=[]):
        if len(self.tableCards) != 0:
            bH, handScore = poker.returnHandScore(list(self.cards + self.tableCards))
            selfEval = self.returnOuts(list(self.cards + self.tableCards), handScore)
            oppEval = self.returnOuts(list(self.cards + self.tableCards), handScore, self.cards)
        else:
            selfEval = self.evalStartHand()
        odds = []



        multiplier = 1

        # Evaluation Process:
        # 1. Evaluate starting hand
        # 2. After flop, turn, river => get odds of achieving different hands
        # 3.



        roundedBet = int(math.ceil(self.blinds * multiplier / 100) * 100)

        return max(roundedBet, curBet)

    # Store an dictionary for every possible score -> cards that would give this score
    # Structure: {handScore (0-8): List of (tuples of) cards required to make that hand}
    def returnOuts(self, cards, start, excludeList=[]):
        scoreTable = {}
        for i in range(start, 9): scoreTable[i] = []

        if len(cards) == 5 or len(excludeList) > 0:

            for i in range(52):
                for j in range(52):
                    if i != j and (i not in cards) and (j not in cards):
                        newHand = list(set(cards + [i,j]) - set(excludeList))
                        bH, score = poker.returnHandScore(newHand)
                        if score in scoreTable.keys():
                            if (j,i) not in scoreTable[score]:
                                scoreTable[score].append((i,j))
        elif len(cards) == 6:
            for i in range(52):
                if i not in cards:
                    newHand = cards + [i]
                    bH,score = poker.returnHandScore(newHand)
                    if score in scoreTable.keys(): scoreTable[score].append(i)

        return scoreTable

    def evalStartHand(self):
        pairValue = (self.cards[0] % 13) if (self.cards[0] % 13) == (self.cards[1] % 13) else 0
        cardValue = (self.cards[0] % 13) + (self.cards[1] % 13)
        flushValue = 1 if (self.cards[0] // 13) == (self.cards[0] // 13) else 0

        diff = 5 if pairValue != 0 else math.fabs((self.cards[0] % 13) - (self.cards[1] % 13))
        straightValue = max(0,5 - diff)

        return sum([pairValue,cardValue,flushValue,straightValue])

    def returnProbs(self,outs,remainDeck,cardToGo):
        denom = 1

        for c in range(cardToGo):
            denom *= remainDeck - c
            #print(denom)

        return (len(outs)/denom)

if __name__ == "__main__":
    Jane = StatsPlayer("Jane")
    Jane.setCards(1)
    Jane.setCards(2)
    Jane.setTableCards([4,20,3,6,7])
    gH = Jane.returnOuts(list(Jane.tableCards + Jane.cards))
    for g in gH.keys():
        print(poker.returnHandName(g),gH[g])
