import sys
from table.env import Table
from player_type.base_player import Player
from player_type.stats_player import StatsPlayer
from player_type.bluff_player import BluffPlayer


def runHands(players, count, blinds):
    table = Table(players, blinds)

    table.run(count)

def createPlayer(name, chips, player_type, args):
    if player_type == 'manual':
        return Player(name, chips)
    elif player_type == 'stats':
        alpha = float(args['alpha'])
        debug = args['debug']
        return StatsPlayer(name, chips, alpha, debug)
    elif player_type == 'bluff':
        alpha = float(args['alpha'])
        bluff_frequency = float(args['bluff_frequency'])
        bluff_strength = float(args['bluff_strength'])
        debug = args['debug']
        return BluffPlayer(name, chips, alpha, bluff_frequency, bluff_strength, debug)


PLAYER_NAMES = [
    'Arrow', 'Justin', 'Kaidrian', 'Lincoln', 'Eric', 'Fiona', 'Greg',
    'Henry', 'Ivy', 'Jess', 'Klaus', 'Lincoln', 'Minnie', 'Naomi'
]
    
PLAYER_TYPES = {
    0: 'manual',
    1: 'stats',
    2: 'bluff'
}

PLAYER_ARGS = {
    'manual': {},
    'stats': {
        'alpha': 0.15,
        'debug': 'True'
    },
    'bluff': {
        'alpha': 0.2,
        'debug': 'True',
        'bluff_frequency': 0.3,
        'bluff_strength': 0.5,
    }
}
CHIPS_DEFAULT = 400
BLINDS_DEFAULT = 20
RUN_DEFAULT = 5

if __name__ == '__main__':    
    create_player = True
   
    player_list = []
    while create_player:
        print(PLAYER_TYPES)
        player_type = PLAYER_TYPES[int(input('Choose a player type to create: '))]
        name = input('Please give a name to this player (%s): ' % (PLAYER_NAMES[len(player_list)]))
        if name == '': name = PLAYER_NAMES[len(player_list)]
        chips = input('Please set the number of chips for %s (%d): ' % (name, CHIPS_DEFAULT))
        if chips == '': chips = CHIPS_DEFAULT
        args = dict(PLAYER_ARGS[player_type])
        for key in args:
            placeholder = input('Please enter value for %s (%s): ' % (key, str(args[key])))
            if placeholder != '': args[key] = placeholder
        player_list.append(createPlayer(name, chips, player_type, args))
        if len(player_list) > 1: create_player = input('Create another player? [Y/n]\n') != 'n'
    
    blinds = input('How much are the blinds (%d)? ' % (BLINDS_DEFAULT))
    if blinds == '': blinds = BLINDS_DEFAULT
    count = input('How many hands to run (%d)? ' % (RUN_DEFAULT))
    if count == '': count = RUN_DEFAULT
    runHands(player_list, int(count), int(blinds))