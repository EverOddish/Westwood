import glob
import os
from django.db import migrations
from lxml import etree

WESTWOOD_XML_PATH = os.path.join('..', 'Westwood', 'xml')

def import_pokemon(apps, schema_editor):
    Pokemon = apps.get_model('westwood', 'Pokemon')
    PokedexNumber = apps.get_model('westwood', 'PokedexNumber')
    PokedexNumbersListElement = apps.get_model('westwood', 'PokedexNumbersListElement')
    db_alias = schema_editor.connection.alias

    pokemon_path = os.path.join(WESTWOOD_XML_PATH, 'pokemon')
    pokemon_objects = []
    pokedex_numbers_list_element_objects = []
    list_counter = 1

    print('\n')

    for pokemon_file in glob.glob(os.path.join(pokemon_path, '*.xml')):
        print('Processing: ' + pokemon_file)
        try:
            pokemon_tag = etree.parse(pokemon_file)

            list_id = list_counter
            list_counter += 1
            sequence_number = 1
            for pokedex_number_tag in pokemon_tag.iter('pokedex_number'):
                name_tag = pokedex_number_tag.find('name')
                number_tag = pokedex_number_tag.find('number')

                pokedex_number_object = PokedexNumber(name=name_tag.text, number=number_tag.text)
                pokedex_number_object.save()

                pokedex_numbers_list_element_object = PokedexNumbersListElement(list_id=list_id, sequence_number=sequence_number, element_id=pokedex_number_object.id)
                pokedex_numbers_list_element_objects.append(pokedex_numbers_list_element_object)
                sequence_number += 1

            name_tag = pokemon_tag.find('name')
            height_tag = pokemon_tag.find('height')
            weight_tag = pokemon_tag.find('weight')

            pokemon_objects.append(Pokemon(name=name_tag.text, pokedex_numbers=list_id, height=height_tag.text, weight=weight_tag.text))
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    PokedexNumbersListElement.objects.using(db_alias).bulk_create(pokedex_numbers_list_element_objects)
    Pokemon.objects.using(db_alias).bulk_create(pokemon_objects)

class Migration(migrations.Migration):

    dependencies = [
        ('westwood', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_pokemon),
    ]
