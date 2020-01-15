# coding:utf-8

import itchat
import requests

from db_msg_type import *

meHelp = '''【提示信息】

add: 订阅【人民日报】【央视新闻】早班新闻
del: 取消订阅'''


def msg_type(msg):
    print('消息处理')
    if 49 == msg['MsgType']:
        if '来了！新闻早班车' in msg['Text'] or '早啊！新闻来了' in msg['Text']:
            title = msg['Text']
            url = short_url(msg['Url'], title).replace(':80', '')
            push(title, url)
    elif msg['Type'] == 'Text':
        friend = itchat.search_friends(userName=msg['FromUserName'])
        nickName = friend['NickName']
        # 如果是自己 / 不发送信息到通知群
        me = itchat.get_friends(update=True)[:1][0]['UserName']
        if msg['FromUserName'] != me:
            groupUserName = itchat.search_chatrooms('oooo')[0]['UserName']
            itchat.send_msg(nickName + ': \n\t' + msg['Text'], groupUserName)
        if msg['Text'] == 'add':
            del_users(nickName)
            itchat.send_msg('订阅成功: ' + nickName, msg['FromUserName'])
        elif msg['Text'] == 'del':
            ins_users(nickName)
            itchat.send_msg('取消成功: ' + nickName, msg['FromUserName'])
        else:
            itchat.send_msg(meHelp, msg['FromUserName'])


# 微信消息发送
def push(title, url):
    # 指定群的 UserName
    groupUserNames = get_group_username()
    # 指定好友的 UserName
    userUserNames = get_user_username()

    # 发送好友
    for user in userUserNames:
        # 用于首次发送提示信息
        itchat.send_msg(title, user)
        itchat.send_msg(url, user)
    # # 发送群组
    for group in groupUserNames:
        itchat.send_msg(title, group)
        itchat.send_msg(url, group)


# 获取指定群的 UserName # 用于发送信息
def get_group_username():
    groupName = get_groups()
    groupUserName = []
    for group_n in groupName:
        group = itchat.search_chatrooms(group_n)
        for gr in group:
            print(gr['NickName'])
            if gr['NickName'] in groupName:
                groupUserName.append(gr['UserName'])
    print('\ngroup')
    print(groupUserName)
    return groupUserName


# 获取所有好友的 UserName # 用于发送信息 # 排除指定不发送的人
def get_user_username():
    userName = get_users()
    userUserName = []
    users = itchat.get_friends()
    for user in users:
        if user['NickName'] in userName or user['RemarkName'] in userName:
            continue
        for name in userName:
            if name in user['NickName']:
                continue
            if name in user['RemarkName']:
                continue
        userUserName.append(user['UserName'])
    print('\nuser')
    print(userUserName)
    return userUserName


# 把长连接转换为短连接
def short_url(url, title):
    data = {'urlValue': url, 'title': title}
    baseUrl = 'http://localhost'
    rep = requests.post(baseUrl, json=data)
    return rep.json()['data']
