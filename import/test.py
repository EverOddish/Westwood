import filecmp
import os
import tempfile

from intermediate.learnset import PokemonLearnset

def validate_pokemon_learnset(pokemon_learnset):
    assert len(pokemon_learnset.learnsets) >= 3, 'There should be at least 3 learnsets for main series games'
    learnset = pokemon_learnset.learnsets[0]
    assert len(learnset.games) == 3, 'There should be 3 games in the first learnset (Generation 1)'
    assert 'Pokemon Blue' in learnset.games, 'Pokemon Blue should be in the list of games'
    assert len(learnset.moves) >= 9, 'There should be at least 9 moves in the first learnset (Generation 1)'
    last_move = learnset.moves[-1]
    assert '48' == last_move[0]
    assert 'Solar Beam' == last_move[1]
    # Validate sorted order
    last_move = None
    for move in learnset.moves:
        if None != last_move:
            assert int(move[0]) >= int(last_move[0]), 'Curent level should be >= last level'
        last_move = move

def test_learnset():
    filename = os.path.join('..', 'xml', 'learnsets', 'bulbasaur.xml')
    pokemon_learnset = PokemonLearnset(filename)

    # Validate the intermediate representation derived from XML
    validate_pokemon_learnset(pokemon_learnset)

    # Validate dumping the intermediate representation back to XML
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_learnset.dump(new_xml_file)
    assert filecmp.cmp(filename, new_xml_file.name, shallow=False), 'The dumped XML file should be identical to the original'

    # Validate re-importing the dumped XML
    new_pokemon_learnset = PokemonLearnset(new_xml_file.name)
    validate_pokemon_learnset(new_pokemon_learnset)
    new_xml_file.close()

    # Validate adding a move in non-sorted order
    move = ('47', 'Ice Beam')
    pokemon_learnset.learnsets[0].moves.insert(0, move)
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon_learnset.dump(new_xml_file)
    new_pokemon_learnset = PokemonLearnset(new_xml_file.name)
    validate_pokemon_learnset(new_pokemon_learnset)
    new_xml_file.close()
