"""
@Date: 2021/7/31 下午4:29
@Author: Chen Zhang
@Brief: 基本任务对象

1、属性
    任务参数
    任务唯一标记（uuid）
    任务具体的执行逻辑，通过函数引用来传递
"""
import uuid


class Task:
    """基本任务对象"""
    def __init__(self, func, *args, **kwargs):
        # 任务的具体逻辑，通过函数引用传递
        self.callable = func  # 任务实际执行的函数
        self.id = uuid.uuid4()

        # 执行任务逻辑可能用到的参数
        self.args = args
        self.kwargs = kwargs  # 字典参数

    def __str__(self):
        return 'Task id:' + str(self.id)


def my_function():
    print('This is a task test.')


if __name__ == '__main__':
    task = Task(func=my_function)
    print(task)
