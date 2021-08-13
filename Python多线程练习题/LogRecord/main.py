"""
@Date: 2021/8/13 下午9:12
@Author: Chen Zhang
@Brief:
"""
import sys
from utils import TraceLog


class Server:

    def log(self):
        print('start server')
        for i in range(100):
            print(i)
        print('end server')  # print的实现是调用sys.stdout.write()方法的结果


if __name__ == '__main__':
    traceLog = TraceLog('main.log')  # 在构造的时候，main.log已经处于被isFile()方法打开的状态，没有被关闭
    traceLog.start()  # 启动线程

    # 原始的sys.stdout指向控制台，如果把文件对象的引用赋值给sys.stdout，
    # 那么print调用的就是文件对象的write方法
    sys.stdout = traceLog
    sys.stderr = traceLog
    server = Server()
    server.log()  # print将会调用traceLog.write()方法
