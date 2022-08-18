from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    path('fb_webhook/', views.facebook_messenger_webhook, name='facebook_messenger_webhook'),
    path('lesson/<str:room_name>/', views.lesson_room, name='room'),
    path('profile', views.profile, name='profile'),
]