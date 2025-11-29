import socket
from typing import Generator

from event_loop import EventType, EventLoop


def server(loop: EventLoop) -> Generator[tuple[EventType, socket.socket], None, None]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()

    while True:
        yield EventType.READ, server_socket
        client_socket, addr = server_socket.accept()

        print(f'Connection: {addr}')
        loop.create_task(handle_client(client_socket))


def handle_client(client_socket: socket.socket) -> Generator[tuple[EventType, socket.socket], None, None]:
    try:
        while True:
            yield EventType.READ, client_socket
            request = client_socket.recv(4096)

            if not request:
                break
            else:
                response = b'Hello World!\n'

                yield EventType.WRITE, client_socket
                client_socket.send(response)
    finally:
        client_socket.close()


if __name__ == '__main__':
    loop = EventLoop()
    loop.create_task(server(loop))
    loop.run()
