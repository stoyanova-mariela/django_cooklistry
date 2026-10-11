from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models

from ingredients.models import Ingredient


class Category(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, validators=[MaxLengthValidator(300)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    class Meta:
        ordering = ['title']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    class Difficulty(models.TextChoices):
        EASY = 'easy', 'Easy'
        MEDIUM = 'medium', 'Medium'
        HARD = 'hard', 'Hard'

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, validators=[MaxLengthValidator(300)])
    instructions = models.TextField(validators=[MaxLengthValidator(1000)])
    preparation_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    servings = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    difficulty = models.CharField(choices=Difficulty.choices, max_length=6)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name='recipe_ingredients')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit = models.CharField(choices=Ingredient.Units.choices, max_length=6)

    def __str__(self):
        return f"{self.recipe.title} - {self.ingredient.name} ({self.quantity} {self.unit})"

