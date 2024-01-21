from django import forms


class LoginForm(forms.Form):
    uername = forms.CharField(max_length=40)
    password = forms.CharField(widget=forms.PasswordInput())

