from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    

class DeleteUserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())

class AddUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        

class UserSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search')