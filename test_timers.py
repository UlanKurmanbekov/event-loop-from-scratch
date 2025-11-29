from event_loop import EventLoop
import time


def task1():
    print(f"Task 1 start: {time.monotonic():.2f}")
    yield from loop.sleep(3)
    print(f"Task 1 end: {time.monotonic():.2f}")


def task2():
    print(f"Task 2 start: {time.monotonic():.2f}")
    yield from loop.sleep(1)
    print(f"Task 2 end: {time.monotonic():.2f}")


def task3():
    print(f"Task 3 start: {time.monotonic():.2f}")
    yield from loop.sleep(2)
    print(f"Task 3 end: {time.monotonic():.2f}")


if __name__ == '__main__':
    loop = EventLoop()
    loop.create_task(task1())
    loop.create_task(task2())
    loop.create_task(task3())
    loop.run()
