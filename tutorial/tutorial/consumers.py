import json
import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Carrera, Libro, Autor

class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print(f"Nueva conexión WebSocket desde {self.scope['client'][0]}:{self.scope['client'][1]}")
        await self.channel_layer.group_add("biblioteca_updates", self.channel_name)
        await self.accept()
        
        # Enviar datos iniciales de carreras y autores
        await self.send_initial_data()
        
    async def send_initial_data(self):
        try:
            # Enviar lista de autores
            autores = await self.getAutores()
            data_autores = [{'nombre': a.nombre, 'apellido': a.apellido, 'id': a.id} for a in autores]
            
            # Enviar lista de carreras
            carreras = await self.getCarreras()
            data_carreras = [{'nombre': c.nombre, 'descripcion': c.descripcion, 'id': c.id} for c in carreras]
            
            # Enviamos todo junto
            await self.send(text_data=json.dumps({
                'type': 'initial_data',
                'autores': data_autores,
                'carreras': data_carreras
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': f"Error al cargar datos iniciales: {str(e)}"
            }))
        
    async def disconnect(self, close_code):
        print(f"Desconexión WebSocket desde {self.scope['client'][0]}:{self.scope['client'][1]}")
        await self.channel_layer.group_discard("biblioteca_updates", self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                data = json.loads(text_data)
                print(f"MyConsumer recibió: {data}")
                
                # Manejar heartbeats para mantener la conexión viva
                if data.get("type") == "heartbeat":
                    print(f"Heartbeat recibido de {self.scope['client'][0]}:{self.scope['client'][1]}")
                    await self.send(text_data=json.dumps({
                        'type': 'heartbeat_response',
                        'status': 'ok',
                        'timestamp': str(datetime.datetime.now())
                    }))
                    return
                
                # Manejar solicitud específica de datos
                if data.get("type") == "request_data":
                    if data.get("entity") == "carreras":
                        carreras = await self.getCarreras()
                        data_carreras = [{'nombre': c.nombre, 'descripcion': c.descripcion, 'id': c.id} for c in carreras]
                        await self.send(text_data=json.dumps({
                            'type': 'carrera_list',
                            'message': data_carreras
                        }))
                        return
                    elif data.get("entity") == "autores":
                        autores = await self.getAutores()
                        data_autores = [{'nombre': a.nombre, 'apellido': a.apellido, 'id': a.id} for a in autores]
                        await self.send(text_data=json.dumps({
                            'type': 'autor_list',
                            'message': data_autores
                        }))
                        return
                
            except json.JSONDecodeError:
                await self.send(text_data=json.dumps({
                    'error': 'Formato JSON inválido'
                }))
            except Exception as e:
                print(f"Error en MyConsumer: {e}")
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

    @database_sync_to_async
    def getAutores(self):
        return list(Autor.objects.all())

class RemoteDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "remote_data_group",
            self.channel_name
        )
        print(f"Nueva conexión RemoteDataConsumer desde {self.scope['client'][0]}:{self.scope['client'][1]}")
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "remote_data_group", 
            self.channel_name
        )
        print(f"Desconexión RemoteDataConsumer desde {self.scope['client'][0]}:{self.scope['client'][1]}")
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"RemoteDataConsumer recibió: {data}")
            
            # Manejar heartbeats
            if data.get("type") == "heartbeat":
                await self.send(text_data=json.dumps({
                    'type': 'heartbeat_response',
                    'status': 'ok',
                    'timestamp': str(datetime.datetime.now())
                }))
                return
            
            # Solicitud de datos de carreras
            if data.get("type") == "request_data":
                if data.get("entity") == "carreras":
                    carreras = await self.get_carreras()
                    await self.send(text_data=json.dumps({
                        'message': carreras,
                        'entity': 'carreras',
                        'type': 'carrera_list'
                    }))
                elif data.get("entity") == "movies":
                    # Esta parte se maneja en el frontend conectándose directamente
                    await self.send(text_data=json.dumps({
                        'type': 'request_forwarded',
                        'entity': 'movies',
                        'status': 'ok'
                    }))
                    
            # Agregar manejo para crear/editar/eliminar carreras remotas
            elif data.get('type') == 'crear_carrera':
                # Aquí necesitarás implementar la lógica para crear carreras remotamente
                # O enviar la petición al otro servidor
                await self.send(text_data=json.dumps({
                    'type': 'carrera_operation',
                    'operation': 'crear',
                    'status': 'not_implemented',
                    'message': 'Funcionalidad no implementada'
                }))
                
            elif data.get('type') == 'editar_carrera':
                await self.send(text_data=json.dumps({
                    'type': 'carrera_operation',
                    'operation': 'editar',
                    'status': 'not_implemented',
                    'message': 'Funcionalidad no implementada'
                }))
                
            elif data.get('type') == 'eliminar_carrera':
                await self.send(text_data=json.dumps({
                    'type': 'carrera_operation',
                    'operation': 'eliminar',
                    'status': 'not_implemented',
                    'message': 'Funcionalidad no implementada'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Formato JSON inválido'
            }))
        except Exception as e:
            print(f"Error en RemoteDataConsumer: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
    
    @sync_to_async
    def get_carreras(self):
        # Obtener todas las carreras y serializarlas
        carreras = Carrera.objects.all()
        data = []
        for carrera in carreras:
            data.append({
                'id': carrera.id,
                'nombre': carrera.nombre,
                'descripcion': carrera.descripcion
            })
        return data
    
    async def remote_data_update(self, event):
        # Enviar actualización a los clientes conectados
        await self.send(text_data=json.dumps({
            'type': 'update',
            'entity': event['entity'],
            'data': event['data']
        }))

class RemoteCarreraConsumer(AsyncWebsocketConsumer):
    """
    Consumer para conectarse a un servidor remoto y recibir datos de carreras
    """
    
    async def connect(self):
        await self.accept()
        print(f"Nueva conexión RemoteCarreraConsumer desde {self.scope['client'][0]}:{self.scope['client'][1]}")
        
    async def disconnect(self, close_code):
        print(f"Desconexión RemoteCarreraConsumer desde {self.scope['client'][0]}:{self.scope['client'][1]}")
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"RemoteCarreraConsumer recibió: {data}")
            
            # Procesamos los datos recibidos del servidor remoto
            if data.get('type') == 'carrera_list':
                # Los datos de carreras han llegado del servidor remoto
                # Podemos procesarlos aquí si es necesario y reenviarlos al frontend
                await self.send(text_data=json.dumps(data))
            
            elif data.get('type') == 'heartbeat_response':
                # Simplemente reenviamos la respuesta del heartbeat
                await self.send(text_data=json.dumps(data))
            
            elif data.get('error'):
                # Si hay un error, lo reenviamos
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'error': data.get('error')
                }))
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Formato JSON inválido'
            }))
        except Exception as e:
            print(f"Error en RemoteCarreraConsumer: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))