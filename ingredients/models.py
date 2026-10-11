from django.db import models

class Ingredient(models.Model):
    class Meta:
        ordering = ['name']

    class Units(models.TextChoices):
        GRAM = 'g', 'g'
        MILLILITER = 'ml', 'ml'
        PIECES = 'pcs', 'pcs'

    name = models.CharField(max_length=80, unique=True)
    default_unit = models.CharField(max_length=3, choices=Units.choices)
    is_allergen = models.BooleanField(default=False)

    def __str__(self):
        return self.name

