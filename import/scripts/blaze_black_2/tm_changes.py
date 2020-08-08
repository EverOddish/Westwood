import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.tm_set import PokemonTmSet

tm_files = ['hurricane.txt', 'bug_buzz.txt', 'sucker_punch.txt']

hurricane_pokemon = []
bug_buzz_pokemon = []
sucker_punch_pokemon = []

all_pokemon = set()

for tm_file in tm_files:
    with open(tm_file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('\n')[0]
            pokemon = line.lower().replace('-', '_').replace('\'', '') + '.xml'
            if 'hurricane' in tm_file:
                hurricane_pokemon.append(pokemon)
                all_pokemon.add(pokemon)
            if 'bug_buzz' in tm_file:
                bug_buzz_pokemon.append(pokemon)
                all_pokemon.add(pokemon)
            if 'sucker_punch' in tm_file:
                sucker_punch_pokemon.append(pokemon)
                all_pokemon.add(pokemon)

for pokemon in all_pokemon:
    path = os.path.join('..', 'xml', 'tm_sets', pokemon)
    tm_set = PokemonTmSet(path)
    tm_set_copy = tm_set.copy_tm_set('Pokemon Black 2')
    tm_set_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']

    for tm_file in tm_files:
        move_name = tm_file.split('.')[0].replace('_', ' ').title()
        add = False
        if 'Hurricane' == move_name:
            if pokemon in hurricane_pokemon:
                add = True
        if 'Bug Buzz' == move_name:
            if pokemon in bug_buzz_pokemon:
                add = True
        if 'Sucker Punch' == move_name:
            if pokemon in sucker_punch_pokemon:
                add = True
        if add:
            if move_name not in tm_set_copy.moves:
                tm_set_copy.moves.append(move_name)

    tm_set.add_tm_set(tm_set_copy)
    with open(path, 'w') as g:
        tm_set.dump(g)
