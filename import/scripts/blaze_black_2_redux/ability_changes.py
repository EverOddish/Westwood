import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet
from intermediate.pokemon import Pokemon, AbilitySet, AbilityRecord

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
                all_pokemon[pokemon] = list(set(changes))
            pokemon = result.group(1)
            changes = []
        else:
            if line.startswith("Ability (Complete"):
                stats = True
            elif stats is True:
                result = re.match(r'New\s{5}([A-Za-z ]+) / ([A-Za-z ]+) / ([A-Za-z ]+)', line)
                if result:
                    changes = [result.group(i + 1).rstrip() for i in range(3)]
                    all_pokemon[pokemon] = list(set(changes))
                    stats = False

#print(all_pokemon)
#sys.exit(0)

for pokemon in all_pokemon.keys():
    abilities = all_pokemon[pokemon]
    if len(abilities) > 0:
        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'pokemon', filename)
        pokemon_object = Pokemon(path)

        ability_set_copy = AbilitySet()
        ability_set_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']

        ability_record = AbilityRecord()
        ability_record.name = abilities[0]
        ability_record.hidden = 'No'
        ability_set_copy.ability_records.append(ability_record)

        ability_record = AbilityRecord()
        ability_record.name = abilities[1]
        ability_record.hidden = 'No' if len(abilities) == 3 else 'Yes'
        ability_set_copy.ability_records.append(ability_record)

        if len(abilities) == 3:
            ability_record = AbilityRecord()
            ability_record.name = abilities[2]
            ability_record.hidden = 'Yes'
            ability_set_copy.ability_records.append(ability_record)

        pokemon_object.add_ability_set(ability_set_copy)

        with open(path, 'w') as g:
            pokemon_object.dump(g)

