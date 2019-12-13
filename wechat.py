# coding:utf-8
import threading
import time

import itchat
from itchat.content import *

# 微信消息接收
from wechat_msg_backup import note_type, backup
from wechat_push import msg_type


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=False, isMpChat=True)
def get_msg(msg):
    print('获取微信消息')
    msg_type(msg)
    backup(msg)


# 接收通知类型消息
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=False, isMpChat=True)
def get_note(msg):
    print('获取通知文本')
    note_type(msg)


# 存活
def alive():
    msg = time.strftime("%Y-%m-%d %H:%M.%S", time.localtime())
    print(msg)
    itchat.send_msg(msg, 'filehelper')
    keep_alive()


# 定时
def keep_alive():
    global timer
    timer = threading.Timer(60 * 60 * 5, alive)  # 每 5 小时执行一次
    timer.start()


# 微信登录
if __name__ == '__main__':
    keep_alive()
    itchat.auto_login(hotReload=True)
    itchat.run()
