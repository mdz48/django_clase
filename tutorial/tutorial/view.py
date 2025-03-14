from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Carrera, Autor, Libro, Prestamo, Usuario, Categoria
from .views import FormCarrera, FormAutor, FormLibro, FormPrestamo, FormUsuario, FormCategoria, FormRegistro
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RegistroCreateViewPage(TemplateView):
    model = Usuario
    template_name = 'registro_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormRegistro(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormRegistro()
        context = { 'form': form }
        return self.render_to_response(context)

class CategoriaCreateViewPage(TemplateView):
    model = Categoria
    template_name = 'categoria_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormCategoria(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormCategoria()
        context = { 'form': form }
        return self.render_to_response(context)
    
class CategoriaDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        categoria.delete()
        return redirect('home')

class CategoriaEditarViewPage(TemplateView):
    template_name = 'categoria_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = FormCategoria(instance=categoria)
        return self.render_to_response({'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        categoria = get_object_or_404(Categoria, pk=pk)
        form = FormCategoria(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})

class UserCreateViewPage(TemplateView):
    model = Usuario
    template_name = 'usuario_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormUsuario()
        context = { 'form': form }
        return self.render_to_response(context)

class UserDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        usuario.delete()
        return redirect('home')

class UserEditarViewPage(TemplateView):
    template_name = 'usuario_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        form = FormUsuario(instance=usuario)
        return self.render_to_response({'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        form = FormUsuario(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})
    

class PrestamoCreateViewPage(TemplateView):
    model = Prestamo
    template_name = 'prestamo_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormPrestamo(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormPrestamo()
        context = { 'form': form }
        return self.render_to_response(context)
    
class PrestamoDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        prestamo.delete()
        return redirect('home')
    
class PrestamoEditarViewPage(TemplateView):
    template_name = 'prestamo_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = FormPrestamo(instance=prestamo)
        return self.render_to_response({'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        prestamo = get_object_or_404(Prestamo, pk=pk)
        form = FormPrestamo(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})

class LibroCreateViewPage(TemplateView):
    model = Libro
    template_name = 'libro_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormLibro(request.POST)
        if form.is_valid():
            libro = form.save()
            
            # AÑADE ESTE CÓDIGO - Enviar notificación WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "biblioteca_updates",
                {
                    "type": "biblioteca_update",
                    "event_type": "libro_creado",
                    "libro": {
                        "id": libro.id,
                        "titulo": libro.titulo,
                        "autor": str(libro.autor) if libro.autor else "Sin autor",
                        "fecha": str(libro.fecha_publicacion)
                    }
                }
            )
            
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormLibro()
        context = { 'form': form }
        return self.render_to_response(context)
    
class LibroDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return redirect('home')

class LibroEditarViewPage(TemplateView):
    template_name = 'libro_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        libro = get_object_or_404(Libro, pk=pk)
        form = FormLibro(instance=libro)
        return self.render_to_response({'form': form})
    def post(self, request, pk, *args, **kwargs):
        libro = get_object_or_404(Libro, pk=pk)
        form = FormLibro(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})
        
# @method_decorator(permission_required('tutorial.add_autor', login_url='home', raise_exception=True), name='dispatch')
class AuthorCreateViewPage(TemplateView):
    model = Autor
    template_name = 'autor_form.html'
    
    def post(self, request, *args, **kwargs):
        form = FormAutor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormAutor()
        context = { 'form': form }
        return self.render_to_response(context)
    
class AuthorDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        autor = get_object_or_404(Autor, pk=pk)
        autor.delete()
        return redirect('home')

class AuthorEditarViewPage(TemplateView):
    template_name = 'autor_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        autor = get_object_or_404(Autor, pk=pk)
        form = FormAutor(instance=autor)
        return self.render_to_response({'form': form, 
                                        'has_perm': request.user.has_perm('tutorial.change_autor'),
                                        'user_name' : request.user.username})
    @method_decorator(permission_required('tutorial.change_autor', login_url='home', raise_exception=True), name='dispatch')
    def post(self, request, pk, *args, **kwargs):
        autor = get_object_or_404(Autor, pk=pk)
        form = FormAutor(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})



class CarreraDeleteViewPage(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        carrera.delete()
        return redirect('home')
    

class CarreraCreateViewPage(TemplateView):
    model = Carrera
    form_class = FormCarrera
    template_name = 'carrera_form.html'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response(self.get_context_data(form=form))	
        
    def get(self, request, *args, **kwargs):
        form = FormCarrera()
        context = { 'form': form }
        return self.render_to_response(context)
    
class CarreraEditarViewPage(TemplateView):
    template_name = 'carrera_form.html'
    
    def get(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(instance=carrera)
        return self.render_to_response({'form': form})
    
    def post(self, request, pk, *args, **kwargs):
        carrera = get_object_or_404(Carrera, pk=pk)
        form = FormCarrera(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.render_to_response({'form': form})

class HomePageView(TemplateView):
    model = Carrera
    authorModel = Autor
    template_name = 'home.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["saludo"] = "Hola Mundo"
        context["lista"] = self.model.objects.all()    
        context["autor"] = self.authorModel.objects.all()
        context["libro"] = Libro.objects.all()
        context["usuario"] = Usuario.objects.all()
        context["prestamo"] = Prestamo.objects.all()
        context["categoria"] = Categoria.objects.all()
        
        return context

class AboutPageView(TemplateView):
    template_name = 'about.html'

def index(request):
    return HttpResponse("Hello, world. You're at the tutorial index. CTM")

class RemoteCarrerasView(TemplateView):
    """Vista para mostrar los datos remotos de carreras"""
    template_name = 'remote_carreras.html'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes pasar aquí cualquier dato adicional que necesites en la plantilla
        return context

class MultipleRemoteDataView(TemplateView):
    """Vista para mostrar los datos remotos de carreras y películas"""
    template_name = 'multiple_remote_data.html'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

