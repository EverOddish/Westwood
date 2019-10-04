from datetime import datetime
from datetime import timezone
import glob
import os
from django.db import migrations
from django.db.models import Max
from lxml import etree

WESTWOOD_XML_PATH = os.path.join('..', 'Westwood', 'xml')

def cache_game_ids(apps, db):
    Game = apps.get_model('westwood', 'Game')
    game_ids = {}
    for game in Game.objects.using(db).all():
        game_ids[game.name] = game.id
    return game_ids

def get_or_create_games_list(apps, db_alias, context, tags):
    Game = apps.get_model('westwood', 'Game')
    GamesListElement = apps.get_model('westwood', 'GamesListElement')

    # Search for an existing list
    new_games_list = []
    for game in tags:
        new_games_list.append(game.text)

    existing_games_list_ids = context
    if len(existing_games_list_ids.keys()) == 0:
        # Games lists haven't been cached from the database, so query them now
        max_list_id = 0
        aggregation = GamesListElement.objects.aggregate(Max('list_id')).get('list_id__max')
        if aggregation:
            max_list_id = aggregation

        for i in range(max_list_id):
            current_list_id = i + 1
            list_elements = GamesListElement.objects.filter(list_id=current_list_id)
            existing_list = []
            for elem in list_elements:
                existing_list.append(elem.element.name)
            existing_games_list_ids[tuple(existing_list)] = current_list_id
    else:
        max_list_id = len(existing_games_list_ids.keys())

    for existing_games_list in existing_games_list_ids.keys():
        if list(existing_games_list) == new_games_list:
            existing_id = existing_games_list_ids[existing_games_list]
            return existing_games_list_ids, existing_id

    # Games list does not exist, so create it
    games_list_id = max_list_id + 1
    sequence_number = 1
    games_list_element_objects = []
    for game in new_games_list:
        game_object = Game.objects.using(db_alias).filter(name=game)[0]
        games_list_element_object = GamesListElement(list_id=games_list_id, sequence_number=sequence_number, element=game_object)
        games_list_element_objects.append(games_list_element_object)
        sequence_number += 1
    GamesListElement.objects.using(db_alias).bulk_create(games_list_element_objects)
    existing_games_list_ids[tuple(new_games_list)] = games_list_id

    return existing_games_list_ids, games_list_id

def import_games(apps, schema_editor):
    print('\nImporting Game data...')
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
            print('Error parsing XML file: ' + game_file)

    Game.objects.using(db_alias).bulk_create(game_objects)

