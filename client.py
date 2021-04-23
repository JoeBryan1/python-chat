import asyncio
import uuid
import re


def construct_message(client_id, msg, username):
    message = ('"' + str(client_id) + '","' + str(msg) + ',"' + str(username) + '"')
    return message


class AsynchronousClient:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.PORT = 8888
        self.HOST = ""
        self.client_id = uuid.uuid4()
        self.reader = None
        self.RECEIVE = 'RECEIVE'

    async def send_message(self, username, msg):
        reader, writer = await asyncio.open_connection(self.HOST, self.PORT)

        # Sending message (id, message, username)
        message = construct_message(self.client_id, msg, username)
        writer.write(message.encode())
        await writer.drain()

    async def receive_message(self, fut):
        data = await self.reader.read(1024)

        data_list = re.split(r',(?=")', data.decode())

        for n, i in enumerate(data_list):
            i = re.sub('"', '', i)
            data_list[n] = i

        fut.set_result(data_list)

    async def handle_connection(self, username, host):
        self.HOST = host
        self.reader, writer = await asyncio.open_connection(self.HOST, self.PORT)
        print(f"Connected to ('{self.HOST}', {self.PORT})")

        # Sending connection message(id, conn_identifier, username)
        message = ('"'+str(self.client_id)+'","'+self.RECEIVE+'","'+str(username)+'"')
        writer.write(message.encode())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
if __name__ == "__main__":
    ac = AsynchronousClient()
