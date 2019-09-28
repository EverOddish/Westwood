from datetime import datetime
from datetime import timezone
import glob
import os
from django.db import migrations
from lxml import etree

WESTWOOD_XML_PATH = os.path.join('..', 'Westwood', 'xml')

def cache_game_ids(apps, db):
    Game = apps.get_model('westwood', 'Game')
    game_ids = {}
    for game in Game.objects.using(db).all():
        game_ids[game.name] = game.id
    return game_ids

def import_games(apps, schema_editor):
    Game = apps.get_model('westwood', 'Game')
    db_alias = schema_editor.connection.alias

    game_path = os.path.join(WESTWOOD_XML_PATH, 'games')
    game_objects = []

    for game_file in glob.glob(os.path.join(game_path, '*.xml')):
        #print('Processing: ' + game_file)
        try:
            game_tag = etree.parse(game_file)
            name_tag = game_tag.find('name')
            generation_tag = game_tag.find('generation')
            generation = int(generation_tag.text)
            release_date_tag = game_tag.find('release_date')
            release_date = datetime.strptime(release_date_tag.text, '%Y-%m-%d')
            release_date = release_date.replace(tzinfo=timezone.utc)
            system_tag = game_tag.find('system')
            region_tag = game_tag.find('region')

            game_object = Game(name=name_tag.text, generation=generation, release_date=release_date, system=system_tag.text, region=region_tag.text)
            game_objects.append(game_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    Game.objects.using(db_alias).bulk_create(game_objects)

def import_pokemon(apps, schema_editor):
    Pokemon = apps.get_model('westwood', 'Pokemon')
    PokedexNumber = apps.get_model('westwood', 'PokedexNumber')
    PokedexNumbersListElement = apps.get_model('westwood', 'PokedexNumbersListElement')
    db_alias = schema_editor.connection.alias

    pokemon_path = os.path.join(WESTWOOD_XML_PATH, 'pokemon')
    pokemon_objects = []
    pokedex_numbers_list_element_objects = []
    list_counter = 1

    for pokemon_file in glob.glob(os.path.join(pokemon_path, '*.xml')):
        #print('Processing: ' + pokemon_file)
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

            pokemon_object = Pokemon(name=name_tag.text, pokedex_numbers=list_id, height=height_tag.text, weight=weight_tag.text)
            pokemon_objects.append(pokemon_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    PokedexNumbersListElement.objects.using(db_alias).bulk_create(pokedex_numbers_list_element_objects)
    Pokemon.objects.using(db_alias).bulk_create(pokemon_objects)

def import_moves(apps, schema_editor):
    Move = apps.get_model('westwood', 'Move')
    db_alias = schema_editor.connection.alias

    move_path = os.path.join(WESTWOOD_XML_PATH, 'moves')
    move_objects = []

    for move_file in glob.glob(os.path.join(move_path, '*.xml')):
        #print('Processing: ' + move_file)
        try:
            move_tag = etree.parse(move_file)
            name_tag = move_tag.find('name')
            generation_tag = move_tag.find('generation')
            type_tag = move_tag.find('type')
            base_power_tag = move_tag.find('base_power')
            power_points_tag = move_tag.find('power_points')
            accuracy_tag = move_tag.find('accuracy')
            priority_tag = move_tag.find('priority')
            damage_category_tag = move_tag.find('damage_category')

            move_object = Move(name=name_tag.text, generation=generation_tag.text, type_1=type_tag.text, base_power=base_power_tag.text, power_points=power_points_tag.text, accuracy=accuracy_tag.text, priority=priority_tag.text, damage_category=damage_category_tag.text)
            move_objects.append(move_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    Move.objects.using(db_alias).bulk_create(move_objects)

def import_abilities(apps, schema_editor):
    Ability = apps.get_model('westwood', 'Ability')
    GamesListElement = apps.get_model('westwood', 'GamesListElement')
    db_alias = schema_editor.connection.alias

    ability_path = os.path.join(WESTWOOD_XML_PATH, 'abilities')
    ability_objects = []
    games_list_element_objects = []
    list_counter = 1
    game_ids = cache_game_ids(apps, db_alias)

    for ability_file in glob.glob(os.path.join(ability_path, '*.xml')):
        #print('Processing: ' + ability_file)
        try:
            ability_tag = etree.parse(ability_file)
            name_tag = ability_tag.find('name')
            description_tag = ability_tag.find('description')

            # TODO: Determine if a matching games list already exists, and reference that list instead of creating a duplicate.
            list_id = list_counter
            list_counter += 1
            sequence_number = 1
            for game_tag in ability_tag.iter('game'):
                game_name = game_tag.text
                game_id = game_ids[game_name]
                games_list_element_object = GamesListElement(list_id=list_id, sequence_number=sequence_number, element_id=game_id)
                games_list_element_objects.append(games_list_element_object)
                sequence_number += 1

            ability_object = Ability(name=name_tag.text, description=description_tag.text, games=list_id)
            ability_objects.append(ability_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    GamesListElement.objects.using(db_alias).bulk_create(games_list_element_objects)
    Ability.objects.using(db_alias).bulk_create(ability_objects)

def import_misc(apps, schema_editor):
    Type = apps.get_model('westwood', 'Type')
    LearnMethod = apps.get_model('westwood', 'LearnMethod')
    db_alias = schema_editor.connection.alias
    misc_path = os.path.join(WESTWOOD_XML_PATH, 'misc')

    type_objects = []
    try:
        types_tag = etree.parse(os.path.join(misc_path, 'types.xml'))
        for type_tag in types_tag.iter('type'):
            type_objects.append(Type(value=type_tag.text))
    except etree.XMLSyntaxError:
        print('Error parsing XML file: ' + pokemon_file)
    Type.objects.using(db_alias).bulk_create(type_objects)

    learn_method_objects = []
    try:
        learn_methods_tag = etree.parse(os.path.join(misc_path, 'learn_methods.xml'))
        for learn_method in learn_methods_tag.iter('learn_method'):
            learn_method_objects.append(LearnMethod(value=learn_method.text))
    except etree.XMLSyntaxError:
        print('Error parsing XML file: ' + pokemon_file)
    LearnMethod.objects.using(db_alias).bulk_create(learn_method_objects)

class Migration(migrations.Migration):

    dependencies = [
        ('westwood', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_games),
        migrations.RunPython(import_pokemon),
        migrations.RunPython(import_moves),
        migrations.RunPython(import_abilities),
        migrations.RunPython(import_misc),
    ]
