import socket
import selectors
from collections import deque
from typing import Generator
from enum import Enum, auto


class EventType(Enum):
    READ = auto()
    WRITE = auto()


def server(loop: 'EventLoop') -> Generator[tuple[EventType, socket.socket], None, None]:
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


class EventLoop:
    def __init__(self) -> None:
        self.selector = selectors.DefaultSelector()
        self.pending_tasks = deque()
        self._event_mapping = {
            EventType.READ: selectors.EVENT_READ,
            EventType.WRITE: selectors.EVENT_WRITE
        }

    def create_task(self, coro: Generator[tuple[EventType, socket.socket], None, None]) -> None:
        self.pending_tasks.append(coro)

    def _register_for_io(
            self,
            sock: socket.socket,
            event_type: EventType,
            task: Generator[tuple[EventType, socket.socket], None, None]
    ) -> None:
        self.selector.register(fileobj=sock, events=self._event_mapping[event_type], data=task)

    def _wait_for_io(self) -> None:
        events = self.selector.select()

        for key, _ in events:
            task = key.data
            self.selector.unregister(key.fileobj)
            self.create_task(task)

    def run(self) -> None:
        print('Event loop started...')

        while True:
            while self.pending_tasks:
                try:
                    task = self.pending_tasks.popleft()
                    op, sock = next(task)

                    if op == EventType.READ:
                        self._register_for_io(sock, EventType.READ, task)
                    elif op == EventType.WRITE:
                        self._register_for_io(sock, EventType.WRITE, task)
                except StopIteration:
                    pass
                except Exception as e:
                    print(f"Task error: {e}")

            self._wait_for_io()


if __name__ == '__main__':
    loop = EventLoop()
    loop.create_task(server(loop))
    loop.run()
