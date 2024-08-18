from django import forms
from .models import User, UserType
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'El correo electrónico es obligatorio',
            'invalid': 'Introduce una dirección de correo electrónico válida',
        }
    )
    rut = forms.CharField(
        required=True,
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'El RUT es obligatorio',
            'invalid': 'Introduce un RUT válido',
        }
    )
    address = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'La dirección es obligatoria',
        }
    )
    phone = forms.CharField(
        required=True,
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'El teléfono es obligatorio',
        }
    )

    user_type = forms.ModelChoiceField(
        queryset=UserType.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'El tipo de usuario es obligatorio',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'rut', 'address', 'phone', 'user_type')
        labels =  {
            'username': 'Nombre de Usuario',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Repita Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'rut': 'RUT',
            'address': 'Dirección',
            'phone': 'Teléfono',
            'user_type': 'Tipo de Usuario',
        }
        error_messages = {
            'username': {
                'required': 'El nombre de usuario es obligatorio',
                'unique': 'Este nombre de usuario ya está en uso',
            },
            'password1': {
                'required': 'La contraseña es obligatoria',
            },
            'password2': {
                'required': 'Repite la contraseña',
                'password_mismatch': 'Las contraseñas no coinciden',
            },
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Repita Contraseña'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['rut'].label = 'RUT'
        self.fields['address'].label = 'Dirección'
        self.fields['phone'].label = 'Teléfono'
        self.fields['user_type'].label = 'Tipo de Usuario'
