import re
import os
import sys

sys.path.append(os.getcwd())
from intermediate.tutor_set import PokemonTutorSet, TutorSet

pokemon = []

class TempPokemon:
    def __init__(self):
        self.learnset_moves = []
        self.tmset_moves = []
        self.move_tutor_moves = []

with open('crown_tundra_stats_learnsets.txt') as f:
    lines = f.readlines()
    parsing_pokemon_name = False
    current_pokemon = None
    parsing_move_tutor = False
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
        elif parsing_move_tutor:
            if line.startswith('- '):
                current_pokemon.move_tutor_moves.append(line.replace('\n', ''))
            else:
                parsing_move_tutor = False
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
        elif line.startswith('Armor Tutors:'):
            parsing_move_tutor = True
        else:
            # Skip
            pass

new_pokemon = []
with open('new_pokemon.txt') as f:
    for line in f.readlines():
        line = line.replace('\n', '')
        new_pokemon.append(line.split(' - ')[-1].replace('.', '').replace(' ', '_').lower())

for pkmn in pokemon:
    pokemon_name = pkmn.name
    filename = '/Users/mikeaustin/github/Westwood/xml/tutor_sets/' + pokemon_name.replace("'", '_').replace(' ', '_').replace('.', '_').replace('-', '_').lower() + '.xml'
    if len(pkmn.move_tutor_moves) > 0:
        if filename.split('/')[-1].split('.xml')[0] in new_pokemon:
            if os.path.exists(filename):
                print('Updating: ' + filename)
            else:
                print('Creating: ' + filename)
                with open(filename, 'w') as new_file:
                    new_file.write("<?xml version='1.0' encoding='utf-8' standalone='no'?>\n")
                    new_file.write("<pokemon_tutor_sets>\n")
                    new_file.write("    <name>" + pkmn.name + "</name>\n")
                    new_file.write("    <tutor_sets>\n")
                    new_file.write("    </tutor_sets>\n")
                    new_file.write("</pokemon_tutor_sets>")
                    new_file.flush()

            pokemon_tutor_set = PokemonTutorSet(filename)

            tutor_set_copy = pokemon_tutor_set.copy_tutor_set('Pokemon Sword')
            if None == tutor_set_copy:
                tutor_set_copy = TutorSet()
                tutor_set_copy.games = ['Pokemon Sword', 'Pokemon Shield']
            tutor_set_copy.moves = []

            for move in pkmn.move_tutor_moves:
                move = move.replace('\n', '').split('- ')[-1]
                tutor_set_copy.moves.append(move)

            pokemon_tutor_set.add_tutor_set(tutor_set_copy)

            with open(filename, 'w') as f:
                pokemon_tutor_set.dump(f)
