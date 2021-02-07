import glob
import os
import sys

from lxml import etree

if len(sys.argv) != 3:
    sys.exit('Usage: ' + sys.argv[0] + ' <ROM hack name> <generation number>')

gen = sys.argv[2]

for filename in glob.glob(os.path.join('xml', 'learnsets', '*.xml')):
    tree = etree.parse(filename)
    pokemon_name = filename.split('/')[-1].split('.')[0].lower()
    should_print = False
    output = pokemon_name + ': {\n'
    output += '    learnset: {\n'

    for learnset in tree.iter('learnset'):
        for game in learnset.iter('game'):
            if sys.argv[1] in game.text:
                for learnset_move in learnset.iter('learnset_move'):
                    name = learnset_move.find('name').text.lower().replace(' ', '').replace('-', '')
                    level = learnset_move.find('level').text
                    output += '        ' + name + ': ["' + gen + 'L' + level + '"],\n'
                    should_print = True

    tmset_path = os.path.join('xml', 'tm_sets', pokemon_name + '.xml')
    if os.path.exists(tmset_path):
        tree = etree.parse(tmset_path)

        for tm_set in tree.iter('tm_set'):
            for game in tm_set.iter('game'):
                if sys.argv[1] in game.text:
                    for tmset_move in tm_set.iter('tmset_move'):
                        name = tmset_move.text.lower().replace(' ', '').replace('-', '')
                        output += '        ' + name + ': ["' + gen + 'M"],\n'
                        should_print = True

    output += '    },\n'
    output += '},\n'
    if should_print:
        print(output)
