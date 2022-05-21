from django.urls import path
from AppJuegos import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("",views.VistaBlog.as_view(),name="Inicio"),
    #path("juego/",views.juego, name="Juego"),
    path("jugador/",views.jugador, name="Jugador"),
    path("consola/",views.consola, name="Consola"),
    path("about/",views.about, name="About"),
    path("login",views.loginRequest, name="Login"),
    path("registro",views.registro, name="Registro"),
    path("editarUsuario",views.editarUsuario, name="EditarUsuario"),
    path("logout",LogoutView.as_view(template_name="AppJuegos/logout.html"), name="Logout"),
    path("buscarJuego/",views.buscarJuego,),
    path("buscarJugador/",views.buscarJugador,),
    path("buscarConsola/",views.buscarConsola,),
    path("juego/", views.VistaJuegos.as_view(), name="ListaJuegos"),
    #path(r"^(?P<pk>\d+)$",views.DetalleJuegos.as_view(),name="DetalleJuego"),
    #path(r"^editar/(?P<pk>\d+)$",views.EditarJuego.as_view(),name="EditarJuego"),
    #path(r"^borrar/(?P<pk>\d+)$",views.EliminarJuego.as_view(),name="EliminarJuego"),
    path("juego/<int:pk>",views.DetalleJuegos.as_view(),name="DetalleJuego"),
    path("editarJuego/<int:pk>",views.EditarJuego.as_view(),name="EditarJuego"),
    path("juego/<int:pk>/eliminar",views.EliminarJuego.as_view(),name="EliminarJuego"),
    path("blog/",views.VistaBlog.as_view(),name="Blog"),
    path("post/<int:pk>",views.VistaPost.as_view(),name="PostCompleto"),
    path("nuevoPost/",views.CrearPost.as_view(),name="CrearPost"),
    path("editarPost/<int:pk>",views.EditarPost.as_view(),name="EditarPost"),
    path("post/<int:pk>/eliminar",views.EliminarPost.as_view(),name="EliminarPost"),

]