import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, AbilitySet, AbilityRecord

pokedex = {}
with open('pokedex.txt') as f:
    for line in f.readlines():
        line = line.split('\n')[0]
        pieces = line.split(' - ')
        number = int(pieces[0])
        pokemon = pieces[1]
        pokedex[number] = pokemon

abilities = {}
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
                abilities[pair] = changes
            starting_number = result.group(1)
            ending_number = result.group(2)
            changes = []
        else:
            result = re.match(r'\s*#(\d+) [A-Za-z \.\-\']+$', line)
            if result:
                if None != starting_number:
                    pair = (starting_number, ending_number)
                    abilities[pair] = changes
                starting_number = result.group(1)
                ending_number = None
                changes = []
            else:
                changes.append(line)

for pair in abilities.keys():
    starting_number = int(pair[0])
    ending_number = pair[1]
    if None != ending_number:
        ending_number = int(ending_number)
    else:
        ending_number = starting_number

    for number in range(starting_number, ending_number + 1):
        pokemon_name = pokedex[number]
        path = os.path.join('..', 'xml', 'pokemon', pokemon_name.lower() + '.xml')
        pokemon = Pokemon(path)

        ability1 = None
        ability2 = None
        for line in abilities[pair]:
            result = re.match(r'Ability One: ([A-Za-z ]+)', line)
            if result:
                ability1 = result.group(1)
            result = re.match(r'Ability Two: ([A-Za-z ]+)', line)
            if result:
                ability2 = result.group(1)

        ability_set_copy = AbilitySet()
        ability_set_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']

        ability_record = AbilityRecord()
        ability_record.name = ability1
        ability_record.hidden = 'No'
        ability_set_copy.ability_records.append(ability_record)

        if None != ability2:
            ability_record = AbilityRecord()
            ability_record.name = ability2
            ability_record.hidden = 'No'
            ability_set_copy.ability_records.append(ability_record)

        pokemon.add_ability_set(ability_set_copy)

        with open(path, 'w') as g:
            pokemon.dump(g)
