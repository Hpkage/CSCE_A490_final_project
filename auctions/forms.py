from django.forms import ModelForm
from django import forms
from .models import Auction, Comment 

# create a new auction listing model form class
class NewListingForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Auction
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                        "placeholder": "Enter the title of your auction list",
                        "class": "form-control"
                    }
            ),
            "description": forms.Textarea(
                attrs={
                        "placeholder": "Enter the description...",
                        "class": "form-control",
                        "rows": 15
                    }
            ),
            "image": forms.FileInput(
                attrs={
                    "placeholder": "Choose file",
                    }
                ) 
        }


# create a new Comment model from class
class NewCommentForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                        "placeholder": "Enter your comment...",
                        "class": "form-control",
                        "rows": 4
                    }
        )}