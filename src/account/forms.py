from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import Profile


class UserLoginForm(forms.Form):
    """ Login form """
    username    = forms.CharField(label='Электронная почта', required=True)
    password    = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label='Запомнить меня', required=False)

class UserRegistrationForm(forms.ModelForm):
    """ Registration form """
    email       = forms.EmailField(label='Электронная почта')
    first_name  = forms.CharField(label='Имя')
    last_name   = forms.CharField(label='Фамилия')
    password    = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class EmailValidationOnForgotPassword(PasswordResetForm):
    """ Notify user if email is not exist """
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
           msg = ("Пользователя с указанной электронной почтой не существует в системе.")
           self.add_error('email', msg)
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')