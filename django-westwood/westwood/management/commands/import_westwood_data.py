from datetime import datetime
from datetime import timezone
import glob
import os
import math
from westwood.models import *
from django.core.management.base import BaseCommand, CommandError
from django.db import migrations
from django.db.models import Max
from lxml import etree

WESTWOOD_XML_PATH = os.path.join('..', 'Westwood', 'xml')

def calculate_stat(base_stat, level=100, ev=0.0, iv=31.0, hindered=False, beneficial=False):
    base_stat = base_stat * 1.0
    nature = 1.0
    if hindered:
        nature = 0.9
    if beneficial:
        nature = 1.1
    stat = math.floor((math.floor((((2 * base_stat) + iv + math.floor(ev / 4)) * level) / 100) + 5) * nature)
    return stat

def calculate_hp(base_hp, level=100, ev=0.0, iv=31.0):
    base_hp = base_hp * 1.0
    hp_stat = math.floor((((2 * base_hp) + iv + math.floor(ev / 4)) * level) / 100) + level + 10
    return hp_stat

class Command(BaseCommand):
    help = 'Imports Westwood XML data into the Westwood database'

    def cache_game_ids(self):
        game_ids = {}
        for game in Game.objects.using(self.db_alias).all():
            game_ids[game.name] = game.id
        return game_ids

    def get_or_create_games_list(self, context, tags):
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
            game_object = Game.objects.using(self.db_alias).filter(name=game)[0]
            games_list_element_object = GamesListElement(list_id=games_list_id, sequence_number=sequence_number, element=game_object)
            games_list_element_objects.append(games_list_element_object)
            sequence_number += 1
        GamesListElement.objects.using(self.db_alias).bulk_create(games_list_element_objects)
        existing_games_list_ids[tuple(new_games_list)] = games_list_id

        return existing_games_list_ids, games_list_id

    def import_games(self):
        self.stdout.write('Importing Game data...')

        game_path = os.path.join(WESTWOOD_XML_PATH, 'games')
        game_objects = []

        for game_file in glob.glob(os.path.join(game_path, '*.xml')):
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
                sequence_tag = game_tag.find('sequence')

                game_object = Game(name=name_tag.text, generation=generation, release_date=release_date, system=system_tag.text, region=region_tag.text, sequence=sequence_tag.text)
                game_objects.append(game_object)
            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + game_file)

        Game.objects.using(self.db_alias).bulk_create(game_objects)

    def import_pokemon(self):
        self.stdout.write('Importing Pokemon data...')

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
        ev_yields_list_counter = 1
        context = {}

        for pokemon_file in glob.glob(os.path.join(pokemon_path, '*.xml')):
            try:
                pokemon_tag = etree.parse(pokemon_file)

                list_id = list_counter
                list_counter += 1
                sequence_number = 1
                for pokedex_number_tag in pokemon_tag.iter('pokedex_number'):
                    name_tag = pokedex_number_tag.find('name')
                    number_tag = pokedex_number_tag.find('number')

                    pokedex_number_object = PokedexNumber(name=name_tag.text, number=number_tag.text)
                    pokedex_number_object.save(using=self.db_alias)

                    pokedex_numbers_list_element_object = PokedexNumbersListElement(list_id=list_id, sequence_number=sequence_number, element_id=pokedex_number_object.id)
                    pokedex_numbers_list_element_objects.append(pokedex_numbers_list_element_object)
                    sequence_number += 1

                name_tag = pokemon_tag.find('name')
                height_tag = pokemon_tag.find('height')
                weight_tag = pokemon_tag.find('weight')
                catch_rate_tag = pokemon_tag.find('catch_rate')
                growth_rate_tag = pokemon_tag.find('growth_rate')
                base_exp_tag = pokemon_tag.find('base_exp')
                egg_groups_tag = pokemon_tag.find('egg_groups')

                stat_sets_list_id = stat_sets_list_counter
                stat_sets_list_counter += 1
                stat_sets_sequence_number = 1
                stat_sets_list_element_objects = []
                for stat_set_tag in pokemon_tag.iter('stat_set'):

                    context, games_list_id = self.get_or_create_games_list(context, stat_set_tag.iter('game'))

                    hp = int(stat_set_tag.find('hp').text)
                    attack = int(stat_set_tag.find('attack').text)
                    defense = int(stat_set_tag.find('defense').text)
                    special_attack = int(stat_set_tag.find('special_attack').text)
                    special_defense = int(stat_set_tag.find('special_defense').text)
                    speed = int(stat_set_tag.find('speed').text)

                    stat_set_object = StatSet(games=games_list_id, hp=hp, attack=attack, defense=defense, special_attack=special_attack, special_defense=special_defense, speed=speed)

                    stat_set_object.max_hp = calculate_hp(hp, ev=252.0)

                    stat_set_object.max_attack_hindered = calculate_stat(attack, ev=252.0, hindered=True)
                    stat_set_object.max_attack_neutral = calculate_stat(attack, ev=252.0)
                    stat_set_object.max_attack_beneficial = calculate_stat(attack, ev=252.0, beneficial=True)

                    stat_set_object.max_defense_hindered = calculate_stat(defense, ev=252.0, hindered=True)
                    stat_set_object.max_defense_neutral = calculate_stat(defense, ev=252.0)
                    stat_set_object.max_defense_beneficial = calculate_stat(defense, ev=252.0, beneficial=True)

                    stat_set_object.max_special_attack_hindered = calculate_stat(special_attack, ev=252.0, hindered=True)
                    stat_set_object.max_special_attack_neutral = calculate_stat(special_attack, ev=252.0)
                    stat_set_object.max_special_attack_beneficial = calculate_stat(special_attack, ev=252.0, beneficial=True)

                    stat_set_object.max_special_defense_hindered = calculate_stat(special_defense, ev=252.0, hindered=True)
                    stat_set_object.max_special_defense_neutral = calculate_stat(special_defense, ev=252.0)
                    stat_set_object.max_special_defense_beneficial = calculate_stat(special_defense, ev=252.0, beneficial=True)

                    stat_set_object.max_speed_hindered = calculate_stat(speed, ev=252.0, hindered=True)
                    stat_set_object.max_speed_neutral = calculate_stat(speed, ev=252.0)
                    stat_set_object.max_speed_beneficial = calculate_stat(speed, ev=252.0, beneficial=True)

                    stat_set_object.save(using=self.db_alias)

                    stat_sets_list_element_object = StatSetsListElement(list_id=stat_sets_list_id, sequence_number=stat_sets_sequence_number, element=stat_set_object)
                    stat_sets_list_element_objects.append(stat_sets_list_element_object)
                    stat_sets_sequence_number += 1

                StatSetsListElement.objects.using(self.db_alias).bulk_create(stat_sets_list_element_objects)

                type_sets_list_id = type_sets_list_counter
                type_sets_list_counter += 1
                type_sets_sequence_number = 1
                type_sets_list_element_objects = []
                for type_set_tag in pokemon_tag.iter('type_set'):

                    context, games_list_id = self.get_or_create_games_list(context, type_set_tag.iter('game'))

                    type1 = type_set_tag.find('type1').text
                    type2 = type_set_tag.find('type2')
                    if None != type2:
                        type2 = type2.text
                    else:
                        type2 = ''
                    type_set_object = TypeSet(games=games_list_id, type1=type1, type2=type2)
                    type_set_object.save(using=self.db_alias)

                    type_sets_list_element_object = TypeSetsListElement(list_id=type_sets_list_id, sequence_number=type_sets_sequence_number, element=type_set_object)
                    type_sets_list_element_objects.append(type_sets_list_element_object)
                    type_sets_sequence_number += 1

                TypeSetsListElement.objects.using(self.db_alias).bulk_create(type_sets_list_element_objects)

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
                        ability_record_object, created = AbilityRecord.objects.using(self.db_alias).get_or_create(name=ability_name_tag.text, hidden=hidden_tag.text)

                        ability_records_list_element_object = AbilityRecordsListElement(list_id=ability_records_list_id, sequence_number=sequence_number, element=ability_record_object)
                        ability_records_list_element_objects.append(ability_records_list_element_object)
                        sequence_number += 1
                    AbilityRecordsListElement.objects.using(self.db_alias).bulk_create(ability_records_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, ability_set_tag.iter('game'))

                    ability_set_object = AbilitySet(games=games_list_id, ability_records=ability_records_list_id)
                    ability_set_object.save(using=self.db_alias)

                    ability_sets_list_element_object = AbilitySetsListElement(list_id=ability_sets_list_id, sequence_number=ability_sets_sequence_number, element=ability_set_object)
                    ability_sets_list_element_objects.append(ability_sets_list_element_object)
                    ability_sets_sequence_number += 1

                AbilitySetsListElement.objects.using(self.db_alias).bulk_create(ability_sets_list_element_objects)

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
                        method_string = ''
                        for method_tag in evolution_record.iter('method'):
                            method_string += method_tag.text + ' '
                        if method_string.endswith(' '):
                            method_string = method_string[:-1]
                        evolution_record_object, created = EvolutionRecord.objects.using(self.db_alias).get_or_create(evolves_to=evolves_to_tag.text, level=level_int, method=method_string)

                        evolution_records_list_element_object = EvolutionRecordsListElement(list_id=evolution_records_list_id, sequence_number=sequence_number, element=evolution_record_object)
                        evolution_records_list_element_objects.append(evolution_records_list_element_object)
                        sequence_number += 1
                    EvolutionRecordsListElement.objects.using(self.db_alias).bulk_create(evolution_records_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, evolution_set_tag.iter('game'))

                    evolution_set_object = EvolutionSet(games=games_list_id, evolution_records=evolution_records_list_id)
                    evolution_set_object.save(using=self.db_alias)

                    evolution_sets_list_element_object = EvolutionSetsListElement(list_id=evolution_sets_list_id, sequence_number=evolution_sets_sequence_number, element=evolution_set_object)
                    evolution_sets_list_element_objects.append(evolution_sets_list_element_object)
                    evolution_sets_sequence_number += 1

                EvolutionSetsListElement.objects.using(self.db_alias).bulk_create(evolution_sets_list_element_objects)

                ev_yields_list_id = ev_yields_list_counter
                ev_yields_list_counter += 1
                ev_yields_sequence_number = 1
                ev_yields_list_element_objects = []
                for ev_yield_tag in pokemon_tag.iter('ev_yield'):

                    stat = ev_yield_tag.find('stat').text
                    value = ev_yield_tag.find('value').text
                    ev_yield_object = EvYield(stat=stat, value=value)
                    ev_yield_object.save(using=self.db_alias)

                    ev_yields_list_element_object = EvYieldsListElement(list_id=ev_yields_list_id, sequence_number=ev_yields_sequence_number, element=ev_yield_object)
                    ev_yields_list_element_objects.append(ev_yields_list_element_object)
                    ev_yields_sequence_number += 1

                EvYieldsListElement.objects.using(self.db_alias).bulk_create(ev_yields_list_element_objects)

                pokemon_object = Pokemon(name=name_tag.text, pokedex_numbers=list_id, height=height_tag.text, weight=weight_tag.text, catch_rate=catch_rate_tag.text, growth_rate=growth_rate_tag.text, base_exp=base_exp_tag.text, ev_yields=ev_yields_list_id, stat_sets=stat_sets_list_id, type_sets=type_sets_list_id, ability_sets=ability_sets_list_id, evolution_sets=evolution_sets_list_id, egg_groups=egg_groups_tag.text)
                pokemon_objects.append(pokemon_object)
            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + pokemon_file)

        PokedexNumbersListElement.objects.using(self.db_alias).bulk_create(pokedex_numbers_list_element_objects)
        Pokemon.objects.using(self.db_alias).bulk_create(pokemon_objects)

    def import_moves(self):
        self.stdout.write('Importing Move data...')

        move_path = os.path.join(WESTWOOD_XML_PATH, 'moves')
        move_objects = []
        move_definitions_list_counter = 1
        games_list_counter = 1
        move_records_list_counter = 1
        context = {}

        for move_file in glob.glob(os.path.join(move_path, '*.xml')):
            try:
                move_tag = etree.parse(move_file)
                name_tag = move_tag.find('name')

                move_records_list_id = move_records_list_counter
                move_records_list_counter += 1
                move_records_sequence_number = 1
                move_records_list_element_objects = []
                for move_record_tag in move_tag.iter('move_record'):

                    context, games_list_id = self.get_or_create_games_list(context, move_record_tag.iter('game'))

                    move_definition_tag = move_record_tag.find('move_definition')
                    generation_tag = move_definition_tag.find('generation')
                    type_tag = move_definition_tag.find('type')
                    base_power_tag = move_definition_tag.find('base_power')
                    power_points_tag = move_definition_tag.find('power_points')
                    accuracy_tag = move_definition_tag.find('accuracy')
                    priority_tag = move_definition_tag.find('priority')
                    damage_category_tag = move_definition_tag.find('damage_category')
                    description_tag = move_definition_tag.find('description')
                    description_text = ''
                    if None != description_tag:
                        description_text = description_tag.text
                    move_definition_object = MoveDefinition(generation=generation_tag.text, type_1=type_tag.text, base_power=base_power_tag.text, power_points=power_points_tag.text, accuracy=accuracy_tag.text, priority=priority_tag.text, damage_category=damage_category_tag.text, description=description_text)
                    move_definition_object.save()

                    move_record_object = MoveRecord(games=games_list_id, move_definition=move_definition_object)
                    move_record_object.save(using=self.db_alias)

                    move_records_list_element_object = MoveRecordsListElement(list_id=move_records_list_id, sequence_number=move_records_sequence_number, element=move_record_object)
                    move_records_list_element_objects.append(move_records_list_element_object)
                    move_records_sequence_number += 1

                MoveRecordsListElement.objects.using(self.db_alias).bulk_create(move_records_list_element_objects)

                move_object = Move(name=name_tag.text, move_records=move_records_list_id)
                move_objects.append(move_object)
            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + move_file)

        Move.objects.using(self.db_alias).bulk_create(move_objects)

    def import_abilities(self):
        self.stdout.write('Importing Ability data...')

        ability_path = os.path.join(WESTWOOD_XML_PATH, 'abilities')
        ability_objects = []
        games_list_element_objects = []
        list_counter = 1
        game_ids = self.cache_game_ids()
        context = {}

        for ability_file in glob.glob(os.path.join(ability_path, '*.xml')):
            try:
                ability_tag = etree.parse(ability_file)
                name_tag = ability_tag.find('name')
                description_tag = ability_tag.find('description')

                context, list_id = self.get_or_create_games_list(context, ability_tag.iter('game'))

                ability_object = Ability(name=name_tag.text, description=description_tag.text, games=list_id)
                ability_objects.append(ability_object)
            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + ability_file)

        Ability.objects.using(self.db_alias).bulk_create(ability_objects)

    def import_misc(self):
        self.stdout.write('Importing Misc data...')
        misc_path = os.path.join(WESTWOOD_XML_PATH, 'misc')

        type_objects = []
        try:
            types_tag = etree.parse(os.path.join(misc_path, 'types.xml'))
            for type_tag in types_tag.iter('type'):
                type_objects.append(Type(value=type_tag.text))
        except etree.XMLSyntaxError:
            self.stdout.write('Error parsing XML file: types.xml')
        Type.objects.using(self.db_alias).bulk_create(type_objects)

        learn_method_objects = []
        try:
            learn_methods_tag = etree.parse(os.path.join(misc_path, 'learn_methods.xml'))
            for learn_method in learn_methods_tag.iter('learn_method'):
                learn_method_objects.append(LearnMethod(value=learn_method.text))
        except etree.XMLSyntaxError:
            self.stdout.write('Error parsing XML file: learn_methods.xml')
        LearnMethod.objects.using(self.db_alias).bulk_create(learn_method_objects)

    def import_learnsets(self):
        self.stdout.write('Importing Learnset data...')

        learnsets_path = os.path.join(WESTWOOD_XML_PATH, 'learnsets')
        learnset_moves_list_counter = 1
        games_list_counter = 1
        learnsets_list_counter = 1
        context = {}

        for learnset_file in glob.glob(os.path.join(learnsets_path, '*.xml')):
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
                        learnset_move_object, created = LearnsetMove.objects.using(self.db_alias).get_or_create(name=name_tag.text, level=level_tag.text)

                        learnset_moves_list_element_object = LearnsetMovesListElement(list_id=learnset_moves_list_id, sequence_number=sequence_number, element=learnset_move_object)
                        learnset_moves_list_element_objects.append(learnset_moves_list_element_object)
                        sequence_number += 1
                    LearnsetMovesListElement.objects.using(self.db_alias).bulk_create(learnset_moves_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, learnset_tag.iter('game'))

                    learnset_object = Learnset(games=games_list_id, learnset_moves=learnset_moves_list_id)
                    learnset_object.save(using=self.db_alias)

                    learnsets_list_element_object = LearnsetsListElement(list_id=learnsets_list_id, sequence_number=learnsets_sequence_number, element=learnset_object)
                    learnsets_list_element_objects.append(learnsets_list_element_object)
                    learnsets_sequence_number += 1

                LearnsetsListElement.objects.using(self.db_alias).bulk_create(learnsets_list_element_objects)

                pokemon_learnsets_object = PokemonLearnsets(name=pokemon_name, learnsets=learnsets_list_id)
                pokemon_learnsets_object.save(using=self.db_alias)

            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + learnset_file)

    def import_tmsets(self):
        self.stdout.write('Importing TmSet data...')

        tm_sets_path = os.path.join(WESTWOOD_XML_PATH, 'tm_sets')
        tmset_moves_list_counter = 1
        games_list_counter = 1
        tm_sets_list_counter = 1
        context = {}

        for tm_set_file in glob.glob(os.path.join(tm_sets_path, '*.xml')):
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
                        tmset_move_object, created = TmsetMove.objects.using(self.db_alias).get_or_create(name=tmset_move.text)

                        tmset_moves_list_element_object = TmsetMovesListElement(list_id=tmset_moves_list_id, sequence_number=sequence_number, element=tmset_move_object)
                        tmset_moves_list_element_objects.append(tmset_moves_list_element_object)
                        sequence_number += 1
                    TmsetMovesListElement.objects.using(self.db_alias).bulk_create(tmset_moves_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, tm_set_tag.iter('game'))

                    tmset_object = TmSet(games=games_list_id, tmset_moves=tmset_moves_list_id)
                    tmset_object.save(using=self.db_alias)

                    tm_sets_list_element_object = TmSetsListElement(list_id=tm_sets_list_id, sequence_number=tm_sets_sequence_number, element=tmset_object)
                    tm_sets_list_element_objects.append(tm_sets_list_element_object)
                    tm_sets_sequence_number += 1

                TmSetsListElement.objects.using(self.db_alias).bulk_create(tm_sets_list_element_objects)

                pokemon_tm_sets_object = PokemonTmSets(name=pokemon_name, tm_sets=tm_sets_list_id)
                pokemon_tm_sets_object.save(using=self.db_alias)

            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + tm_set_file)

    def import_items(self):
        self.stdout.write('Importing Item data...')

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
            self.stdout.write('Error parsing XML file: ' + item_path)

        Item.objects.using(self.db_alias).bulk_create(item_objects)

    def import_type_effectiveness(self):
        self.stdout.write('Importing Type Effectiveness data...')

        type_effectiveness_file = os.path.join(WESTWOOD_XML_PATH, 'misc', 'type_effectiveness.xml')
        effectiveness_sets_list_counter = 1
        effectiveness_records_list_counter = 1
        context = {}

        try:
            effectiveness_sets_tag = etree.parse(type_effectiveness_file)

            effectiveness_sets_list_id = effectiveness_sets_list_counter
            effectiveness_sets_list_counter += 1
            effectiveness_sets_sequence_number = 1
            effectiveness_sets_list_element_objects = []
            for effectiveness_set_tag in effectiveness_sets_tag.iter('effectiveness_set'):

                effectiveness_records_list_id = effectiveness_records_list_counter
                effectiveness_records_list_counter += 1
                sequence_number = 1
                effectiveness_records_list_element_objects = []
                for effectiveness_record in effectiveness_set_tag.iter('effectiveness_record'):
                    source_type_tag = effectiveness_record.find('source_type')
                    target_type_tag = effectiveness_record.find('target_type')
                    damage_factor_tag = effectiveness_record.find('damage_factor')
                    damage_factor_int = int(damage_factor_tag.text)
                    effectiveness_record_object, created = EffectivenessRecord.objects.using(self.db_alias).get_or_create(source_type=source_type_tag.text, target_type=target_type_tag.text, damage_factor=damage_factor_int)

                    effectiveness_records_list_element_object = EffectivenessRecordsListElement(list_id=effectiveness_records_list_id, sequence_number=sequence_number, element=effectiveness_record_object)
                    effectiveness_records_list_element_objects.append(effectiveness_records_list_element_object)
                    sequence_number += 1
                EffectivenessRecordsListElement.objects.using(self.db_alias).bulk_create(effectiveness_records_list_element_objects)

                context, games_list_id = self.get_or_create_games_list(context, effectiveness_set_tag.iter('game'))

                effectiveness_set_object = EffectivenessSet(games=games_list_id, effectiveness_records=effectiveness_records_list_id)
                effectiveness_set_object.save(using=self.db_alias)

                effectiveness_sets_list_element_object = EffectivenessSetsListElement(list_id=effectiveness_sets_list_id, sequence_number=effectiveness_sets_sequence_number, element=effectiveness_set_object)
                effectiveness_sets_list_element_objects.append(effectiveness_sets_list_element_object)
                effectiveness_sets_sequence_number += 1

            EffectivenessSetsListElement.objects.using(self.db_alias).bulk_create(effectiveness_sets_list_element_objects)

        except etree.XMLSyntaxError:
            self.stdout.write('Error parsing XML file: ' + type_effectiveness_file)

    def import_natures(self):
        self.stdout.write('Importing Nature data...')

        natures_file = os.path.join(WESTWOOD_XML_PATH, 'misc', 'natures.xml')
        nature_objects = []

        try:
            natures_tag = etree.parse(natures_file)

            for nature_tag in natures_tag.iter('nature'):
                name_tag = nature_tag.find('name')
                inc_stat_tag = nature_tag.find('increased_stat')
                dec_stat_tag = nature_tag.find('decreased_stat')

                nature_object = Nature(name=name_tag.text, increased_stat=inc_stat_tag.text, decreased_stat=dec_stat_tag.text)
                nature_objects.append(nature_object)

            Nature.objects.using(self.db_alias).bulk_create(nature_objects)
        except etree.XMLSyntaxError:
            self.stdout.write('Error parsing XML file: ' + nature_file)

    def import_forms(self):
        self.stdout.write('Importing PokemonForm data...')

        pokemon_form_path = os.path.join(WESTWOOD_XML_PATH, 'forms')
        pokemon_form_objects = []
        pokedex_numbers_list_element_objects = []
        stat_sets_list_counter = StatSetsListElement.objects.using(self.db_alias).order_by('-list_id')[0].list_id + 1
        type_sets_list_counter = TypeSetsListElement.objects.using(self.db_alias).order_by('-list_id')[0].list_id + 1
        ability_sets_list_counter = AbilitySetsListElement.objects.using(self.db_alias).order_by('-list_id')[0].list_id + 1
        ability_records_list_counter = AbilityRecordsListElement.objects.using(self.db_alias).order_by('-list_id')[0].list_id + 1
        ev_yields_list_counter = EvYieldsListElement.objects.using(self.db_alias).order_by('-list_id')[0].list_id + 1
        context = {}

        for pokemon_form_file in glob.glob(os.path.join(pokemon_form_path, '*.xml')):
            try:
                pokemon_form_tag = etree.parse(pokemon_form_file)

                name_tag = pokemon_form_tag.find('name')
                height_tag = pokemon_form_tag.find('height')
                weight_tag = pokemon_form_tag.find('weight')
                base_exp_tag = pokemon_form_tag.find('base_exp')

                stat_sets_list_id = stat_sets_list_counter
                stat_sets_list_counter += 1
                stat_sets_sequence_number = 1
                stat_sets_list_element_objects = []
                for stat_set_tag in pokemon_form_tag.iter('stat_set'):

                    context, games_list_id = self.get_or_create_games_list(context, stat_set_tag.iter('game'))

                    hp = int(stat_set_tag.find('hp').text)
                    attack = int(stat_set_tag.find('attack').text)
                    defense = int(stat_set_tag.find('defense').text)
                    special_attack = int(stat_set_tag.find('special_attack').text)
                    special_defense = int(stat_set_tag.find('special_defense').text)
                    speed = int(stat_set_tag.find('speed').text)
                    stat_set_object = StatSet(games=games_list_id, hp=hp, attack=attack, defense=defense, special_attack=special_attack, special_defense=special_defense, speed=speed)

                    stat_set_object.max_hp = calculate_hp(hp, ev=252.0)

                    stat_set_object.max_attack_hindered = calculate_stat(attack, ev=252.0, hindered=True)
                    stat_set_object.max_attack_neutral = calculate_stat(attack, ev=252.0)
                    stat_set_object.max_attack_beneficial = calculate_stat(attack, ev=252.0, beneficial=True)

                    stat_set_object.max_defense_hindered = calculate_stat(defense, ev=252.0, hindered=True)
                    stat_set_object.max_defense_neutral = calculate_stat(defense, ev=252.0)
                    stat_set_object.max_defense_beneficial = calculate_stat(defense, ev=252.0, beneficial=True)

                    stat_set_object.max_special_attack_hindered = calculate_stat(special_attack, ev=252.0, hindered=True)
                    stat_set_object.max_special_attack_neutral = calculate_stat(special_attack, ev=252.0)
                    stat_set_object.max_special_attack_beneficial = calculate_stat(special_attack, ev=252.0, beneficial=True)

                    stat_set_object.max_special_defense_hindered = calculate_stat(special_defense, ev=252.0, hindered=True)
                    stat_set_object.max_special_defense_neutral = calculate_stat(special_defense, ev=252.0)
                    stat_set_object.max_special_defense_beneficial = calculate_stat(special_defense, ev=252.0, beneficial=True)

                    stat_set_object.max_speed_hindered = calculate_stat(speed, ev=252.0, hindered=True)
                    stat_set_object.max_speed_neutral = calculate_stat(speed, ev=252.0)
                    stat_set_object.max_speed_beneficial = calculate_stat(speed, ev=252.0, beneficial=True)

                    stat_set_object.save(using=self.db_alias)

                    stat_sets_list_element_object = StatSetsListElement(list_id=stat_sets_list_id, sequence_number=stat_sets_sequence_number, element=stat_set_object)
                    stat_sets_list_element_objects.append(stat_sets_list_element_object)
                    stat_sets_sequence_number += 1

                StatSetsListElement.objects.using(self.db_alias).bulk_create(stat_sets_list_element_objects)

                type_sets_list_id = type_sets_list_counter
                type_sets_list_counter += 1
                type_sets_sequence_number = 1
                type_sets_list_element_objects = []
                for type_set_tag in pokemon_form_tag.iter('type_set'):

                    context, games_list_id = self.get_or_create_games_list(context, type_set_tag.iter('game'))

                    type1 = type_set_tag.find('type1').text
                    type2 = type_set_tag.find('type2')
                    if None != type2:
                        type2 = type2.text
                    else:
                        type2 = ''
                    type_set_object = TypeSet(games=games_list_id, type1=type1, type2=type2)
                    type_set_object.save(using=self.db_alias)

                    type_sets_list_element_object = TypeSetsListElement(list_id=type_sets_list_id, sequence_number=type_sets_sequence_number, element=type_set_object)
                    type_sets_list_element_objects.append(type_sets_list_element_object)
                    type_sets_sequence_number += 1

                TypeSetsListElement.objects.using(self.db_alias).bulk_create(type_sets_list_element_objects)

                ability_sets_list_id = ability_sets_list_counter
                ability_sets_list_counter += 1
                ability_sets_sequence_number = 1
                ability_sets_list_element_objects = []
                for ability_set_tag in pokemon_form_tag.iter('ability_set'):

                    ability_records_list_id = ability_records_list_counter
                    ability_records_list_counter += 1
                    sequence_number = 1
                    ability_records_list_element_objects = []
                    for ability_record in ability_set_tag.iter('ability_record'):
                        ability_name_tag = ability_record.find('name')
                        hidden_tag = ability_record.find('hidden')
                        ability_record_object, created = AbilityRecord.objects.using(self.db_alias).get_or_create(name=ability_name_tag.text, hidden=hidden_tag.text)

                        ability_records_list_element_object = AbilityRecordsListElement(list_id=ability_records_list_id, sequence_number=sequence_number, element=ability_record_object)
                        ability_records_list_element_objects.append(ability_records_list_element_object)
                        sequence_number += 1
                    AbilityRecordsListElement.objects.using(self.db_alias).bulk_create(ability_records_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, ability_set_tag.iter('game'))

                    ability_set_object = AbilitySet(games=games_list_id, ability_records=ability_records_list_id)
                    ability_set_object.save(using=self.db_alias)

                    ability_sets_list_element_object = AbilitySetsListElement(list_id=ability_sets_list_id, sequence_number=ability_sets_sequence_number, element=ability_set_object)
                    ability_sets_list_element_objects.append(ability_sets_list_element_object)
                    ability_sets_sequence_number += 1

                AbilitySetsListElement.objects.using(self.db_alias).bulk_create(ability_sets_list_element_objects)

                ev_yields_list_id = ev_yields_list_counter
                ev_yields_list_counter += 1
                ev_yields_sequence_number = 1
                ev_yields_list_element_objects = []
                for ev_yield_tag in pokemon_form_tag.iter('ev_yield'):

                    stat = ev_yield_tag.find('stat').text
                    value = ev_yield_tag.find('value').text
                    ev_yield_object = EvYield(stat=stat, value=value)
                    ev_yield_object.save(using=self.db_alias)

                    ev_yields_list_element_object = EvYieldsListElement(list_id=ev_yields_list_id, sequence_number=ev_yields_sequence_number, element=ev_yield_object)
                    ev_yields_list_element_objects.append(ev_yields_list_element_object)
                    ev_yields_sequence_number += 1

                EvYieldsListElement.objects.using(self.db_alias).bulk_create(ev_yields_list_element_objects)

                pokemon_form_object = PokemonForm(name=name_tag.text, height=height_tag.text, weight=weight_tag.text, base_exp=base_exp_tag.text, ev_yields=ev_yields_list_id, stat_sets=stat_sets_list_id, type_sets=type_sets_list_id, ability_sets=ability_sets_list_id)
                pokemon_form_objects.append(pokemon_form_object)
            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + pokemon_form_file)

        PokemonForm.objects.using(self.db_alias).bulk_create(pokemon_form_objects)

    def import_rom_hacks(self):
        self.stdout.write('Importing RomHack data...')

        rom_hacks_file = os.path.join(WESTWOOD_XML_PATH, 'misc', 'rom_hacks.xml')
        rom_hack_objects = []

        try:
            rom_hacks_tag = etree.parse(rom_hacks_file)

            for rom_hack_tag in rom_hacks_tag.iter('rom_hack'):
                title_tag = rom_hack_tag.find('title')
                base_game_tag = rom_hack_tag.find('base_game')
                author_tag = rom_hack_tag.find('author')
                description_tag = rom_hack_tag.find('description')

                rom_hack_object = RomHack(title=title_tag.text, base_game=base_game_tag.text, author=author_tag.text, description=description_tag.text)
                rom_hack_objects.append(rom_hack_object)

            RomHack.objects.using(self.db_alias).bulk_create(rom_hack_objects)
        except etree.XMLSyntaxError:
            self.stdout.write('Error parsing XML file: ' + rom_hack_file)

    def import_tutor_sets(self):
        self.stdout.write('Importing TutorSet data...')

        tutor_sets_path = os.path.join(WESTWOOD_XML_PATH, 'tutor_sets')
        tutor_set_moves_list_counter = 1
        games_list_counter = 1
        tutor_sets_list_counter = 1
        context = {}

        for tutor_set_file in glob.glob(os.path.join(tutor_sets_path, '*.xml')):
            try:
                pokemon_tutor_sets_tag = etree.parse(tutor_set_file)
                pokemon_name = pokemon_tutor_sets_tag.find('name').text
                
                tutor_sets_list_id = tutor_sets_list_counter
                tutor_sets_list_counter += 1
                tutor_sets_sequence_number = 1
                tutor_sets_list_element_objects = []
                for tutor_set_tag in pokemon_tutor_sets_tag.iter('tutor_set'):

                    tutor_set_moves_list_id = tutor_set_moves_list_counter
                    tutor_set_moves_list_counter += 1
                    sequence_number = 1
                    tutor_set_moves_list_element_objects = []
                    for tutor_set_move in tutor_set_tag.iter('tutor_set_move'):
                        tutor_set_move_object, created = TutorSetMove.objects.using(self.db_alias).get_or_create(name=tutor_set_move.text)

                        tutor_set_moves_list_element_object = TutorSetMovesListElement(list_id=tutor_set_moves_list_id, sequence_number=sequence_number, element=tutor_set_move_object)
                        tutor_set_moves_list_element_objects.append(tutor_set_moves_list_element_object)
                        sequence_number += 1
                    TutorSetMovesListElement.objects.using(self.db_alias).bulk_create(tutor_set_moves_list_element_objects)

                    context, games_list_id = self.get_or_create_games_list(context, tutor_set_tag.iter('game'))

                    tutor_set_object = TutorSet(games=games_list_id, tutor_set_moves=tutor_set_moves_list_id)
                    tutor_set_object.save(using=self.db_alias)

                    tutor_sets_list_element_object = TutorSetsListElement(list_id=tutor_sets_list_id, sequence_number=tutor_sets_sequence_number, element=tutor_set_object)
                    tutor_sets_list_element_objects.append(tutor_sets_list_element_object)
                    tutor_sets_sequence_number += 1

                TutorSetsListElement.objects.using(self.db_alias).bulk_create(tutor_sets_list_element_objects)

                pokemon_tutor_sets_object = PokemonTutorSets(name=pokemon_name, tutor_sets=tutor_sets_list_id)
                pokemon_tutor_sets_object.save(using=self.db_alias)

            except etree.XMLSyntaxError:
                self.stdout.write('Error parsing XML file: ' + tutor_set_file)

    def handle(self, *args, **options):
        self.db_alias = 'westwood'
        self.import_games()
        self.import_pokemon()
        self.import_moves()
        self.import_abilities()
        self.import_misc()
        self.import_learnsets()
        self.import_tmsets()
        self.import_items()
        self.import_type_effectiveness()
        self.import_natures()
        self.import_forms()
        self.import_rom_hacks()
        self.import_tutor_sets()
