import random,math
import poker

class Player(object):
    
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []

    def __repr__(self):
        return repr((self.name, self.hand, self.chips))

    def setHand(self, hand):
        self.hand = hand

    def setTable(self, tableCards):
        self.tableCards = tableCards

    def getAction(self, toCall):
        """ 
        Returns integer:
        <: fold
        0: check
        >: call/bet/raise
        """
        pass

    def setRecord(self, action):
        pass

    

    
