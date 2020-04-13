import itchat
from itchat.content import *
from utils.util_msg_backup import *
from utils.util_msg_forward import *


help = """
1 : 防撤回模式开启/关闭
"""


# 微信消息接收
# isGroupChat=False 关闭接收群消息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=False, isMpChat=True)
def receive_msg(msg):
    user_msg = itchat.search_friends(userName=msg['FromUserName'])
    # 处理发送接收的消息
    send_receive_msg(msg)
    if msg['ToUserName'] == 'filehelper':
        if '退出' in msg['Content']:
            print(msg['Content'])
            itchat.logout()
    else:
        # 如果是接收到好友发送的消息, 则进行备份, 用户
        backup_msg(msg)
        print(msg['Content'])


# 接收通知类型消息处理
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=False, isMpChat=True)
def get_note(msg):
    note_type(msg)


# 登陆成功函数调用
def lc():
    me = itchat.search_friends()
    itchat.send("欢迎使用", toUserName='filehelper')


# 登出操作函数调用
def ec():
    itchat.send("谢谢使用", toUserName='filehelper')


# 微信登录
if __name__ == '__main__':
    '''
    记住登陆状态 hotReload=True
    命令行二维码 enableCmdQR=True
    部分的linux系统命令行二维码 enableCmdQR=2
    登录 赋值方法到 loginCallback
    退出 赋值方法到 exitCallback
    '''

    itchat.auto_login(hotReload=True, loginCallback=lc, exitCallback=ec)
    itchat.run()
