# Remote Controller

基于Socket，CV2的远程控制

### 文件结构

- 服务端：server.py
- 服务端启动程序：server_start.py
- 客户端：client.py
- 客户端启动程序：client_start.py

### 工作原理

1. 服务端与客户端建立Socket通信，客户端连接服务端套接字，服务端给客户端发送欢迎信息。
2. 客户端向服务端发送屏幕尺寸信息，服务端确认后发送确认信息。
3. 客户端和服务端分别创建监听线程，处理对方发来的信息。
4. 客户端不断捕获自己屏幕，转化为jpg图像并压缩传给服务端。服务端监听线程展示图像。
5. 服务端记录并发送鼠标移动及按键事件，当不是静止状态时发送事件给客户端。客户端接收到事件信息后模拟服务端操作进行响应。
6. 不断重复4、5直至通信结束。

### 系统工作流程图

![流程图](\image\流程图.png)

### 通信协议

服务端向客户端发送鼠标事件：

​	msg_length（0-4字节）：表示下个消息长度的二进制数据

​	mouse_msg（msg_length字节）：json格式的鼠标事件信息。形如：{'mouse_position': (screen_x, screen_y), 'event': event, 'flags': flags}

客户端向服务端发送屏幕截图：

​	encode_header_len（0-4字节）：消息头长度的二进制数据

​	encode_header（encode_header_len字节）：json格式的消息头，含msg_length图像长度和msg_md5图像md5编码字段。形如：{'msg_length': msg_length,'msg_md5': msg_md5}

​	img_data（msg_length字节）：图像数据

### 使用的核心库

PIL.ImageGrab 捕获客户端画面

socket 服务端客户端通信

pynput.mouse.Controller, pynput.mouse.Button 映射鼠标键盘操作

threading 创建线程处理socket收到的消息

time 设置客户端发送画面间隔

struct 使用pack方法对传输的消息进行编码解码

cv2 获取服务端键盘鼠标操作，在服务端显示客户端屏幕，对客户端图片进行编码

json 格式化服务端客户端通信的数据

hashlib md5加密图像，判断图像在传输过程中是否被篡改

### 程序设计

#### server.py

##### socket_service()：

​	创建套接字，监听socket通信请求，可以挂起的最大连接数量为5。
​    Args:
​        host:本机ip地址
​        port:绑定端口号

##### deal_data(conn,addr)：

​    处理客户端连接，打印并返回连接信息
​    Args:
​        conn:客户端连接
​        addr:客户端地址

##### get_msg(conn, length):

​    接收客户端消息
​    Args:
​        conn:客户端连接
​        addr:消息字节数
​    Returns:接收到客户端指定长度的消息

##### recv_msg(conn, msg_header):

​    接收消息主体部分图像
​    Args:
​        conn:客户端连接
​        msg_header:json解析后的消息头
​    Returns:接收到的图像数据

##### OnMouseMove(event, x, y, flags, param):

​	鼠标移动时，给客户端发送鼠标位置信息
​    Args:
​        event:鼠标事件
​        x:鼠标x轴坐标
​        y:鼠标y轴坐标
​        flags:按键flag。
​            1:cv2.EVENT_FLAG_LBUTTON
​            2:cv2.EVENT_FLAG_RBUTTON,
​            4:cv2.EVENT_FLAG_MBUTTON,
​            8:cv2.EVENT_FLAG_CTRLKEY,
​            16:cv2.EVENT_FLAG_SHIFTKEY,
​            32:cv2.EVENT_FLAG_ALTKEY,
​        param:默认参数

#### client.py

##### socket_client(host, port):

​    与服务端建立连接
​    Args:
​        host:服务端地址
​        port:服务端端口号

##### make_screen_img(encode_param):

​    cv2捕捉屏幕画面
​    Args:
​        encode_param:编码参数
​    Returns:编码成jpg格式的屏幕图片

##### get_msg_info(msg):

​    将发送给服务端的数据提取文件头
​    Args:
​        msg:待发送消息
​    Returns:消息长度,md5加密后的编码

##### make_msg_header(msg_length, msg_md5):

​    制作JSON编码后的消息头
​    Args:
​        msg_length:消息长度
​        msg_md5:md5后加密的图片编码
​    Returns:json后的消息长度及md5编码后的图片

##### send_msg(conn, msg):

​    向服务端发送屏幕图像
​    Args:
​        conn:与服务端的连接
​        msg:待发送消息
​    Returns:发送消息是否成功

##### receive_mouse_msg(conn, ):

​    处理从服务端接收的鼠标信息
​    Args:
​        conn:与服务端的连接

##### mouse_event(mouse, x, y, event, flags):

​    映射服务端传来的鼠标事件
​    Args:
​        event:鼠标事件
​        x:鼠标x轴坐标
​        y:鼠标y轴坐标
​        flags:按键flag

##### get_flag_event(value):

​    识别flag代表的事件
​    Args:
​        value:待识别的参数
​    Returns:value参数代表的鼠标键盘事件