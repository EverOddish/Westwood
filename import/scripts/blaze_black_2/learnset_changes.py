import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.learnset import PokemonLearnset, Learnset

all_pokemon = {}

with open('learnset_changes.txt') as f:
    pokemon = None
    changes = []
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'\s*#\d{3} ([A-Za-z\' _\-]+)', line)
        if result:
            if None != pokemon:
                #print('Adding pokemon: ' + pokemon)
                all_pokemon[pokemon] = changes
                changes = []
            pokemon = result.group(1)
        elif len(line) > 0:
            changes.append(line)

for pokemon in all_pokemon.keys():
    filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
    path = os.path.join('..', 'xml', 'learnsets', filename)
    learnset = PokemonLearnset(path)
    changes = all_pokemon[pokemon]

    new_set = False
    for line in changes:
        if 'Lv.' in line:
            new_set = True
            break

    learnset_copy = None
    if new_set:
        learnset_copy = Learnset()
        learnset_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']
        for line in changes:
            result = re.match(r'Lv\. (\d+) ([A-Za-z \-\']+)', line)
            if result:
                level = result.group(1)
                level = int(level)
                level = str(level)
                move = result.group(2)
                learnset_copy.moves.append((level, move))
    else:
        learnset_copy = learnset.copy_learnset('Pokemon Black 2')
        learnset_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']
        for line in changes:
            result = re.match(r'\+ Level (\d+) - ([A-Za-z \-\']+)', line)
            if result:
                level = result.group(1)
                level = int(level)
                level = str(level)
                move = result.group(2)
                learnset_copy.moves.append((level, move))
            else:
                result = re.match(r'\- Level (\d+) - ([A-Za-z \-\']+)', line)
                if result:
                    level = result.group(1)
                    level = int(level)
                    level = str(level)
                    move = result.group(2)
                    success = False
                    count = 0
                    for learnset_move in learnset_copy.moves:
                        if learnset_move[0] == level:
                            new_tuple = (learnset_move[0], move)
                            learnset_copy.moves[count] = new_tuple
                            success = True
                            break
                        count = count + 1
                    if not success:
                        print('Warning: Failed on line: ' + pokemon + ' ' + line)
                else:
                    result = re.match(r'= Level (\d+) - ([A-Za-z \-\']+)', line)
                    if result:
                        level = result.group(1)
                        level = int(level)
                        level = str(level)
                        move = result.group(2)
                        success = False
                        count = 0
                        for learnset_move in learnset_copy.moves:
                            if learnset_move[1] == move:
                                new_tuple = (level, learnset_move[1])
                                learnset_copy.moves[count] = new_tuple
                                success = True
                                break
                            count = count + 1
                        if not success:
                            print('Warning: Failed on line: ' + pokemon + ' ' + line)

    learnset.add_learnset(learnset_copy)
    with open(path, 'w') as g:
        learnset.dump(g)
