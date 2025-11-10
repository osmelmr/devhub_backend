from django.db import models
from apps.users.models import User
import uuid

# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    tech_stack = models.JSONField(default=list)  # ej: ["React", "TypeScript"]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# STATUS_CHOICES: Define los posibles estados del proyecto (borrador o publicado)
# id: Identificador único del proyecto (UUID), clave primaria, no editable
# title: Nombre del proyecto, obligatorio, máximo 255 caracteres
# slug: URL amigable y único del proyecto, ej: /projects/todo
# description: Breve descripción del proyecto, obligatorio
# thumbnail: URL opcional de la imagen/miniatura representativa del proyecto
# tech_stack: Lista de tecnologías usadas en el proyecto, por defecto lista vacía
# status: Estado del proyecto, puede ser 'draft' o 'published', por defecto 'draft'
# created_by: Usuario que creó el proyecto, clave foránea hacia User
# created_at: Fecha de creación, generada automáticamente al crear el registro
# updated_at: Fecha de última actualización, se actualiza automáticamente al modificar
# __str__: Retorna el título del proyecto al convertir el objeto a cadena
