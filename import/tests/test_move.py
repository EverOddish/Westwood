import filecmp
import os
import tempfile

from intermediate.move import Move

def validate_move_record(move_record):
    assert len(move_record.games) >= 11, 'There should be at least 11 games for Absorb in the first record'
    assert 'Pokemon Blue' in move_record.games, 'Pokemon Blue should be in the list of games'
    assert '1' == move_record.generation, 'Generation 1'
    assert 'Grass' == move_record.move_type, 'Grass type'
    assert '20' == move_record.base_power, '20 base power'
    assert '20' == move_record.power_points, '20 PP'
    assert '100' == move_record.accuracy, '100% accuracy'
    assert '0' == move_record.priority, 'No priority'
    assert 'Special' == move_record.damage_category, 'Special move'
    assert len(move_record.effect) > 0, 'Non-empty effect'
    assert len(move_record.description) > 0, 'Non-empty description'

def test_move():
    filename = os.path.join('..', 'xml', 'moves', 'absorb.xml')
    move = Move(filename)

    # Validate the intermediate representation derived from XML
    validate_move_record(move.move_records[0])

    # Validate dumping the intermediate representation back to XML
    new_xml_file = tempfile.NamedTemporaryFile(mode='w')
    move.dump(new_xml_file)
    assert filecmp.cmp(filename, new_xml_file.name, shallow=False), 'The dumped XML file should be identical to the original'

    # Validate re-importing the dumped XML
    new_move = Move(new_xml_file.name)
    validate_move_record(move.move_records[0])
    new_xml_file.close()

    # Base game not found
    move_record_copy = move.copy_move_record('Pokemon Non-Existent')
    assert None == move_record_copy, 'MoveRecord not found should be None'

    # Copy and add an unmodified move record
    old_move_record_count = len(move.move_records)
    move_record_copy = move.copy_move_record('Pokemon Blue')
    assert None != move_record_copy, 'MoveRecord should not be None for existing move record'
    move_record_copy.games = ['Pokemon Sky Blue']
    move.add_move_record(move_record_copy)
    new_move_record_count = len(move.move_records)
    assert old_move_record_count == new_move_record_count, 'There should not be a separate entry for a duplicate move record'
    assert 'Pokemon Sky Blue' in move.move_records[0].games

    # Copy and add a modified move record
    old_move_record_count = len(move.move_records)
    move_record_copy = move.copy_move_record('Pokemon Blue')
    assert None != move_record_copy, 'MoveRecord should not be None for existing move record'
    move_record_copy.games = ['Pokemon Sky Blue']
    move_record_copy.base_power = '120'
    move.add_move_record(move_record_copy)
    new_move_record_count = len(move.move_records)
    assert old_move_record_count < new_move_record_count, 'There should be a separate entry for a modified move record'
    assert 'Pokemon Sky Blue' in move.move_records[-1].games
    assert '120' == move.move_records[-1].base_power
