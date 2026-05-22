# crud_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('perfil/', views.perfil, name='perfil'),
    path('materias/', views.materias, name='materias'),
    path('materias/eliminar/<int:pk>/', views.eliminar_materia, name='eliminar_materia'),
    path('tareas/', views.tareas, name='tareas'),
    path('tareas/editar/<int:pk>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/iniciar/<int:pk>/', views.iniciar_tarea, name='iniciar_tarea'),
    path('tareas/completar/<int:pk>/', views.completar_tarea, name='completar_tarea'),
    path('tareas/eliminar/<int:pk>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('planificador/', views.planificador, name='planificador'),
    path('pomodoro/', views.pomodoro, name='pomodoro'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registrarse/', views.register_user, name='register'),
    path('mover-tarea/', views.mover_tarea, name='mover_tarea'),
]
