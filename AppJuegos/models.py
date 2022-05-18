from django.db import models

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
    email=models.EmailField()
    jugadorActivo=models.BooleanField()
    horasJugadasPorDia=models.IntegerField()

    def __str__(self):
        return f"Nombre: {self.nombre} - Apellido: {self.apellido} - Email: {self.email}"

    class Meta:
        verbose_name="Jugador"
        verbose_name_plural="Jugadores"

class Consola(models.Model):
    nombre=models.CharField(max_length=40)
    compania=models.CharField(max_length=40)
    precio=models.IntegerField()

    def __str__(self):
        return f"Nombre: {self.nombre} - Compañía: {self.compania}"
    