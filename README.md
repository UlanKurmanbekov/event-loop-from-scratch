# Event Loop From Scratch

A minimalist implementation of an async event loop in Python using generators and `select()`. This project demonstrates the core concepts behind async I/O frameworks like `asyncio`

## Purpose

This is an **educational project** designed to illustrate:
- How event loops work at a fundamental level
- Cooperative multitasking with Python generators
- I/O multiplexing with `select()` to avoid blocking
- The basic architecture behind async frameworks

**Note:** This is NOT production-ready code. Use `asyncio` or similar libraries for real applications

## How It Works

The implementation consists of three main components:

### 1. **Generator-based Tasks**
```python
def server():
    while True:
        yield 'read', server_socket  # Suspend until socket is ready
        client_socket, addr = server_socket.accept()
        # ...
```

Each task is a generator that yields control back to the event loop when it needs to wait for I/O

### 2. **Event Loop**
```python
def event_loop():
    while any([pending_tasks, sockets_waiting_for_read, sockets_waiting_for_write]):
        # Use select() to wait for ready sockets
        # Resume tasks when their sockets are ready
```

The event loop orchestrates all tasks, using `select()` to efficiently wait for I/O operations

### 3. **I/O Multiplexing**
- Tasks waiting for readable sockets go into `sockets_waiting_for_read`
- Tasks waiting for writable sockets go into `sockets_waiting_for_write`
- `select()` monitors all sockets and returns which ones are ready

## Usage

### Run the server:
```bash
python event_loop.py
```

### Test with telnet:
```bash
telnet localhost 8000
# Type anything and press Enter
# Server responds: Hello World!
```

### Test with multiple connections:
```bash
# Terminal 1
telnet localhost 8000

# Terminal 2
telnet localhost 8000

# Terminal 3
telnet localhost 8000
```

All connections are handled concurrently by a single thread

## Code Structure

```python
pending_tasks = deque()                # Tasks ready to run
sockets_waiting_for_read = {}          # Socket → Task mappings
sockets_waiting_for_write = {}         # Socket → Task mappings

def server():                          # Accept connections
def handle_client(client_socket):     # Handle client requests
def event_loop():                      # Main event loop
```

## Key Concepts Demonstrated

1. **Cooperative Multitasking**: Tasks voluntarily yield control
2. **I/O Multiplexing**: One thread handles multiple connections
3. **Generator Coroutines**: Generators as primitive async functions
4. **Event-Driven Architecture**: React to I/O readiness events

## Learn More

To understand what's happening under the hood of async frameworks, read:
- David Beazley's ["Build Your Own Async"](http://www.dabeaz.com/coroutines/)
- [PEP 3156](https://www.python.org/dev/peps/pep-3156/) - Async I/O
- ["A Web Crawler With asyncio Coroutines"](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

## Limitations

This is a teaching tool with deliberate simplifications:
- No error handling for connection errors
- No timeout handling
- No graceful shutdown
- Messages must be small enough to send in one send() call