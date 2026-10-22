from django import forms
from .models import MealPlan

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['title', 'week_start', 'notes', 'recipes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter meal plan title'}),
            'week_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add notes (optional)', 'rows': 3}),
            'recipes': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Meal Plan Title',
            'week_start': 'Week Starting Date',
            'notes': 'Additional Notes',
            'recipes': 'Select Recipes',
        }
        help_texts = {
            'title': 'Give your weekly meal plan a descriptive name.',
            'week_start': 'Choose the Monday when your meal plan begins.',
            'notes': 'Add any additional information (optional).',
            'recipes': 'Select the recipes you want to include in this meal plan.',
        }
        error_messages = {
            'title': {
                'required': 'Please enter your meal plan title.',
                'max_length': 'The meal plan title is too long.',
            },
            'week_start': {
                'required': 'Please select a starting date.',
                'invalid': 'Please enter a valid date.',
            },
            'recipes': {
                'required': 'Please select at least one recipe.',
            }
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Meal plan title must contain at least 3 characters.')
        return title

    def clean_week_start(self):
        week_start = self.cleaned_data.get('week_start')
        if week_start and week_start.weekday() != 0:
            raise forms.ValidationError('Meal plan must start on a Monday.')
        return week_start
