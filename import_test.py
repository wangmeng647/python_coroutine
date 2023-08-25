import time
from tqdm import tqdm
from time import  sleep
import requests


if __name__ == '__main__':

    try:
        res = requests.request(method='post', url='http://www.qqqqqq.com')
    except requests.exceptions.HTTPError as e:
        print(e)

    print(res)