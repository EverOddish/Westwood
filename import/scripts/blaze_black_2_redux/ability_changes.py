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
                all_pokemon[pokemon] = changes
            pokemon = result.group(1)
            changes = []
        else:
            if line.startswith("Ability (Complete"):
                stats = True
            elif stats is True:
                result = re.match(r'New\s{5}([A-Za-z ]+) / ([A-Za-z ]+) / ([A-Za-z ]+)', line)
                if result:
                    changes = [result.group(i + 1).rstrip() for i in range(3)]
                    all_pokemon[pokemon] = changes
                    stats = False

#print(all_pokemon['Bulbasaur'])
#sys.exit(0)

for pokemon in all_pokemon.keys():
    abilities = all_pokemon[pokemon]
    if len(abilities) > 0:
        if len(abilities) == 3:
            if abilities[0] == abilities[2]:
                del abilities[0]
            elif abilities[1] == abilities[2]:
                del abilities[1]
        print(abilities)

        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'pokemon', filename)
        pokemon_object = Pokemon(path)

        ability_set_copy = pokemon_object.copy_ability_set('Pokemon Blaze Black 2 Redux')
        pokemon_object.remove_ability_set('Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux')

        ability_set_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']

        ability_set_copy.ability_records[0].name = abilities[0]
        ability_set_copy.ability_records[0].hidden = 'No'

        ability_set_copy.ability_records[1].name = abilities[1]
        ability_set_copy.ability_records[1].hidden = 'No' if len(abilities) == 3 else 'Yes'

        if len(abilities) == 3:
            if len(ability_set_copy.ability_records) < 3:
                ability_record = AbilityRecord()
                ability_record.name = abilities[2]
                ability_record.hidden = 'Yes'
                ability_set_copy.ability_records.append(ability_record)
            else:
                ability_set_copy.ability_records[2].name = abilities[2]
                ability_set_copy.ability_records[2].hidden = 'Yes'

        pokemon_object.add_ability_set(ability_set_copy)

        with open(path, 'w') as g:
            pokemon_object.dump(g)
