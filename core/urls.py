from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teste-digitacao/', views.digitacao, name='digitacao'),
    path('teste-personalidade/', views.personalidade, name='personalidade'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('candidato/<int:user_id>/', views.detalhes_candidato, name='detalhes_candidato'),
    path('api/save-typing-test/', views.save_typing_test, name='save_typing_test'),
    path('api/save-behavioral-test/', views.save_behavioral_test, name='save_behavioral_test'),
]