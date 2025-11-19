import socket
from select import select
from collections import deque

pending_tasks = deque()

sockets_waiting_for_read = {}
sockets_waiting_for_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8000))
    server_socket.listen()

    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()

        print(f'Connection: {addr}')
        pending_tasks.append(handle_client(client_socket))


def handle_client(client_socket):
    while True:
        yield 'read', client_socket
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = b'Hello World!\n'

            yield 'write', client_socket
            client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([pending_tasks, sockets_waiting_for_read, sockets_waiting_for_write]):

        if not pending_tasks:
            ready_to_read, ready_to_write, _ = select(
                sockets_waiting_for_read,
                sockets_waiting_for_write,
                []
            )

            for sock in ready_to_read:
                pending_tasks.append(sockets_waiting_for_read.pop(sock))

            for sock in ready_to_write:
                pending_tasks.append(sockets_waiting_for_write.pop(sock))

        try:
            task = pending_tasks.popleft()

            operation, sock = next(task)

            if operation == 'read':
                sockets_waiting_for_read[sock] = task
            elif operation == 'write':
                sockets_waiting_for_write[sock] = task
        except StopIteration:
            print('Done')


pending_tasks.append(server())
event_loop()
