import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer, database_sync_to_async
from .models import Carrera

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Hola mundo!'}))
        
    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            json = json.loads(text_data)
            json["nombre"]
            
            @database_sync_to_async
            def crear_carrera(self, nombre, descripcion):
                carrera = Carrera.objects.create(nombre=nombre, descripcion=descripcion)
                carrera.save()
            