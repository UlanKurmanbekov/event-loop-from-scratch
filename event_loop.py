import socket
import selectors
from collections import deque
from typing import Generator, Any
from enum import Enum, auto
import heapq
import time


class EventType(Enum):
    READ = auto()
    WRITE = auto()
    TIMER = auto()


class EventLoop:
    def __init__(self) -> None:
        self.selector = selectors.DefaultSelector()
        self.pending_tasks = deque()
        self._event_mapping = {
            EventType.READ: selectors.EVENT_READ,
            EventType.WRITE: selectors.EVENT_WRITE
        }
        self.timers = []

    def create_task(self, coro: Generator[tuple[EventType, Any], None, None]) -> None:
        self.pending_tasks.append(coro)

    def _register_for_io(
            self,
            sock: socket.socket,
            event_type: EventType,
            task: Generator[tuple[EventType, socket.socket], None, None]
    ) -> None:
        self.selector.register(fileobj=sock, events=self._event_mapping[event_type], data=task)

    def _wait_for_events(self, timeout: float | None = None) -> None:
        if not self.selector.get_map():
            if timeout is not None:
                time.sleep(timeout)
            return

        events = self.selector.select(timeout=timeout)

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
                    event_type, event_data = next(task)

                    if event_type == EventType.READ:
                        self._register_for_io(event_data, EventType.READ, task)
                    elif event_type == EventType.WRITE:
                        self._register_for_io(event_data, EventType.WRITE, task)
                    elif event_type == EventType.TIMER:
                        heapq.heappush(self.timers, (event_data, task))
                except StopIteration:
                    pass
                except Exception as e:
                    print(f"Task error: {e}")

            timeout = self._calculate_timeout()
            self._wait_for_events(timeout)
            self._process_timers()

    def sleep(self, delay):
        deadline = time.monotonic() + delay

        yield EventType.TIMER, deadline

    def _process_timers(self) -> None:
        now = time.monotonic()

        while self.timers and self.timers[0][0] <= now:
            _, task = heapq.heappop(self.timers)
            self.pending_tasks.append(task)

    def _calculate_timeout(self) -> None | int:
        if not self.timers:
            return None

        return max(0, self.timers[0][0] - time.monotonic())
