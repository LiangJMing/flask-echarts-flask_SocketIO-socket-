import os
import time
import socket


def server():
    IP_PORT = ('0.0.0.0', 9999)
    sk = socket.socket()
    sk.bind(IP_PORT)
    sk.listen(0)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    print('服务开启成功！\n等待连接')

    while True:
        conn, addr = sk.accept()
        print("{0},{1}已连接".format(addr[0], addr[1]))

        while True:
            inp = input('>>>').strip()
            cmd, path = inp.split('|')
            path = os.path.join(BASE_DIR, path)
            file_name = os.path.basename(path)
            file_size = os.stat(path).st_size
            file_info = 'post|%s|%s' % (file_name, file_size)

            conn.sendall(bytes(file_info, 'utf-8'))

            has_sent = 0

            with open(path, 'rb') as fp:
                while has_sent != file_size:
                    data = fp.read(1024)
                    conn.sendall(data)

                    has_sent += len(data)

                    print('\r' + '[上传进度]：%s%.02f%%' %
                          ('>' * int((has_sent / file_size) * 50), float(has_sent / file_size) * 100), end='')

                    print('%s 上传成功' % file_name)


if __name__ =='__main__':
    server()