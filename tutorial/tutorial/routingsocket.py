from django.urls import path, re_path
from tutorial.consumers import MyConsumer, RemoteDataConsumer, RemoteCarreraConsumer

websocket_urlpatterns = [
    path('ws/test/', MyConsumer.as_asgi()),
    re_path(r'ws/remote-data/$', RemoteDataConsumer.as_asgi()),
    path('ws/remote-carreras/', RemoteCarreraConsumer.as_asgi()),
]
#