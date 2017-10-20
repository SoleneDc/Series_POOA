from django import forms

class SearchForm(forms.Form):
    your_name = forms.CharField(label='What do you search ?', max_length=100, required=False)
    #Il y a un truc bizarre avec le required... TO DO!

class RegisterForm(forms.Form):
    email = forms.CharField(label='your email address')