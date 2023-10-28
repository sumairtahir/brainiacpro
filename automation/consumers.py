import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OperationStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('operations_group', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def update_status(self, event):
        message = {
            'operation_id': event['operation_id'],
            'type': 'update_status',
            'status': event['status']
        }
        await self.send(text_data=json.dumps(message))
    
    async def update_iterations(self, event):
        message = {
            'operation_id': event['operation_id'],
            'type': 'update_iterations',
            'iteration_count': event['iteration_count'],
            'total_iterations': event['total_iterations'],
        }
        await self.send(text_data=json.dumps(message))
