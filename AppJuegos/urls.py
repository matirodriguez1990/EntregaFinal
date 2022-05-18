from django.urls import path
from AppJuegos import views

urlpatterns = [
    path("",views.inicio,name="Inicio"),
    path("juego/",views.juego, name="Juego"),
    path("jugador/",views.jugador, name="Jugador"),
    path("consola/",views.consola, name="Consola"),
    path("buscarJuego/",views.buscarJuego,),
    path("buscarJugador/",views.buscarJugador,),
    path("buscarConsola/",views.buscarConsola,)
]