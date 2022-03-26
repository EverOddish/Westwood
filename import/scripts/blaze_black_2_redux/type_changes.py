import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet, TypeSet
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
            if line.startswith("Type (Complete"):
                stats = True
            elif stats is True:
                result = re.match(r'New\s{5}([A-Za-z]+)( / )*([A-Za-z]+)*( \[!!!\])*', line)
                if result:
                    type1 = result.group(1)
                    type2 = result.group(3)
                    if type2:
                        type2 = type2.rstrip()
                    changes = [type1, type2]
                    all_pokemon[pokemon] = list(set(changes))
                    stats = False

#for k, v in all_pokemon.items():
#    if len(all_pokemon[k]) > 0:
#        print(k + ' ' + str(all_pokemon[k]))
#sys.exit(0)

for pokemon in all_pokemon.keys():
    types = all_pokemon[pokemon]
    if len(types) > 0:
        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'pokemon', filename)
        pokemon_object = Pokemon(path)

        type_set_copy = TypeSet()
        type_set_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']

        type_set_copy.type1 = types[0]
        if types[1] is not None:
            type_set_copy.type2 = types[1]

        pokemon_object.add_type_set(type_set_copy)

        with open(path, 'w') as g:
            pokemon_object.dump(g)

