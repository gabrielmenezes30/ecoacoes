from django.urls import path
from . import views

app_name = 'grupos'

urlpatterns = [
    path('criar/', views.create_group, name='create_group'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/invite/', views.generate_invite, name='generate_invite'),
    path('entrar/<str:invite_code>/', views.join_group, name='join_group'),
    path('<int:pk>/adicionar-pontos/', views.add_points, name='add_points'),
]
