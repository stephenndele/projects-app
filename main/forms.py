from django import forms
from .models import *
from .models import Profile 

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
        fields = ("comment", "design_rating")
        # "usability_rating", "content_rating")

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')


class ProfileForm(forms.ModelForm):
	class Meta: 
		model = Profile
		fields = ('user', 'bio', 'image', 'projects') 