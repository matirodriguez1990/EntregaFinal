from cProfile import label
from datetime import datetime
from enum import unique
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

class ConsolaFormulario(forms.Form):
    nombre=forms.CharField()
    compania=forms.CharField(label="Compañía")
    precio=forms.IntegerField()

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

class PostFormulario(forms.Form):
    titulo = forms.CharField(label="Título")
    subtitulo = forms.CharField(label="Subtítulo")
    cuerpo = forms.TextField()
    #autor=Jugador()
    autor = forms.ForeignKey(User, on_delete=forms.CASCADE)
    fecha = forms.DateField(initial=datetime.date.today)

