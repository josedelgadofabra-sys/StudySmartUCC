from django import forms
from .models import (
    Producto,
    Perfil,
    Materia,
    Tarea,
    SesionEstudio
)


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'carrera', 'metas']


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'


# -------- TAREAS --------

class TareaForm(forms.ModelForm):

    class Meta:
        model = Tarea
        fields = [
            'materia',
            'titulo',
            'descripcion',
            'prioridad',
            'horas_estimadas'
        ]

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        if usuario:
            self.fields['materia'].queryset = Materia.objects.filter(
                usuario=usuario
            )


class TareaEditForm(forms.ModelForm):

    class Meta:
        model = Tarea
        fields = [
            'materia',
            'titulo',
            'descripcion',
            'prioridad',
            'fecha_programada',
            'horas_estimadas'
        ]

        widgets = {
            'fecha_programada': forms.DateInput(
                attrs={'type':'date'}
            )
        }

    def __init__(self,*args,usuario=None,**kwargs):

        super().__init__(*args,**kwargs)

        if usuario:
            self.fields[
                'materia'
            ].queryset = Materia.objects.filter(
                usuario=usuario
            )


# -------- POMODORO --------

class SesionEstudioForm(forms.ModelForm):

    class Meta:
        model = SesionEstudio
        fields = ['materia', 'minutos']

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        if usuario:
            self.fields['materia'].queryset = Materia.objects.filter(
                usuario=usuario
            )