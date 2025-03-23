from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Orden

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'login__input', 'placeholder': ' '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': ' '}))

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': ' '}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': ' '}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'login__input', 'placeholder': ' '}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'login__input', 'placeholder': ' '}))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class OrdenForm(forms.ModelForm):
    METODOS_PAGO = [
        ('nequi', 'Nequi'),
        ('bancolombia', 'Bancolombia'),
    ]

    metodo_pago = forms.ChoiceField(
        choices=METODOS_PAGO,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = Orden
        fields = ['nombre', 'email', 'telefono', 'metodo_pago']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