def import_pokemon(apps, schema_editor):
    print('Importing Pokemon data...')
    Pokemon = apps.get_model('westwood', 'Pokemon')
    PokedexNumber = apps.get_model('westwood', 'PokedexNumber')
    PokedexNumbersListElement = apps.get_model('westwood', 'PokedexNumbersListElement')
    Game = apps.get_model('westwood', 'Game')
    StatSet = apps.get_model('westwood', 'StatSet')
    StatSetsListElement = apps.get_model('westwood', 'StatSetsListElement')
    TypeSet = apps.get_model('westwood', 'TypeSet')
    TypeSetsListElement = apps.get_model('westwood', 'TypeSetsListElement')
    AbilityRecord = apps.get_model('westwood', 'AbilityRecord')
    AbilityRecordsListElement = apps.get_model('westwood', 'AbilityRecordsListElement')
    AbilitySet = apps.get_model('westwood', 'AbilitySet')
    AbilitySetsListElement = apps.get_model('westwood', 'AbilitySetsListElement')
    EvolutionRecord = apps.get_model('westwood', 'EvolutionRecord')
    EvolutionRecordsListElement = apps.get_model('westwood', 'EvolutionRecordsListElement')
    EvolutionSet = apps.get_model('westwood', 'EvolutionSet')
    EvolutionSetsListElement = apps.get_model('westwood', 'EvolutionSetsListElement')
    db_alias = schema_editor.connection.alias

    pokemon_path = os.path.join(WESTWOOD_XML_PATH, 'pokemon')
    pokemon_objects = []
    pokedex_numbers_list_element_objects = []
    list_counter = 1
    stat_sets_list_counter = 1
    type_sets_list_counter = 1
    ability_sets_list_counter = 1
    ability_records_list_counter = 1
    evolution_sets_list_counter = 1
    evolution_records_list_counter = 1
    context = {}

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
                pokedex_number_object.save(using=db_alias)

                pokedex_numbers_list_element_object = PokedexNumbersListElement(list_id=list_id, sequence_number=sequence_number, element_id=pokedex_number_object.id)
                pokedex_numbers_list_element_objects.append(pokedex_numbers_list_element_object)
                sequence_number += 1

            name_tag = pokemon_tag.find('name')
            height_tag = pokemon_tag.find('height')
            weight_tag = pokemon_tag.find('weight')

            stat_sets_list_id = stat_sets_list_counter
            stat_sets_list_counter += 1
            stat_sets_sequence_number = 1
            stat_sets_list_element_objects = []
            for stat_set_tag in pokemon_tag.iter('stat_set'):

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, stat_set_tag.iter('game'))

                hp = int(stat_set_tag.find('hp').text)
                attack = int(stat_set_tag.find('attack').text)
                defense = int(stat_set_tag.find('defense').text)
                special_attack = int(stat_set_tag.find('special_attack').text)
                special_defense = int(stat_set_tag.find('special_defense').text)
                speed = int(stat_set_tag.find('speed').text)
                stat_set_object = StatSet(games=games_list_id, hp=hp, attack=attack, defense=defense, special_attack=special_attack, special_defense=special_defense, speed=speed)
                stat_set_object.save(using=db_alias)

                stat_sets_list_element_object = StatSetsListElement(list_id=stat_sets_list_id, sequence_number=stat_sets_sequence_number, element=stat_set_object)
                stat_sets_list_element_objects.append(stat_sets_list_element_object)
                stat_sets_sequence_number += 1

            StatSetsListElement.objects.using(db_alias).bulk_create(stat_sets_list_element_objects)

            type_sets_list_id = type_sets_list_counter
            type_sets_list_counter += 1
            type_sets_sequence_number = 1
            type_sets_list_element_objects = []
            for type_set_tag in pokemon_tag.iter('type_set'):

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, type_set_tag.iter('game'))

                type1 = type_set_tag.find('type1').text
                type2 = type_set_tag.find('type2')
                if None != type2:
                    type2 = type2.text
                else:
                    type2 = ''
                type_set_object = TypeSet(games=games_list_id, type1=type1, type2=type2)
                type_set_object.save(using=db_alias)

                type_sets_list_element_object = TypeSetsListElement(list_id=type_sets_list_id, sequence_number=type_sets_sequence_number, element=type_set_object)
                type_sets_list_element_objects.append(type_sets_list_element_object)
                type_sets_sequence_number += 1

            TypeSetsListElement.objects.using(db_alias).bulk_create(type_sets_list_element_objects)

            ability_sets_list_id = ability_sets_list_counter
            ability_sets_list_counter += 1
            ability_sets_sequence_number = 1
            ability_sets_list_element_objects = []
            for ability_set_tag in pokemon_tag.iter('ability_set'):

                ability_records_list_id = ability_records_list_counter
                ability_records_list_counter += 1
                sequence_number = 1
                ability_records_list_element_objects = []
                for ability_record in ability_set_tag.iter('ability_record'):
                    ability_name_tag = ability_record.find('name')
                    hidden_tag = ability_record.find('hidden')
                    ability_record_object, created = AbilityRecord.objects.using(db_alias).get_or_create(name=ability_name_tag.text, hidden=hidden_tag.text)

                    ability_records_list_element_object = AbilityRecordsListElement(list_id=ability_records_list_id, sequence_number=sequence_number, element=ability_record_object)
                    ability_records_list_element_objects.append(ability_records_list_element_object)
                    sequence_number += 1
                AbilityRecordsListElement.objects.using(db_alias).bulk_create(ability_records_list_element_objects)

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, ability_set_tag.iter('game'))

                ability_set_object = AbilitySet(games=games_list_id, ability_records=ability_records_list_id)
                ability_set_object.save(using=db_alias)

                ability_sets_list_element_object = AbilitySetsListElement(list_id=ability_sets_list_id, sequence_number=ability_sets_sequence_number, element=ability_set_object)
                ability_sets_list_element_objects.append(ability_sets_list_element_object)
                ability_sets_sequence_number += 1

            AbilitySetsListElement.objects.using(db_alias).bulk_create(ability_sets_list_element_objects)

            evolution_sets_list_id = evolution_sets_list_counter
            evolution_sets_list_counter += 1
            evolution_sets_sequence_number = 1
            evolution_sets_list_element_objects = []
            for evolution_set_tag in pokemon_tag.iter('evolution_set'):

                evolution_records_list_id = evolution_records_list_counter
                evolution_records_list_counter += 1
                sequence_number = 1
                evolution_records_list_element_objects = []
                for evolution_record in evolution_set_tag.iter('evolution_record'):
                    evolves_to_tag = evolution_record.find('evolves_to')
                    level_tag = evolution_record.find('level')
                    if None != level_tag:
                        level_int = int(level_tag.text)
                    else:
                        level_int = 0
                    evolution_record_object, created = EvolutionRecord.objects.using(db_alias).get_or_create(evolves_to=evolves_to_tag.text, level=level_int)

                    evolution_records_list_element_object = EvolutionRecordsListElement(list_id=evolution_records_list_id, sequence_number=sequence_number, element=evolution_record_object)
                    evolution_records_list_element_objects.append(evolution_records_list_element_object)
                    sequence_number += 1
                EvolutionRecordsListElement.objects.using(db_alias).bulk_create(evolution_records_list_element_objects)

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, ability_set_tag.iter('game'))

                evolution_set_object = EvolutionSet(games=games_list_id, evolution_records=evolution_records_list_id)
                evolution_set_object.save(using=db_alias)

                evolution_sets_list_element_object = EvolutionSetsListElement(list_id=evolution_sets_list_id, sequence_number=evolution_sets_sequence_number, element=evolution_set_object)
                evolution_sets_list_element_objects.append(evolution_sets_list_element_object)
                evolution_sets_sequence_number += 1

            EvolutionSetsListElement.objects.using(db_alias).bulk_create(evolution_sets_list_element_objects)

            pokemon_object = Pokemon(name=name_tag.text, pokedex_numbers=list_id, height=height_tag.text, weight=weight_tag.text, stat_sets=stat_sets_list_id, type_sets=type_sets_list_id, ability_sets=ability_sets_list_id, evolution_sets=evolution_sets_list_id)
            pokemon_objects.append(pokemon_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + pokemon_file)

    PokedexNumbersListElement.objects.using(db_alias).bulk_create(pokedex_numbers_list_element_objects)
    Pokemon.objects.using(db_alias).bulk_create(pokemon_objects)

