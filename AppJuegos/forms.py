from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from AppJuegos.models import Avatar, Comentarios, Post, Juego, Consola, Imagen
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import capfirst


###################################################################################################
#Formularios para Usuario
###################################################################################################
#Función para validar email antes de crear un usuario
def validate_email(request):
    if User.objects.filter(email = request).exists():
        raise ValidationError((f"{request} ya existe."))

#Función para validar un usuario antes de ser creado
def validate_user(request):
    if User.objects.filter(username = request).exists():
        raise ValidationError((f"{request} ya existe."))

#Formulario para registrar usuarios nuevos
class RegistrarUsuarioFormulario(UserCreationForm):
    username = forms.CharField(validators= [validate_user], widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(validators= [validate_email], widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget = forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Repetir la contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]
        help_texts = {
            "username": None,
            "first_name": None,
            "last_name": None,
            "email": None,
            "password1": None,
            "password2": None}

#Formulario para editar el nombre de los usuarios
class EditarNombreUsuarioFormulario(forms.ModelForm):
    username = forms.CharField(validators= [validate_user], widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ["username"]
        help_texts = {
            "username": None,
        }

#Formulario para editar los datos del usuario
class EditarUsuarioFormulario(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label="Nombre", widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Apellido", widget = forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ["first_name","last_name","email"]
        help_texts = {
            "first_name": None,
            "last_name": None,
            "email": None,
           }

#Formulario para login de usuario

class LoginFormulario(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': _("Credenciales incorrectas"),
        'inactive': _("Cuenta inactiva."),
    }
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginFormulario, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache





#Formulario para editar la password del usuario
class EditarPasswordFormulario(PasswordChangeForm):
    error_css_class = "Tiene erorres"
    error_messages = {"password_incorrect":"Contraseña incorrecta"}
    old_password=forms.CharField(required=True,label="Contraseña vieja", widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={"requeried":"La contraseña no puede ser vacía"})
    new_password1 = forms.CharField(required=True,label="Contraseña nueva", widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={"requeried":"La contraseña no puede ser vacía"})
    new_password1 = forms.CharField(required=True,label="Repetir la contraseña", widget=forms.PasswordInput(attrs={'class':'form-control'}),error_messages={"requeried":"La contraseña no puede ser vacía"})

###################################################################################################
#Fin Formularios para Usuario
###################################################################################################


###################################################################################################
#Formularios para Juego
###################################################################################################

#Formulario para Juegos nuevos
class JuegoFormulario(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ('nombre','fechaLanzamiento','compania','copiasCreadas','genero')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: Elden Ring'}),
            'fechaLanzamiento': forms.DateInput(attrs={'class':'form-control','placeholder':'DD/MM/AAAA'}),
            'compania': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: FromSoftware'}),
            'copiasCreadas': forms.NumberInput(attrs={'class':'form-control','placeholder':'Por ejemplo: 1000000'}),
            'genero': forms.TextInput(attrs={'class':'form-control','placeholder':'Por ejemplo: RPG'}),
        }

###################################################################################################
#Fin Formularios para Juego
###################################################################################################


###################################################################################################
#Formularios para Post
###################################################################################################

#Formulario para nuevo Post
class PostFormulario(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo','subtitulo','cuerpo','autor','consola','juego')
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class':'form-control'}),
            'autor': forms.TextInput(attrs={'class':'form-control','placeholder':'Autor','value':'','id':'blogGames','type':'hidden'}),
            'consola':forms.Select(attrs={'class':'form-control'}),
            'juego':forms.Select(attrs={'class':'form-control'}),
        }

#Formulario para editar Post
class PostEditFormulario(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo','subtitulo','cuerpo','consola','juego')
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'subtitulo': forms.TextInput(attrs={'class':'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class':'form-control'}),
            'consola':forms.Select(attrs={'class':'form-control'}),
            'juego':forms.Select(attrs={'class':'form-control'}),

        }

###################################################################################################
#Fin Formularios para Post
###################################################################################################


###################################################################################################
#Formularios para Consolas
###################################################################################################

#Formulario para consola nueva
class ConsolaFormulario(forms.ModelForm):
    class Meta:
        model = Consola
        fields = ('nombre','compania','fechaLanzamiento','precio','unidadesVendidas')
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Título'}),
            'compania': forms.TextInput(attrs={'class':'form-control'}),
            'fechaLanzamiento': forms.DateInput(attrs={'class':'form-control','placeholder':'DD/MM/AAAA'}),
            'precio': forms.NumberInput(attrs={'class':'form-control'}),
            'unidadesVendidas' : forms.NumberInput(attrs={'class':'form-control'}),
        }

###################################################################################################
#Fin Formularios para Consolas
###################################################################################################

###################################################################################################
#Formularios para Comentarios
###################################################################################################

#Formulario para comentario nuevo
class ComentarioFormulario(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ('titulo','cuerpo')
        widgets = {
            'autor': forms.TextInput(attrs={'class':'form-control','placeholder':'Autor','value':'','id':'blogGames','type':'hidden'}),
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class':'form-control'}),
        }

###################################################################################################
#Fin Formularios para Comentarios
###################################################################################################

###################################################################################################
#Formularios para Avatar
###################################################################################################

#Formulario para Avatar nuevo
class AvatarFormulario(forms.ModelForm):

    class Meta:
        model=Avatar
        fields=["user","imagen"]
        widgets = {
            "user":forms.TextInput(attrs={'value':'','id':'blogGames',"type":"hidden"}),
            "imagen":forms.FileInput()
            }

###################################################################################################
#Fin Formularios para Avatar
###################################################################################################


###################################################################################################
#Formularios para Imagen
###################################################################################################

#Formulario para Imagen nueva
class ImagenFormulario(forms.ModelForm):
    imagen = forms.FileField(label="Imagen")
    class Meta:
        model=Imagen
        fields=["nombre","imagen"]

###################################################################################################
#Formularios para Imagen
###################################################################################################