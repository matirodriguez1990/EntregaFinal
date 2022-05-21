from cProfile import label
from datetime import date, datetime
from enum import unique
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
<<<<<<< HEAD
from AppJuegos.models import Post, Juego
"""from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
"""

=======

from AppJuegos.models import Consola, Post, Juego
>>>>>>> 6c3e1b3f2b3034e8c922d89ee1437cbf09963954

def validate_email(request):
    if User.objects.filter(email = request).exists():
        raise ValidationError((f"{request} ya existe."))

def validate_user(request):
    if User.objects.filter(username = request).exists():
        raise ValidationError((f"{request} ya existe."))

class JuegoFormulario(forms.Form):
    nombre=forms.CharField()
    fechaLanzamiento=forms.DateField(label="Fecha de lanzamiento",help_text="MM/DD/AAAA")
    compania=forms.CharField(label="Compañía")
    copiasCreadas=forms.IntegerField(label="Copias creadas")
    genero=forms.CharField(label="Género")

class JugadorFormulario(forms.Form):
    nombre=forms.CharField()
    apellido=forms.CharField()
    email=forms.EmailField()
    jugadorActivo=forms.BooleanField(required=False,label="Jugador activo")
    horasJugadasPorDia=forms.IntegerField(label="Horas jugadas por día")

class RegistrarUsuarioFormulario(UserCreationForm):
    username = forms.CharField(validators= [validate_user], widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(validators= [validate_email], widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget = forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]
        help_texts = {
            "username": None,
            "first_name": None,
            "last_name": None,
            "email": None,
            "password1": None,
            "password2": None}
        
#class PostFormulario(forms.Form):
#    titulo = forms.CharField(label="Título")
#    subtitulo = forms.CharField(label="Subtítulo")
#    cuerpo = forms.CharField()
#    fecha = forms.DateField(initial=date.today())
#    class Meta:
#        model = Post
#        fields = 'autor'

class PostFormulario(forms.ModelForm):
    #fecha = forms.DateField(initial=date.today())
    class Meta:
        model = Post
        fields = ('titulo','subtitulo','cuerpo','autor')
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class':'form-control'}),
            'autor': forms.TextInput(attrs={'class':'form-control','placeholder':'Autor','value':'','id':'blogGames','type':'hidden'}),
        }

class PostEditFormulario(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo','subtitulo','cuerpo',)
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class':'form-control'}),
        }

class JuegoEditFormulario(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ('nombre','fechaLanzamiento','compania','copiasCreadas','genero')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'fechaLanzamiento': forms.DateInput(attrs={'class':'form-control','placeholder':'MM/DD/AAAA'}),
            'compania': forms.TextInput(attrs={'class':'form-control'}),
            'copiasCreadas': forms.NumberInput(attrs={'class':'form-control'}),
            'genero': forms.TextInput(attrs={'class':'form-control'}),
        }

<<<<<<< HEAD
"""
class LoginFormulario(forms.Form):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class':'form-control'}))

    error_messages = {
        'invalid_login': _("Credenciales incorrectas"),
        'inactive': _("Cuenta inactiva"),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache"""
=======
class ConsolaFormulario(forms.ModelForm):
    class Meta:
        model = Consola
        fields = ('nombre','compania','fechaLanzamiento','precio','unidadesVendidas')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'compania': forms.TextInput(attrs={'class':'form-control'}),
            'fechaLanzamiento': forms.DateInput(attrs={'class':'form-control','placeholder':'DD/MM/AAAA'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'unidadesVendidas' : forms.NumberInput(attrs={'class':'form-control'}),
        }
>>>>>>> 6c3e1b3f2b3034e8c922d89ee1437cbf09963954
