from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MensajeContacto


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo ya está en uso.')
        return email

class UsuarioAdminForm(PerfilForm):
    class Meta(PerfilForm.Meta):
        fields = PerfilForm.Meta.fields + ('is_staff', 'is_active')
        labels = {
            **PerfilForm.Meta.labels,
            'is_staff': 'Administrador',
            'is_active': 'Cuenta activa',
        }
        help_texts = {
            'is_staff': 'Si lo marcas, tendrá acceso al panel de administración.',
            'is_active': 'Si lo desmarcas, no podrá iniciar sesión.',
        }

class ContactoForm(forms.ModelForm):
    sitio_web = forms.CharField(
        required=False,
        label='Sitio web',
        widget=forms.TextInput(attrs={'tabindex': '-1', 'autocomplete': 'off'}),
    )

    class Meta:
        model = MensajeContacto
        fields = ('nombre', 'email', 'asunto', 'mensaje')
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_sitio_web(self):
        if self.cleaned_data.get('sitio_web'):
            raise forms.ValidationError('Spam detectado.')
        return ''