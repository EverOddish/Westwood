import filecmp
import os
import tempfile
import sys

sys.path.append(os.getcwd())
from intermediate.tm_set import PokemonTmSet

def validate_pokemon_tm_set(pokemon_tm_set):
    assert len(pokemon_tm_set.tm_sets) >= 3, 'There should be at least 3 TM sets for main series games'
    tm_set = pokemon_tm_set.tm_sets[0]
    assert len(tm_set.games) == 3, 'There should be 3 games in the first TM set (Generation 1)'
    assert 'Pokemon Blue' in tm_set.games, 'Pokemon Blue should be in the list of games'
    assert len(tm_set.moves) >= 15, 'There should be at least 15 moves in the first TM set (Generation 1)'
    last_move = tm_set.moves[-1]
    assert 'Substitute' == last_move

def test_learnset():
    filename = os.path.join('..', 'xml', 'tm_sets', 'bulbasaur.xml')
    pokemon_tm_set = PokemonTmSet(filename)

    # Validate the intermediate representation derived from XML
    validate_pokemon_tm_set(pokemon_tm_set)

    # Validate dumping the intermediate representation back to XML
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_tm_set.dump(new_xml_file)
    assert filecmp.cmp(filename, new_xml_file.name, shallow=False), 'The dumped XML file should be identical to the original'

    # Validate re-importing the dumped XML
    new_pokemon_tm_set = PokemonTmSet(new_xml_file.name)
    validate_pokemon_tm_set(new_pokemon_tm_set)
    new_xml_file.close()

    # Validate adding a move
    move = 'Ice Beam'
    pokemon_tm_set.tm_sets[0].moves.insert(0, move)
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_tm_set.dump(new_xml_file)
    new_pokemon_tm_set = PokemonTmSet(new_xml_file.name)
    validate_pokemon_tm_set(new_pokemon_tm_set)
    new_xml_file.close()

    # Start with a fresh copy
    pokemon_tm_set = PokemonTmSet(filename)

    # Base game not found
    tm_set_copy = pokemon_tm_set.copy_tm_set('Pokemon Non-Existent')
    assert None == tm_set_copy, 'TM set not found should be None'

    # Copy and add an unmodified TM set
    old_tm_set_count = len(pokemon_tm_set.tm_sets)
    tm_set_copy = pokemon_tm_set.copy_tm_set('Pokemon Blue')
    assert None != tm_set_copy, 'TM set should not be None for existing TM set'
    tm_set_copy.games = ['Pokemon Sky Blue']
    temp_tm = tm_set_copy.moves[0]  # Switch the ordering of the first two TMs
    tm_set_copy.moves[0] = tm_set_copy.moves[1]
    tm_set_copy.moves[1] = temp_tm
    pokemon_tm_set.add_tm_set(tm_set_copy)
    new_tm_set_count = len(pokemon_tm_set.tm_sets)
    assert old_tm_set_count == new_tm_set_count, 'There should not be a separate entry for a duplicate TM set'
    assert 'Pokemon Sky Blue' in pokemon_tm_set.tm_sets[0].games

    # Copy and add a modified TM set
    old_tm_set_count = len(pokemon_tm_set.tm_sets)
    tm_set_copy = pokemon_tm_set.copy_tm_set('Pokemon Blue')
    assert None != tm_set_copy, 'TM set should not be None for existing TM set'
    tm_set_copy.games = ['Pokemon Sky Blue']
    new_move = 'Ice Beam'
    tm_set_copy.moves.insert(0, new_move)
    pokemon_tm_set.add_tm_set(tm_set_copy)
    new_tm_set_count = len(pokemon_tm_set.tm_sets)
    assert old_tm_set_count < new_tm_set_count, 'There should be a separate entry for a modified TM set'
    assert 'Pokemon Sky Blue' in pokemon_tm_set.tm_sets[-1].games
    assert new_move in pokemon_tm_set.tm_sets[-1].moves
