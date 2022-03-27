import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.move import Move

move_changes = {}

with open('scripts/blaze_black_2_redux/MoveChanges.txt') as f:
    lines = f.readlines()
    current_move = ''
    changes = []
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'^([A-Za-z -]+)$', line)
        if result:
            if len(current_move) > 0:
                move_changes[current_move] = changes
            current_move = result.group(1)
            changes = []
        else:
            result = re.match(r' - Power \d+ -> (\d+)', line)
            if result:
                changes.append(('Power', result.group(1)))

            result = re.match(r' - PP \d+ -> (\d+)', line)
            if result:
                changes.append(('PP', result.group(1)))

            result = re.match(r' - Accuracy \d+ -> (\d+)', line)
            if result:
                changes.append(('Accuracy', result.group(1)))

#print(move_changes)
#sys.exit(0)

for move_name, changes in move_changes.items():
    print(move_name)
    move_name = move_name.lower().replace(' ', '_').replace('-', '_')
    filename = os.path.join('..', 'xml', 'moves', move_name + '.xml')
    move = Move(filename)
    move_record_copy = move.copy_move_record('Pokemon Sword')
    if move_record_copy is None:
        move_record_copy = move.copy_move_record('Pokemon Legends Arceus')
    move_record_copy.games = ['Pokemon Blaze Black 2 Redux', 'Pokemon Volt White 2 Redux']
    for change in changes:
        if change[0] == 'Power':
            move_record_copy.base_power = change[1]
        elif change[0] == 'PP':
            move_record_copy.power_points = change[1]
        elif change[0] == 'Accuracy':
            move_record_copy.accuracy = change[1]
    move.add_move_record(move_record_copy)
    with open(filename, 'w') as f:
        move.dump(f)
