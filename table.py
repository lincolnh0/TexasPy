from random import shuffle
from collections import defaultdict, deque

import player, poker

class GameObject(object):
    
    TABLE_CARDS_NAME = ['FLOP', 'TURN', 'RIVER']

    def __init__(self, players, blinds, ante=0):
        self.players = {id:player for id, player in enumerate(players)}
        self.blinds = blinds
        self.dealer = -1

    def run(self, count):
        for i in range(count):
            print('\n------ GAME NO. %d ------' % (i + 1))
            self.setup()
            self.playHand()

            print('\n------QUICK SUMMARY------')
            self.getPlayerSummary()

    def setup(self):
        ''' Performs initial set up of a new hand. '''
        # Update dealer, collect blinds / antes
        self.dealer = (self.dealer + 1) % len(self.players)

        # Clear player hands, community cards and pot
        self.table = []
        self.pot = []

        # Shuffle cards
        self.deck = list(range(52))
        shuffle(self.deck)

        # Deal two cards to each player
        for id, player in self.players.items():
            start_index = 2 * id
            player.setHand(self.deck[start_index: start_index+ 2])
        
        # Remove dealt cards from deck
        self.deck = self.deck[len(self.players) * 2:]

    def dealTable(self):
        ''' Store the first n cards of the remaining deck as community cards '''
        if len(self.table) == 0:
            self.table = self.deck[:3]
        elif len(self.table) < 5:
            self.table = self.deck[:len(self.table) + 1]
        

    def createSidePots(self, round_bet, in_play):
        pot = []
        
        # Get all the bets of the in play players
        bets = [round_bet[x] for x in in_play]

        # While not all bets are equal
        while (len(set(bets)) >= 1):

            # Get lowest common bet
            lowest_common_bet = min(bets)

            # Get bets from folded player that are up for grabs this turn
            leftover_bets = sum([min(round_bet[x], lowest_common_bet) for x in round_bet.keys() if x not in in_play])
            pot.append((leftover_bets + lowest_common_bet * len(in_play), in_play))


            # Update the remainging bets to be subtracted from the sidepot that was just generated
            # And add them to the next sidepot generation only if they are greater than the one just now
            in_play = [x for x in in_play if round_bet[x] > lowest_common_bet]
            bets = [round_bet[x] - lowest_common_bet for x in in_play]
            round_bet = {x:round_bet[x] - lowest_common_bet for x in round_bet.keys() if round_bet[x] > lowest_common_bet}

        return pot

    def playHand(self):
        
        # Setup players in play and rotate table
        # Ids of in-play players
        in_play = deque(self.players.keys())
        in_play.rotate(-self.dealer)

        small_blind = in_play[-2]
        big_blind = in_play[-1]

        self.players[small_blind].chips -= self.blinds / 2
        self.players[big_blind].chips -= self.blinds

        # Set up round bet records
        round_bet = defaultdict(int)
        round_bet[small_blind] = self.blinds / 2
        round_bet[big_blind] = self.blinds
        
        # Starts hand
        for i in range(4):

            current_player_id = in_play[0]
            last_bet_player_id = in_play[-1]
            all_checked = True

            # Three conditions
            # 1. Current player is not the one who last betted
            # 2. Everyone before has checked
            # 3. Big blind gets to check the first round
            while current_player_id != last_bet_player_id or all_checked or (i == 0 and current_player_id == big_blind):
                
                print('\nTABLE CARDS: ' , poker.returnCardStringShort(self.table))
                # Skip player's turn if they have zero chips but are still in play i.e. have already all-ined.
                if round_bet[current_player_id] != 0 and self.players[current_player_id].chips == 0:
                    current_player_id = in_play[(in_play.index(current_player_id) + 1) % len(in_play)]
                    continue

                to_call = round_bet[last_bet_player_id] - round_bet[current_player_id]
                action = self.players[current_player_id].getAction(to_call, self.table)


                if action == -1 or (action < to_call and action != self.players[current_player_id].chips):
                    next_pointer = in_play.index(current_player_id) 
                    in_play.remove(current_player_id)
                else:
                    self.players[current_player_id].chips -= action
                    round_bet[current_player_id] += action
                    next_pointer = in_play.index(current_player_id) + 1

                    # Reverse all checked flags if current player has betted
                    all_checked = action == 0 and all_checked

                    # If raise, set this bet round to end with current player.
                    if round_bet[current_player_id] > round_bet[last_bet_player_id]:
                        last_bet_player_id = current_player_id
                    
                # Terminates this round when the last player has also checked.
                if all_checked and current_player_id == last_bet_player_id:
                    break
                if i == 0 and action == 0 and current_player_id == big_blind:
                    break

                current_player_id = in_play[next_pointer % len(in_play)]
                to_call = round_bet[last_bet_player_id] - round_bet[current_player_id]
                
            # Update eligible players for current pot
            pot = self.createSidePots(round_bet, list(in_play))
            
            # Let last standing player collect pot
            if len(in_play) == 1: break

            print('\n------DEALING THE %s------' % (self.TABLE_CARDS_NAME[0]))

            # Deals table card once betting is finished
            self.dealTable()
        
        self.getWinner(pot)


    def getWinner(self, pot):
        for index, (sidepot, players) in enumerate(pot):
            # Stores player hands score in dictionary {score: [(player_id, hand_sum_for_tie_break)]}        
            player_score = defaultdict(list)
            for player_id in players:
                hand, score = poker.returnHandScore(self.table + self.players[player_id].hand)

                # Append results to existing list of players with same score
                player_score[score] += [(player_id, sum([x % 13 for x in hand]))]

                # Showdown only if more than one players
                if len(players) > 1:
                    print('%s has a %s' % (self.players[player_id].name, poker.returnHandName(score)))
                    print(poker.returnCardStringShort(hand))

            # Winners are the ones with the highest score
            winner = player_score[max(player_score)]

            # Tiebreak - rank by hand sum
            if len(winner) > 1:
                tie_break_score = defaultdict(list)
                for (player_id, hand_sum) in winner:
                    tie_break_score[hand_sum] += [player_id]

                winner = tie_break_score[max(tie_break_score)]

                for player_id in winner:
                    self.players[player_id].chips += int(sidepot / len(winner))
                    print('%s wins %d from Pot #%d' % (self.players[player_id].name, int(sidepot / len(winner)), index + 1))
                
            else:
                self.players[winner[0][0]].chips += sidepot
                print('%s wins %d from Pot #%d' % (self.players[winner[0][0]].name, sidepot, index + 1))
    
    def getPlayerSummary(self):
        for player in self.players.values():
            print(player)