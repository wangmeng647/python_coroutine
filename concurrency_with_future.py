import os
import time
import sys

import requests
from concurrent import futures
from time import sleep, strftime

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'
max_workers = 20


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
    return len(cc_list)


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many_concurrency(cc_list):
    workers = min(max_workers, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


def download_many_future(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print('scheduled for {}: {}'.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            print('{} result: {!r}'.format(future, res))
            results.append(res)

    return len(results)


def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


def display(*args):
    # print(strftime('[%H:%M:%S]'))
    print(*args)


def loiter(n):
    display('{}loiter({}): doing nothing for {}s...'.format('\t'*n, n, n))
    sleep(n)
    display('{}loiter({}): done.'.format('\t'*n, n))
    return n * 10


def main_experimenting_executor_map():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, [5,3,2,1,0])
    print('results:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))



if __name__ == '__main__':
    main_experimenting_executor_map()