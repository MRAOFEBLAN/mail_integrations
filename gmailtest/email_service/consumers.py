from channels.consumer import AsyncConsumer




class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": "Hello from Django socket"
        })

    async def websocket_disconnect(self, event):
        pass

    async def send_messages(self):
        messages = Message.objects.all()  # Получаем все сообщения из базы данных
        serializer = MessageSerializer(messages, many=True)  # Сериализуем данные

        await self.send(text_data=json.dumps({
            'messages': serializer.data  # Отправляем сериализованные данные клиенту
        }))
