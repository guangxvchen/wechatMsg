# coding:utf-8
import threading

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


def keep_alive():
    itchat.send_msg('alive', 'filehelper')
    global timer
    timer = threading.Timer(60 * 60 * 3, keep_alive)  # 每 3 小时发送一次
    timer.start()


# 微信登录
if __name__ == '__main__':
    timer = threading.Timer(60 * 10, keep_alive)
    timer.start()
    itchat.auto_login(hotReload=True)
    itchat.run()
