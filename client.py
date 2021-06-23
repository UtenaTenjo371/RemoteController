from PIL import ImageGrab
from pynput.mouse import Controller, Button
import numpy as np
import socket
import sys
import cv2
import time
import struct
import json
import hashlib
import win32api
import win32con
import threading
# pyinstaller 打包时需添加 --hidden-import=pynput.keyboard._win32 --hidden-import=pynput.mouse._win32

resolution = (win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
resize = (1400, 800)


def socket_client(host, port):
    """
    与服务端建立连接
    Args:
        host:服务端地址
        port:服务端端口号
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print(s.recv(1024).decode())
    except socket.error as e:
        print(e)
        sys.exit(1)

    resize_ratio = (resolution[0]/resize[0], resolution[1]/resize[1])

    base_info = {
        'resize_ratio': resize_ratio
    }
    s.send(json.dumps(base_info).encode())
    while True:
        response = s.recv(1024)
        if response.decode() == "client info confirm":
            break

    receive_thread = threading.Thread(target=receive_mouse_msg, args=(s, ))
    receive_thread.start()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
    while True:
        flag, msg = make_screen_img(encode_param)
        if not flag:
            break
        flag = send_msg(s, msg)
        if not flag:
            break
        time.sleep(0.01)
    s.close()

def make_screen_img(encode_param):
    """
    cv2捕捉屏幕画面
    Args:
        encode_param:编码参数
    Returns:编码成jpg格式的屏幕图片
    """
    try:
        screen = ImageGrab.grab()
        #颜色空间转换, cv2.COLOR_RGB2BGR 将RGB格式转换成BGR格式
        bgr_img = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        #缩放图片
        img = cv2.resize(bgr_img, resize)
        #把当前图片img按照jpg格式编码
        return True, cv2.imencode(".jpg", img, encode_param)[1].tobytes()
    except Exception as e:
        print(e)
        return False, None


def get_msg_info(msg):
    """
    将发送给服务端的数据提取文件头
    Args:
        msg:待发送消息
    Returns:消息长度,md5加密后的编码
    """
    return len(msg), hashlib.md5(msg).hexdigest()


def make_msg_header(msg_length, msg_md5):
    """
    制作JSON编码后的消息头
    Args:
        msg_length:消息长度
        msg_md5:md5后加密的图片编码
    Returns:json后的消息长度及md5编码后的图片
    """
    header = {
        'msg_length': msg_length,
        'msg_md5': msg_md5
    }
    return json.dumps(header).encode()

def send_msg(conn, msg):
    """
    向服务端发送屏幕图像
    Args:
        conn:与服务端的连接
        msg:待发送消息
    Returns:发送消息是否成功
    """
    msg_length, msg_md5 = get_msg_info(msg)
    msg_header = make_msg_header(msg_length, msg_md5)
    msg_header_length = struct.pack('i', len(msg_header))
    try:
        header_len_res = conn.send(msg_header_length)
        header_res = conn.send(msg_header)
        msg_res = conn.sendall(msg)
        return True
    except socket.error as e:
        print(e)
        return False


def receive_mouse_msg(conn, ):
    """
    处理从服务端接收的鼠标信息
    Args:
        conn:与服务端的连接
    """
    mouse = Controller()
    while True:
        try:
            msg_length = struct.unpack('i', conn.recv(4))[0]
            mouse_msg = json.loads(conn.recv(msg_length).decode())
            mouse_position = mouse_msg.get('mouse_position')
            event = mouse_msg.get('event')
            flags = mouse_msg.get('flags')
            mouse_event(mouse, mouse_position[0], mouse_position[1], event, flags)
            print(mouse_position[0], mouse_position[1], event, flags)

        except Exception as e:
            print(e)
            break
    conn.close()

def mouse_event(mouse, x, y, event, flags):
    """
    映射服务端传来的鼠标事件
    Args:
        event:鼠标事件
        x:鼠标x轴坐标
        y:鼠标y轴坐标
        flags:按键flag
    """
    flag_event = get_flag_event(flags)
    mouse.position = (x, y)
    # 鼠标左键
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse.press(Button.left)
    elif event == cv2.EVENT_LBUTTONUP:
        mouse.release(Button.left)
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        mouse.click(Button.left, 2)
    # 鼠标中键
    elif event == cv2.EVENT_MBUTTONDOWN:
        mouse.press(Button.middle)
    elif event == cv2.EVENT_MBUTTONUP:
        mouse.release(Button.middle)
    elif event == cv2.EVENT_MBUTTONDBLCLK:
        mouse.click(Button.middle, 2)
    # 鼠标右键
    elif event == cv2.EVENT_RBUTTONDOWN:
        mouse.press(Button.right)
    elif event == cv2.EVENT_RBUTTONUP:
        mouse.release(Button.right)
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        mouse.click(Button.right, 2)


def get_flag_event(value):
    """
    识别flag代表的事件
    Args:
        value:待识别的参数
    Returns:value参数代表的鼠标键盘事件
    """
    flags = [
        cv2.EVENT_FLAG_LBUTTON, # 1
        cv2.EVENT_FLAG_RBUTTON, # 2
        cv2.EVENT_FLAG_MBUTTON, # 4
        cv2.EVENT_FLAG_CTRLKEY, # 8
        cv2.EVENT_FLAG_SHIFTKEY, # 16
        cv2.EVENT_FLAG_ALTKEY, # 32
    ]
    flag_events = []
    for flag in sorted(flags, reverse=True):
        if value >= flag:
            flag_events.append(flag)
            value -= flag
    return flag_events


if __name__ == '__main__':
    socket_client(server_host, server_port)