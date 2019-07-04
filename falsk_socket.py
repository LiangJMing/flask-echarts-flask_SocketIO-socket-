from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import threading
import socket
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sercret!'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


@app.route('/')
def hello_1():
    fo = open("data/boundaries.txt", "r")
    data = []
    for line in fo:
        list1 = line.split()
        a, b = list1
        a = int(a)
        b = int(b)
        data.append([a, b])
    fo.close()
    # data = [[30, 0], [-50, 10], [-56.5, 20], [-46.5, 30], [-22.1, 40], [30, 0]]
    return render_template('line-draggable.html', data=data)


@app.route('/test')
def index():
    return render_template('test.html', async_mode=socketio.async_mode)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


def background_thread():
    while True:
        socketio.sleep(1)
        with open("data/boundaries.txt", "r") as fo:
            data = []
            for line in fo:
                list1 = line.split()
                a, b = list1
                a = int(a)
                b = int(b)
                data.append([a, b])
        socketio.emit('server_response',
                      {'data': data},
                      namespace='/test')


def background_thread2():
    IP_PORT = ('127.0.0.1', 9999)
    sk = socket.socket()
    sk.connect(IP_PORT)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    while True:
        data = sk.recv(1024)
        cmd, file_name, file_size = str(data, 'utf-8').split('|')
        #path = os.path.join(BASE_DIR, 'data', file_name)
        path = os.path.join(BASE_DIR, 'data', 'boundaries.txt')
        file_size = int(file_size)
        has_sent = 0
        with open(path, "wb") as fp:
            while has_sent != file_size:
                data = sk.recv(1024)
                fp.write(data)
                has_sent += len(data)
                print('\r' + '[保存进度]：%s%.02f%%' %
                      ('>' * int((has_sent / file_size) * 50), float(has_sent / file_size) * 100), end='')

        print('%s 保存成功！' % file_name)


class MyThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        background_thread2()


thread1 = MyThread(1, "Thread-1", 1)
if __name__ == "__main__":
    thread1.start()
    socketio.run(app)


