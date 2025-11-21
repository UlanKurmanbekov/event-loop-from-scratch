# Event Loop From Scratch

A minimalist implementation of an async event loop in Python using generators and selectors. This project demonstrates the core concepts behind async I/O frameworks like `asyncio`.

## Purpose

This is an **educational project** designed to illustrate:
- How event loops work at a fundamental level
- Cooperative multitasking with Python generators
- I/O multiplexing with selectors to avoid blocking
- The basic architecture behind async frameworks

**Note:** This is NOT production-ready code. Use `asyncio` or similar libraries for real applications

## How It Works

The implementation consists of three main components:

### 1. **Generator-based Tasks**
```python
def server(loop: 'EventLoop') -> Generator[tuple[EventType, socket.socket], None, None]:
    # ...
    while True:
        yield EventType.READ, server_socket  # Suspend until socket is ready
        client_socket, addr = server_socket.accept()
        # ...
```

Each task is a generator that yields control back to the event loop when it needs to wait for I/O

### 2. **Event Loop Class**
```python
class EventLoop:
    def run(self):
        while True:
            while self.pending_tasks:
                # Process all ready tasks
            self._wait_for_io()  # Wait for I/O events
```

The event loop orchestrates all tasks, using selectors to efficiently wait for I/O operations

### 3. **I/O Multiplexing**
- Tasks register their sockets with the selector
- Selector monitors all sockets for readiness
- When a socket is ready, its task is moved back to the pending queue

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
class EventType(Enum):                 # READ/WRITE operations
    READ = auto()
    WRITE = auto()

def server(loop):                      # Accept connections
def handle_client(client_socket):     # Handle client requests

class EventLoop:                       # Main event loop
    def create_task(...)               # Add task to queue
    def _register_for_io(...)          # Register socket for I/O
    def _wait_for_io(...)              # Wait for ready sockets
    def run(...)                       # Run the loop
```

## Key Concepts Demonstrated

1. **Cooperative Multitasking**: Tasks voluntarily yield control
2. **I/O Multiplexing**: One thread handles multiple connections via selectors
3. **Generator Coroutines**: Generators as primitive async functions
4. **Event-Driven Architecture**: React to I/O readiness events
5. **Type Safety**: Full type annotations for clarity

## Learn More

To understand what's happening under the hood of async frameworks, read:
- David Beazley's ["Build Your Own Async"](http://www.dabeaz.com/coroutines/)
- [PEP 3156](https://www.python.org/dev/peps/pep-3156/) - Async I/O
- ["A Web Crawler With asyncio Coroutines"](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

## Limitations

This is a teaching tool with deliberate simplifications:
- Basic error handling (logs but continues)
- No timeout handling
- No graceful shutdown mechanism
- Messages must fit in a single recv()/send() call