def import_moves(apps, schema_editor):
    print('Importing Move data...')
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
            print('Error parsing XML file: ' + move_file)

    Move.objects.using(db_alias).bulk_create(move_objects)

def import_abilities(apps, schema_editor):
    print('Importing Ability data...')
    Ability = apps.get_model('westwood', 'Ability')
    db_alias = schema_editor.connection.alias

    ability_path = os.path.join(WESTWOOD_XML_PATH, 'abilities')
    ability_objects = []
    games_list_element_objects = []
    list_counter = 1
    game_ids = cache_game_ids(apps, db_alias)
    context = {}

    for ability_file in glob.glob(os.path.join(ability_path, '*.xml')):
        #print('Processing: ' + ability_file)
        try:
            ability_tag = etree.parse(ability_file)
            name_tag = ability_tag.find('name')
            description_tag = ability_tag.find('description')

            context, list_id = get_or_create_games_list(apps, db_alias, context, ability_tag.iter('game'))

            ability_object = Ability(name=name_tag.text, description=description_tag.text, games=list_id)
            ability_objects.append(ability_object)
        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + ability_file)

    Ability.objects.using(db_alias).bulk_create(ability_objects)

def import_misc(apps, schema_editor):
    print('Importing Misc data...')
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
        print('Error parsing XML file: types.xml')
    Type.objects.using(db_alias).bulk_create(type_objects)

    learn_method_objects = []
    try:
        learn_methods_tag = etree.parse(os.path.join(misc_path, 'learn_methods.xml'))
        for learn_method in learn_methods_tag.iter('learn_method'):
            learn_method_objects.append(LearnMethod(value=learn_method.text))
    except etree.XMLSyntaxError:
        print('Error parsing XML file: learn_methods.xml')
    LearnMethod.objects.using(db_alias).bulk_create(learn_method_objects)

