from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Juego(models.Model):
    nombre=models.CharField(max_length=100)
    fechaLanzamiento=models.DateField()
    compania=models.CharField(max_length=40)
    copiasCreadas=models.IntegerField()
    genero=models.CharField(max_length=40)

    def __str__(self):
        return f"Nombre: {self.nombre} - Compañía: {self.compania}"

class Jugador(models.Model):
    nombre=models.CharField(max_length=40)
    apellido=models.CharField(max_length=40)
    email=models.EmailField(max_length=254)
    jugadorActivo=models.BooleanField()
    horasJugadasPorDia=models.IntegerField()

    def __str__(self):
        return f"Nombre: {self.first_name} - Apellido: {self.last_name}"

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

<<<<<<< HEAD
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="usuario")
=======
class Comentarios(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comentarios")
>>>>>>> 1d0ba0978220cffb5f6a260d9ecced2cffb09295
    titulo = models.CharField(max_length=50)
    cuerpo = models.TextField()
    fechaComentario = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
<<<<<<< HEAD
        return '%s - %s' % (self.post.titulo, self.nombre)
=======
        return '%s - %s' % (self.post.titulo, self.titulo)
>>>>>>> 1d0ba0978220cffb5f6a260d9ecced2cffb09295

class Avatar(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares",null=True, blank=True)

    class Meta:
        verbose_name = "Avatar"
        verbose_name_plural = "Avatares"


