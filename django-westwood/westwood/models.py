from django.db import models

class Type(models.Model):
    value = models.CharField(max_length=50)    # Enumeration

class LearnMethod(models.Model):
    value = models.CharField(max_length=50)    # Enumeration

class Game(models.Model):
    name = models.CharField(max_length=500)
    generation = models.IntegerField(default=0)
    release_date = models.DateTimeField()
    system = models.CharField(max_length=500)
    region = models.CharField(max_length=500)
    sequence = models.IntegerField(default=0)

class TypesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Type, on_delete=models.CASCADE)

class PokedexNumber(models.Model):
    name = models.CharField(max_length=500)
    number = models.IntegerField(default=0)

class PokedexNumbersListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(PokedexNumber, on_delete=models.CASCADE)

class GamesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Game, on_delete=models.CASCADE)

class StatSet(models.Model):
    games = models.IntegerField()    # Games list_id
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)

class StatSetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(StatSet, on_delete=models.CASCADE)

class TypeSet(models.Model):
    games = models.IntegerField()    # Games list_id
    type1 = models.CharField(max_length=500)
    type2 = models.CharField(max_length=500, null=True)

class TypeSetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(TypeSet, on_delete=models.CASCADE)

class AbilityRecord(models.Model):
    name = models.CharField(max_length=500)
    hidden = models.CharField(max_length=500)

class AbilityRecordsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(AbilityRecord, on_delete=models.CASCADE)

class AbilitySet(models.Model):
    games = models.IntegerField()    # Games list_id
    ability_records = models.IntegerField()    # AbilityRecords list_id

class AbilitySetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(AbilitySet, on_delete=models.CASCADE)

class EvolutionRecord(models.Model):
    evolves_to = models.CharField(max_length=500)
    level = models.IntegerField(default=0)

class EvolutionRecordsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(EvolutionRecord, on_delete=models.CASCADE)

class EvolutionSet(models.Model):
    games = models.IntegerField()    # Games list_id
    evolution_records = models.IntegerField()    # EvolutionRecords list_id

class EvolutionSetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(EvolutionSet, on_delete=models.CASCADE)

class EvYield(models.Model):
    stat = models.CharField(max_length=500)
    value = models.IntegerField(default=0)

class EvYieldsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(EvYield, on_delete=models.CASCADE)

class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    pokedex_numbers = models.IntegerField()    # PokedexNumbers list_id
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    catch_rate = models.IntegerField(default=0)
    growth_rate = models.CharField(max_length=500)
    base_exp = models.IntegerField(default=0)
    ev_yields = models.IntegerField()    # EvYields list_id
    stat_sets = models.IntegerField()    # StatSets list_id
    type_sets = models.IntegerField()    # TypeSets list_id
    ability_sets = models.IntegerField()    # AbilitySets list_id
    evolution_sets = models.IntegerField()    # EvolutionSets list_id

class Move(models.Model):
    name = models.CharField(max_length=500)
    generation = models.IntegerField(default=0)
    type_1 = models.CharField(max_length=500)
    base_power = models.IntegerField(default=0)
    power_points = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    damage_category = models.CharField(max_length=500)
    effect = models.CharField(max_length=500, null=True)
    effect_chance = models.IntegerField(default=0)

class Ability(models.Model):
    name = models.CharField(max_length=500)
    games = models.IntegerField()    # Games list_id
    description = models.CharField(max_length=500)

class LearnMethodsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(LearnMethod, on_delete=models.CASCADE)

class LearnsetMove(models.Model):
    name = models.CharField(max_length=500)
    level = models.IntegerField(default=0)

class LearnsetMovesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(LearnsetMove, on_delete=models.CASCADE)

class Learnset(models.Model):
    games = models.IntegerField()    # Games list_id
    learnset_moves = models.IntegerField()    # LearnsetMoves list_id

class LearnsetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Learnset, on_delete=models.CASCADE)

class PokemonLearnsets(models.Model):
    name = models.CharField(max_length=500)
    learnsets = models.IntegerField()    # Learnsets list_id

class TmsetMove(models.Model):
    name = models.CharField(max_length=500)

class TmsetMovesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(TmsetMove, on_delete=models.CASCADE)

class TmSet(models.Model):
    games = models.IntegerField()    # Games list_id
    tmset_moves = models.IntegerField()    # TmsetMoves list_id

class TmSetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(TmSet, on_delete=models.CASCADE)

class PokemonTmSets(models.Model):
    name = models.CharField(max_length=500)
    tm_sets = models.IntegerField()    # TmSets list_id

class Item(models.Model):
    name = models.CharField(max_length=500)
    cost = models.IntegerField(default=0)
    description = models.CharField(max_length=500)

class ItemsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Item, on_delete=models.CASCADE)

class EffectivenessRecord(models.Model):
    source_type = models.CharField(max_length=500)
    target_type = models.CharField(max_length=500)
    damage_factor = models.IntegerField(default=0)

class EffectivenessRecordsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(EffectivenessRecord, on_delete=models.CASCADE)

class EffectivenessSet(models.Model):
    games = models.IntegerField()    # Games list_id
    effectiveness_records = models.IntegerField()    # EffectivenessRecords list_id

class EffectivenessSetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(EffectivenessSet, on_delete=models.CASCADE)

class Nature(models.Model):
    name = models.CharField(max_length=500)
    increased_stat = models.CharField(max_length=500)
    decreased_stat = models.CharField(max_length=500)

class NaturesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Nature, on_delete=models.CASCADE)

class PokemonForm(models.Model):
    name = models.CharField(max_length=500)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    base_exp = models.IntegerField(default=0)
    ev_yields = models.IntegerField()    # EvYields list_id
    stat_sets = models.IntegerField()    # StatSets list_id
    type_sets = models.IntegerField()    # TypeSets list_id
    ability_sets = models.IntegerField()    # AbilitySets list_id

