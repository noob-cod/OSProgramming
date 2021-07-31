"""
@Date: 2021/7/31 下午4:36
@Author: Chen Zhang
@Brief: 条件变量

1、概念
    条件变量类似于一种锁，当线程不满足条件时会进入休眠状态，当条件满足后会被唤醒

2、Python原语
    申请（创建）条件变量：condition = threading.Condition()  # 底层自动申请配套的互斥锁
    加锁：condition.acquire()  # 底层自动给互斥锁加锁
    解锁：condition.release()  # 底层自动给互斥锁解锁
    等待（线程睡眠）：condition.wait()
    通知（唤醒线程）：condition.notify()
"""

if __name__ == '__main__':
    pass
