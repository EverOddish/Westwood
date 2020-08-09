import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet

pokedex = {}
with open('pokedex.txt') as f:
    for line in f.readlines():
        line = line.split('\n')[0]
        pieces = line.split(' - ')
        number = int(pieces[0])
        pokemon = pieces[1]
        pokedex[number] = pokemon

stat_changes = {}
with open('pokemon_changes.txt') as f:
    starting_number = None
    ending_number = None
    changes = []
    for line in f.readlines():
        line = line.split('\n')[0]
        result = re.match(r'\s*#(\d+) [A-Za-z \.\-\']+ - #(\d+) ', line)
        if result:
            if None != starting_number:
                pair = (starting_number, ending_number)
                stat_changes[pair] = changes
            starting_number = result.group(1)
            ending_number = result.group(2)
            changes = []
        else:
            result = re.match(r'\s*#(\d+) [A-Za-z \.\-\']+$', line)
            if result:
                if None != starting_number:
                    pair = (starting_number, ending_number)
                    stat_changes[pair] = changes
                starting_number = result.group(1)
                ending_number = None
                changes = []
            else:
                changes.append(line)

for pair in stat_changes.keys():
    starting_number = int(pair[0])
    ending_number = pair[1]
    if None != ending_number:
        ending_number = int(ending_number)
    else:
        ending_number = starting_number

    for number in range(starting_number, ending_number + 1):
        for line in stat_changes[pair]:
            result = re.match(r'New (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)', line)
            if result:
                pokemon_name = pokedex[number]
                path = os.path.join('..', 'xml', 'pokemon', pokemon_name.lower() + '.xml')
                pokemon = Pokemon(path)
                stat_set_copy = StatSet()
                stat_set_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']
                stat_set_copy.hp = result.group(1)
                stat_set_copy.attack = result.group(2)
                stat_set_copy.defense = result.group(3)
                stat_set_copy.special_attack = result.group(4)
                stat_set_copy.special_defense = result.group(5)
                stat_set_copy.speed = result.group(6)
                pokemon.add_stat_set(stat_set_copy)

                with open(path, 'w') as g:
                    pokemon.dump(g)
