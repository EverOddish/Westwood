import re
import os
import sys

sys.path.append(os.getcwd())
from intermediate.learnset import PokemonLearnset

pokemon = []

class TempPokemon:
    def __init__(self):
        self.learnset_moves = []
        self.tmset_moves = []

with open('crown_tundra_stats_learnsets.txt') as f:
    lines = f.readlines()
    parsing_pokemon_name = False
    current_pokemon = None
    for line in lines:
        if line.startswith('==='):
            parsing_pokemon_name = not parsing_pokemon_name
            if parsing_pokemon_name:
                if current_pokemon:
                    pokemon.append(current_pokemon)
                current_pokemon = TempPokemon()
        elif parsing_pokemon_name:
            result = re.match(r'\d+ - ([A-Za-z0-9\'\. -:]+)( \d)* \(', line)
            if result:
                current_pokemon.name = result.group(1)
            else:
                print('Did not match on: ' + line)
        elif line.startswith('Base Stats:'):
            result = re.match(r'Base Stats: (\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+) ', line)
            if result:
                current_pokemon.hp = result.group(1)
                current_pokemon.attack = result.group(2)
                current_pokemon.defense = result.group(3)
                current_pokemon.sp_attack = result.group(4)
                current_pokemon.sp_defense = result.group(5)
                current_pokemon.speed = result.group(6)
        elif line.startswith('EV Yield:'):
            result = re.match(r'EV Tield: (\d)\.(\d)\.(\d)\.(\d)\.(\d)\.(\d)', line)
            if result:
                current_pokemon.hp_yield = result.group(1)
                current_pokemon.attack_yield = result.group(2)
                current_pokemon.defense_yield = result.group(3)
                current_pokemon.sp_attack_yield = result.group(4)
                current_pokemon.sp_defense_yield = result.group(5)
                current_pokemon.speed_yield = result.group(6)
        elif line.startswith('Abilities'):
            current_pokemon.abilities = line.split('Abilities: ')[1].replace('\n', '').replace(' (1)', '').replace(' (2)', '').replace(' (H)', '').split(' | ')
        elif line.startswith('Type: '):
            current_pokemon.types = line.split('Type: ')[1]
        elif line.startswith('Egg Group: '):
            current_pokemon.egg_groups = line.split('Egg Group: ')[1]
        elif line.startswith('- [') and not line.startswith('- [TM') and not line.startswith('- [TR'):
            current_pokemon.learnset_moves.append(line)
        elif line.startswith('- [TM') or line.startswith('- [TR'):
            current_pokemon.tmset_moves.append(line)
        elif line.startswith('Evolves'):
            current_pokemon.evolution = line
        else:
            # Skip
            pass

for pkmn in pokemon:
    pokemon_name = pkmn.name
    filename = '/Users/mikeaustin/github/Westwood/xml/learnsets/' + pokemon_name.replace("'", '_').replace(' ', '_').replace('.', '_').replace('-', '_').lower() + '.xml'
    if os.path.exists(filename):
        print('Updating: ' + filename)

        pokemon_learnset = PokemonLearnset(filename)

        learnset_copy = pokemon_learnset.copy_learnset('Pokemon Sword')
        if None == learnset_copy:
            learnset_copy = pokemon_learnset.copy_learnset('Pokemon Ultra Sun')
            learnset_copy.games = ['Pokemon Sword', 'Pokemon Shield']
        learnset_copy.moves = []

        for level_move in pkmn.learnset_moves:
            level_move = level_move.replace('\n', '').replace('- [', '')
            pieces = level_move.split('] ')
            pieces[0] = str(int(pieces[0]))
            if 0 == int(pieces[0]):
                pieces[0] = '1'
            pair = (pieces[0], pieces[1])
            learnset_copy.moves.append(pair)

        pokemon_learnset.add_learnset(learnset_copy)

        with open(filename, 'w') as f:
            pokemon_learnset.dump(f)
