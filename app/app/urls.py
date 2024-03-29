from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings

from app import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
    path("profile/", views.TutorProfileView.as_view(), name="profile"),
    path(
        "tutor/reminders",
        views.TutorReminderUpdateView.as_view(),
        name="tutor-reminders",
    ),
    path("students/create/", views.StudentCreateView.as_view(), name="students-create"),
    path(
        "students/<int:pk>/delete/",
        views.StudentDeleteView.as_view(),
        name="students-delete",
    ),
    path(
        "students/<int:pk>/edit",
        views.StudentUpdateView.as_view(),
        name="students-edit",
    ),
    path(
        "students/create-from-csv/",
        views.StudentCreateFromCSVView.as_view(),
        name="student-create-from-csv",
    ),
    path("students/<int:pk>", views.StudentDetailView.as_view(), name="student-detail"),
    path("students/", views.StudentListView.as_view(), name="students"),
    path("lesson/<str:room_code>/", views.lesson_room, name="teaching-room"),
    path("lessons/create/", views.LessonCreateView.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/edit", views.LessonUpdateView.as_view(), name="lesson-edit"),
    path("lessons/", views.LessonListView.as_view(), name="lessons"),
    path(
        "change-payment-status",
        views.change_payment_status,
        name="change-payment-status",
    ),
]
