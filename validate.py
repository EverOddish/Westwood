import os
import shutil
import subprocess
import sys

if not shutil.which('xmllint'):
    raise SystemExit('xmllint not found!')

invalid_pokemon = []

for filename in os.listdir(os.path.join('xml', 'pokemon')):
    path = os.path.join('xml', 'pokemon', filename)
    command = ['xmllint', '--noout', '--schema', 'xsd/pokemon.xsd', path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'validates' not in result.stderr.decode('utf-8'):
        invalid_pokemon.append(path)

for invalid in invalid_pokemon:
    print('Failed to validate: ' + invalid)

if len(invalid_pokemon) > 0:
    raise SystemExit("Invalid data!")
else:
    print("All data is valid!")
