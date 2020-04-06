import poker
from base_player import Player
from collections import defaultdict, deque

class StatsPlayer(Player):

    def __init__(self, name, chips, alpha):
        super().__init__(name, chips)
        self.alpha = float(alpha)

    def __repr__(self):
        return repr((self.name, self.chips, self.alpha))

    def getAction(self, to_call, table_cards, pot_size, in_play_names, blinds):
        
        # print('Hand: ' , poker.returnCardStringShort(self.hand))
        if len(table_cards) == 0:
            # Evaluate starting hand by pairs then card value
            return self.evaluateStartingHand(to_call, pot_size, blinds)
        else:
            # Get all possible hands your opponents can have
            opponent_permutations = self.getPermutations(table_cards, 2, self.hand)
            opponent_possibilities = sum([len(x) for x in opponent_permutations.values()])

            hand, score = poker.returnHandScore(self.hand + table_cards)
            hand_sum = poker.returnHandDigitSum(hand)
            opponent_win_probability = sum([len(opponent_permutations[x]) / opponent_possibilities for x in opponent_permutations if x > score])

            # Tie-break evaluation
            for same_score_hand in opponent_permutations[score]:
                tie_hand, tie_score = poker.returnHandScore(table_cards + list(same_score_hand))
                tie_hand_sum = poker.returnHandDigitSum(tie_hand)
                if tie_hand_sum > hand_sum:opponent_win_probability += 1 / opponent_possibilities

            # Scale probability to all opponents losing
            opponent_win_probability = 1 - (1 - opponent_win_probability) ** len(in_play_names)

            print('Probability of losing: %f' % (opponent_win_probability))
            
            if self.alpha >= opponent_win_probability or (to_call != 0 and to_call / pot_size <= self.alpha):
                return self.getBetSize(1 - opponent_win_probability, to_call, pot_size, blinds)
            elif to_call != 0: return -1
        return to_call     

    def evaluateStartingHand(self, to_call, pot_size, blinds):
        # Any pair gets 12 points
        # Plus sum of both digits if > 24 * (1 - self.alpha)
        # Call or raise
        hand_score = int(self.hand[0] % 13 == self.hand[1] % 13) * 12
        if (hand_score + sum(self.hand)) / 24 >= (1 - self.alpha):
            return to_call
        if to_call / pot_size <= self.alpha: 
            return to_call
        return -1

    def getBetSize(self, win_probability, to_call, pot_size, blinds):
        rounded_bet = (win_probability * pot_size // blinds) * blinds
        bet = self.getMaxBet(to_call, (rounded_bet - to_call), blinds)
        return bet

    def getWinProbability(self, own_permutations, own_possibilities, opponent_permutations, opponent_possibilities):
        probability = 0
        for score in range(9):
            probability += (len(own_permutations[score + 1] / own_possibilities)) * (len(opponent_permutations[score]) / opponent_possibilities)

            for possible_own_hand in own_permutations[score]:
                temp_own_hand, _ = poker.returnHandScore(self.hand + list(possible_own_hand))
                for possible_opp_hand in opponent_permutations[score]:
                    temp_opp_hand, _ = poker.returnHandScore
        
    def getMaxBet(self, to_call, intended_bet, blinds):
        return int(max(to_call, min(intended_bet, self.chips) // blinds * blinds) )

    def getPermutations(self, base_cards, cards_to_guess, excluded_cards=[]):
        ''' 
        Generate all possible hands based on cards provided.
        Can exclude specific cards during the process.
        '''
        probability_table = defaultdict(deque)
        if cards_to_guess == 2:
            for card_1 in range(52):
                if card_1 in (base_cards + excluded_cards): continue
                for card_2 in range(card_1 + 1, 52):
                    if card_2 in (base_cards + excluded_cards): continue
                    hand, score = poker.returnHandScore(base_cards + [card_1, card_2])
                    probability_table[score] += [(card_1, card_2)]

        elif cards_to_guess == 1:
            for card in range(52):
                if card in (base_cards + excluded_cards): continue
                hand, score = poker.returnHandScore(base_cards + [card])
                probability_table[score] += [card]
        return probability_table

    

if __name__ == '__main__':
    s = StatsPlayer('Annie', 1200, 0.2)
    p_table = s.getPermutations([0, 1, 14, 36, 27], 2)
    p_total = sum([len(x) for x in p_table.values()])

    for key in p_table:
        print(key, len(p_table[key]), len(p_table[key]) / p_total)