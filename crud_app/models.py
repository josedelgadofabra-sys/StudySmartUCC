from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    carrera = models.CharField(max_length=120, blank=True)
    metas = models.TextField(blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class MateriaBase(models.Model):
    """Catálogo global de materias preestablecidas. No pertenece a ningún usuario."""
    CARRERAS = [
        ('sistemas', 'Ingeniería de Sistemas'),
        ('derecho', 'Derecho'),
        ('psicologia', 'Psicología'),
        ('contaduria', 'Contaduría Pública'),
        ('administracion', 'Administración de Empresas'),
        ('enfermeria', 'Enfermería'),
    ]

    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=150)
    semestre = models.PositiveSmallIntegerField(default=1)
    carrera = models.CharField(max_length=30, choices=CARRERAS, default='sistemas')

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} — {self.nombre}'


class Materia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    base = models.ForeignKey(MateriaBase, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=10, blank=True)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#0d6efd')
    semestre = models.PositiveSmallIntegerField(default=1)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.codigo} — {self.nombre}' if self.codigo else self.nombre


class Tarea(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('completada', 'Completada'),
    ]

    PRIORIDADES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='media'
    )

    fecha_programada = models.DateField(
        null=True,
        blank=True
    )

    horas_estimadas = models.DecimalField(max_digits=5, decimal_places=2, default=1)
    horas_estudiadas = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class SesionEstudio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    minutos = models.PositiveIntegerField(default=25)
    fecha = models.DateField(auto_now_add=True)
    creado_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.materia.nombre} - {self.minutos} minutos'

class EventoCalendario(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.tarea.titulo} - {self.fecha}"