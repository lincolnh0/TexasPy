import poker
from random import random
from player_type.stats_player import StatsPlayer

class BluffPlayer(StatsPlayer):
    
    def __init__(self, name, chips, alpha, bluff_frequency, bluff_strength, debug):
        ''' 
        Bluff Player constructor. 
        Player will proceed if its opponents have a probability less than **alpha** to win.
        If not, it will also proceed if 
        '''
        super().__init__(name, chips, alpha, debug)
        self.bluff_frequency = float(bluff_frequency)
        self.bluff_strength = float(bluff_strength)
        self.is_bluffing = self.bluff_frequency > random() 


    def __repr__(self):
        ''' 
        String representation with alpha and bluff_alpha values. 
        '''
        return repr((self.name, self.chips, self.alpha, self.bluff_frequency, self.bluff_strength))
    
    def getBetSize(self, opponent_win_probability, to_call, pot_size, blinds):
        ''' 
        Return appropriate bet size based on winning probability, with a chance to bluff.
        '''
        if self.is_bluffing:
            if self.debug: print('Bluffing', opponent_win_probability * (1 - self.bluff_strength))
            opponent_win_probability *= 1 - self.bluff_strength
        
        bet = 0
        if self.alpha >= opponent_win_probability or (to_call != 0 and to_call / pot_size <= self.alpha):
            bet = self.getMaxBet(to_call, (1 - opponent_win_probability) * (pot_size - to_call), blinds)
        elif to_call != 0: bet = -1
        return bet

    def setRecord(self, message):
        super().setRecord(message)
        if message[0] == 'WINNER':
            self.is_bluffing = self.bluff_frequency > random() 
            