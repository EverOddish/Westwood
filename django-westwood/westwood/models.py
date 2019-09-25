from django.db import models

class PokemonTmSets(models.Model):
    name = models.CharField(max_length=500)
    tm_sets = models.CharField(max_length=500)

class TmSets(models.Model):

class TmSet(models.Model):
    games = models.CharField(max_length=500)
    moves = models.CharField(max_length=500)

class GamesListElement(models.Model):

class MovesListElement(models.Model):

class TypesListElement(models.Model):

class PokemonLearnsetsListElement(models.Model):
    name = models.CharField(max_length=500)
    learnsets = models.CharField(max_length=500)

class LearnsetsListElement(models.Model):

class Learnset(models.Model):
    games = models.CharField(max_length=500)
    moves = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    level = models.IntegerField(default=0)

class Move(models.Model):
    name = models.CharField(max_length=500)
    level = models.IntegerField(default=0)

class Game(models.Model):
    name = models.CharField(max_length=500)
    generation = models.IntegerField(default=0)
    release_date = models.DateTimeField()
    system = models.CharField(max_length=500)
    region = models.CharField(max_length=500)

class AbilityListElement(models.Model):
    name = models.CharField(max_length=500)
    games = models.CharField(max_length=500)
    description = models.CharField(max_length=500)

class Pokemon(models.Model):
    name = models.CharField(max_length=500)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

class PokedexNumber(models.Model):
    name = models.CharField(max_length=500)
    number = models.IntegerField(default=0)

class PokedexNumbersListElement(models.Model):

class LearnMethodsListElement(models.Model):

