from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=500)
    generation = models.IntegerField(default=0)
    release_date = models.DateTimeField()
    system = models.CharField(max_length=500)
    region = models.CharField(max_length=500)

class TypesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Type, on_delete=models.CASCADE)

class PokedexNumbersListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(PokedexNumber, on_delete=models.CASCADE)

class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    pokedex_numbers = models.IntegerField()    # PokedexNumbers list_id
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

class PokedexNumber(models.Model):
    name = models.CharField(max_length=500)
    number = models.IntegerField(default=0)

class Move(models.Model):
    name = models.CharField(max_length=500)
    generation = models.IntegerField(default=0)
    type_ = models.CharField(max_length=500)
    base_power = models.CharField(max_length=500)
    power_points = models.IntegerField(default=0)
    accuracy = models.CharField(max_length=500)
    priority = models.CharField(max_length=500)
    damage_category = models.CharField(max_length=500)

class AbilityListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Ability, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    games = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

class GamesListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Game, on_delete=models.CASCADE)

class LearnMethodsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(LearnMethod, on_delete=models.CASCADE)

class LearnsetsListElement(models.Model):
    list_id = models.IntegerField()
    sequence_number = models.IntegerField()
    element = models.ForeignKey(Learnset, on_delete=models.CASCADE)

class PokemonLearnsets(models.Model):
    name = models.CharField(max_length=500)
    learnsets = models.IntegerField()    # Learnsets list_id

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

