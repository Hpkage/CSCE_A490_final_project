from django.forms import ModelForm
from django import forms
from .models import User, Auction, Comment 

class NewUser(ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirmation = forms.CharField(label='confirmation', widget=forms.PasswordInput)
    
    # specify the name of model to use
    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmation", "profile_pic"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Enter your username",
                    "class": "form-control"
                }
            ),
            "email": forms.TextInput(
                attrs={
                        "placeholder": "Enter your email",
                        "class": "form-control"
                    }
            ),
            "password": forms.TextInput(
                attrs={
                        "placeholder": "Enter your password",
                        "class": "form-control"
                    }
            ),  
            "confirmation": forms.TextInput(
                attrs={
                        "placeholder": "Enter your password",
                        "class": "form-control"
                    }
            ),         
            "profile_pic": forms.FileInput(
                attrs={
                    "placeholder": "Choose file",
                    }
            ) 
        }
    
    def clean_confirmation(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        confirmation = self.cleaned_data.get("confirmation")
        if password and confirmation and password != confirmation:
            raise forms.ValidationError("Passwords don't match")
        return confirmation
    
    def saveIt(self, commit=True):
        # Save the provided password in hashed format
        user = super(NewUser, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


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