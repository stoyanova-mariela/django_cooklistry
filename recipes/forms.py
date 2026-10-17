from django import forms
from recipes.models import Category, Recipe, RecipeIngredient
from django.forms import BaseInlineFormSet, inlineformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter a short description', 'rows': 3, 'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        matching_categories = Category.objects.filter(name__iexact=name).exclude(pk=self.instance.pk)
        if matching_categories.exists():
            raise forms.ValidationError("This category already exists.")
        return name


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'instructions',
            'preparation_time',
            'servings',
            'difficulty',
            'category',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter recipe name', 'class': 'form-control',}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter a short description', 'rows': 3, 'class': 'form-control',}),
            'instructions': forms.Textarea(attrs={'placeholder': 'Enter cooking instructions', 'rows': 5, 'class': 'form-control',}),
            'preparation_time': forms.NumberInput(attrs={'placeholder': 'Preparation time in minutes', 'min': 1, 'class': 'form-control',}),
            'servings': forms.NumberInput(attrs={'placeholder': 'Number of servings', 'min': 1, 'class': 'form-control',}),
            'difficulty': forms.Select(attrs={'class': 'form-select',}),
            'category': forms.Select(attrs={'class': 'form-select',}),
        }

        labels = {
            'title': 'Recipe Name',
            'instructions': 'Cooking Instructions',
            'preparation_time': 'Preparation Time (minutes)',
            'servings': 'Number of Servings',
            'difficulty': 'Difficulty Level',
        }

        help_texts = {
            'instructions': 'Maximum 1000 characters.',
            'preparation_time': 'Enter the time in minutes.',
        }

        error_messages = {
            'title': {
                'required': 'Please enter a recipe name.',
                'max_length': 'Recipe name cannot exceed 100 characters.',
            },
            'instructions': {
                'required': 'Please enter cooking instructions.',
            },
            'category': {
                'required': 'Please select a category.',
            },
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()

        if len(title) < 3:
            raise forms.ValidationError('Recipe name must contain at least 3 characters.')

        return title


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = [
            'ingredient',
            'quantity',
            'unit',
        ]

        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-select',}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity', 'min': 1, 'class': 'form-control',}),
            'unit': forms.Select(attrs={'class': 'form-select',}),
        }

        labels = {
            'ingredient': 'Ingredient',
            'quantity': 'Quantity',
            'unit': 'Unit',
        }

        error_messages = {
            'ingredient': {
                'required': 'Please select an ingredient.',
            },
            'quantity': {
                'required': 'Please enter a quantity.',
                'min_value': 'Quantity must be greater than zero.',
            },
            'unit': {
                'required': 'Please select a unit.',
            },
        }


class BaseRecipeIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        used_ingredients = set()
        ingredient_count = 0

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get('DELETE'):
                continue

            ingredient = form.cleaned_data.get('ingredient')

            if ingredient is None:
                continue

            ingredient_count += 1

            if ingredient.pk in used_ingredients:
                raise forms.ValidationError('Each ingredient can only be added once per recipe.')

            used_ingredients.add(ingredient.pk)

        if ingredient_count == 0:
            raise forms.ValidationError('Please add at least one ingredient to the recipe.')


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    formset=BaseRecipeIngredientFormSet,
    extra=3,
    can_delete=True,
)
