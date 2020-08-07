import copy
import os

from lxml import etree
from .pokemon_object import PokemonObject

class TmSet():
    def __init__(self):
        self.games = []
        self.moves = []

class PokemonTmSet(PokemonObject):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        super().__init__()

        self.tm_sets = []

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.parse(xml_file, parser)
        pokemon_tm_sets_tag = root.getroot()

        self.pokemon = pokemon_tm_sets_tag.findall('name')[0].text

        for tm_set_tag in pokemon_tm_sets_tag.iter('tm_set'):
            tm_set = TmSet()

            games_tag = tm_set_tag.find('games')
            for game_tag in games_tag:
                tm_set.games.append(game_tag.text)

            for tmset_move_tag in tm_set_tag.iter('tmset_move'):
                move_name = tmset_move_tag.text
                tm_set.moves.append(move_name)

            self.tm_sets.append(tm_set)

    def copy_tm_set(self, specified_game):
        for tm_set in self.tm_sets:
            for game in tm_set.games:
                if specified_game == game:
                    return copy.deepcopy(tm_set)
        return None

    def add_tm_set(self, new_tm_set):
        for tm_set in self.tm_sets:
            if sorted(tm_set.moves) == sorted(new_tm_set.moves):
                # Just add the game entry to the existing duplicate learnset
                for new_game in new_tm_set.games:
                    tm_set.games.append(new_game)
                return
        # No matching learnset was found, so add the new unique learnset
        self.tm_sets.append(new_tm_set)

    def dump(self, xml_file=None):
        pokemon_tm_sets_tag = etree.Element('pokemon_tm_sets')

        name_tag = self.make_tag_with_text('name', self.pokemon)
        pokemon_tm_sets_tag.append(name_tag)

        tm_sets_tag = etree.Element('tm_sets')

        for tm_set in self.tm_sets:
            tm_set_tag = etree.Element('tm_set')

            games_tag = etree.Element('games')
            for game in tm_set.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            tm_set_tag.append(games_tag)

            tmset_moves_tag = etree.Element('tmset_moves')

            for move in tm_set.moves:
                tmset_move_tag = etree.Element('tmset_move')
                tmset_move_tag.text = move
                tmset_moves_tag.append(tmset_move_tag)
            tm_set_tag.append(tmset_moves_tag)
            tm_sets_tag.append(tm_set_tag)

        pokemon_tm_sets_tag.append(tm_sets_tag)

        self.dump_to_file(pokemon_tm_sets_tag, xml_file)
