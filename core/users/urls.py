from django.urls import path
from users.views import auth
from users.views.profile import profile_update_view

urlpatterns = [
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('register/', auth.register_view, name='register'),
    path('profile/update/', profile_update_view, name='profile_update'),
]
