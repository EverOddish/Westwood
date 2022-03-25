import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet

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
            if line.startswith("Base Stats (Complete)"):
                stats = True
            elif stats is True:
                result = re.match(r'New\s+(\d+) HP / (\d+) Atk / (\d+) Def / (\d+) SAtk / (\d+) SDef / (\d+) Spd / .*', line)
                if result:
                    changes = [result.group(i + 1) for i in range(6)]
                    all_pokemon[pokemon] = changes
                    stats = False

#print(all_pokemon)
#sys.exit(0)

for pokemon in all_pokemon.keys():
    stats = all_pokemon[pokemon]
    if len(stats) > 0:
        filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
        path = os.path.join('..', 'xml', 'pokemon', filename)
        pokemon_object = Pokemon(path)
        stat_set_copy = StatSet()
        stat_set_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']
        stat_set_copy.hp = stats[0]
        stat_set_copy.attack = stats[1]
        stat_set_copy.defense = stats[2]
        stat_set_copy.special_attack = stats[3]
        stat_set_copy.special_defense = stats[4]
        stat_set_copy.speed = stats[5]
        pokemon_object.add_stat_set(stat_set_copy)

        with open(path, 'w') as g:
            pokemon_object.dump(g)

