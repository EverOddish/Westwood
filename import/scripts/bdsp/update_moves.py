import glob
import os
import sys

sys.path.append(os.getcwd())
from intermediate.move import MoveRecord, Move, TmRecord

for name in glob.glob('../xml/moves/*'):
    move = Move(name)
    move_record_copy = move.copy_move_record('Pokemon Sword')
    move_record_copy.games = ['Pokemon Brilliant Diamond', 'Pokemon Shining Pearl']
    move.add_move_record(move_record_copy)
    with open(name, 'w') as f:
        move.dump(f)
