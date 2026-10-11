from django import forms
from ingredients.models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient

        fields = [
            'name',
            'default_unit',
            'is_allergen',
        ]

        labels = {
            'name': 'Ingredient name',
            'default_unit': 'Default measurement unit',
            'is_allergen': 'Contains allergens',
        }

        help_texts = {
            'name': 'Enter a unique ingredient name (max 80 characters).',
            'default_unit': 'Choose the unit used to measure this ingredient.',
            'is_allergen': 'Check this box if the ingredient is a common allergen.',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Flour, Milk, Eggs',}),
            'default_unit': forms.Select(attrs={'class': 'form-select'}),
            'is_allergen': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        error_messages = {
            'name': {
                'required': 'Please enter an ingredient name.',
                'max_length': 'Ingredient name cannot exceed 80 characters.',
                'unique': 'An ingredient with this name already exists.',
            },
            'default_unit': {
                'required': 'Please select a measurement unit.',
                'invalid_choice': 'Please select a valid measurement unit.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        matching_ingredients = Ingredient.objects.filter(name__iexact=name).exclude(pk=self.instance.pk)
        if matching_ingredients.exists():
            raise forms.ValidationError('An ingredient with this name already exists.')
        return name

