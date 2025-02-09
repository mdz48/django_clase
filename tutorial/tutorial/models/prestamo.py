from django.db import models

class Prestamo(models.Model):
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Préstamo de {self.libro.titulo} a {self.usuario.nombre}"