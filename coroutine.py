import argparse
import inspect
import queue
import random
from time import sleep, time
import asyncio
import time
from functools import wraps
import sys
from inspect import getgeneratorstate
from contextlib import contextmanager
from collections import namedtuple


def demo():
    async def washing1():
        await asyncio.sleep(3)
        print('1finished')

    async def washing2():
        await asyncio.sleep(2)
        print('2finished')

    async def washing3():
        await asyncio.sleep(5)
        print('3finished')

    loop = asyncio.get_event_loop()

    task = [
        loop.create_task(washing1()),
        loop.create_task(washing2()),
        loop.create_task(washing3())
    ]
    loop.run_until_complete(asyncio.wait(task))
    loop.close()


async def main():
    print('22')
    await asyncio.sleep(1)
    print('33')






async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

#asyncio.run(main())


async def net():
    #return 42
    print(22)


async def mm():
    task = asyncio.create_task(net())
    await task


def consumer():
    status = True
    while True:
        n = yield status
        print("我拿到了{}!".format(n))
        if n == 3:
            status = False


def qq():
    print('qq')


def add():
    while True:
        a = yield 2


# try:
#     print(a[0])
#     #print(3)
# except:
#     print(2)
# else:
#     print(4)
#

# with open('aaa') as f:
#     print(2)


class LookingGlass:
    def __init__(self):
        self.x = 2

    def __enter__(self):
        import sys
        self.original_writ = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWO'

    def reverse_write(self, text):
        self.original_writ(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys
        sys.stdout.write = self.original_writ
        if exc_type is ZeroDivisionError:
            print('do not divide zero')
            return True


@contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 23
    sys.stdout.write = original_write

a = looking_glass()
# print(a.__dir__())
# print(a.__enter__())
# print(a.__exit__(None, None,None))
# with looking_glass() as what:
#     print('qwert')
#     print(what)
# print('123')


def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer



def average():
    total = 0.0
    count = 0
    ave = None
    while True:
        term = yield ave
        total += term
        count += 1
        ave = total / count


# ave = average()
# print(getgeneratorstate(ave))
# print(ave.send(1))
# print(ave.send(2))
# print(ave.send('qq'))
# print(ave.send(3))





class DemoEc(Exception):
    pass

def demo_ex():
    while True:
        x = yield
        if x is None:
            break
    return 'qwe'

# dem = demo_ex()
# next(dem)
# dem.send(3)
# try:
#     ss = dem.send(None)
# except StopIteration as exc:
#     print(exc)
#     print(exc.value)



def ge(x):
    for i in x:
        if isinstance(i, int):
            yield i
        else:
            yield from ge(i)

def ge1(x):
    for i in x:
        yield from i


def averager():
    total = 0.0
    count = 0
    ave = None
    while True:
        term = yield 1 / 0
        if term is None:
            break
        total += term
        count += 1
        ave = total / count
    return Result(count, ave)


def grouper(results, key):
    while True:
        results[key] = yield from averager()


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group,result.average, unit))


def main_fun(data):
    results = {}
    for key, value in data.items():
        group = grouper(results, key)
        next(group)
        for value in value:
            s = group.send(value)
        #group.send(None)
    print(results)
    report(results)


Result = namedtuple('result', 'count average')
Event = namedtuple('Event', ['time', 'proc', 'action'])
DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIM = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPARTURE_INTERVAL = 5

def taxi_process(ident, trips, start_time=0):
    time_ = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time_ = yield Event(time_, ident, 'pick up passenger')
        time_ = yield Event(time_, ident, 'drop off passenger')

    yield Event(time_, ident, 'going home')


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)

    def run(self, end_time):
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('end of events')
                break

            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('taxi:', proc_id, proc_id * '  ', current_event)
            active_proc = self.procs[proc_id]
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            print('end of simulation time: {} events pending'.format(self.events.qsize()))

def compute_duration(previous_action):
    if previous_action in ['leave garage', 'drop off passenger']:
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1 / interval)) + 1

def main_taxi(end_time=DEFAULT_END_TIM, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    if seed is not None:
        random.seed(seed)

    taxis = {i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERVAL) for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Taxi fleet simulator'
    )
    parser.add_argument('-e', '--end_time', type=int, default=DEFAULT_END_TIM, help='simulation end time')
    parser.add_argument('-t', '--taxis_number', type=int, default=DEFAULT_NUMBER_OF_TAXIS, help='number of taxis')
    parser.add_argument('-s', '--seed', type=int, default=3, help='random generator seed')
    args = parser.parse_args()
    main_taxi(args.end_time, args.taxis_number, args.seed)

