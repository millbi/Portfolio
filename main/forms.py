from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from portfolio.models import Portfolio, Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def clean_first(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError("Пожалуйста, введите своё имя")

    def clean_last(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise forms.ValidationError("Пожалуйста, введите свою фамилию")


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('title', 'description', 'subjects', 'main_image')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['edu_class', 'avatar_url']
