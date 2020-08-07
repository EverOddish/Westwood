import copy
import os

from lxml import etree
from .pokemon_object import PokemonObject

class StatSet():
    def __init__(self):
        self.games = []
        self.hp = ''
        self.attack = ''
        self.defense = ''
        self.special_attack = ''
        self.special_defense = ''
        self.speed = ''

    def __eq__(self, other):
        if None == other:
            return False
        return self.hp == other.hp and \
               self.attack == other.attack and \
               self.defense == other.defense and \
               self.special_attack == other.special_attack and \
               self.special_defense == other.special_defense and \
               self.speed == other.speed

class TypeSet():
    def __init__(self):
        self.games = []
        self.type1 = ''
        self.type2 = None

    def __eq__(self, other):
        if None == other:
            return False
        return self.type1 == other.type1 and \
               self.type2 == other.type2

class AbilitySet():
    def __init__(self):
        self.games = []
        self.ability_records = []

    def __eq__(self, other):
        if None == other:
            return False
        return self.ability_records == other.ability_records

class AbilityRecord():
    def __init__(self):
        self.name = ''
        self.hidden = ''

    def __eq__(self, other):
        if None == other:
            return False
        return self.name == other.name and \
               self.hidden == other.hidden

class EvolutionSet():
    def __init__(self):
        self.games = []
        self.evolution_records = []

    def __eq__(self, other):
        if None == other:
            return False
        return self.evolution_records == other.evolution_records

class EvolutionRecord():
    def __init__(self):
        self.evolves_to = ''
        self.level = ''
        self.method = ''

    def __eq__(self, other):
        if None == other:
            return False
        return self.evolves_to == other.evolves_to and \
               self.level == other.level and \
               self.method == other.method

