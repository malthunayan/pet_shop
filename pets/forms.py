from django import forms
from .models import Pet
from django.contrib.auth.models import User

class PetForm(forms.ModelForm):
	class Meta:
		model = Pet
		exclude = ['available', 'owner']

class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','first_name','last_name','email','password']

		widgets = {
			'password': forms.PasswordInput(),
		}

class SigninForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(widget=forms.PasswordInput(), required=True)

class PetUpdateForm(forms.ModelForm):
	class Meta:
		model = Pet
		exclude = ['owner']