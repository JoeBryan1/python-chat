import asyncio
import socket
import re

clients = []


class Server:
    def __init__(self):
        self.USER = 'USER'
        self.clients = []
        self.typing_clients = []

        self.interval = 1/120

    async def handle_data(self, reader, writer):

        data = await reader.read(1024)
        client_data = data.decode()

        # Client Data (id, message, username)
        client_data = re.split(r',(?=")', client_data)

        for n, i in enumerate(client_data):
            i = re.sub('"', '', i)
            client_data[n] = i

        client_id = client_data[0]
        message = client_data[1]
        username = client_data[2]

        if message == 'RECEIVE':
            client = [writer, client_id, username]
            print(username+" has connected!")
            self.clients.append(client)

            for cl in self.clients:
                for user in self.clients:
                    user = ('"'+user[1]+'","'+self.USER+'","'+user[2]+'"')
                    writer = cl[0]
                    writer.write(user.encode())
                    await writer.drain()
                    await asyncio.sleep(1/120)

        elif message == 'TYPING':
            for client in self.clients:
                writer = client[0]
                writer.write(data)
                await writer.drain()
                await asyncio.sleep(1 / 120)

        elif message == 'NOT TYPING':
            for client in self.clients:
                writer = client[0]
                writer.write(data)
                await writer.drain()
                await asyncio.sleep(1 / 120)

        else:
            print(username+': '+message)
            for client in self.clients:
                writer = client[0]
                writer.write(data)
                await writer.drain()

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_data, '0.0.0.0', 8888)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f'IP: {ip}')

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    s = Server()
    asyncio.run(s.start_server())
