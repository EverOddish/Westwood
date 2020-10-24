import copy
import os

from lxml import etree
from .pokemon_object import PokemonObject

class Learnset():
    def __init__(self):
        self.games = []
        self.moves = []

class PokemonLearnset(PokemonObject):
    def __init__(self, xml_file):
        self.xml_file = xml_file
        super().__init__()

        self.learnsets = []

        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.parse(xml_file, parser)
        pokemon_learnsets_tag = root.getroot()

        self.pokemon = pokemon_learnsets_tag.findall('name')[0].text

        for learnset_tag in pokemon_learnsets_tag.iter('learnset'):
            learnset = Learnset()

            games_tag = learnset_tag.find('games')
            for game_tag in games_tag:
                learnset.games.append(game_tag.text)

            for learnset_move_tag in learnset_tag.iter('learnset_move'):
                move_name = learnset_move_tag.find('name').text
                level = learnset_move_tag.find('level').text
                pair = (level, move_name)
                learnset.moves.append(pair)

            self.learnsets.append(learnset)

    def copy_learnset(self, specified_game):
        for learnset in self.learnsets:
            for game in learnset.games:
                if specified_game == game:
                    return copy.deepcopy(learnset)
        return None

    def add_learnset(self, new_learnset):
        for learnset in self.learnsets:
            if learnset.moves == new_learnset.moves:
                # Just add the game entry to the existing duplicate learnset
                for new_game in new_learnset.games:
                    if new_game not in learnset.games:
                        learnset.games.append(new_game)
                return
        # No matching learnset was found, so add the new unique learnset
        self.learnsets.append(new_learnset)

    def dump(self, xml_file=None):
        pokemon_learnsets_tag = etree.Element('pokemon_learnsets')

        name_tag = self.make_tag_with_text('name', self.pokemon)
        pokemon_learnsets_tag.append(name_tag)

        learnsets_tag = etree.Element('learnsets')

        for learnset in self.learnsets:
            learnset_tag = etree.Element('learnset')

            games_tag = etree.Element('games')
            for game in learnset.games:
                game_tag = self.make_tag_with_text('game', game)
                games_tag.append(game_tag)
            learnset_tag.append(games_tag)

            learnset_moves_tag = etree.Element('learnset_moves')

            # Always ensure sorted order
            learnset.moves = sorted(learnset.moves, key=lambda x: int(x[0]))

            for move in learnset.moves:
                learnset_move_tag = etree.Element('learnset_move')

                name_tag = self.make_tag_with_text('name', move[1])
                learnset_move_tag.append(name_tag)

                level_tag = self.make_tag_with_text('level', move[0])
                learnset_move_tag.append(level_tag)

                learnset_moves_tag.append(learnset_move_tag)
            learnset_tag.append(learnset_moves_tag)
            learnsets_tag.append(learnset_tag)

        pokemon_learnsets_tag.append(learnsets_tag)

        self.dump_to_file(pokemon_learnsets_tag, xml_file)
