from cProfile import label
from dataclasses import field
from datetime import date, datetime
from enum import unique
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from AppJuegos.models import Avatar, Jugador, Post, Juego, Consola
from django.core.files.images import get_image_dimensions

def validate_email(request):
    if User.objects.filter(email = request).exists():
        raise ValidationError((f"{request} ya existe."))

def validate_user(request):
    if User.objects.filter(username = request).exists():
        raise ValidationError((f"{request} ya existe."))

class JuegoFormulario(forms.Form):
    nombre=forms.CharField()
    fechaLanzamiento=forms.DateField(required=False, label="Fecha de lanzamiento",help_text="MM/DD/AAAA")
    compania=forms.CharField(required=False, label="Compañía")
    copiasCreadas=forms.IntegerField(required=False, label="Copias creadas")
    genero=forms.CharField(required=False, label="Género")

class JugadorFormulario(forms.Form):
    nombre=forms.CharField()
    apellido=forms.CharField()
    email=forms.EmailField()
    jugadorActivo=forms.BooleanField(required=False,label="Jugador activo")
    horasJugadasPorDia=forms.IntegerField(label="Horas jugadas por día")

"""
class UsuarioFormulario(forms.ModelForm):
    username = forms.CharField(validators= [validate_user], widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(validators= [validate_email], widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget = forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    jugadorActivo = forms.BooleanField(label="Jugador activo")
    horasJugadasPorDia=forms.IntegerField(label="Horas jugadas por día", widget=forms.NumberInput(attrs={'class':'form-control'}))
    avatar=forms.ImageField(label="Avatar")

    class Meta:
        model=Jugador
        fields = ["username","first_name","last_name","email","password1","password2","jugadorActivo","horasJugadasPorDia","avatar"]
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            
            #Handles case when we are updating the user profile
            #and do not supply a new avatar
            
            pass

        return avatar
"""


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

class JuegoFormulario(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ('nombre','fechaLanzamiento','compania','copiasCreadas','genero')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: Elden Ring'}),
            'fechaLanzamiento': forms.DateInput(attrs={'class':'form-control','placeholder':'DD/MM/AAAA'}),
            'compania': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: FromSoftware'}),
            'copiasCreadas': forms.NumberInput(attrs={'class':'form-control','placeholder':'Por ejemplo: 1000000'}),
            'genero': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: RPG'}),
        }

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

class ComentarioFormulario(UserCreationForm):
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class':'form-control'}))
    cuerpo = forms.CharField(label="Cuerpo",widget=forms.Textarea(attrs={'class':'form-control'}))
class AvatarFormulario(forms.ModelForm):

    class Meta:
        model=Avatar
        fields=["user","imagen"]
        widgets = {
            "user":forms.TextInput(attrs={'value':'','id':'blogGames',"type":"hidden"}),
            "imagen":forms.FileInput()
            }
