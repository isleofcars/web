from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import Ad


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required = True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        )
    first_name = forms.CharField(
        max_length=100,
        required = True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        )
    last_name = forms.CharField(
        max_length=100,
        required = True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        )
    username = forms.CharField(
        max_length=200,
        required = True,
        help_text='Enter Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        )
    password1 = forms.CharField(
        help_text='Enter Password',
        required = True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        )
    password2 = forms.CharField(
        required = True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
        )

    class Meta:
        model = User
        fields = [
        'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
        ]


class NewAddForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = '__all__'


class FiltersForm(forms.Form):
    make = forms.ChoiceField(choices=[], required=False)
    model = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_makes = Ad.objects.exclude(make__isnull=True).values_list('make', 'make').distinct().order_by()
        self.fields['make'].choices = [[None, 'All Makes']] + list(all_makes)
