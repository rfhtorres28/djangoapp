import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapp.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(), # routes http requests to django view handles 
    'websocket': AuthMiddlewareStack (
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    )

})
