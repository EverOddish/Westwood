import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.tm_set import PokemonTmSet

all_pokemon = {}
with open('scripts/blaze_black_2_redux/PokemonChanges.txt') as f:
    pokemon = None
    changes = []
    stats = False
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'\d{3} - ([A-Za-z\' _\-]+)', line)
        if result:
            if pokemon:
                all_pokemon[pokemon] = changes
            pokemon = result.group(1)
            changes = []
            stats = False
        else:
            if line.startswith("Moves:"):
                stats = True
            elif stats is True:
                result = re.match(r'Now compatible with [A-Z0-9]+, ([A-Za-z ]+)\.', line)
                if result:
                    changes.append(result.group(1))

#print(all_pokemon)
#sys.exit(0)

for pokemon in all_pokemon.keys():
    print(pokemon)
    if len(all_pokemon[pokemon]) > 0:
        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'tm_sets', filename)
        tm_set = PokemonTmSet(path)
        tm_set_copy = tm_set.copy_tm_set('Pokemon Sword')
        if tm_set_copy is None:
            tm_set_copy = tm_set.copy_tm_set('Pokemon Ultra Moon')
        tm_set_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']

        for move in all_pokemon[pokemon]:
            if move not in tm_set_copy.moves:
                tm_set_copy.moves.append(move)

        tm_set.add_tm_set(tm_set_copy)
        with open(path, 'w') as g:
            tm_set.dump(g)
