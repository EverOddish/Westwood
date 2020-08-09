import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.tm_set import PokemonTmSet, TmSet

tm_changes = {}
with open('tm_changes.txt') as f:
    for line in f.readlines():
        line = line.split('\n')[0]
        result = re.match(r'([A-Za-z]+) - TM: (.*)', line)
        if result:
            pokemon = result.group(1)
            changes = result.group(2)
            tm_changes[pokemon] = changes

def add_tm(pokemon_tm_set, tm):
    if tm.startswith(' '):
        tm = tm[1:]
    tm = tm.replace('.', '')

    tm_set_copy = None
    for tm_set in pokemon_tm_set.tm_sets:
        if 'Blaze Black 2' in tm_set.games:
            tm_set_copy = tm_set
            print('Using existing')
            break

    add = False
    if None == tm_set_copy:
        tm_set_copy = pokemon_tm_set.copy_tm_set('Pokemon Black 2')
        tm_set_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']
        add = True

    tm_set_copy.moves.append(tm)

    if add:
        pokemon_tm_set.add_tm_set(tm_set_copy)

for pokemon in tm_changes.keys():
    path = os.path.join('..', 'xml', 'tm_sets', pokemon.lower() + '.xml')
    pokemon_tm_set = PokemonTmSet(path)

    line = tm_changes[pokemon]
    pieces = line.split(',')
    for i in range(len(pieces)):
        piece = pieces[i]
        result = re.match(r'TM\d{2}$', piece)
        if result:
            tm = pieces[i + 1]
            add_tm(pokemon_tm_set, tm)
        else:
            result = re.match(r'TM\d{2} ([A-Za-z]+)', piece)
            if result:
                tm = result.group(1)
                add_tm(pokemon_tm_set, tm)

    with open(path, 'w') as g:
        pokemon_tm_set.dump(g)
