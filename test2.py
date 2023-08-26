import import_test
from enum import Enum
import import_test as tt
import json
import tqdm
from time import sleep
from concurrent import futures
if __name__ == "__main__":
    def sleep2():
        print('start sleep2')
        sleep(2)
        print('end sleep2')
        return 2

    def sleep4():
        print('start sleep 4')
        sleep(4)
        print('end sleep 4')
        return 4

    def sleep3():
        print('start sleep 3')
        sleep(3)
        print('end sleep 3')
        return 3

    def sleep1():
        print('start sleep 1')
        sleep(1)
        print('end sleep 1')
        return 1

    to_do = []
    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        future4 = executor.submit(sleep4)
        to_do.append(future4)
        future2 = executor.submit(sleep2)
        to_do.append(future2)
        future1 = executor.submit(sleep1)
        to_do.append(future1)
        future3 = executor.submit(sleep3)
        to_do.append(future3)

        # future = executor.submit(sleep4)
        # to_do.append(future)
        # future = executor.submit(sleep2)
        # to_do.append(future)
        # future = executor.submit(sleep1)
        # to_do.append(future)
        # future = executor.submit(sleep3)
        # to_do.append(future)

        done_iter = futures.as_completed(to_do)
        for future in done_iter:
            res = future.result()
            print(res)

