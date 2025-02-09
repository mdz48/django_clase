from django.db import models 

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    categoria = models.ForeignKey(
        'Categoria', 
        on_delete=models.CASCADE,
        null=True,  # Allow null values
        blank=True  # Allow blank in forms
    )
    
    def __str__(self):
        return self.titulo