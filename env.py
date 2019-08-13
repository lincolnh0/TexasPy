import numpy as np
import scipy
from random import shuffle
import random

import player, poker

# TODO: Add betting records for players
#       Check if player can afford blinds / all in mechanisms

class GameObject(object):
    """Game Object"""
    def __init__(self, listOfPlayers,startChips):

        self.players = listOfPlayers
        self.blinds = startChips / 20
        self.dealer = self.players[0]
        self.playerChips = {}
        for p in self.players: self.playerChips[p] = startChips
        self.playerCount = len(self.players)

    def runGame(self,count):
        for i in range(count):
            self.setupRound()
            self.runRound()

    def setupRound(self):
        # Reset Cards
        self.playerCards = {}
        for p in self.players:
            self.playerCards[p] =[0,0]
            p.setBlinds(self.blinds)

        self.dealer = self.players[(self.players.index(self.dealer) + 1) % len(self.players)]
        self.activePlayers = list(self.players)
        self.deck = [i for i in range(52)]
        self.record = []
        self.shuffleCards()
        self.table = []
        self.pot = 0

    def shuffleCards(self):
        riffle = random.randint(1,5)
        for i in range(riffle):
            shuffle(self.deck)
        cut = random.randint(10,40)
        for i in range(cut):
            self.deck.append(self.deck.pop(0))

    def runRound(self):
        rRecord = []


        self.dealPlayerCards()

        # Collect blinds
        smallB = self.activePlayers[((self.activePlayers.index(self.dealer)) + len(self.activePlayers) - 2) % len(self.activePlayers)]
        bigB = self.activePlayers[((self.activePlayers.index(self.dealer)) + len(self.activePlayers) - 1) % len(self.activePlayers)]
        print("----Blinds %d/%d----" % (self.blinds / 2, self.blinds))

        self.addPlayerChips(smallB, -(self.blinds / 2))
        self.addPlayerChips(bigB, - self.blinds)
        self.pot += self.blinds * 1.5

        self.sidepot = {}


        # Four rounds of betting
        for i in range(4):
            print("---BETTING ROUND %d---" % (i+1))
            print("Table Cards are %s" % poker.returnCardStringShort(self.table))
            curBet = self.blinds if i == 0 else 0

            betted = {}
            for p in self.activePlayers:
                betted[p] = 0

            roundRecord = []

            curPlayer = self.dealer

            # When should the round finish, default set to the player before the dealer
            loopFinish = bigB

            # While the table is still enquiring each player, ask for their bet
            # If all in, create potential side pot
            # If less than zero (i.e. folding), remove them from the list of active players
            # if greater or equak, update currentBet (if necessary), set last to to bet as the previous player
            # Add betting amout to pot

            # roundRecord => printing in real time
            # rRecord => for player
            while True:
                if i == 0:
                    betted[smallB] = self.blinds / 2
                    betted[bigB] = self.blinds

                betToMatch = (int)(curBet-betted[curPlayer])
                pBet = self.getBetFromPlayer(curPlayer, betToMatch)


                if pBet < 0: # if player folds
                    rRecord.append((curPlayer.returnName(),-1))
                    roundRecord.append("%s folds" % (curPlayer.returnName()))
                else:


                    # Try to implement all in verification only when pBet < betToMatch
                    # Because all inning with enough chips is the same as normal betting
                    # Then extend the side pot mechanics to blinds as well


                    # Idea for adding players to all available sidepots:
                    # for each sidepot, cycle betted for each player, those who betted more than that amount is added to the pot.

                    # If a player goes all in
                    if pBet < betToMatch:
                        if self.verifyAllIn(curPlayer,pBet):
                            verb = ("goes all in with £%d" % (pBet))
                            for k in self.sidepot.keys():    # add player to all sidepots that they are eligible to enter
                                if pBet >= k:
                                    self.sidepot[k].append(curPlayer)

                            if pBet not in self.sidepot.keys(): # create a new sidepot if there isn't one with the current amount
                                self.sidepot[pBet] = [curPlayer]
                                for p in self.activePlayers:
                                    if p != curPlayer and betted[p] >= pBet:
                                        self.sidepot[pBet].append(p)

                            curBet = pBet + betted[curPlayer]

                        else:
                            pBet = betToMatch # if the player has the necessary chips but sets a bet lower than the currentBet, make it equal

                    if pBet == betToMatch: verb = "checks" if pBet == 0 else str("calls with £%d" % (pBet))


                    if pBet > betToMatch:
                        loopFinish = self.activePlayers[(self.activePlayers.index(curPlayer) + len(self.activePlayers) - 1) % len(self.activePlayers)]
                        verb = ("bets £%d" % (pBet)) if betToMatch == 0 else ("raises £%d" % ((pBet)))
                        curBet = pBet + betted[curPlayer]

                    roundRecord.append("%s %s" % (curPlayer.returnName(),verb))
                    rRecord.append((curPlayer.returnName(),pBet))

                    betted[curPlayer] += pBet



                    self.pot += pBet
                    self.addPlayerChips(curPlayer,-pBet)




                if len(self.activePlayers) > 1:

                    nextPlayer = self.activePlayers[(self.activePlayers.index(curPlayer) + 1) % len(self.activePlayers)]
                if pBet == -1: self.activePlayers.remove(curPlayer)

                rRecord.append((curPlayer.returnName(),curBet))
                if curPlayer == loopFinish: break
                curPlayer = nextPlayer



            for r in roundRecord: print(r)
            print("Pot has £%d" % (self.pot))
            self.record.append(rRecord)
            if len(self.activePlayers) == 1: break # end game early when all but one folds
            self.dealTableCards()

        if len(self.activePlayers) == 1: # if everyone else folds, the last player staning collects the pot
            print('---------------------')
            print('%s has won £%d' %(self.activePlayers[0].returnName(),self.pot))
            self.addPlayerChips(self.activePlayers[0],self.pot)



    def getBetFromPlayer(self,player,betToMatch):
        player.setTableCards(self.table)
        player.setAvailableChips(self.playerChips[player])
        pBet = player.returnBet(betToMatch,self.record)
        return pBet

    def verifyAllIn(self,player,pBet):
        if self.playerChips[player] == pBet:
            return True

        return False

    def addPlayerChips(self,player,amount):
        self.playerChips[player] += amount
        player.setAvailableChips(self.playerChips[player])

    def dealPlayerCards(self):
        for i in range(2):
            for j in self.players:
                card = self.deck.pop(0)
                self.playerCards[j][i] = card
                j.setCards(card)


    def dealTableCards(self):
        """Deal flops, turn and river"""
        if len(self.table) < 5:
            self.deck.pop(0)
            if(len(self.table) <3):
                for i in range(3):self.table.append(self.deck.pop(0))
            else:
                self.table.append(self.deck.pop(0))
        else:
            self.endRound()

    def endRound(self):
        print("---Betting Ended---")
        for i in self.players:
            if i in self.activePlayers:
                print("%s's hand: %s" % (i.returnName(),poker.returnCardStringShort(self.playerCards[i])))

        print("Table's Card: ")
        print(poker.returnCardStringShort(self.table))



        if len(self.sidepot.keys()) == 0:   # If there is no sidepot
            wP,wHand,wS = self.returnWinner(self.activePlayers)

            print("%s has won with %s\nWinning Hand:%s" % (wP.returnName(),poker.returnHandName(wS),poker.returnCardStringShort(wHand)))
            self.record[len(self.record) -1].append((wP.returnName(),-2))
            self.addPlayerChips(wP,self.pot)
        else:                               # If there exists > 0 sidepots
            lastSidePot = 0
            sortedKeys = sorted(self.sidepot.keys())
            for k in sortedKeys:
                wP,wHand,wS = self.returnWinner(self.sidepot[k])

                self.addPlayerChips(wP,(k-lastSidePot) * len(self.sidepot[k]))
                lastSidePot = k
                if len(self.sidepot[k]) > 1:
                    print("%s has won the £%d sidepot with %s\nWinning Hand:%s" % (wP.returnName(),k,poker.returnHandName(wS),poker.returnCardStringShort(wHand)))
                else:
                    print("£%d is returned to %s" % (k, wP.returnName()))

        self.printChips()
    def printChips(self):
        print("----Chips Update----")
        for p in self.players:
            print("%s has £%d" % (p.returnName(),self.playerChips[p]))


    '''Functions for determining winner and winning hand'''
    def returnWinner(self, playerList):
        'Returns Player Object, Winning Hand and Hand name'
        maxScore = 0
        winner = []
        winningHand = []

        # Compare scores of different players
        for i in playerList:
            tch = self.returnCombinedHand(i)
            h,s = poker.returnHandScore(tch)
            if s > maxScore:
                winner = [i]
                maxScore = s
                winningHand = [h]
            elif s == maxScore:
                winner.append(i)
                winningHand.append(h)

        # return the winner if no tie
        if len(winner) == 1: return i, winningHand[0], maxScore

        # tie-breaking try 1: card values
        cardValue = []
        for w in winningHand:
            cardValue.append(sum(list(map(lambda x: x% 13, w))))

        return winner[cardValue.index(max(cardValue))], winningHand[cardValue.index(max(cardValue))], maxScore

    def returnCombinedHand(self,playerID):
        totalHand = list(self.table)
        totalHand += self.playerCards[playerID]

        return totalHand


pList = []
pList.append(player.Player("Jessica"))
pList.append(player.StatsPlayer("Benjamin"))
pList.append(player.Player("Lincoln"))
pList.append(player.Player("Caleb"))
pList.append(player.Player("Melody"))
pList.append(player.Player("Melissa"))

go = GameObject(pList,2000)
go.runGame(1)
#go.run()
# hand = [0,1,2,3,4,5,6]
