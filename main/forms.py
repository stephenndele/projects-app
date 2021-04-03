from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'user', 'link', 'description', 'publish_date', 'image')

        widgets = {
            'image': forms.TextInput(attrs={'placeholder': 'Add image url.... '}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "design_rating", "usability_rating", "content_rating")
