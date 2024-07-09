from django.urls import re_path
from myapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server', consumers.QuizConsumer.as_asgi()),
    # Add more WebSocket URL patterns as needed
]