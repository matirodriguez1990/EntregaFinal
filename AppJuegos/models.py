from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Juego(models.Model):
    nombre=models.CharField(max_length=100)
    fechaLanzamiento=models.DateField(default="01/01/1950")
    compania=models.CharField(default="compañía",max_length=40)
    copiasCreadas=models.IntegerField(default=1000000)
    genero=models.CharField(default="juego",max_length=40)

    def __str__(self):
        return f"Nombre: {self.nombre} - Compañía: {self.compania}"

class Jugador(models.Model):
    #usuario=models.OneToOneField(User,related_name="autor",on_delete=models.CASCADE,default=666)
    nombre=models.CharField(max_length=40)
    apellido=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    jugadorActivo=models.BooleanField()
    horasJugadasPorDia=models.IntegerField()

    def __str__(self):
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Email: {self.email}"

    class Meta:
        verbose_name="Jugador"
        verbose_name_plural="Jugadores"

class Consola(models.Model):
    nombre = models.CharField(max_length=40)
    compania = models.CharField(max_length=40)
    fechaLanzamiento = models.DateField()
    precio = models.FloatField()
    unidadesVendidas = models.IntegerField()

    def __str__(self):
        return f"Nombre: {self.nombre} - Compañía: {self.compania}"

    def get_absolute_url(self):
        return reverse('Consola')
    
class Post(models.Model):
    titulo = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.titulo + ' - ' + str(self.autor)
    
    def get_absolute_url(self):
        return reverse('Blog')

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    titulo = models.CharField(max_length=50)
    cuerpo = models.TextField()
    fechaComentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.titulo, self.nombre)
