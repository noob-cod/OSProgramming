"""
@Date: 2021/8/13 下午9:13
@Author: Chen Zhang
@Brief: 工具类的实现

codecs模块
    （1）概述：codecs专门用作编码转换
    （2）常用方法：
        I. codecs.open(filename, mode='r', encoding=None, errors='strict', buffering=-1)
            对于应用来说，需要明确指定encoding的值，而errors和buffering使用默认值就可以了。

            举例：
                import codecs

                # 从文件读取数据
                # 步骤一：打开文件
                data = codecs.open('text.txt', encoding='UTF-8')

                # 步骤二：一行一行读取数据
                data1 = data.readline()
                print(data1)

                # 步骤三：关闭文件
                data.close()

        II. codecs.lookup(__encoding)
            该lookup()方法接收一个字符编码名称为参数，返回指定字符编码对应的encoder, decoder, StreamReader
            和StreamWriter的函数对象和类对象的引用

            举例：
                import codecs

                t = codecs.lookup('utf-8')  # 返回的t是一个四元组
                encoder = t[0]  # 元组第一个位置，指定字符编码的encoder函数对象引用
                decoder = t[1]  # 元组第二个位置，指定字符编码的decoder函数对象引用
                StreamReader = t[2]  # 元组第三个位置，指定字符编码的StreamReader类对象引用
                StreamWriter = t[3]  # 元组第四个位置，指定字符编码的StreamWriter类对象引用
"""
import codecs
from threading import Thread, Lock
import os


class TraceLog(Thread):

    def __init__(self, logName):
        super().__init__()
        self.logName = logName  # 日志名
        self.lock = Lock()  # 互斥锁
        self.contexts = []  # 保存要写入日志的信息
        self.isFile()  # 判断该日志名文件是否存在，若不存在则新建

    def isFile(self):
        if not os.path.exists(self.logName):
            with codecs.open(self.logName, 'w') as f:  # 以写入模式新建或打开文件
                f.write('This log name is: {0}\n'.format(self.logName))  # 写入控制信息
                f.write('start log\n')
            f.close()

    def write(self, context):
        self.contexts.append(context)

    def run(self):
        while True:
            self.lock.acquire()  # 加锁
            if len(self.contexts) != 0:
                with codecs.open(self.logName, 'a') as f:  # 以附加到文件末尾方式打开
                    for context in self.contexts:
                        f.write(context)
                f.close()
                del self.contexts[:]  # 写入完成后清空列表
            self.lock.release()  # 解锁


if __name__ == '__main__':
    pass
