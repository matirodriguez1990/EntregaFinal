from django.http import HttpResponse
from django.shortcuts import redirect, render
from AppJuegos.models import Consola, Juego, Jugador
from AppJuegos.forms import ConsolaFormulario, JuegoFormulario, JugadorFormulario
#from AppJuegos.forms import 
#from .models import Curso, Profesor

# Create your views here.
def inicio(request):
    return render(request,"AppJuegos/inicio.html")

def juego(request):
    if request.method == "POST":
        miFormulario= JuegoFormulario(request.POST)
        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            juego=Juego(nombre=info["nombre"],fechaLanzamiento=info["fechaLanzamiento"],compania=info["compania"], copiasCreadas=info["copiasCreadas"], genero=info["genero"])
            juego.save()
            return redirect("Juego")
    else:
        miFormulario=JuegoFormulario()
    
    return render(request,"AppJuegos/juego.html",{"miFormulario":miFormulario})

def jugador(request):
    if request.method == "POST":
        miFormulario= JugadorFormulario(request.POST)
        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            jugador=Jugador(nombre=info["nombre"],apellido=info["apellido"],email=info["email"], jugadorActivo=info["jugadorActivo"], horasJugadasPorDia=info["horasJugadasPorDia"])
            jugador.save()
            return redirect("Jugador")
    else:
        miFormulario=JugadorFormulario()
    
    return render(request,"AppJuegos/jugador.html",{"miFormulario":miFormulario})

def consola(request):
    if request.method == "POST":
        miFormulario= ConsolaFormulario(request.POST)
        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            consola=Consola(nombre=info["nombre"],compania=info["compania"],precio=info["precio"])
            consola.save()
            return redirect("Consola")
    else:
        miFormulario=ConsolaFormulario()
    
    return render(request,"AppJuegos/consola.html",{"miFormulario":miFormulario})

def buscarJuego(request):
    if request.GET["compania"]:
        companiaJuego=request.GET["compania"]
        juegos=Juego.objects.filter(compania__iexact=companiaJuego)
        return render(request,"AppJuegos/resBusquedaJuego.html",{"juegos":juegos,"compania":companiaJuego})
    return redirect("Juego")

def buscarConsola(request):
    if request.GET["compania"]:
        companiaConsolas=request.GET["compania"]
        consolas=Consola.objects.filter(compania__iexact=companiaConsolas)
        return render(request,"AppJuegos/resBusquedaConsola.html",{"consolas":consolas,"compania":companiaConsolas})
    return redirect("Consola")

def buscarJugador(request):
    if request.GET["nombre"]:
        nombreJugador=request.GET["nombre"]
        jugadores=Jugador.objects.filter(nombre__iexact=nombreJugador)
        return render(request,"AppJuegos/resBusquedaJugador.html",{"jugadores":jugadores,"nombre":nombreJugador})
    return redirect("Jugador")

