import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.learnset import PokemonLearnset, Learnset

all_pokemon = {}

with open('scripts/crystal_kaizo_plus/learnsets.csv') as f:
    pokemon = None
    changes = []
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'([A-Za-z\' _\-]+),', line)
        if result:
            if pokemon:
                all_pokemon[pokemon] = changes
            pokemon = result.group(1)
            if "Farfetch D" == pokemon:
                pokemon = "FarfetchD"
            if "Mr  Mime" == pokemon:
                pokemon = "Mr Mime"
            changes = []
        else:
            result = re.match(r'(\d)+,([A-Za-z\' _\-]+)', line)
            if result:
                changes.append(line)
    all_pokemon[pokemon] = changes

for pokemon in all_pokemon.keys():
    filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
    path = os.path.join('..', 'xml', 'learnsets', filename)
    learnset = PokemonLearnset(path)
    changes = all_pokemon[pokemon]

    learnset_copy = Learnset()
    learnset_copy.games = ['Pokemon Crystal Kaizo+']
    for line in changes:
        result = re.match(r'(\d+),([A-Za-z \-\']+)', line)
        if result:
            level = result.group(1)
            level = int(level)
            level = str(level)
            move = result.group(2)
            learnset_copy.moves.append((level, move))

    learnset.add_learnset(learnset_copy)
    print("Added " + pokemon)
    with open(path, 'w') as g:
        learnset.dump(g)
