from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from AppJuegos.models import Comentario, Consola, Juego, Jugador, Post
from AppJuegos.forms import ConsolaFormulario, JuegoFormulario, JugadorFormulario, RegistrarUsuarioFormulario,PostFormulario,PostEditFormulario, JuegoEditFormulario,ComentarioFormulario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
            return render(request,"AppJuegos/Usuario/login.html",{"miFormulario":miFormulario})
    else:
        miFormulario = AuthenticationForm()
    return render(request,"AppJuegos/Usuario/login.html",{"miFormulario":miFormulario})

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
    return render(request,"AppJuegos/Usuario/registro.html",{"miFormulario":miFormulario})

@login_required
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

    return render (request,"AppJuegos/Usuario/editarUsuario.html",{"miFormulario":miFormulario,"usuario":usuario.username})

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

def buscarJuego(request):
    if request.GET["nombre"]:
        nombreJuego=request.GET["nombre"]
        juegos=Juego.objects.filter(nombre__icontains=nombreJuego)
        return render(request,"AppJuegos/Juegos/resBusquedaJuego.html",{"juegos":juegos,"nombre":nombreJuego})
    return redirect("Juego")

def buscarJugador(request):
    if request.GET["nombre"]:
        nombreJugador=request.GET["nombre"]
        jugadores=Jugador.objects.filter(nombre__iexact=nombreJugador)
        return render(request,"AppJuegos/resBusquedaJugador.html",{"jugadores":jugadores,"nombre":nombreJugador})
    return redirect("Jugador")

class VistaBlog(ListView):
    model = Post
    template_name = 'AppJuegos/blog.html'
    ordering = ['-id']
    paginate_by = 3
    #ordering = ['-fecha']

class VistaPost(DetailView):
    model = Post
    template_name = 'AppJuegos/post.html'

class CrearPost(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostFormulario
    template_name = 'AppJuegos/nuevoPost.html'
    #fields = ['titulo','subtitulo','cuerpo']

class EliminarPost(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'AppJuegos/eliminarPost.html'
    success_url = reverse_lazy('Inicio')

class EditarPost(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'AppJuegos/editarPost.html'
    form_class = PostEditFormulario

"""def publicarPost(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostFormulario(request.POST)
            for field in form:
                print(field.value())
        if form.is_valid():
            obj = form.save(commit=False)
            obj.autor = User.objects.get(pk=request.user.id)
            obj.save()
        else:
            print("ERROR : Formulario invalido")
            print(form.errors)
    return redirect("Blog")
"""
class VistaJuegos(ListView):
    model = Juego
    template_name = 'AppJuegos/Juegos/listarJuego.html'
    ordering = ['nombre']
    paginate_by = 10

class DetalleJuegos(DetailView):
    model = Juego
    template_name = 'AppJuegos/Juegos/detalleJuego.html'
    ordering = ['nombre']

class EliminarJuego(LoginRequiredMixin,DeleteView):
    model = Juego
    template_name = 'AppJuegos/Juegos/eliminarJuego.html'
    success_url = reverse_lazy('ListaJuegos')

class EditarJuego(LoginRequiredMixin,UpdateView):
    model = Juego
    template_name = 'AppJuegos/Juegos/editarJuego.html'
    form_class = JuegoEditFormulario
    success_url = reverse_lazy('ListaJuegos')

class VistaConsolas(ListView):
    model = Consola
    template_name = 'AppJuegos/Consolas/listaConsolas.html'
    ordering = ['nombre']
    paginate_by = 3

class DetalleConsola(DetailView):
    model = Consola
    template_name = 'AppJuegos/Consolas/detalleConsola.html'

class NuevaConsola(LoginRequiredMixin,CreateView):
    model = Consola
    form_class = ConsolaFormulario
    template_name = 'AppJuegos/Consolas/nuevaConsola.html'

class EditarConsola(LoginRequiredMixin,UpdateView):
    model = Consola
    template_name = 'AppJuegos/Consolas/editarConsola.html'
    form_class = ConsolaFormulario
    success_url = reverse_lazy('Consola')

class EliminarConsola(LoginRequiredMixin,DeleteView):
    model = Consola
    template_name = 'AppJuegos/Consolas/eliminarConsola.html'
    success_url = reverse_lazy('Consola')
"""
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
"""
def buscarConsola(request):
    if request.GET["compania"]:
        companiaConsolas=request.GET["compania"]
        consolas=Consola.objects.filter(compania__iexact=companiaConsolas)
        return render(request,"AppJuegos/resBusquedaConsola.html",{"consolas":consolas,"compania":companiaConsolas})
    return redirect("Consola")

class NuevoComentario(CreateView):
    model = Comentario
    form_class = ComentarioFormulario
    template_name = 'AppJuegos/Posts/nuevoComentario.html'