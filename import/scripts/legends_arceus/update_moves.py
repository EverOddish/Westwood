import glob
import os
import sys

sys.path.append(os.getcwd())
from intermediate.move import MoveRecord, Move, TmRecord

type_map = [
    'Normal',
    'Fighting',
    'Flying',
    'Poison',
    'Ground',
    'Rock',
    'Bug',
    'Ghost',
    'Steel',
    'Fire',
    'Water',
    'Grass',
    'Electric',
    'Psychic',
    'Ice',
    'Dragon',
    'Dark',
    'Fairy',
]

INDEX = 0
MOVE_NAME = 1
MOVE_ID = 2
CAN_USE = 3
FTYPE = 4
FQUALITY = 5
FCATEGORY = 6
FPOWER = 7
FACCURACY = 8
FPP = 9
FPRIORITY = 10
FHIT_MIN = 11
FHIT_MAX = 12
FINFLICT = 13
FINFLICT_PERCENT = 14
FRAW_INFLICT_COUNT = 15
FTURN_MIN = 16
FTURN_MAX = 17
FCRIT_STAGE = 18
FFLINCH = 19
FEFFECT_SEQUENCE = 20
FRECOIL = 21
FRAW_HEALING = 22
FRAW_TARGET = 23
FSTAT_1 = 24
FSTAT_2 = 25
FSTAT_3 = 26
FSTAT_1_STAGE = 27
FSTAT_2_STAGE = 28
FSTAT_3_STAGE = 29
FSTAT_1_PERCENT = 30
FSTAT_2_PERCENT = 31
FSTAT_3_PERCENT = 32
FSTAT_1_DURATION = 33
FSTAT_2_DURATION = 34
FSTAT_3_DURATION = 35
GMAX_POWER = 36

SPLINTER_MOD = 54

DAMAGE_PERCENT_STATUSED = 68
CAN_STYLE = 69
ACTION_SPEED_MOD = 70
AGILE_ACTION_SPEED_MOD = 71
STRONG_ACTION_SPEED_MOD = 72
TARGET_ACTION_SPEED_MOD = 73
STRONG_TARGET_ACTION_SPEED_MOD = 74
AGILE_POWER = 75

TYPE = 92
QUALITY = 93
CATEGORY = 94
POWER = 95
ACCURACY = 96
PP = 97
PRIORITY = 98

def get_gen(move):
    for move_record in move.move_records:
        if 'Pokemon Brilliant Diamond' in move_record.games:
            return move_record.generation
    return '8'

done = []

with open('scripts/legends_arceus/moves.txt') as f:
    for line in f.readlines():
        columns = line.split('\t')
        move_name = columns[MOVE_NAME]
        if "Moves" == move_name or "———" == move_name:
            continue

        filename = '../xml/moves/' + move_name.lower().replace(' ', '_').replace('-', '_').replace('’', '_').replace(',', '_') + '.xml'
        if filename in done:
            continue
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write('<move/>')
        else:
            continue

        move = Move(filename)

        move_record = MoveRecord()
        move_record.games = ['Pokemon Legends Arceus']
        move_record.generation = get_gen(move)
        move_record.move_type = type_map[int(columns[TYPE])]
        move_record.base_power = columns[POWER]
        move_record.power_points = columns[PP]
        if columns[ACCURACY] == '101':
            columns[ACCURACY] = '100'
        move_record.accuracy = columns[ACCURACY]
        move_record.priority = columns[PRIORITY]
        if '0' == columns[CATEGORY]:
            move_record.damage_category = 'Status'
        elif '1' == columns[CATEGORY]:
            move_record.damage_category = 'Physical'
        elif '2' == columns[CATEGORY]:
            move_record.damage_category = 'Special'
        #move_record.effect = columns[PRIORITY]
        #move_record.effect_chance = columns[PRIORITY]
        #move_record.description = columns[PRIORITY]

        move.add_move_record(move_record)
        with open(filename, 'w') as f:
            move.dump(f)
        done.append(filename)
