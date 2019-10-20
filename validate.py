import os
import shutil
import subprocess
import sys

if not shutil.which('xmllint'):
    raise SystemExit('xmllint not found!')

invalid_files = []

def run_xmllint(schema, target):
    command = ['xmllint', '--noout', '--schema', schema, target]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'validates' not in result.stderr.decode('utf-8'):
        invalid_files.append(target)
        print('Failed to validate: ' + target)

print('Processing Pokemon XML...')
schema = os.path.join('xsd', 'pokemon.xsd')
for filename in os.listdir(os.path.join('xml', 'pokemon')):
    target = os.path.join('xml', 'pokemon', filename)
    run_xmllint(schema, target)

print('Processing Move XML...')
schema = os.path.join('xsd', 'move.xsd')
for filename in os.listdir(os.path.join('xml', 'moves')):
    target = os.path.join('xml', 'moves', filename)
    run_xmllint(schema, target)

print('Processing Game XML...')
schema = os.path.join('xsd', 'game.xsd')
for filename in os.listdir(os.path.join('xml', 'games')):
    target = os.path.join('xml', 'games', filename)
    run_xmllint(schema, target)

print('Processing Learnset XML...')
schema = os.path.join('xsd', 'learnset.xsd')
for filename in os.listdir(os.path.join('xml', 'learnsets')):
    target = os.path.join('xml', 'learnsets', filename)
    run_xmllint(schema, target)

print('Processing TM Set XML...')
schema = os.path.join('xsd', 'tm_set.xsd')
for filename in os.listdir(os.path.join('xml', 'tm_sets')):
    target = os.path.join('xml', 'tm_sets', filename)
    run_xmllint(schema, target)

print('Processing Ability XML...')
schema = os.path.join('xsd', 'ability.xsd')
for filename in os.listdir(os.path.join('xml', 'abilities')):
    target = os.path.join('xml', 'abilities', filename)
    run_xmllint(schema, target)

print('Processing miscellaneous XML...')
schema = os.path.join('xsd', 'types.xsd')
target = os.path.join('xml', 'misc', 'types.xml')
run_xmllint(schema, target)

schema = os.path.join('xsd', 'learn_methods.xsd')
target = os.path.join('xml', 'misc', 'learn_methods.xml')
run_xmllint(schema, target)

schema = os.path.join('xsd', 'item.xsd')
target = os.path.join('xml', 'misc', 'items.xml')
run_xmllint(schema, target)

schema = os.path.join('xsd', 'type_effectiveness.xsd')
target = os.path.join('xml', 'misc', 'type_effectiveness.xml')
run_xmllint(schema, target)

schema = os.path.join('xsd', 'nature.xsd')
target = os.path.join('xml', 'misc', 'natures.xml')
run_xmllint(schema, target)

schema = os.path.join('xsd', 'rom_hack.xsd')
target = os.path.join('xml', 'misc', 'rom_hacks.xml')
run_xmllint(schema, target)

if len(invalid_files) > 0:
    raise SystemExit("Invalid data!")
else:
    print("All data is valid!")
