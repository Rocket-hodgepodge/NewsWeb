"""
访问量统计模块
Auth： TTC
Data: 2018-7-12 10:32
"""
import datetime
from functools import wraps
from threading import Thread

from redis import Redis, RedisError

from hodgepodge.settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_DB


def redis_error(fn):
    """
    Redis 连接错误处理装饰器
    :param fn:
    :return:
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except RedisError as e:
            print('错误' + str(e))
            return None

    return wrapper


class RedisControl(object):
    def __init__(self):
        self._redis = Redis(host=REDIS_HOST,
                            port=REDIS_PORT,
                            password=REDIS_PASSWORD,
                            db=REDIS_DB)

    @redis_error
    def set_access_total(self, date, total):
        self._redis.hset('access_total', date, total)

    @redis_error
    def get_access_total(self, date):
        total = self._redis.hget('access_total', date)
        if not total:
            total = 0
        else:
            total = total.decode('utf-8')
        return int(total) if total else 0


class StatisticsThread(Thread):
    def __init__(self):
        super().__init__()
        self._redis_control = RedisControl()

    def run(self):
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        total = self._redis_control.get_access_total(now_date)
        total += 1
        self._redis_control.set_access_total(now_date, total)

