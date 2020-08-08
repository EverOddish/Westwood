import os
import re
import sys

sys.path.append(os.getcwd())
from intermediate.move import Move

move_changes = []

with open('move_changes.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.split('\n')[0]
        result = re.match(r'([A-Za-z ]+) is now (\d+) power.', line)
        if result:
            move_name = result.group(1)
            power = result.group(2)
            move_changes.append((move_name, power))

for move_change in move_changes:
    move_name = move_change[0].lower().replace(' ', '_')
    filename = os.path.join('..', 'xml', 'moves', move_name + '.xml')
    move = Move(filename)
    move_record_copy = move.copy_move_record('Pokemon Black 2')
    move_record_copy.games = ['Pokemon Blaze Black 2', 'Pokemon Volt White 2']
    move_record_copy.base_power = move_change[1]
    move.add_move_record(move_record_copy)
    with open(filename, 'w') as f:
        move.dump(f)
