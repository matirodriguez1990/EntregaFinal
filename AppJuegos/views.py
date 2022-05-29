from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from AppJuegos.models import Comentarios, Consola, Juego, Post, Avatar
from AppJuegos.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

###################################################################################################
#Vistas generales
###################################################################################################

#Función para ingresar al about
def about(request):
    return render(request,"AppJuegos/about.html")

#Clase para listar los posts del blog
class VistaBlog(ListView):
    model = Post
    template_name = 'AppJuegos/blog.html'
    ordering = ['-id']
    paginate_by = 2

###################################################################################################
#Fin Vistas generales
###################################################################################################



###################################################################################################
#Vistas de Usuario
###################################################################################################

#Función para solicitar al usuario el login
def loginRequest(request):
    if request.method == "POST":
        miFormulario= LoginFormulario(request, data=request.POST)
        if miFormulario.is_valid():
            usuario=miFormulario.cleaned_data.get("username")
            contrasenia=miFormulario.cleaned_data.get("password")
            user=authenticate(username=usuario, password=contrasenia)
            if user:
                login(request,user)
                return redirect("Blog")
        else:
            return render(request,"AppJuegos/Usuario/login.html",{"miFormulario":miFormulario})
    else:
        miFormulario = LoginFormulario()
    return render(request,"AppJuegos/Usuario/login.html",{"miFormulario":miFormulario})


#Función para solicitar al usuario el registro
def registro(request):
    if request.method == "POST":
        miFormulario= RegistrarUsuarioFormulario(request.POST)
        if miFormulario.is_valid():
            username=miFormulario.cleaned_data["username"]
            miFormulario.save()
            username= miFormulario.cleaned_data["username"]
            user = User.objects.get(username=username)
            login(request,user)
            return redirect("Blog")
    else:
        miFormulario = RegistrarUsuarioFormulario()
    return render(request,"AppJuegos/Usuario/registro.html",{"miFormulario":miFormulario})


#Función para solicitar al usuario que suba un nuevo Avatar
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


#Función para editar al usuario
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
            return redirect ("Blog")
    else:
        miFormulario= EditarUsuarioFormulario(initial={"first_name":usuario.first_name,"last_name":usuario.last_name,"email":usuario.email})

    return render (request,"AppJuegos/Usuario/editarUsuario.html",{"miFormulario":miFormulario})


#Función para editar el nombre usuario
@login_required
def editarNombreUsuario(request):
    usuario= request.user

    if request.method == "POST":
        miFormulario = EditarNombreUsuarioFormulario(request.POST)

        if miFormulario.is_valid():
            info=miFormulario.cleaned_data
            usuario.username=info["username"]
            usuario.save()
            return redirect ("Blog")
    else:
        miFormulario= EditarNombreUsuarioFormulario(initial={"username":usuario.username})

    return render (request,"AppJuegos/Usuario/editarNombreUsuario.html",{"miFormulario":miFormulario})


#Función para editar la password del usuario
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


#Clase para listar los jugadores representados por los usuarios
class VistaJugadores(ListView):
    model = User
    template_name = 'AppJuegos/Usuario/listarJugadores.html'
    ordering = ['id']
    paginate_by = 6

###################################################################################################
#Fin de Vistas de Usuario
###################################################################################################


###################################################################################################
#Vistas de Juego
###################################################################################################

#Clase para listar los juegos
class VistaJuegos(ListView):
    model = Juego
    template_name = 'AppJuegos/Juegos/listarJuego.html'
    ordering = ['nombre']
    paginate_by = 7

#Clase para detallar los juegos
class DetalleJuego(DetailView):
    model = Juego
    template_name = 'AppJuegos/Juegos/detalleJuego.html'
    ordering = ['nombre']

#Clase para eliminar los juegos
class EliminarJuego(LoginRequiredMixin,DeleteView):
    model = Juego
    template_name = 'AppJuegos/Juegos/eliminarJuego.html'
    success_url = reverse_lazy('ListaJuegos')

#Clase para editar los juegos
class EditarJuego(LoginRequiredMixin,UpdateView):
    model = Juego
    template_name = 'AppJuegos/Juegos/editarJuego.html'
    form_class = JuegoFormulario
    success_url = reverse_lazy('ListaJuegos')

