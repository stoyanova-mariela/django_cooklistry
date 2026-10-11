from django import forms
from recipes.models import Category


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

