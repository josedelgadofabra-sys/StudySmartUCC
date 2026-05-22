# Generated manually for avance frontend/backend académico
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crud_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('color', models.CharField(default='#0d6efd', max_length=20)),
                ('creado_el', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('carrera', models.CharField(blank=True, max_length=120)),
                ('metas', models.TextField(blank=True)),
                ('creado_el', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SesionEstudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutos', models.PositiveIntegerField(default=25)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('creado_el', models.DateTimeField(auto_now_add=True)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud_app.materia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha_entrega', models.DateField()),
                ('horas_estimadas', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('horas_estudiadas', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En proceso'), ('completada', 'Completada')], default='pendiente', max_length=20)),
                ('creado_el', models.DateTimeField(auto_now_add=True)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud_app.materia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
