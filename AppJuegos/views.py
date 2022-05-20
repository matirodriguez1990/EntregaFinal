from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from AppJuegos.models import Consola, Juego, Jugador, Post
from AppJuegos.forms import ConsolaFormulario, JuegoFormulario, JugadorFormulario, RegistrarUsuarioFormulario,PostFormulario,PostEditFormulario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

# Create your views here.
def inicio(request):
    return render(request,"AppJuegos/inicio.html")

def about(request):
    return render(request,"AppJuegos/about.html")

def loginRequest(request):
    if request.method == "POST":
        miFormulario= AuthenticationForm(request, data=request.POST)
        if miFormulario.is_valid():
            usuario=miFormulario.cleaned_data.get("username")
            contrasenia=miFormulario.cleaned_data.get("password")
            user=authenticate(username=usuario, password=contrasenia)
            if user:
                login(request,user)
                return redirect("Inicio")
        else:
            return render(request,"AppJuegos/login.html",{"miFormulario":miFormulario})
    else:
        miFormulario = AuthenticationForm()
    return render(request,"AppJuegos/login.html",{"miFormulario":miFormulario})

def registro(request):
    if request.method == "POST":
        miFormulario= RegistrarUsuarioFormulario(request.POST)
        if miFormulario.is_valid():
            username=miFormulario.cleaned_data["username"]
            miFormulario.save()
            username= miFormulario.cleaned_data["username"]
            user = User.objects.get(username=username)
            login(request,user)
            return redirect("Inicio")
    else:
        miFormulario = RegistrarUsuarioFormulario()
    return render(request,"AppJuegos/registro.html",{"miFormulario":miFormulario})

def editarUsuario(request):
    usuario= request.user

    if request.method == "POST":
        miFormulario = RegistrarUsuarioFormulario(request.POST)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            usuario.username=info["username"]
            usuario.email=info["email"]
            usuario.password1=info["password1"]
            usuario.password2=info["password1"]
            usuario.save()
            return redirect ("Inicio")
    else:
        miFormulario= RegistrarUsuarioFormulario(initial={"username":usuario.username,"email":usuario.email})

    return render (request,"AppJuegos/editarUsuario.html",{"miFormulario":miFormulario,"usuario":usuario.username})


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

class VistaBlog(ListView):
    model = Post
    template_name = 'AppJuegos/blog.html'

class VistaPost(DetailView):
    model = Post
    template_name = 'AppJuegos/post.html'

class CrearPost(CreateView):
    model = Post
    form_class = PostFormulario
    template_name = 'AppJuegos/nuevoPost.html'
    #fields = ['titulo','subtitulo','cuerpo','autor']

class EliminarPost(DeleteView):
    model = Post
    template_name = 'AppJuegos/eliminarPost.html'
    success_url = reverse_lazy('Inicio')

class EditarPost(UpdateView):
    model = Post
    template_name = 'AppJuegos/editarPost.html'
    form_class = PostEditFormulario

