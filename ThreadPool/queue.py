"""
@Date: 2021/7/31 下午4:28
@Author: Chen Zhang
@Brief: 线程安全的队列

1、概念
    用于存放多个元素，是存放各种元素的“池”。在存放线程时为线程池

2、什么是线程安全的队列
    （1）需要获取当前队列元素的数量
    （2）允许往队列中加入元素
    （3）允许从队列中取出元素
    （4）有多个线程同时访问队列元素时，保证多个线程获取的串行 -> 用锁保护队列
    （5）队列为空时，阻塞，等待队列不为空 -> 用条件变量等待队列元素
"""
import time
import threading


class ThreadSafeQueueException(Exception):
    pass


class ThreadSafeQueue:
    """线程安全的队列"""
    def __init__(self, max_size=0):
        """

        :param max_size:
        """
        self.queue = []  # 队列
        self.max_size = max_size  # 队列的最大长度，默认0表示无穷大
        self.lock = threading.Lock()  # 互斥量
        self.condition = threading.Condition()  # 条件量

    def size(self):
        """获取当前队列元素的数量"""
        self.lock.acquire()  # 加锁，防止读取size时产生访问冲突
        size = len(self.queue)
        self.lock.release()
        return size

    def put(self, item):
        """放入元素"""
        # 检查队列是否已满
        if self.max_size != 0 and self.size() > self.max_size:
            return ThreadSafeQueueException()

        # 添加元素到self.queue时使用互斥量保证线程安全
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()

        # 当队列为空时，条件量可通知阻塞的线程
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def batch_put(self, item_list):
        """批量放入元素"""
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.put(item)

    def pop(self, block=False, timeout=0):
        """从队列头部取出元素

        :param block: 当队列为空时是否阻塞地等待
        :param timeout: 如果阻塞的话，等待的时间
        """
        if self.size() == 0:
            # 需要阻塞等待
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None

        # 这里需要注意，保证判空与取出元素的组合操作的原子性
        self.lock.acquire()
        item = None
        if len(self.queue) > 0:  # 使用带互斥锁的self.size()方法会导致程序无法顺利执行
            item = self.queue[0]
            self.queue = self.queue[1:]  # 弹出队首元素
        self.lock.release()
        return item

    def get(self, index):
        """获取指定索引的元素"""
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item


if __name__ == '__main__':
    queue = ThreadSafeQueue(max_size=100)

    def producer():
        while True:
            queue.batch_put([1, 2, 3])
            time.sleep(5)

    def consumer():
        while True:
            item = queue.get(0)
            print('get item from queue: %d' % item)
            time.sleep(1)

    threading1 = threading.Thread(target=producer)
    threading2 = threading.Thread(target=consumer)
    threading1.start()
    threading2.start()
    threading1.join()
    threading2.join()