#Clase para crear los juegos
class CrearJuego(LoginRequiredMixin,CreateView):
    model = Juego
    form_class = JuegoFormulario
    template_name = 'AppJuegos/Juegos/nuevoJuego.html'
    success_url = reverse_lazy('ListaJuegos')


#Función para subir una imagen del juego
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

#Función para buscar juegos con paginación
juegosPorPagina = 7

def buscarJuego(request):
    contexto = {}
    query = ""
    if request.GET:
        query = request.GET["nombre"]
        contexto['query'] = str(query)
    
    resultadoBusqueda = Juego.objects.filter(nombre__startswith=query)
    page = request.GET.get('page', 1)
    resultadoBusqueda_paginator = Paginator(resultadoBusqueda, juegosPorPagina)
    try:
        resultadoBusqueda = resultadoBusqueda_paginator.page(page)
    except PageNotAnInteger:
        resultadoBusqueda = resultadoBusqueda_paginator.page(juegosPorPagina)
    except EmptyPage:
        resultadoBusqueda = resultadoBusqueda_paginator.page(resultadoBusqueda_paginator.num_pages)
    
    contexto['resultadoBusqueda'] = resultadoBusqueda
    return render(request, "AppJuegos/Juegos/busquedaJuego.html", contexto)

###################################################################################################
#Fin de Vistas de Juego
###################################################################################################


###################################################################################################
#Vistas de Post
###################################################################################################

#Clase para detallar los posts
class VistaPost(DetailView):
    model = Post
    template_name = 'AppJuegos/Posts/post.html'

#Clase para crear los posts
class CrearPost(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostFormulario
    template_name = 'AppJuegos/Posts/nuevoPost.html'

#Clase para eliminar los posts
class EliminarPost(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'AppJuegos/Posts/eliminarPost.html'
    success_url = reverse_lazy('Blog')

#Clase para editar los posts
class EditarPost(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'AppJuegos/Posts/editarPost.html'
    form_class = PostEditFormulario


#Clase para agregar un nuevo comentario al post
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

###################################################################################################
#Fin de Vistas de Post
###################################################################################################


###################################################################################################
#Vistas de Consolas
###################################################################################################

#Clase para listar las consolas
class VistaConsolas(ListView):
    model = Consola
    template_name = 'AppJuegos/Consolas/listaConsolas.html'
    ordering = ['nombre']
    paginate_by = 3

#Clase para detallar las consolas
class DetalleConsola(DetailView):
    model = Consola
    template_name = 'AppJuegos/Consolas/detalleConsola.html'

#Clase para crear nuevas consolas
class NuevaConsola(LoginRequiredMixin,CreateView):
    model = Consola
    form_class = ConsolaFormulario
    template_name = 'AppJuegos/Consolas/nuevaConsola.html'

#Clase para editar las consolas
class EditarConsola(LoginRequiredMixin,UpdateView):
    model = Consola
    template_name = 'AppJuegos/Consolas/editarConsola.html'
    form_class = ConsolaFormulario
    success_url = reverse_lazy('Consola')

#Clase para eliminar las consolas
class EliminarConsola(LoginRequiredMixin,DeleteView):
    model = Consola
    template_name = 'AppJuegos/Consolas/eliminarConsola.html'
    success_url = reverse_lazy('Consola')

#Función para buscar juegos con paginación
consolasPorPagina = 5

def buscarConsola(request):
    contexto = {}
    query = ""
    if request.GET:
        query = request.GET["compania"]
        contexto['query'] = str(query)
    
    resultadoBusqueda = Consola.objects.filter(compania__startswith=query)
    page = request.GET.get('page', 1)
    resultadoBusqueda_paginator = Paginator(resultadoBusqueda, consolasPorPagina)
    try:
        resultadoBusqueda = resultadoBusqueda_paginator.page(page)
    except PageNotAnInteger:
        resultadoBusqueda = resultadoBusqueda_paginator.page(consolasPorPagina)
    except EmptyPage:
        resultadoBusqueda = resultadoBusqueda_paginator.page(resultadoBusqueda_paginator.num_pages)
    
    contexto['resultadoBusqueda'] = resultadoBusqueda
    return render(request, "AppJuegos/Consolas/busquedaConsola.html", contexto)

###################################################################################################
#Fin de Vistas de Consolas
###################################################################################################