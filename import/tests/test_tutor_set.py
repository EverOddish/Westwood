import filecmp
import os
import tempfile
import sys

sys.path.append(os.getcwd())
from intermediate.tutor_set import PokemonTutorSet

def validate_pokemon_tutor_set(pokemon_tutor_set):
    assert len(pokemon_tutor_set.tutor_sets) >= 3, 'There should be at least 3 tutor sets for main series games'
    tutor_set = pokemon_tutor_set.tutor_sets[0]
    assert len(tutor_set.games) == 1, 'There should be 1 games in the first tutor set (Generation 3)'
    assert 'Pokemon Emerald' in tutor_set.games, 'Pokemon Emerald should be in the list of games'
    assert len(tutor_set.moves) >= 12, 'There should be at least 15 moves in the first tutor set (Generation 3)'
    last_move = tutor_set.moves[-1]
    assert 'Sleep Talk' == last_move

def test_learnset():
    filename = os.path.join('..', 'xml', 'Tutor_sets', 'bulbasaur.xml')
    pokemon_tutor_set = PokemonTutorSet(filename)

    # Validate the intermediate representation derived from XML
    validate_pokemon_tutor_set(pokemon_tutor_set)

    # Validate dumping the intermediate representation back to XML
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_tutor_set.dump(new_xml_file)
    assert filecmp.cmp(filename, new_xml_file.name, shallow=False), 'The dumped XML file should be identical to the original'

    # Validate re-importing the dumped XML
    new_pokemon_tutor_set = PokemonTutorSet(new_xml_file.name)
    validate_pokemon_tutor_set(new_pokemon_tutor_set)
    new_xml_file.close()

    # Validate adding a move
    move = 'Ice Beam'
    pokemon_tutor_set.tutor_sets[0].moves.insert(0, move)
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_tutor_set.dump(new_xml_file)
    new_pokemon_tutor_set = PokemonTutorSet(new_xml_file.name)
    validate_pokemon_tutor_set(new_pokemon_tutor_set)
    new_xml_file.close()

    # Start with a fresh copy
    pokemon_tutor_set = PokemonTutorSet(filename)

    # Base game not found
    tutor_set_copy = pokemon_tutor_set.copy_tutor_set('Pokemon Non-Existent')
    assert None == tutor_set_copy, 'Tutor set not found should be None'

    # Copy and add an unmodified tutor set
    old_tutor_set_count = len(pokemon_tutor_set.tutor_sets)
    tutor_set_copy = pokemon_tutor_set.copy_tutor_set('Pokemon Emerald')
    assert None != tutor_set_copy, 'Tutor set should not be None for existing tutor set'
    tutor_set_copy.games = ['Pokemon Sky Blue']
    temp_tm = tutor_set_copy.moves[0]  # Switch the ordering of the first two TMs
    tutor_set_copy.moves[0] = tutor_set_copy.moves[1]
    tutor_set_copy.moves[1] = temp_tm
    pokemon_tutor_set.add_tutor_set(tutor_set_copy)
    new_tutor_set_count = len(pokemon_tutor_set.tutor_sets)
    assert old_tutor_set_count == new_tutor_set_count, 'There should not be a separate entry for a duplicate tutor set'
    assert 'Pokemon Sky Blue' in pokemon_tutor_set.tutor_sets[0].games

    # Copy and add a modified tutor set
    old_tutor_set_count = len(pokemon_tutor_set.tutor_sets)
    tutor_set_copy = pokemon_tutor_set.copy_tutor_set('Pokemon Emerald')
    assert None != tutor_set_copy, 'Tutor set should not be None for existing tutor set'
    tutor_set_copy.games = ['Pokemon Sky Blue']
    new_move = 'Ice Beam'
    tutor_set_copy.moves.insert(0, new_move)
    pokemon_tutor_set.add_tutor_set(tutor_set_copy)
    new_tutor_set_count = len(pokemon_tutor_set.tutor_sets)
    assert old_tutor_set_count < new_tutor_set_count, 'There should be a separate entry for a modified tutor set'
    assert 'Pokemon Sky Blue' in pokemon_tutor_set.tutor_sets[-1].games
    assert new_move in pokemon_tutor_set.tutor_sets[-1].moves
