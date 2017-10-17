from django import forms

class SearchForm(forms.Form):
    your_name = forms.CharField(label='What do you search ?', max_length=1000)

class RegisterForm(forms.Form):
    email = forms.CharField(label='your email adress')