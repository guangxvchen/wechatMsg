# coding:utf-8
import os
import re
import time

import itchat

msg_information = {}
face_bug = None  # 针对表情包的内容


# 通知消息发送群


# 关于通知文本处理
def note_type(msg):
    if msg['Type'] == 'Note':  # 通知文本
        print('通知文本处理')
        # 撤回消息处理
        if '撤回了一条消息' in msg['Content']:
            print('撤回消息处理')
            backup_push(msg)
    else:
        backup(msg)


# 把消息备份起来
def backup(msg):
    print('消息备份')
    # if 'ActualNickName' in msg:
    #     msg_from = msg['ActualNickName']
    # else:
    # 直接获取用户昵称
    user_msg = itchat.search_friends(userName=msg['FromUserName'])
    msg_from = user_msg['NickName']  # if (user_msg['RemarkName'] == '') else user_msg['RemarkName']
    global face_bug
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    # print(msg['Type'])
    # print(msg['MsgId'])
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':  # 如果发送的消息是文本或者好友推荐
        msg_content = msg['Text']
        # print(msg_content)

    # 如果发送的消息是附件、视屏、图片、语音
    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" \
            or msg['Type'] == 'Picture' \
            or msg['Type'] == 'Recording':
        msg_content = msg['FileName']  # 内容就是他们的文件名
        msg['Text'](str(msg_content))  # 下载文件
    elif msg['Type'] == 'Card':  # 如果消息是推荐的名片
        msg_content = msg['RecommendInfo']['NickName'] + '的名片'  # 内容就是推荐人的昵称和性别
        if msg['RecommendInfo']['Sex'] == 1:
            msg_content += '性别为男'
        else:
            msg_content += '性别为女'
        # print(msg_content)
    elif msg['Type'] == 'Map':  # 如果消息为分享的位置信息
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()  # 内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':  # 如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
        msg_content = msg['Text']
        msg_share_url = msg['Url']  # 记录分享的url
        # print(msg_share_url)
    face_bug = msg_content

    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


# 这个是用于监听是否有消息撤回
def backup_push(msg):
    # 发送信息到通知群
    groupUserName = itchat.search_chatrooms('oooo')[0]['UserName']
    print('消息撤回')
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)  # 在返回的content查找撤回的消息的id
    old_msg = msg_information.get(old_msg_id)  # 得到消息
    # print(old_msg)
    if len(old_msg_id) < 11:  # 如果发送的是表情包
        itchat.send_msg(face_bug, groupUserName)
    else:  # 发送撤回的提示给文件助手
        msg_body = old_msg.get('msg_from') + ":\n" + time.strftime("%H:%M\n",
                                                                   time.localtime()) + "撤回" + old_msg.get(
            "msg_type") + "\n" + "\n" + old_msg.get('msg_content')
        # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
        if old_msg['msg_type'] == "Sharing":
            msg_body += "\n➣\n" + old_msg.get('msg_share_url')

        # 将撤回消息发送到文件助手
        itchat.send_msg(msg_body, groupUserName)
        # 有文件的话也要将文件发送回去
        if old_msg["msg_type"] == "Picture" \
                or old_msg["msg_type"] == "Recording" \
                or old_msg["msg_type"] == "Video" \
                or old_msg["msg_type"] == "Attachment":
            file = '@fil@%s' % (old_msg['msg_content'])
            itchat.send_msg(file, groupUserName)
            os.remove(old_msg['msg_content'])
        # 删除字典旧消息
        msg_information.pop(old_msg_id)
