from django.urls import path

from . import views

app_name='horario'
urlpatterns = [
    path('', views.index, name='index'),
    path('gerarhorario', views.gerarhorario, name='gerarhorario'),
    path('horarios/', views.HorarioListView.as_view(), name='horarios'),
    path('horarios/<int:pk>', views.horario, name='horario'),
]