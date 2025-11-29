# Event Loop From Scratch

A minimalist async event loop implementation in Python demonstrating how `asyncio` works internally.

## Purpose

Educational project illustrating:
- Event loop fundamentals with generators and selectors
- Cooperative multitasking without threads
- Timer-based scheduling (non-blocking sleep)
- I/O multiplexing for concurrent connections

**Not for production.** Use `asyncio` for real applications.

## Features

- Non-blocking I/O (READ/WRITE events)
- Timer support (sleep without blocking)
- Concurrent task execution
- Type-annotated

## How It Works

### Generator-Based Coroutines
Tasks are Python generators that yield control when waiting for events:
- `yield EventType.READ, socket` - pause until socket is readable
- `yield EventType.WRITE, socket` - pause until socket is writable  
- `yield EventType.TIMER, deadline` - pause until time is reached

### Event Loop Cycle
1. **Execute ready tasks** - run all tasks in the pending queue
2. **Register waits** - tasks yield events (I/O or timers) they're waiting for
3. **Calculate timeout** - find nearest timer deadline
4. **Wait for events** - `selector.select(timeout)` blocks until I/O or timeout
5. **Wake tasks** - move tasks with ready events back to pending queue
6. **Repeat** - process timers and return to step 1

The loop uses `selectors` for I/O multiplexing and `heapq` for timer scheduling.

## Usage

### TCP Server
```bash
python tcp_server.py
```

Test with multiple concurrent connections:
```bash
telnet localhost 8000
```

### Timer Test
```bash
python test_timers.py
```

Shows concurrent execution:
```
Task 1 start: 0.00
Task 2 start: 0.00
Task 3 start: 0.00
Task 2 end: 1.00    # Completes first despite starting last
Task 3 end: 2.00
Task 1 end: 3.00
```

## Project Structure
```
event_loop.py    # EventLoop and EventType
tcp_server.py    # TCP echo server example
test_timers.py   # Timer concurrency demo
```

## Key Concepts Demonstrated

1. **Cooperative Multitasking** - Tasks yield voluntarily
2. **I/O Multiplexing** - `selector.select()` monitors multiple sockets
3. **Timer Heap** - Efficient scheduling with `heapq`
4. **Generator Protocol** - `yield` suspends, `next()` resumes

## Learn More

- [David Beazley's Coroutines Course](http://www.dabeaz.com/coroutines/)
- [PEP 3156 - asyncio](https://www.python.org/dev/peps/pep-3156/)
- [500 Lines: asyncio Web Crawler](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

## Limitations

Teaching tool with simplifications:
- No task cancellation
- Basic error handling
- No graceful shutdown
- Single recv/send per operation