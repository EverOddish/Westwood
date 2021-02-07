import glob
import os
import sys

from lxml import etree

if len(sys.argv) != 2:
    sys.exit('Usage: ' + sys.argv[0] + ' <ROM hack name>')

for filename in glob.glob(os.path.join('xml', 'moves', '*.xml')):
    tree = etree.parse(filename)
    move_name = filename.split('/')[-1].split('.')[0].lower().replace('_', '')
    should_print = False
    output = move_name + ': {\n'
    output += '    inherit: true,\n'

    for move_record in tree.iter('move_record'):
        for game in move_record.iter('game'):
            if sys.argv[1] in game.text:
                move_definition = move_record.find('move_definition')
                output += '    type: "' + move_definition.find('type').text + '",\n'
                output += '    basePower: ' + move_definition.find('base_power').text + ',\n'
                output += '    pp: ' + move_definition.find('power_points').text + ',\n'
                output += '    accuracy: ' + move_definition.find('accuracy').text + ',\n'
                output += '    priority: ' + move_definition.find('priority').text + ',\n'
                should_print = True

    output += '},'
    if should_print:
        print(output)
