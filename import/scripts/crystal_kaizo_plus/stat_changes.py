import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet

all_pokemon = {}
for filename in os.listdir("scripts/crystal_kaizo_plus/base_stats"):
    with open(os.path.join("scripts/crystal_kaizo_plus/base_stats", filename)) as f:
        pokemon = filename.split(".")[0]
        lines = f.readlines()
        for line in lines:
            line = line.split('\n')[0]
            result = re.match(r'\s+db\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+)', line)
            if result:
                changes = [result.group(i + 1) for i in range(6)]
                all_pokemon[pokemon] = changes
                break

#print(all_pokemon)
#sys.exit(0)

for pokemon in all_pokemon.keys():
    stats = all_pokemon[pokemon]
    if len(stats) > 0:
        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'pokemon', filename)
        pokemon_object = Pokemon(path)
        stat_set_copy = StatSet()
        stat_set_copy.games = ['Pokemon Crystal Kaizo+']
        stat_set_copy.hp = stats[0]
        stat_set_copy.attack = stats[1]
        stat_set_copy.defense = stats[2]
        stat_set_copy.special_attack = stats[3]
        stat_set_copy.special_defense = stats[4]
        stat_set_copy.speed = stats[5]
        pokemon_object.add_stat_set(stat_set_copy)

        #with open(path, 'w') as g:
        #    pokemon_object.dump(g)

