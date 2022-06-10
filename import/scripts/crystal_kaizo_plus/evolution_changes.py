import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.pokemon import Pokemon, StatSet, TypeSet
from intermediate.pokemon import Pokemon, AbilitySet, AbilityRecord

evolutions = []
with open('scripts/crystal_kaizo_plus/evolutions.csv') as f:
    pokemon = None
    changes = None
    stats = False
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        chunks = line.split(',')
        pokemon = chunks[0]
        level = chunks[2]
        evolves_to = chunks[4]
        evolutions.append((pokemon, level, evolves_to))

#print(evolutions)

for pokemon, level, evolves_to in evolutions:
    filename = pokemon.lower().replace(' ', '_').replace('\'', '_').replace('-', '_') + '.xml'
    path = os.path.join('..', 'xml', 'pokemon', filename)
    pokemon_object = Pokemon(path)

    evolution_copy = pokemon_object.copy_evolution_set("Pokemon Crystal")
    evolution_copy.games = ["Pokemon Crystal Kaizo+"]
    found = False
    for record in evolution_copy.evolution_records:
        if record.evolves_to == evolves_to:
            found = True
            if len(level) > 0:
                record.level = level
                print(f"Updated {pokemon}")
    pokemon_object.add_evolution_set(evolution_copy)

    with open(path, 'w') as g:
        pokemon_object.dump(g)
