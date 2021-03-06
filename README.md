# TexasPy

A modularly-built Texas Hold'em simulation in Python. Currently in a rebuild, previous work can be found on the <code>legacy</code> branch.

<code>**_player.py - various player types</code>

<code>env.py - poker game environment (non-interactable)</code>

<code>poker.py - generic poker-related evaluation functions that can be used outside of active games</code>

## Instructions

Currently, the best way to run this program is to run <code>app.py</code> and follows the on-screen instructions.

### base_player.py
Base palyer class whose actions are determined by user input. Action codes are as follows:

- Fold: -1 or betting below to call value while having sufficient chips
- Check: 0
- Bet / Raise: > 0

### stats_player.py
A player class that utilises statistics to decide its action. 

### bluff_player.py
Extends stats_player, includes a random bluff factor. (In progress)


## Contribution

This project is built on the basis of honest and fair play. Any PR with player implementation that violates this rule by illegally manipulating data will not be considered. However, it is encouraged that you play around with it in your local environment to understand the project more.
