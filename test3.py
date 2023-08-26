import time

# 创建一个时间元组，表示2021年1月1日0时0分0秒
time_tuple = (2023, 8, 19, 16, 40, 0, 0, 0, 0)

# 将时间元组转换为时间戳
timestamp_past = time.mktime(time_tuple)
timestamp_now = time.time()
# 输出时间戳pr
range = 7 * 24 * 60 * 60
print(timestamp_now - timestamp_past)
if timestamp_now - timestamp_past < range:
    print(True)
else:
    print(False)