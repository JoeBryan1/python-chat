import asyncio
import socket
import re


class Server:
    def __init__(self):
        self.USER = 'USER'
        self.IS_TYPING = 'TYPING'
        self.NOT_TYPING = 'NOT TYPING'
        self.clients = []
        self.typing_clients = []

        self.interval = 1/120

    async def send_to_all(self, msg, client_list):
        for cl in self.clients:
            for user in client_list:
                user = ('"' + user[0] + '","' + msg + '","' + user[1] + '"')
                writer = cl[2]
                writer.write(user.encode())
                await writer.drain()
                await asyncio.sleep(1 / 120)

    async def handle_data(self, reader, writer):
        loop = asyncio.get_event_loop()
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
            client = [client_id, username, writer]
            print(username+" has connected!")
            self.clients.append(client)

            task = loop.create_task(self.send_to_all(self.USER, self.clients))
            await task
            task = loop.create_task(self.send_to_all(self.IS_TYPING, self.typing_clients))
            await task

        elif message == self.IS_TYPING:
            self.typing_clients.append([client_id, username])
            task = loop.create_task(self.send_to_all(self.IS_TYPING, self.typing_clients))
            await task

        elif message == self.NOT_TYPING:
            self.typing_clients.remove([client_id, username])
            task = loop.create_task(self.send_to_all(self.NOT_TYPING, self.typing_clients))
            await task

        else:
            print(username+': '+message)
            for client in self.clients:
                writer = client[2]
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
