from django.forms import ModelForm
from django import forms
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostCreateForm(ModelForm):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'image'
		]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = [
			'firstname',
			'lastname',
			'email',
			'avatar',
		]