import os
import shutil
import subprocess

if not shutil.which('xmllint'):
    raise SystemExit('xmllint not found!')

invalid_files = []

dataset_mapping = {
    'ability': 'abilities',
    'game': 'games',
    'learnset': 'learnsets',
    'move': 'moves',
    'pokemon': 'pokemon',
    'tm_set': 'tm_sets',
    'form': 'forms',
    'tutor_set': 'tutor_sets',
}

misc_mapping = {
    'item': 'items',
    'learn_methods': 'learn_methods',
    'type_effectiveness': 'type_effectiveness',
    'types': 'types',
    'nature': 'natures',
    'rom_hack': 'rom_hacks',
}


def run_xmllint(schema, target):
    command = ['xmllint', '--noout', '--schema', schema, target]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'validates' not in result.stderr.decode('utf-8'):
        invalid_files.append(target)
        print('Failed to validate: ' + target)

def validate():

    schemas = os.listdir('xsd')

    for schema in schemas:
        if schema == 'enumerations':
            continue

        schema_name = schema.split('.')[0]
        schema = os.path.join('xsd', schema)

        print(f'Processing {schema_name.title()} XML...')
        if schema_name not in dataset_mapping:
            target = os.path.join(
                'xml', 'misc', '{}.xml'.format(misc_mapping[schema_name]))
            run_xmllint(schema, target)
            continue

        files = os.listdir(os.path.join('xml', dataset_mapping[schema_name]))

        for filename in files:
            target = os.path.join(
                'xml', dataset_mapping[schema_name], filename)
            run_xmllint(schema, target)

    if invalid_files:
        raise SystemExit("Invalid data!")
    else:
        print("All data is valid!")


validate()
