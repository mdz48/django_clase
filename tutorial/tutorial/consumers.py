# C:\Users\maxdi\Universidad\python\jango\tutorial\tutorial\consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Carrera, Libro

class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print(f"Nueva conexión WebSocket desde {self.scope['client'][0]}:{self.scope['client'][1]}")
        # Unirse al grupo "biblioteca_updates"
        await self.channel_layer.group_add("biblioteca_updates", self.channel_name)
        await self.accept()
        
        try:
            carr = await self.getCarreras()
            data = [{'nombre': c.nombre, 'descripcion': c.descripcion, 'id': c.id} for c in carr]
            await self.send(text_data=json.dumps({
                'message': data
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
        
    async def disconnect(self, close_code):
        # Abandonar el grupo al desconectar
        await self.channel_layer.group_discard("biblioteca_updates", self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                data = json.loads(text_data)
                
                # Manejar heartbeats para mantener la conexión viva
                if data.get("type") == "heartbeat":
                    await self.send(text_data=json.dumps({
                        'type': 'heartbeat_response',
                        'status': 'ok'
                    }))
                    return
                
                # Resto del código para manejar mensajes...
                
            except json.JSONDecodeError:
                await self.send(text_data=json.dumps({
                    'error': 'Formato JSON inválido'
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'error': str(e)
                }))
                
    # Método para recibir notificaciones de grupo
    async def biblioteca_update(self, event):
        # Enviar el mensaje al WebSocket
        print(f"Enviando actualización a cliente: {event}")
        await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def getCarreras(self):
        return list(Carrera.objects.all())