class Pokemon(PokemonObject):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        super().__init__()

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.parse(xml_file, parser)
        pokemon_tag = root.getroot()

        self.name = pokemon_tag.findall('name')[0].text

        self.pokedex_numbers = []
        for pokedex_number_tag in pokemon_tag.iter('pokedex_number'):
            name_tag = pokedex_number_tag.find('name')
            number_tag = pokedex_number_tag.find('number')
            pair = (name_tag.text, number_tag.text)
            self.pokedex_numbers.append(pair)
            
        tag = pokemon_tag.find('height')
        self.height = tag.text

        tag = pokemon_tag.find('weight')
        self.weight = tag.text

        tag = pokemon_tag.find('catch_rate')
        self.catch_rate = tag.text

        tag = pokemon_tag.find('growth_rate')
        self.growth_rate = tag.text

        tag = pokemon_tag.find('base_exp')
        self.base_exp = tag.text

        tag = pokemon_tag.find('egg_groups')
        self.egg_groups = tag.text

        self.ev_yields = []
        for ev_yield_tag in pokemon_tag.iter('ev_yield'):
            stat_tag = ev_yield_tag.find('stat')
            value_tag = ev_yield_tag.find('value')
            pair = (stat_tag.text, value_tag.text)
            self.ev_yields.append(pair)

        self.stat_sets = []
        for stat_set_tag in pokemon_tag.iter('stat_set'):
            stat_set = StatSet()
            games_tag = stat_set_tag.find('games')
            for game_tag in games_tag:
                stat_set.games.append(game_tag.text)

            stat_set.hp = stat_set_tag.find('hp').text
            stat_set.attack = stat_set_tag.find('attack').text
            stat_set.defense = stat_set_tag.find('defense').text
            stat_set.special_attack = stat_set_tag.find('special_attack').text
            stat_set.special_defense = stat_set_tag.find('special_defense').text
            stat_set.speed = stat_set_tag.find('speed').text

            self.stat_sets.append(stat_set)

        self.type_sets = []
        for type_set_tag in pokemon_tag.iter('type_set'):
            type_set = TypeSet()
            games_tag = type_set_tag.find('games')
            for game_tag in games_tag:
                type_set.games.append(game_tag.text)

            type_set.type1 = type_set_tag.find('type1').text
            type_set.type2 = None
            type2_tag = type_set_tag.find('type2')
            if None != type2_tag:
                type_set.type2 = type2_tag.text

            self.type_sets.append(type_set)

        self.ability_sets = []
        for ability_set_tag in pokemon_tag.iter('ability_set'):
            ability_set = AbilitySet()
            games_tag = ability_set_tag.find('games')
            for game_tag in games_tag:
                ability_set.games.append(game_tag.text)

            for ability_record_tag in ability_set_tag.iter('ability_record'):
                ability_record = AbilityRecord()
                name_tag = ability_record_tag.find('name')
                hidden_tag = ability_record_tag.find('hidden')
                ability_record.name = name_tag.text
                ability_record.hidden = hidden_tag.text
                ability_set.ability_records.append(ability_record)

            self.ability_sets.append(ability_set)

        self.evolution_sets = []
        for evolution_set_tag in pokemon_tag.iter('evolution_set'):
            evolution_set = EvolutionSet()
            games_tag = evolution_set_tag.find('games')
            for game_tag in games_tag:
                evolution_set.games.append(game_tag.text)

            for evolution_record_tag in evolution_set_tag.iter('evolution_record'):
                evolution_record = EvolutionRecord()
                evolves_to_tag = evolution_record_tag.find('evolves_to')
                evolution_record.evolves_to = evolves_to_tag.text
                level_tag = evolution_record_tag.find('level')
                if None != level_tag:
                    evolution_record.level = level_tag.text
                method_tag = evolution_record_tag.find('method')
                if None != method_tag:
                    evolution_record.method = method_tag.text
                evolution_set.evolution_records.append(evolution_record)

            self.evolution_sets.append(evolution_set)

    def copy_stat_set(self, specified_game):
        for stat_set in self.stat_sets:
            for game in stat_set.games:
                if specified_game == game:
                    return copy.deepcopy(stat_set)
        return None

    def copy_type_set(self, specified_game):
        for type_set in self.type_sets:
            for game in type_set.games:
                if specified_game == game:
                    return copy.deepcopy(type_set)
        return None

    def copy_ability_set(self, specified_game):
        for ability_set in self.ability_sets:
            for game in ability_set.games:
                if specified_game == game:
                    return copy.deepcopy(ability_set)
        return None

    def copy_evolution_set(self, specified_game):
        for evolution_set in self.evolution_sets:
            for game in evolution_set.games:
                if specified_game == game:
                    return copy.deepcopy(evolution_set)
        return None

    # Internal helper
    def add_set(self, new_set, sets):
        for set_object in sets:
            if set_object == new_set:
                # Just add the game entry to the existing duplicate set
                for new_game in new_set.games:
                    set_object.games.append(new_game)
                return
        # No matching set was found, so add the new unique set
        sets.append(new_set)

    def add_stat_set(self, new_stat_set):
        self.add_set(new_stat_set, self.stat_sets)

    def add_type_set(self, new_type_set):
        self.add_set(new_type_set, self.type_sets)

    def add_ability_set(self, new_ability_set):
        self.add_set(new_ability_set, self.ability_sets)

    def add_evolution_set(self, new_evolution_set):
        self.add_set(new_evolution_set, self.evolution_sets)

    def dump(self, xml_file=None):
        pokemon_tag = etree.Element('pokemon')

        name_tag = self.make_tag_with_text('name', self.name)
        pokemon_tag.append(name_tag)

        pokedex_numbers_tag = etree.Element('pokedex_numbers')

        for pokedex_number in self.pokedex_numbers:
            pokedex_number_tag = etree.Element('pokedex_number')
            name_tag = etree.Element('name')
            name_tag.text = pokedex_number[0]
            number_tag = etree.Element('number')
            number_tag.text = pokedex_number[1]
            pokedex_number_tag.append(name_tag)
            pokedex_number_tag.append(number_tag)
            pokedex_numbers_tag.append(pokedex_number_tag)
        pokemon_tag.append(pokedex_numbers_tag)

        tag = self.make_tag_with_text('height', self.height)
        pokemon_tag.append(tag)

        tag = self.make_tag_with_text('weight', self.weight)
        pokemon_tag.append(tag)

        tag = self.make_tag_with_text('catch_rate', self.catch_rate)
        pokemon_tag.append(tag)

        tag = self.make_tag_with_text('growth_rate', self.growth_rate)
        pokemon_tag.append(tag)

        tag = self.make_tag_with_text('base_exp', self.base_exp)
        pokemon_tag.append(tag)

        ev_yields_tag = etree.Element('ev_yields')
        for ev_yield in self.ev_yields:
            ev_yield_tag = etree.Element('ev_yield')
            stat_tag = etree.Element('stat')
            stat_tag.text = ev_yield[0]
            value_tag = etree.Element('value')
            value_tag.text = ev_yield[1]
            ev_yield_tag.append(stat_tag)
            ev_yield_tag.append(value_tag)
            ev_yields_tag.append(ev_yield_tag)
        pokemon_tag.append(ev_yields_tag)

        stat_sets_tag = etree.Element('stat_sets')
        for stat_set in self.stat_sets:
            stat_set_tag = etree.Element('stat_set')
            games_tag = etree.Element('games')
            for game in stat_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            stat_set_tag.append(games_tag)

            tag = self.make_tag_with_text('hp', stat_set.hp)
            stat_set_tag.append(tag)
            tag = self.make_tag_with_text('attack', stat_set.attack)
            stat_set_tag.append(tag)
            tag = self.make_tag_with_text('defense', stat_set.defense)
            stat_set_tag.append(tag)
            tag = self.make_tag_with_text('special_attack', stat_set.special_attack)
            stat_set_tag.append(tag)
            tag = self.make_tag_with_text('special_defense', stat_set.special_defense)
            stat_set_tag.append(tag)
            tag = self.make_tag_with_text('speed', stat_set.speed)
            stat_set_tag.append(tag)

            stat_sets_tag.append(stat_set_tag)
        pokemon_tag.append(stat_sets_tag)

        type_sets_tag = etree.Element('type_sets')
        for type_set in self.type_sets:
            type_set_tag = etree.Element('type_set')
            games_tag = etree.Element('games')
            for game in type_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            type_set_tag.append(games_tag)

            tag = self.make_tag_with_text('type1', type_set.type1)
            type_set_tag.append(tag)

            if None != type_set.type2:
                tag = self.make_tag_with_text('type2', type_set.type2)
                type_set_tag.append(tag)

            type_sets_tag.append(type_set_tag)
        pokemon_tag.append(type_sets_tag)

        ability_sets_tag = etree.Element('ability_sets')
        for ability_set in self.ability_sets:
            ability_set_tag = etree.Element('ability_set')
            games_tag = etree.Element('games')
            for game in ability_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            ability_set_tag.append(games_tag)

            ability_records_tag = etree.Element('ability_records')
            for ability_record in ability_set.ability_records:
                ability_record_tag = etree.Element('ability_record')
                name_tag = etree.Element('name')
                name_tag.text = ability_record.name
                hidden_tag = etree.Element('hidden')
                hidden_tag.text = ability_record.hidden
                ability_record_tag.append(name_tag)
                ability_record_tag.append(hidden_tag)
                ability_records_tag.append(ability_record_tag)
            ability_set_tag.append(ability_records_tag)

            ability_sets_tag.append(ability_set_tag)
        pokemon_tag.append(ability_sets_tag)

        evolution_sets_tag = etree.Element('evolution_sets')
        for evolution_set in self.evolution_sets:
            evolution_set_tag = etree.Element('evolution_set')
            games_tag = etree.Element('games')
            for game in evolution_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            evolution_set_tag.append(games_tag)

            evolution_records_tag = etree.Element('evolution_records')
            for evolution_record in evolution_set.evolution_records:
                evolution_record_tag = etree.Element('evolution_record')
                evolves_to_tag = etree.Element('evolves_to')
                evolves_to_tag.text = evolution_record.evolves_to
                evolution_record_tag.append(evolves_to_tag)
                if None != evolution_record.level and len(evolution_record.level) > 0:
                    level_tag = etree.Element('level')
                    level_tag.text = evolution_record.level
                    evolution_record_tag.append(level_tag)
                if None != evolution_record.method and len(evolution_record.method) > 0:
                    method_tag = etree.Element('method')
                    method_tag.text = evolution_record.method
                    evolution_record_tag.append(method_tag)
                evolution_records_tag.append(evolution_record_tag)
            evolution_set_tag.append(evolution_records_tag)

            evolution_sets_tag.append(evolution_set_tag)
        pokemon_tag.append(evolution_sets_tag)

        tag = self.make_tag_with_text('egg_groups', self.egg_groups)
        pokemon_tag.append(tag)

        self.dump_to_file(pokemon_tag, xml_file)
