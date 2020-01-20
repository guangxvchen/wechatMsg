import itchat
from itchat.content import *

# 微信消息接收
from new_msg_util import not_friends, clean_not_friends, note_type, backup

not_send = []


# 不获取群信息
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True,
                     isGroupChat=False, isMpChat=True)
def new_year(msg):
    if msg['ToUserName'] == 'filehelper':
        groupUserName = itchat.search_chatrooms('uuuu')[0]['UserName']
        if '发送人' in msg['Content'][0:3]:
            # 要发送的消息
            # 所有好友
            users = itchat.get_friends(update=True)
            for user in users[1:]:
                # 好友备注
                userRemarkName = user['RemarkName']
                if '-' in userRemarkName:
                    # 昵称
                    petName = userRemarkName[userRemarkName.rindex('-') + 1:]
                    '''
                        发送信息格式大致为:
                        start: 
                        昵称:
                            祝福语
                        end;
                    '''
                    sendMsg = petName + ':\n' + text_br_index(msg['Content'][3:])
                    # 发送消息
                    itchat.send_msg(sendMsg, user['UserName'])
                else:
                    not_send.append(userRemarkName)
            print('所有用户数量: ' + str(len(users)))
        elif '发送群' in msg['Content'][0:3]:
            # 要发送的消息
            sendMsg = text_br_index(msg['Content'][3:])
            # 所有群
            groups = itchat.get_chatrooms()
            for group in groups:
                groupName = group['NickName']
                if '快乐一家人' == groupName or '幸福大家庭' == groupName:
                    # 不做处理
                    continue
                else:
                    # 对群内发送消息
                    toUserName = group['UserName']
                    itchat.send_msg(sendMsg, toUserName)
            print('所有群数量: ' + str(len(groups)))
        elif '非好友' == msg['Content']:
            # 获取非好友对象
            print(not_friends())
        elif '清空' == msg['Content']:
            # 获取非好友对象
            print(clean_not_friends())
        itchat.send_msg('未发送\n' + str(not_send), groupUserName)
    else:
        # 如果是接收到好友发送的消息, 则进行备份, 用户
        backup(msg)


# 不接收群信息
# 接收通知类型消息
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=False, isMpChat=True)
def get_note(msg):
    # 获取系统通知信息
    print(msg['Text'])
    note_type(msg)


# 去除首行换行
def text_br_index(msg):
    if '\n' in msg:
        if msg.index('\n') == 0:
            return msg[1:]
    return msg


# 微信登录
if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    itchat.run()
