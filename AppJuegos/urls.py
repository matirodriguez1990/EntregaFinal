from django.urls import path
from AppJuegos import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #URLs generales
    path("",views.VistaBlog.as_view(),name="Blog"),
    path("about/",views.about, name="About"),
    
    #URLs de Usuario
    path("usuario/login",views.loginRequest, name="Login"),
    path("usuario/registro",views.registro, name="Registro"),
    path("usuario/editar",views.editarUsuario, name="EditarUsuario"),
    path("usuario/editarNombre",views.editarNombreUsuario, name="EditarNombreUsuario"),
    path("usuario/password",views.editarPassword, name="EditarPassword"),
    path("usuario/logout",LogoutView.as_view(template_name="AppJuegos/Usuario/logout.html"), name="Logout"),
    path("usuario/avatar",views.subirAvatar, name="SubirAvatar"),
    path("usuario/listar/", views.VistaJugadores.as_view(), name="Jugador"),
    
    #URLs de Juego
    path("juego/listar/", views.VistaJuegos.as_view(), name="ListaJuegos"),
    path("juego/buscar/", views.buscarJuego, name="BuscarJuegos"),
    path("juego/detalle/<int:pk>",views.DetalleJuego.as_view(),name="DetalleJuego"),
    path("juego/editar/<int:pk>",views.EditarJuego.as_view(),name="EditarJuego"),
    path("juego/eliminar/<int:pk>",views.EliminarJuego.as_view(),name="EliminarJuego"),
    path("juego/nuevo",views.CrearJuego.as_view(),name="CrearJuego"),
    path("juego/imagen",views.subirImagen, name="SubirImagen"),
    
    #URLs de Post
    path("post/<int:pk>",views.VistaPost.as_view(),name="PostCompleto"),
    path("post/nuevo/",views.CrearPost.as_view(),name="CrearPost"),
    path("post/editar/<int:pk>",views.EditarPost.as_view(),name="EditarPost"),
    path("post/eliminar/<int:pk>",views.EliminarPost.as_view(),name="EliminarPost"),
    path("post/nuevoComentario/<int:pk>",views.NuevoComentario.as_view(),name="NuevoComentario"),
    
    #URLs de Consola
    path("consolas/lista/",views.VistaConsolas.as_view(),name="Consola"),
    path("consolas/nueva/",views.NuevaConsola.as_view(),name="NuevaConsola"),
    path("consolas/detalle/<int:pk>",views.DetalleConsola.as_view(),name="DetalleConsola"),
    path("consolas/editar/<int:pk>",views.EditarConsola.as_view(),name="EditarConsola"),
    path("consolas/detalle/<int:pk>/eliminar",views.EliminarConsola.as_view(),name="EliminarConsola"),
    path("consolas/buscar/", views.buscarConsola, name="BuscarConsolas"),    
]