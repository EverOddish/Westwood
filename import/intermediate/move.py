import copy
import os

from lxml import etree
from .pokemon_object import PokemonObject

class MoveRecord():
    def __init__(self):
        self.games = []
        self.generation = ''
        self.move_type = ''
        self.base_power = ''
        self.power_points = ''
        self.accuracy = ''
        self.priority = ''
        self.damage_category = ''
        self.effect = None
        self.effect_chance = None
        self.description = ''

    def __eq__(self, other):
        if None == other:
            return False
        return self.generation == other.generation and \
               self.move_type == other.move_type and \
               self.base_power == other.base_power and \
               self.power_points == other.power_points and \
               self.accuracy == other.accuracy and \
               self.priority == other.priority and \
               self.damage_category == other.damage_category and \
               self.effect == other.effect and \
               self.description == other.description

class TmRecord():
    def __init__(self):
        self.games = []
        self.number = ''
        self.location = ''
        self.cost = None

class Move(PokemonObject):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        super().__init__()

        self.move_records = []
        self.tm_records = []

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.parse(xml_file, parser)
        move_tag = root.getroot()

        self.move_name = move_tag.findall('name')[0].text

        for move_record_tag in move_tag.iter('move_record'):
            move_record = MoveRecord()

            games_tag = move_record_tag.find('games')
            for game_tag in games_tag:
                move_record.games.append(game_tag.text)

            move_definition_tag = move_record_tag.find('move_definition')
            move_record.generation = move_definition_tag.find('generation').text
            move_record.move_type = move_definition_tag.find('type').text
            move_record.base_power = move_definition_tag.find('base_power').text
            move_record.power_points = move_definition_tag.find('power_points').text
            move_record.accuracy = move_definition_tag.find('accuracy').text
            move_record.priority = move_definition_tag.find('priority').text
            move_record.damage_category = move_definition_tag.find('damage_category').text
            effect_tag = move_definition_tag.find('effect')
            if None != effect_tag:
                move_record.effect = effect_tag.text
            effect_chance_tag = move_definition_tag.find('effect_chance')
            if None != effect_chance_tag:
                move_record.effect_chance = effect_chance_tag.text
            move_record.description = move_definition_tag.find('description').text

            self.move_records.append(move_record)

        for tm_record_tag in move_tag.iter('tm_record'):
            tm_record = TmRecord()

            games_tag = tm_record_tag.find('games')
            for game_tag in games_tag:
                tm_record.games.append(game_tag.text)

            tm_definition_tag = tm_record_tag.find('tm_definition')
            tm_record.number = tm_definition_tag.find('number').text
            tm_record.location = tm_definition_tag.find('location').text

            cost_tag = tm_definition_tag.find('cost')
            if None != cost_tag:
                tm_record.cost = cost_tag.text

            self.tm_records.append(tm_record)

    def copy_move_record(self, specified_game):
        for move_record in self.move_records:
            for game in move_record.games:
                if specified_game == game:
                    return copy.deepcopy(move_record)
        return None

    def add_move_record(self, new_move_record):
        for move_record in self.move_records:
            if move_record == new_move_record:
                # Just add the game entry to the existing duplicate learnset
                for new_game in new_move_record.games:
                    move_record.games.append(new_game)
                return
        # No matching learnset was found, so add the new unique learnset
        self.move_records.append(new_move_record)

    def dump(self, xml_file=None):
        move_tag = etree.Element('move')

        name_tag = self.make_tag_with_text('name', self.move_name)
        move_tag.append(name_tag)

        move_records_tag = etree.Element('move_records')

        for move_record in self.move_records:
            move_record_tag = etree.Element('move_record')

            games_tag = etree.Element('games')
            for game in move_record.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            move_record_tag.append(games_tag)

            move_definition_tag = etree.Element('move_definition')

            tag = self.make_tag_with_text('generation', move_record.generation)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('type', move_record.move_type)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('base_power', move_record.base_power)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('power_points', move_record.power_points)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('accuracy', move_record.accuracy)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('priority', move_record.priority)
            move_definition_tag.append(tag)
            tag = self.make_tag_with_text('damage_category', move_record.damage_category)
            move_definition_tag.append(tag)
            if None != move_record.effect:
                tag = self.make_tag_with_text('effect', move_record.effect)
                move_definition_tag.append(tag)
            if None != move_record.effect_chance:
                tag = self.make_tag_with_text('effect_chance', move_record.effect_chance)
                move_definition_tag.append(tag)
            tag = self.make_tag_with_text('description', move_record.description)
            move_definition_tag.append(tag)

            move_record_tag.append(move_definition_tag)
            move_records_tag.append(move_record_tag)

        move_tag.append(move_records_tag)

        if len(self.tm_records) > 0:
            tm_records_tag = etree.Element('tm_records')

            for tm_record in self.tm_records:
                tm_record_tag = etree.Element('tm_record')

                games_tag = etree.Element('games')
                for game in tm_record.games:
                    game_tag = self.make_tag_with_text('game', game)
                    games_tag.append(game_tag)
                tm_record_tag.append(games_tag)

                tm_definition_tag = etree.Element('tm_definition')

                tag = self.make_tag_with_text('number', tm_record.number)
                tm_definition_tag.append(tag)

                tag = self.make_tag_with_text('location', tm_record.location)
                tm_definition_tag.append(tag)

                if None != tm_record.cost:
                    tag = self.make_tag_with_text('cost', tm_record.cost)
                    tm_definition_tag.append(tag)

                tm_record_tag.append(tm_definition_tag)
                tm_records_tag.append(tm_record_tag)

            move_tag.append(tm_records_tag)

        self.dump_to_file(move_tag, xml_file)
