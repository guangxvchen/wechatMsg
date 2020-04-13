# coding:utf-8

import itchat


def send_receive_msg(msg):
    # 直接获取用户昵称
    # 如果是自己 / 不备份
    me = itchat.search_friends()['UserName']
    if msg['FromUserName'] == me:
        return
    msg_from_user_info = itchat.search_friends(userName=msg['FromUserName'])
    forName = str(msg_from_user_info['Sex']) + '-' + msg_from_user_info['RemarkName'] + '-' + msg_from_user_info['NickName'] + '-' + str(msg_from_user_info['Uin'])
    print(forName)

