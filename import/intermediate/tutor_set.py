import copy
import os

from lxml import etree
from .pokemon_object import PokemonObject

class TutorSet():
    def __init__(self):
        self.games = []
        self.moves = []

class PokemonTutorSet(PokemonObject):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        super().__init__()

        self.tutor_sets = []

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.parse(xml_file, parser)
        pokemon_tutor_sets_tag = root.getroot()

        self.pokemon = pokemon_tutor_sets_tag.findall('name')[0].text

        for tutor_set_tag in pokemon_tutor_sets_tag.iter('tutor_set'):
            tutor_set = TutorSet()

            games_tag = tutor_set_tag.find('games')
            for game_tag in games_tag:
                tutor_set.games.append(game_tag.text)

            for tutor_set_move_tag in tutor_set_tag.iter('tutor_set_move'):
                move_name = tutor_set_move_tag.text
                tutor_set.moves.append(move_name)

            self.tutor_sets.append(tutor_set)

    def copy_tutor_set(self, specified_game):
        for tutor_set in self.tutor_sets:
            for game in tutor_set.games:
                if specified_game == game:
                    return copy.deepcopy(tutor_set)
        return None

    def add_tutor_set(self, new_tutor_set):
        for tutor_set in self.tutor_sets:
            if sorted(tutor_set.moves) == sorted(new_tutor_set.moves):
                # Just add the game entry to the existing duplicate learnset
                for new_game in new_tutor_set.games:
                    if new_game not in tutor_set.games:
                        tutor_set.games.append(new_game)
                return
        # No matching learnset was found, so add the new unique learnset
        self.tutor_sets.append(new_tutor_set)

    def dump(self, xml_file=None):
        pokemon_tutor_sets_tag = etree.Element('pokemon_tutor_sets')

        name_tag = self.make_tag_with_text('name', self.pokemon)
        pokemon_tutor_sets_tag.append(name_tag)

        tutor_sets_tag = etree.Element('tutor_sets')

        for tutor_set in self.tutor_sets:
            tutor_set_tag = etree.Element('tutor_set')

            games_tag = etree.Element('games')
            for game in tutor_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            tutor_set_tag.append(games_tag)

            tutor_set_moves_tag = etree.Element('tutor_set_moves')

            for move in tutor_set.moves:
                tutor_set_move_tag = etree.Element('tutor_set_move')
                tutor_set_move_tag.text = move
                tutor_set_moves_tag.append(tutor_set_move_tag)
            tutor_set_tag.append(tutor_set_moves_tag)
            tutor_sets_tag.append(tutor_set_tag)

        pokemon_tutor_sets_tag.append(tutor_sets_tag)

        self.dump_to_file(pokemon_tutor_sets_tag, xml_file)
