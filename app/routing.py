from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/lesson/<str:room_code>/', consumers.LessonConsumer.as_asgi()),
]
