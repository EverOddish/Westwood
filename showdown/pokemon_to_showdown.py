import glob
import os
import sys

from lxml import etree

if len(sys.argv) != 2:
    sys.exit('Usage: ' + sys.argv[0] + ' <ROM hack name>')

for filename in glob.glob(os.path.join('xml', 'pokemon', '*.xml')):
    tree = etree.parse(filename)
    pokemon_name = filename.split('/')[-1].split('.')[0].lower()
    should_print = False
    output = pokemon_name + ': {\n'
    output += '    inherit: true,\n'

    for stat_set in tree.iter('stat_set'):
        for game in stat_set.iter('game'):
            if sys.argv[1] in game.text:
                output += '    baseStats: {hp: ' + stat_set.find('hp').text + ', atk: ' + stat_set.find('attack').text + ', def: ' + stat_set.find('defense').text + ', spa: ' + stat_set.find('special_attack').text + ', spd: ' + stat_set.find('special_defense').text + ', spe: ' + stat_set.find('speed').text + '},\n'
                should_print = True

    for ability_set in tree.iter('ability_set'):
        for game in ability_set.iter('game'):
            if sys.argv[1] in game.text:
                output += '    abilities: {'
                index = '0'
                for ability_record in ability_set.iter('ability_record'):
                    if 'Yes' == ability_record.find('hidden').text:
                        index = 'H'
                    output += index + ': "' + ability_record.find('name').text + '", '
                    if '0' == index:
                        index = '1'
                output += '}\n'
                should_print = True

    for type_set in tree.iter('type_set'):
        for game in type_set.iter('game'):
            if sys.argv[1] in game.text:
                output += '    types: ["' + type_set.find('type1').text + '"'
                if type_set.find('type2'):
                    output += ', "' + type_set.find('type2').text + '"'
                output += '],\n'
                should_print = True

    output += '},'
    if should_print:
        print(output)
