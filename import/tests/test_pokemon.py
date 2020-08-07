import filecmp
import os
import tempfile

from intermediate.pokemon import Pokemon

def validate_pokemon(pokemon):
    assert len(pokemon.stat_sets) >= 1, 'There should be at least 1 stat set for main series games'
    stat_set = pokemon.stat_sets[0]
    assert len(stat_set.games) >= 3, 'There should be 3 games in the first stat set (Generation 1)'
    assert 'Pokemon Blue' in stat_set.games, 'Pokemon Blue should be in the list of games'

    assert len(pokemon.type_sets) >= 1, 'There should be at least 1 type set for main series games'
    type_set = pokemon.type_sets[0]
    assert len(type_set.games) >= 3, 'There should be 3 games in the first type set (Generation 1)'
    assert 'Pokemon Blue' in type_set.games, 'Pokemon Blue should be in the list of games'

    assert len(pokemon.ability_sets) >= 1, 'There should be at least 1 ability set for main series games'
    ability_set = pokemon.ability_sets[0]
    assert len(ability_set.games) >= 3, 'There should be 3 games in the first ability set (Generation 1)'
    assert 'Pokemon Blue' in ability_set.games, 'Pokemon Blue should be in the list of games'

    assert len(pokemon.evolution_sets) >= 1, 'There should be at least 1 evolution set for main series games'
    evolution_set = pokemon.evolution_sets[0]
    assert len(evolution_set.games) >= 3, 'There should be 3 games in the first evolution set (Generation 1)'
    assert 'Pokemon Blue' in evolution_set.games, 'Pokemon Blue should be in the list of games'

