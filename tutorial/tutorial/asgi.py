"""
ASGI config for tutorial project.
¿que es asgi?

ASGI es un protocolo de intercambio de aplicaciones web para aplicaciones web basadas en Python.
que es son las siglas asgi?


It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Configura explícitamente la variable de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
django.setup()

# Importa después de configurar Django
from tutorial import routingsocket

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routingsocket.websocket_urlpatterns
        )
    ),
})