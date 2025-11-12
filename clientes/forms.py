from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class ClienteRegistroForm(forms.ModelForm):
    # Campos del User
    username = forms.CharField(
        max_length=150,
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=150,
        label='Nombres',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        label='Apellidos',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Cliente
        fields = [
            'tipo_documento', 'numero_documento',
            'fecha_nacimiento', 'genero',
            'telefono', 'telefono_alternativo', 'email_alternativo',
            'direccion', 'barrio', 'ciudad', 'departamento', 'codigo_postal',
            'acepta_promociones', 'acepta_notificaciones'
        ]
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_alternativo': forms.TextInput(attrs={'class': 'form-control'}),
            'email_alternativo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'acepta_promociones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acepta_notificaciones': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Las contraseñas no coinciden')
        
        return password_confirm
    
    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if Cliente.objects.filter(numero_documento=numero_documento).exists():
            raise forms.ValidationError('Ya existe un cliente con este número de documento')
        return numero_documento
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico')
        return email
