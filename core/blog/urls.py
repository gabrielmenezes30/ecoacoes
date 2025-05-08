from django.urls import path
from .feeds import LatestPostsFeed
from .views import noticias_sustentabilidade, index

urlpatterns = [
    # ... outras rotas
    path('', index, name='index'),
    path('rss/', LatestPostsFeed(), name='post_feed'),
    path('noticias-externas/', noticias_sustentabilidade, name='noticias_externas'),

]
