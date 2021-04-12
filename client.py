import asyncio
import uuid


class AsyncronousClient:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.PORT = 8888
        self.HOST = ""
        self.client_id = uuid.uuid4()
        self.reader = None

    async def send_message(self, username, user_input):
        reader, writer = await asyncio.open_connection(self.HOST, self.PORT)

        # Sending message (id, message, username)
        message = (str(self.client_id)+","+str(user_input)+","+str(username))
        writer.write(message.encode())
        await writer.drain()

    async def receive_message(self, fut):
        data = await self.reader.read(1024)
        fut.set_result(data)

    async def handle_connection(self, username, HOST):
        self.HOST = HOST
        self.reader, writer = await asyncio.open_connection(self.HOST, self.PORT)
        print(f"Connected to ('{self.HOST}', {self.PORT})")

        # Sending connection message(id, conn_identifier, username)
        message = (str(self.client_id)+",RECEIVE,"+str(username))
        writer.write(message.encode())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if __name__ == "__main__":
    ac = AsyncronousClient()
