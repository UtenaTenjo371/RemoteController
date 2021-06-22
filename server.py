from PIL import ImageGrab
import socket
import threading
import time
import struct
import sys
import cv2
import json
import hashlib
import numpy as np
import win32api
import win32con

host = '0.0.0.0'
port = 8001

def socket_service():
    """
    创建套接字，监听socket通信请求，可以挂起的最大连接数量为5。
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
    except socket.error as e:
        print(e)
        sys.exit(1)
    print('Waiting connection...')

    #接收客户端连接时调用deal_data方法处理信息传输
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    """
    处理客户端连接，打印并返回连接信息
    Args:
        conn:客户端连接
        addr:客户端地址
    """
    print('Accept new connection from {0}'.format(addr))
    conn.send('Hi, Welcome to the server!'.encode())

    while True:
        try:
            resize_ratio = json.loads(get_msg(conn, 1024).decode())
            if resize_ratio.get('resize_ratio'):
                conn.send("client info confirm".encode())
                break
        except Exception as e:
            print(e)

    param = {
        'resize_ratio': resize_ratio.get('resize_ratio'),
        'conn': conn,
        'pos': (0, 0)
    }
    window_name = addr[0]
    cv2.namedWindow(window_name)
    #鼠标操作回调OnMouseMove函数
    cv2.setMouseCallback(window_name, OnMouseMove, param=param)

    while True:
        #获取消息头长度
        encode_header_len = get_msg(conn, 4)
        if not encode_header_len:
            break
        msg_header_length = struct.unpack('i', encode_header_len)[0]
        #获取消息头
        encode_header = get_msg(conn, msg_header_length)
        if not encode_header:
            break
        #json读取消息头中的信息，含msg_length,msg_md5
        msg_header = json.loads(encode_header.decode())
        #读取消息的图像数据
        img_data = recv_msg(conn, msg_header)
        if not img_data:
            break
        #判断md5加密后的图像数据是否与消息头中md5加密后的字符串匹配
        if hashlib.md5(img_data).hexdigest() != msg_header['msg_md5']:
            break
        #以uint8格式读入缓冲区的消息,cv2解析图片并显示
        msg_decode = np.frombuffer(img_data, np.uint8)
        img_decode = cv2.imdecode(msg_decode, cv2.IMREAD_COLOR)

        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) <= 0:
            break
        cv2.imshow(window_name, img_decode)
        key = cv2.waitKey(20)
        print(key) if key != -1 else None

    cv2.destroyAllWindows()
    conn.close()

def get_msg(conn, length):
    """
    接收客户端消息
    Args:
        conn:客户端连接
        addr:消息字节数
    Returns:接收到客户端指定长度的消息
    """
    try:
        return conn.recv(length)
    except socket.error as e:
        print(e)


def recv_msg(conn, msg_header):
    """
    接收消息主体部分图像
    Args:
        conn:客户端连接
        msg_header:json解析后的消息头
    Returns:接收到的图像数据
    """
    recv_size = 0
    img_data = b''
    while recv_size < msg_header['msg_length']:
        if msg_header['msg_length'] - recv_size > 10240:
            recv_data = get_msg(conn, 10240)
        else:
            recv_data = get_msg(conn, msg_header['msg_length']-recv_size)
        recv_size += len(recv_data)
        img_data += recv_data
    return img_data


def OnMouseMove(event, x, y, flags, param):
    """
    鼠标移动时，给客户端发送鼠标位置信息
    Args:
        event:鼠标事件
        x:鼠标x轴坐标
        y:鼠标y轴坐标
        flags:按键flag。
            1:cv2.EVENT_FLAG_LBUTTON
            2:cv2.EVENT_FLAG_RBUTTON,
            4:cv2.EVENT_FLAG_MBUTTON,
            8:cv2.EVENT_FLAG_CTRLKEY,
            16:cv2.EVENT_FLAG_SHIFTKEY,
            32:cv2.EVENT_FLAG_ALTKEY,
        param:默认参数
    """
    win32api.SetCursor(win32api.LoadCursor(0, win32con.IDC_ARROW ))

    conn = param['conn']
    screen_x = round(x * param['resize_ratio'][0])
    screen_y = round(y * param['resize_ratio'][1])

    if (screen_x, screen_y) == param['pos'] and event == 0 and flags == 0:
        pass
    else:
        param['pos'] = (screen_x, screen_y)
        msg = {'mouse_position': (screen_x, screen_y), 'event': event, 'flags': flags}
        try:
            conn.send(struct.pack('i', len(json.dumps(msg))))
            conn.send(json.dumps(msg).encode())
            #print('event: {},  x: {},  y: {}  flags: {}'.format(event, x, y, flags))
        except socket.error as e:
            print(e)


if __name__ == '__main__':
    socket_service()