from random import shuffle
from collections import deque
import numpy as np
import random

import player, poker

class GameObject(object):

    def __init__(self, players, blinds, ante=0):
        self.players = {id:player for id, player in enumerate(players)}
        self.dealer = 0

    def setup(self):
        ''' Performs initial set up of a new hand. '''
        # Update dealer, collect blinds / antes
        self.dealer = (self.dealer + 1) % len(self.players)

        # Clear player hands, community cards and pot
        self.table = []
        self.pot = []

        # Shuffle cards
        self.deck = list(range(52))
        random.shuffle(self.deck)

        # Deal two cards to each player
        for id, player in self.players.items():
            startIndex = 2 * id
            player.setHand([self.deck[startIndex: startIndex+ 2]])
        
        # Remove dealt cards from deck
        self.deck = self.deck[len(self.players) * 2:]

    def dealTable(self):
        ''' Store the first 3, 4 or 5 cards of the remaining deck as community cards '''
        if len(self.table) == 0:
            self.table = self.deck[:3]
        elif len(self.table) < 5:
            self.table = self.deck[:(len(self.table))]
        

    def run(self):
        
        # Setup players in play and rotate table
        inPlay = deque(self.players.keys())
        inPlay.rotate(self.dealer)
        # Keep track of main and sidepots
        self.pot = [(0, inPlay)]

        toCall = 0 
        currentPot = 0

        while len(self.table) <= 5:
            folded = []

            for id in inPlay:
                action = self.players[id].getAction(toCall)
                if action == -1: folded.append(id)
                

            
            # Update eligible players for current pot
            inPlay = [id for id in inPlay if id not in folded]
            self.pot[-1] = (currentPot, inPlay)

            # Deals table card once betting is finished
            self.dealTable()
            