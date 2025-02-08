from django.db import models 

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey('Autor', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo