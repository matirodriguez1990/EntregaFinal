from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from AppJuegos.models import Comentarios, Consola, Juego, Jugador, Post
from AppJuegos.models import Consola, Juego, Jugador, Post, Avatar
from AppJuegos.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
def subirAvatar(request):
    if request.method == "POST":
        miFormulario = AvatarFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            avatar = Avatar(user=request.user, imagen=info["imagen"])
            avatar.save()
            return render(request, "AppJuegos/Usuario/confirmacionAvatar.html")
    else:
        miFormulario = AvatarFormulario()
    
    return render(request, "AppJuegos/Usuario/subirAvatar.html", {"miFormulario":miFormulario})

@login_required
def editarUsuario(request):
    usuario= request.user

    if request.method == "POST":
        miFormulario = EditarUsuarioFormulario(request.POST)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            usuario.first_name=info["first_name"]
            usuario.last_name=info["last_name"]
            usuario.email=info["email"]
            usuario.save()
            return redirect ("Inicio")
    else:
        miFormulario= EditarUsuarioFormulario(initial={"first_name":usuario.first_name,"last_name":usuario.last_name,"email":usuario.email})

    return render (request,"AppJuegos/Usuario/editarUsuario.html",{"miFormulario":miFormulario})

@login_required
def editarNombreUsuario(request):
    usuario= request.user

    if request.method == "POST":
        miFormulario = EditarNombreUsuarioFormulario(request.POST)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            usuario.username=info["username"]
            usuario.save()
            return redirect ("Inicio")
    else:
        miFormulario= EditarNombreUsuarioFormulario(initial={"username":usuario.username})

    return render (request,"AppJuegos/Usuario/editarNombreUsuario.html",{"miFormulario":miFormulario})

@login_required
def editarPassword(request):
    if request.method == "POST":
        miFormulario = EditarPasswordFormulario(data=request.POST, user=request.user)

        if miFormulario.is_valid():
            miFormulario.save()
            login(request,request.user)
            return render(request,"AppJuegos/Usuario/confirmacionPassword.html")
    else:
        miFormulario= EditarPasswordFormulario(user=request.user)

    return render (request,"AppJuegos/Usuario/editarPassword.html",{"miFormulario":miFormulario})


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

class VistaJugadores(ListView):
    model = User
    template_name = 'AppJuegos/Usuario/listarJugadores.html'
    ordering = ['id']
    paginate_by = 5
"""
def buscarJuego(request):
    if request.GET["nombre"]:
        nombreJuego=request.GET["nombre"]
        juegos=Juego.objects.filter(nombre__icontains=nombreJuego)
        return render(request,"AppJuegos/Juegos/resBusquedaJuego.html",{"juegos":juegos,"nombre":nombreJuego})
    return redirect("ListaJuegos")
"""
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
    paginate_by = 2

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

"""
class BuscarJuego(ListView):
    template_name = 'AppJuegos/Juegos/resBusquedaJuego.html'
    model = Juego
    paginate_by = 2
    
    def get_context_data(self,**kwargs):
        object_list = self.model.objects.filter(nombre__startswith=self.request.GET.get('nombre'))
        data = super().get_context_data(**kwargs)
        data['object_list'] = object_list
        data["query"] = self.request.GET.get('nombre')
        return data"""

class DetalleJuego(DetailView):
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
    form_class = JuegoFormulario
    success_url = reverse_lazy('ListaJuegos')

class CrearJuego(LoginRequiredMixin,CreateView):
    model = Juego
    form_class = JuegoFormulario
    template_name = 'AppJuegos/Juegos/nuevoJuego.html'
    success_url = reverse_lazy('ListaJuegos')

@login_required
def subirImagen(request):
    if request.method == "POST":
        miFormulario = ImagenFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            imagen= Imagen(nombre=info["nombre"], imagen=info["imagen"])
            imagen.save()
            return render(request, "AppJuegos/Juegos/confirmacionImagen.html")
    else:
        miFormulario = ImagenFormulario()
    
    return render(request, "AppJuegos/Juegos/subirImagen.html", {"miFormulario":miFormulario})

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

class NuevoComentario(LoginRequiredMixin,CreateView):
    model = Comentarios
    form_class = ComentarioFormulario
    template_name = 'AppJuegos/Posts/nuevoComentario.html'
    success_url = reverse_lazy('Blog')
    ordering = ['-fechaComentario']
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


"""
def buscarJuego(request):
    if request.GET["nombre"]:
        nombreJuego=request.GET["nombre"]
        juegos = Juego.objects.filter(nombre__icontains=nombreJuego)
        return render(request, 'AppJuegos/Juegos/resBusquedaJuego.html', {"juegos":juegos,"nombre":nombreJuego})
    return redirect("ListaJuegos")"""

"""
def home_screen_view(request, *args, **kwargs):
	
	context = {}
	# Search
	query = ""
	if request.GET:
		query = request.GET.get('q', '')
		context['query'] = str(query)

	resultadoBusqueda = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	resultadoBusqueda_paginator = Paginator(resultadoBusqueda, 5)
	try:
		resultadoBusqueda = resultadoBusqueda_paginator.page(page)
	except PageNotAnInteger:
		resultadoBusqueda = resultadoBusqueda_paginator.page(5)
	except EmptyPage:
		resultadoBusqueda = resultadoBusqueda_paginator.page(resultadoBusqueda_paginator.num_pages)

	context['resultadoBusqueda'] = resultadoBusqueda

	return render(request, "personal/home.html", context)"""

juegosPorPagina = 2

def buscarJuego(request):
    context = {}
    query = ""
    if request.GET:
        query = request.GET["nombre"]
        context['query'] = str(query)
    
    resultadoBusqueda = Juego.objects.filter(nombre__startswith=query)
    page = request.GET.get('page', 1)
    resultadoBusqueda_paginator = Paginator(resultadoBusqueda, juegosPorPagina)
    try:
        resultadoBusqueda = resultadoBusqueda_paginator.page(page)
    except PageNotAnInteger:
        resultadoBusqueda = resultadoBusqueda_paginator.page(juegosPorPagina)
    except EmptyPage:
        resultadoBusqueda = resultadoBusqueda_paginator.page(resultadoBusqueda_paginator.num_pages)
    
    context['resultadoBusqueda'] = resultadoBusqueda
    return render(request, "AppJuegos/Juegos/busquedaJuego.html", context)