def import_learnsets(apps, schema_editor):
    print('Importing Learnset data...')
    PokemonLearnsets = apps.get_model('westwood', 'PokemonLearnsets')
    Learnset = apps.get_model('westwood', 'Learnset')
    LearnsetsListElement = apps.get_model('westwood', 'LearnsetsListElement')
    LearnsetMove = apps.get_model('westwood', 'LearnsetMove')
    LearnsetMovesListElement = apps.get_model('westwood', 'LearnsetMovesListElement')
    db_alias = schema_editor.connection.alias

    learnsets_path = os.path.join(WESTWOOD_XML_PATH, 'learnsets')
    learnset_moves_list_counter = 1
    games_list_counter = 1
    learnsets_list_counter = 1
    context = {}

    for learnset_file in glob.glob(os.path.join(learnsets_path, '*.xml')):
        #print('Processing: ' + learnset_file)
        try:
            pokemon_learnsets_tag = etree.parse(learnset_file)
            pokemon_name = pokemon_learnsets_tag.find('name').text
            
            learnsets_list_id = learnsets_list_counter
            learnsets_list_counter += 1
            learnsets_sequence_number = 1
            learnsets_list_element_objects = []
            for learnset_tag in pokemon_learnsets_tag.iter('learnset'):

                learnset_moves_list_id = learnset_moves_list_counter
                learnset_moves_list_counter += 1
                sequence_number = 1
                learnset_moves_list_element_objects = []
                for learnset_move in learnset_tag.iter('learnset_move'):
                    name_tag = learnset_move.find('name')
                    level_tag = learnset_move.find('level')
                    learnset_move_object, created = LearnsetMove.objects.using(db_alias).get_or_create(name=name_tag.text, level=level_tag.text)

                    learnset_moves_list_element_object = LearnsetMovesListElement(list_id=learnset_moves_list_id, sequence_number=sequence_number, element=learnset_move_object)
                    learnset_moves_list_element_objects.append(learnset_moves_list_element_object)
                    sequence_number += 1
                LearnsetMovesListElement.objects.using(db_alias).bulk_create(learnset_moves_list_element_objects)

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, learnset_tag.iter('game'))

                learnset_object = Learnset(games=games_list_id, learnset_moves=learnset_moves_list_id)
                learnset_object.save(using=db_alias)

                learnsets_list_element_object = LearnsetsListElement(list_id=learnsets_list_id, sequence_number=learnsets_sequence_number, element=learnset_object)
                learnsets_list_element_objects.append(learnsets_list_element_object)
                learnsets_sequence_number += 1

            LearnsetsListElement.objects.using(db_alias).bulk_create(learnsets_list_element_objects)

            pokemon_learnsets_object = PokemonLearnsets(name=pokemon_name, learnsets=learnsets_list_id)
            pokemon_learnsets_object.save(using=db_alias)

        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + learnset_file)

