from ast import alias
from django.urls import path
from AppJuegos import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("",views.VistaBlog.as_view(),name="Inicio"),
    #path("juego/",views.juego, name="Juego"),
    path("jugador/",views.jugador, name="Jugador"),
    #path("consola/",views.consola, name="Consola"),
    path("about/",views.about, name="About"),
    #Usuario
    path("usuario/login",views.loginRequest, name="Login"),
    path("usuario/registro",views.registro, name="Registro"),
    path("usuario/editar",views.editarUsuario, name="EditarUsuario"),
    path("usuario/password",views.editarPassword, name="EditarPassword"),
    path("usuario/logout",LogoutView.as_view(template_name="AppJuegos/Usuario/logout.html"), name="Logout"),
    path("usuario/avatar",views.subirAvatar, name="SubirAvatar"),
    #Juego
    #path("juego/buscar/",views.buscarJuego),
    path("juego/listar/", views.VistaJuegos.as_view(), name="ListaJuegos"),
    path("juego/buscar/", views.BuscarJuego.as_view(), name="BuscarJuegos"),
    path("juego/detalle/<int:pk>",views.DetalleJuego.as_view(),name="DetalleJuego"),
    path("juego/editar/<int:pk>",views.EditarJuego.as_view(),name="EditarJuego"),
    path("juego/eliminar/<int:pk>",views.EliminarJuego.as_view(),name="EliminarJuego"),
    path("juego/nuevo",views.CrearJuego.as_view(),name="CrearJuego"),

    path("buscarJugador/",views.buscarJugador,),
    path("buscarConsola/",views.buscarConsola,),
    path("blog/",views.VistaBlog.as_view(),name="Blog"),
    path("post/<int:pk>",views.VistaPost.as_view(),name="PostCompleto"),
    path("nuevoPost/",views.CrearPost.as_view(),name="CrearPost"),
    path("editarPost/<int:pk>",views.EditarPost.as_view(),name="EditarPost"),
    path("post/<int:pk>/eliminar",views.EliminarPost.as_view(),name="EliminarPost"),
    path("post/<int:pk>/nuevoComentario/",views.NuevoComentario.as_view(),name="NuevoComentario"),
    #Consola
    path("consolas/lista/",views.VistaConsolas.as_view(),name="Consola"),
    path("consolas/nueva/",views.NuevaConsola.as_view(),name="NuevaConsola"),
    path("consolas/detalle/<int:pk>",views.DetalleConsola.as_view(),name="DetalleConsola"),
    path("consolas/editar/<int:pk>",views.EditarConsola.as_view(),name="EditarConsola"),
    path("consolas/detalle/<int:pk>/eliminar",views.EliminarConsola.as_view(),name="EliminarConsola"),    

]