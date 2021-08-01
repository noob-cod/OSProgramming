"""
@Date: 2021/7/31 下午4:28
@Author: Chen Zhang
@Brief: 线程池

1、什么是线程池
    （1）线程池是存放多个线程的容器。
    （2）CPU调度线程执行后，不会销毁线程，而是将线程放回线程池重复利用

2、为什么要使用线程池
    （1）线程是稀缺资源，不应该频繁创建与销毁，增加系统开销；
    （2）进行架构解耦，线程创建与业务处理解耦，更加优雅，易于复用和扩展
    （3）线程池是使用线程的最佳实践

3、任务处理线程的特点
    （1）需要不断从任务队列中取任务执行；
    （2）任务处理线程需要有一个标记，白哦及线程什么时候应该停止

4、实现任务处理线程必须的属性
    （1）基本属性（任务队列、标记）
    （2）线程执行的逻辑(run)
    （3）线程停止的方法(stop)

5、线程池的基本功能
    （1）存放多个任务处理线程
    （2）负责多个线程的启停
    （3）管理向线程池提交的任务，下发给线程去执行

6、线程池的实现属性
    （1）基本属性
    （2）提交任务（put, batch_put）
    （3）线程启停（start, join）
    （4）线程池大小(size)
"""
import threading
import psutil

from ThreadPool.task import Task
from ThreadPool.queue import ThreadSafeQueue


class ProcessThread(threading.Thread):
    """任务处理线程"""

    def __init__(self, task_queue, *args, **kwargs):
        super(ProcessThread).__init__(*args, **kwargs)
        self.dismiss_flag = threading.Event()  # 任务线程停止的标记
        self.task_queue = task_queue  # 任务队列（处理线程不断从队列取出任务处理）
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break

            task = self.task_queue.pop()
            if not isinstance(taks, Task):
                continue

            # 执行task实际逻辑（是通过函数调用引进来的）
            result = task.callable(*task.args, **task.kwargs)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()  # 停止线程


class ThreadPool:
    """线程池"""
    def __init__(self, size=0):
        if not size:
            size = psutil.cpu_count() * 2  # 约定线程池大小为CPU核心数的两倍（最佳实践）
        self.pool = ThreadSafeQueue(size)  # 线程池
        self.task_queue = ThreadSafeQueue()  # 任务队列

        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    def start(self):
        """启动线程池"""
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    def join(self):
        """停止线程池"""
        for i in range(self.pool.size()):  # 向线程池中的所有处理线程发送停止信号
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.pop()  # 从线程池中取出线程
            thread.join()  # 等待线程真正停止

    def put(self, item):
        """向线程池中提交任务"""
        if not isinstance(item, Task):
            raise TaskTypeErrorException()
        self.task_queue.put(item)

    def batch_put(self, item_list):
        """批量提交任务"""
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    def size(self):
        """获取线程池的尺寸"""
        return self.pool.size()


class TaskTypeErrorException(Exception):
    pass


if __name__ == '__main__':
    pass
