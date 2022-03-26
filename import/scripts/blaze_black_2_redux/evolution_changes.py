import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet, TypeSet
from intermediate.pokemon import Pokemon, AbilitySet, AbilityRecord

all_pokemon = {}
with open('scripts/blaze_black_2_redux/PokemonChanges.txt') as f:
    pokemon = None
    changes = None
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
            if line.startswith("Evolution:"):
                stats = True
            elif stats is True:
                #result = re.match(r'Now able to evolve into ([A-Za-z]+) at level (\d+)\.', line)
                result = re.match(r'Now able to evolve into ([A-Za-z]+) by using a ([A-Za-z \']+)\.', line)
                if result:
                    changes = (result.group(1), result.group(2))
                    all_pokemon[pokemon] = changes
                    stats = False

for k, v in all_pokemon.items():
    if len(all_pokemon[k]) > 0:
        print(k + ' ' + str(all_pokemon[k]))

