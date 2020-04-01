from random import shuffle
from collections import defaultdict, deque

import player, poker

class GameObject(object):

    def __init__(self, players, blinds, ante=0):
        self.players = {id:player for id, player in enumerate(players)}
        self.blinds = blinds
        self.dealer = 0

    def run(self, count):
        for i in range(count):
            self.setup()
            self.playHand()

    def setup(self):
        ''' Performs initial set up of a new hand. '''
        # Update dealer, collect blinds / antes
        # self.dealer = (self.dealer + 1) % len(self.players)

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
        else:
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
            leftover_bets = lowest_common_bet * len([x for x in round_bet.keys() if x not in in_play and round_bet[x] >= lowest_common_bet])
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

        # Set up round bet records
        round_bet = defaultdict(int)
        round_bet[small_blind] = self.blinds / 2
        round_bet[big_blind] = self.blinds
        

        # Keep track of main and sidepots
        pot = [(0, in_play)]

        # Starts hand
        for i in range(4):
            print('Table cards: ' , poker.returnCardStringShort(self.table))
            

            current_player_id = in_play[0]
            last_bet_player_id = in_play[-1]

            while current_player_id != last_bet_player_id or round_bet[last_bet_player_id] == self.blinds:
                
                # Skip player's turn if they have zero chips but are still in play i.e. have already all-ined.
                if round_bet[current_player_id] != 0 and self.players[current_player_id].chips == 0:
                    current_player_id = in_play[(in_play.index(current_player_id) + 1) % len(in_play)]
                    continue

                toCall = round_bet[last_bet_player_id] - round_bet[current_player_id]
                action, all_in = self.players[current_player_id].getAction(toCall, self.table)

                # Move pointer when current player does not fold and not an all in
                next_pointer = in_play.index(current_player_id) + int(action != -1)

                if action == -1 or (action < toCall and action != self.players[current_player_id].chips):
                    in_play.remove(current_player_id)
                else:
                    round_bet[current_player_id] += action

                    if action < toCall:
                        leftover_bets = sum([round_bet[x] for x in round_bet.keys if x not in in_play])


                    # If raise, set this bet round to end with current player.
                    if round_bet[current_player_id] > round_bet[last_bet_player_id]:
                        last_bet_player_id = current_player_id

                # Special case for big blinds to check.
                if current_player_id == last_bet_player_id and round_bet[current_player_id] == self.blinds: break

                current_player_id = in_play[next_pointer % len(in_play)]
                
            
            if len(in_play) == 1: break
            # Update eligible players for current pot

            pot = self.createSidePots(round_bet, in_play)

            print('Round %d ended\n' % (i+1))

            # Deals table card once betting is finished
            self.dealTable()
            