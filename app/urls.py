from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('social-auth/', include('social_django.urls', namespace="social")),
    path('fb_webhook/', views.facebook_messenger_webhook, name='facebook_messenger_webhook'),

    path('lesson/<str:room_code>/', views.lesson_room, name='teaching-room'),
    path('profile', views.profile_view, name='profile'),

    path('students/create/', views.StudentCreateView.as_view(), name='students-create'),
    path('students/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/', views.StudentListView.as_view(), name='students'),

    path('lessons/create/', views.LessonCreateView.as_view(), name='lessons-create'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='lessons-detail'),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
]