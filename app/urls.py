from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('finish_task/<int:task_id>', views.finish_task, name='finish_task'),
    path('fb_webhook/', views.facebook_messenger_webhook, name='facebook_messenger_webhook'),
]