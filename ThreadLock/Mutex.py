"""
@Date: 2021/7/31 下午4:33
@Author: Chen Zhang
@Brief: 互斥锁

1、概念
    当线程访问临界资源时，互斥锁可以保证其他线程无法同时对临界资源进行操作，保证线程同步

2、Python互斥锁
    申请（创建）互斥锁： lock = threading.Lock()
    加锁： lock.acquire()
    解锁： lock.release()
"""

if __name__ == '__main__':
    pass
