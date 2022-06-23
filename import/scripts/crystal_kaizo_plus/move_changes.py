import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.move import Move

move_changes = {}

with open('scripts/crystal_kaizo_plus/moves.asm') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'\s+move ([A-Z_]+),\s+[A-Z0-9_]+,\s+(\d+),\s+([A-Z]+),\s+(\d+),\s+(\d+),\s+(\d+)', line)
        if result:
            move = result.group(1).lower()
            base_power = result.group(2)
            move_type = result.group(3).lower().capitalize()
            accuracy = result.group(4)
            pp = result.group(5)
            effect_chance = result.group(6)
            move_changes[move] = (base_power, move_type, accuracy, pp, effect_chance)

#print(move_changes)
#sys.exit(0)

for move_name, changes in move_changes.items():
    if move_name == "doubleslap":
        move_name = "double_slap"
    if move_name == "dynamicpunch":
        move_name = "dynamic_punch"
    if move_name == "thunderpunch":
        move_name = "thunder_punch"
    if move_name == "vicegrip":
        move_name = "vice_grip"
    if move_name == "sonicboom":
        move_name = "sonic_boom"
    if move_name == "bubblebeam":
        move_name = "bubble_beam"
    if move_name == "solarbeam":
        move_name = "solar_beam"
    if move_name == "poisonpowder":
        move_name = "poison_powder"
    if move_name == "thundershock":
        move_name = "thunder_shock"
    if move_name == "selfdestruct":
        move_name = "self_destruct"
    if move_name == "softboiled":
        move_name = "soft_boiled"
    if move_name == "hi_jump_kick":
        move_name = "high_jump_kick"
    if move_name == "faint_attack":
        move_name = "feint_attack"
    if move_name == "dragonbreath":
        move_name = "dragon_breath"
    if move_name == "extremespeed":
        move_name = "extreme_speed"
    if move_name == "ancientpower":
        move_name = "ancient_power"
    print(move_name)
    move_name = move_name.lower().replace(' ', '_').replace('-', '_')
    filename = os.path.join('..', 'xml', 'moves', move_name + '.xml')
    move = Move(filename)
    move_record_copy = move.copy_move_record('Pokemon Crystal')
    move_record_copy.games = ['Pokemon Crystal Kaizo+']

    move_record_copy.base_power = changes[0]
    move_record_copy.type = changes[1]
    move_record_copy.accuracy = changes[2]
    move_record_copy.power_points = changes[3]
    move_record_copy.effect_chance = changes[4]

    move.add_move_record(move_record_copy)

    with open(filename, 'w') as f:
        move.dump(f)
