"""
@Date: 2021/7/31 下午4:29
@Author: Chen Zhang
@Brief:
"""
import time

from pool import ThreadPool
from task import Task, AsyncTask


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


def test_async_task():

    def async_process():
        num = 0
        for i in range(100):
            num += i
        return num

    # 1. 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()

    # 2. 生成一系列的任务
    for i in range(10):
        async_task = AsyncTask(func=async_process)
        test_pool.put(async_task)
        result = async_task.get_result()
        print('Get result:{}'.format(result))


def test_async_task2():
    """测试是否可以真正等待"""
    def async_process():
        num = 0
        for i in range(100):
            num += i
        time.sleep(1)
        return num

    # 1. 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()

    # 2. 生成一系列的任务
    for i in range(10):
        async_task = AsyncTask(func=async_process)
        test_pool.put(async_task)
        print('Acquire result in timestamp:{}'.format(time.time()))
        result = async_task.get_result()
        print('Get result in timestamp:{}'.format(time.time()))  # 时间相差1s
        print('Get result:{}'.format(result))


def test_async_task3():
    """没有等待是否也可以正常获取结果"""
    def async_process():
        num = 0
        for i in range(100):
            num += i
        return num

    # 1. 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()

    # 2. 生成一系列的任务
    for i in range(10):
        async_task = AsyncTask(func=async_process)
        test_pool.put(async_task)
        print('Acquire result in timestamp:{}'.format(time.time()))
        time.sleep(5)
        result = async_task.get_result()
        print('Get result in timestamp:{}'.format(time.time()))  # 时间相差1s
        print('Get result:{}'.format(result))


if __name__ == '__main__':
    # test()
    # test_async_task()
    # test_async_task2()
    test_async_task3()
