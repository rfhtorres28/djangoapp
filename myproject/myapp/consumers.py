import json
from channels.generic.websocket import AsyncWebsocketConsumer


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'default_room'  # Set a default room name
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


       
        await self.accept() # Accepts the websocket connection from the client side

        await self.send(text_data = json.dumps({'message': 'Connection has been established.', 'group_name':self.room_group_name }))


    async def disconnect(self, close_code):

     
        await self.send(text_data = json.dumps({'message': f'The connection has been disconnected{close_code}'}))
        print({'message': f'The connection has been disconnected{close_code}'})


    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

        await self.send(text_data = json.dumps({'type':'acknowledgment', 'message':'thanks for acknowledging'}))


    async def chat_message(self, event):
        message = event['message']

        await  self.send(text_data = json.dumps({
               'type':'chat',
              'message':message
             }))
        

    async def quiz_result(self, event):
        # Send quiz result to WebSocket
        await self.send(text_data=json.dumps({
            'type':event['type'],
            'message': event['message'],
            'username': event['username'],
            'subject': event['subject'],
            'score_percentage': event['score_percentage'],
            'user_pic': event['user_pic'],
            'difference': event['difference'],
        }))