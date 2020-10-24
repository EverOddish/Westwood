import os
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon

with open('crown_tundra_pokemon.txt') as f:
    for line in f.readlines():
        pokemon = line.split(' - ')[-1].replace('\n', '')
        pokemon = pokemon.replace(' ', '_').replace('.', '').lower()
        filename = os.path.join('..', 'xml', 'pokemon', pokemon + '.xml')
        if os.path.exists(filename):
            pokemon_object = Pokemon(filename)

            found = False
            for stat_set in pokemon_object.stat_sets:
                if 'Pokemon Sword' in stat_set.games:
                    found = True

            if not found:
                for stat_set in pokemon_object.stat_sets:
                    if 'Pokemon Ultra Sun' in stat_set.games:
                        stat_set.games.append('Pokemon Sword')
                        stat_set.games.append('Pokemon Shield')
                        break

                for ability_set in pokemon_object.ability_sets:
                    if 'Pokemon Ultra Sun' in ability_set.games:
                        ability_set.games.append('Pokemon Sword')
                        ability_set.games.append('Pokemon Shield')
                        break

                for type_set in pokemon_object.type_sets:
                    if 'Pokemon Ultra Sun' in type_set.games:
                        type_set.games.append('Pokemon Sword')
                        type_set.games.append('Pokemon Shield')
                        break

                for evolution_set in pokemon_object.evolution_sets:
                    if 'Pokemon Ultra Sun' in evolution_set.games:
                        evolution_set.games.append('Pokemon Sword')
                        evolution_set.games.append('Pokemon Shield')
                        break

            with open(filename, 'w') as g:
                pokemon_object.dump(g)
        else:
            #print(pokemon + ' does not exist')
            pass
