"""
@Date: 2021/7/31 下午4:29
@Author: Chen Zhang
@Brief:
"""
import time

from pool import ThreadPool
from task import Task


class SimpleTask(Task):
    def __init__(self, callable):
        super(SimpleTask, self).__init__(callable)


def process():
    print('This is a SimpleTask callable function.')
    time.sleep(1)


def test():
    # 1. 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()

    # 2. 生成一系列的任务
    for i in range(10):
        simple_task = SimpleTask(process)

        # 3. 往线程池提交任务执行
        test_pool.put(simple_task)
    pass


if __name__ == '__main__':
    test()
