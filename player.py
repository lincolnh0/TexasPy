import random,math
import poker

class Player(object):
    
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []

    def __repr__(self):
        return repr((self.name, self.hand, self.chips))

    def setId(self, id):
        self.id = id

    def setHand(self, hand):
        self.hand = hand

    def getAction(self, toCall, tableCards):
        """ 
        Returns integer:
        <: fold
        0: check
        >: call/bet/raise
        """
        print('\n%s\'s turn -- %d to call' % (self.name, toCall))
        print('Hand: ' , poker.returnCardStringShort(self.hand))
        self.action = input('Please enter your value: ')
        return int(self.action), int(self.action == self.chips)

    def setAction(self, value):
        self.action = value

    def setRecord(self, action):
        pass

    

    
