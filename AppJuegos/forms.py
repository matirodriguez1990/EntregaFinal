from django import forms

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