def test_pokemon():
    filename = os.path.join('..', 'xml', 'pokemon', 'bulbasaur.xml')
    pokemon = Pokemon(filename)

    # Validate the intermediate representation derived from XML
    validate_pokemon(pokemon)

    # Validate dumping the intermediate representation back to XML
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    pokemon.dump(new_xml_file)
    assert filecmp.cmp(filename, new_xml_file.name, shallow=False), 'The dumped XML file should be identical to the original'

    # Validate re-importing the dumped XML
    new_pokemon = Pokemon(new_xml_file.name)
    validate_pokemon(new_pokemon)
    new_xml_file.close()

    # Base game not found
    set_copy = pokemon.copy_stat_set('Pokemon Non-Existent')
    assert None == set_copy, 'Stat set not found should be None'

    # Copy and add an unmodified stat set
    old_stat_set_count = len(pokemon.stat_sets)
    stat_set_copy = pokemon.copy_stat_set('Pokemon Blue')
    assert None != stat_set_copy, 'Stat set should not be None for existing stat set'
    stat_set_copy.games = ['Pokemon Sky Blue']
    pokemon.add_stat_set(stat_set_copy)
    new_stat_set_count = len(pokemon.stat_sets)
    assert old_stat_set_count == new_stat_set_count, 'There should not be a separate entry for a duplicate stat set'
    assert 'Pokemon Sky Blue' in pokemon.stat_sets[0].games

    # Copy and add a modified stat set
    old_stat_set_count = len(pokemon.stat_sets)
    stat_set_copy = pokemon.copy_stat_set('Pokemon Blue')
    assert None != stat_set_copy, 'Stat set should not be None for existing stat set'
    stat_set_copy.games = ['Pokemon Sky Blue']
    stat_set_copy.attack = '150'
    pokemon.add_stat_set(stat_set_copy)
    new_stat_set_count = len(pokemon.stat_sets)
    assert old_stat_set_count < new_stat_set_count, 'There should be a separate entry for a modified stat set'
    assert 'Pokemon Sky Blue' in pokemon.stat_sets[-1].games
    assert '150' == pokemon.stat_sets[-1].attack

    # Copy and add an unmodified type set
    old_type_set_count = len(pokemon.type_sets)
    type_set_copy = pokemon.copy_type_set('Pokemon Blue')
    assert None != type_set_copy, 'Type set should not be None for existing type set'
    type_set_copy.games = ['Pokemon Sky Blue']
    pokemon.add_type_set(type_set_copy)
    new_type_set_count = len(pokemon.type_sets)
    assert old_type_set_count == new_type_set_count, 'There should not be a separate entry for a duplicate type set'
    assert 'Pokemon Sky Blue' in pokemon.type_sets[0].games

    # Copy and add a modified type set
    old_type_set_count = len(pokemon.type_sets)
    type_set_copy = pokemon.copy_type_set('Pokemon Blue')
    assert None != type_set_copy, 'Type set should not be None for existing type set'
    type_set_copy.games = ['Pokemon Sky Blue']
    type_set_copy.type1 = 'Ice'
    pokemon.add_type_set(type_set_copy)
    new_type_set_count = len(pokemon.type_sets)
    assert old_type_set_count < new_type_set_count, 'There should be a separate entry for a modified type set'
    assert 'Pokemon Sky Blue' in pokemon.type_sets[-1].games
    assert 'Ice' == pokemon.type_sets[-1].type1

    # Copy and add an unmodified ability set
    old_ability_set_count = len(pokemon.ability_sets)
    ability_set_copy = pokemon.copy_ability_set('Pokemon Blue')
    assert None != ability_set_copy, 'Ability set should not be None for existing ability set'
    ability_set_copy.games = ['Pokemon Sky Blue']
    pokemon.add_ability_set(ability_set_copy)
    new_ability_set_count = len(pokemon.ability_sets)
    assert old_ability_set_count == new_ability_set_count, 'There should not be a separate entry for a duplicate ability set'
    assert 'Pokemon Sky Blue' in pokemon.ability_sets[0].games

    # Copy and add a modified ability set
    old_ability_set_count = len(pokemon.ability_sets)
    ability_set_copy = pokemon.copy_ability_set('Pokemon Blue')
    assert None != ability_set_copy, 'Ability set should not be None for existing ability set'
    ability_set_copy.games = ['Pokemon Sky Blue']
    ability_set_copy.ability_records[0].name = 'Intimidate'
    pokemon.add_ability_set(ability_set_copy)
    new_ability_set_count = len(pokemon.ability_sets)
    assert old_ability_set_count < new_ability_set_count, 'There should be a separate entry for a modified ability set'
    assert 'Pokemon Sky Blue' in pokemon.ability_sets[-1].games
    assert 'Intimidate' == pokemon.ability_sets[-1].ability_records[0].name

    # Copy and add an unmodified evolution set
    old_evolution_set_count = len(pokemon.evolution_sets)
    evolution_set_copy = pokemon.copy_evolution_set('Pokemon Blue')
    assert None != evolution_set_copy, 'Evolution set should not be None for existing evolution set'
    evolution_set_copy.games = ['Pokemon Sky Blue']
    pokemon.add_evolution_set(evolution_set_copy)
    new_evolution_set_count = len(pokemon.evolution_sets)
    assert old_evolution_set_count == new_evolution_set_count, 'There should not be a separate entry for a duplicate evolution set'
    assert 'Pokemon Sky Blue' in pokemon.evolution_sets[0].games

    # Copy and add a modified evolution set
    old_evolution_set_count = len(pokemon.evolution_sets)
    evolution_set_copy = pokemon.copy_evolution_set('Pokemon Blue')
    assert None != evolution_set_copy, 'Evolution set should not be None for existing evolution set'
    evolution_set_copy.games = ['Pokemon Sky Blue']
    evolution_set_copy.evolution_records[0].level = '99'
    pokemon.add_evolution_set(evolution_set_copy)
    new_evolution_set_count = len(pokemon.evolution_sets)
    assert old_evolution_set_count < new_evolution_set_count, 'There should be a separate entry for a modified ability set'
    assert 'Pokemon Sky Blue' in pokemon.evolution_sets[-1].games
    assert '99' == pokemon.evolution_sets[-1].evolution_records[0].level
