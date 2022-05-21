from cProfile import label
from datetime import date, datetime
from enum import unique
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from AppJuegos.models import Consola, Post, Juego

def validate_email(request):
    if User.objects.filter(email = request).exists():
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
    email = forms.EmailField(validators= [validate_email])
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        help_texts = {
            "username": None,
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