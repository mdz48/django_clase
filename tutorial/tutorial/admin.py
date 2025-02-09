from django.contrib import admin
from .models import Carrera, Autor, Libro, Prestamo, Usuario, Categoria

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'fecha_nacimiento']
    
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'descripcion', 'fecha_publicacion']
    
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['libro', 'usuario', 'fecha_prestamo', 'fecha_devolucion']
    
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'fecha_registro']
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    
     