def import_tmsets(apps, schema_editor):
    print('Importing TmSet data...')
    PokemonTmSets = apps.get_model('westwood', 'PokemonTmSets')
    TmSet = apps.get_model('westwood', 'TmSet')
    TmSetsListElement = apps.get_model('westwood', 'TmSetsListElement')
    TmsetMove = apps.get_model('westwood', 'TmsetMove')
    TmsetMovesListElement = apps.get_model('westwood', 'TmsetMovesListElement')
    db_alias = schema_editor.connection.alias

    tm_sets_path = os.path.join(WESTWOOD_XML_PATH, 'tm_sets')
    tmset_moves_list_counter = 1
    games_list_counter = 1
    tm_sets_list_counter = 1
    context = {}

    for tm_set_file in glob.glob(os.path.join(tm_sets_path, '*.xml')):
        #print('Processing: ' + tm_set_file)
        try:
            pokemon_tm_sets_tag = etree.parse(tm_set_file)
            pokemon_name = pokemon_tm_sets_tag.find('name').text
            
            tm_sets_list_id = tm_sets_list_counter
            tm_sets_list_counter += 1
            tm_sets_sequence_number = 1
            tm_sets_list_element_objects = []
            for tm_set_tag in pokemon_tm_sets_tag.iter('tm_set'):

                tmset_moves_list_id = tmset_moves_list_counter
                tmset_moves_list_counter += 1
                sequence_number = 1
                tmset_moves_list_element_objects = []
                for tmset_move in tm_set_tag.iter('tmset_move'):
                    tmset_move_object, created = TmsetMove.objects.using(db_alias).get_or_create(name=tmset_move.text)

                    tmset_moves_list_element_object = TmsetMovesListElement(list_id=tmset_moves_list_id, sequence_number=sequence_number, element=tmset_move_object)
                    tmset_moves_list_element_objects.append(tmset_moves_list_element_object)
                    sequence_number += 1
                TmsetMovesListElement.objects.using(db_alias).bulk_create(tmset_moves_list_element_objects)

                context, games_list_id = get_or_create_games_list(apps, db_alias, context, tm_set_tag.iter('game'))

                tmset_object = TmSet(games=games_list_id, tmset_moves=tmset_moves_list_id)
                tmset_object.save(using=db_alias)

                tm_sets_list_element_object = TmSetsListElement(list_id=tm_sets_list_id, sequence_number=tm_sets_sequence_number, element=tmset_object)
                tm_sets_list_element_objects.append(tm_sets_list_element_object)
                tm_sets_sequence_number += 1

            TmSetsListElement.objects.using(db_alias).bulk_create(tm_sets_list_element_objects)

            pokemon_tm_sets_object = PokemonTmSets(name=pokemon_name, tm_sets=tm_sets_list_id)
            pokemon_tm_sets_object.save(using=db_alias)

        except etree.XMLSyntaxError:
            print('Error parsing XML file: ' + learnset_file)

def import_items(apps, schema_editor):
    print('Importing Item data...')
    Item = apps.get_model('westwood', 'Item')
    db_alias = schema_editor.connection.alias

    item_path = os.path.join(WESTWOOD_XML_PATH, 'misc', 'items.xml')
    item_objects = []
    list_counter = 1

    try:
        items_tag = etree.parse(item_path)
        for item_tag in items_tag.iter('item'):
            name_tag = item_tag.find('name')
            cost_tag = item_tag.find('cost')
            description_tag = item_tag.find('description')

            item_object = Item(name=name_tag.text, cost=cost_tag.text, description=description_tag.text)
            item_objects.append(item_object)
    except etree.XMLSyntaxError:
        print('Error parsing XML file: ' + item_path)

    Item.objects.using(db_alias).bulk_create(item_objects)

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
        migrations.RunPython(import_learnsets),
        migrations.RunPython(import_tmsets),
        migrations.RunPython(import_items),
    ]
