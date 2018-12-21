import urllib.request
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

def getUserName(userCode):
    # user code를 이용해서 사용자 이름을 반환
    # ex> getUserName('UEUMV8TR7')
    #  -> 김준희
    token = ''
    url = 'https://slack.com/api/users.info?token=' + token + '&user=' + userCode
    return str(json.loads(BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser").get_text())['user']['real_name'])
def addUser(userCode):
    '''
    user code에 해당하는 사용자를 json 파일에 등록
    구조 : {
               'users': {
                           'UEUMV8TR7': {'name': '김준희', 'money': 20}
                           'UEWBQUVUP': {'name': '박병현', 'money': 30}
                        }
             }
     ex> addUser('UEUMV8TR7')
    '''
    userName = getUserName(userCode)
    money = 0
    bid = 1000
    ts = datetime.now().strftime('%Y-%m-%d')
    userList = dict()
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                return -2
            userList['users'][userCode] = {'name': userName, 'money': 0, 'bid': bid, 'ts': ts}
    except FileNotFoundError:
        userList = {'users': {userCode: {'name': userName, 'money': 0, 'bid': bid, 'ts': ts}}}
    except:
        return -1
    finally:
        with open('user_list.json', 'w') as file:
            file.write(json.dumps(userList))
    return 0

def delUser(userCode):
    userList = dict()
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                del userList['users'][userCode]
    except FileNotFoundError:
        return -1
    except:
        return -1
    finally:
        with open('user_list.json', 'w') as file:
            file.write(json.dumps(userList))
    return 0

def getUserInfo(userCode):
    '''
    user code에 해당하는 사용자 정보를 반환
    ex> getUserInfo('UEUMV8TR7')
     -> {'name': '김준희', 'money': 20}
    '''
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                return userList['users'][userCode]
            else:
                return None
    except FileNotFoundError:
        return None


def updateUserMoney(userCode, money):
    '''
    user code에 해당하는 사용자의 money 정보를 갱신
    ex> updateUserMoney('UEUMV8TR7', 30)
    '''
    userList = dict()
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                userList['users'][userCode] ['money'] += money
            else:
                return -1
    except FileNotFoundError:
        return -1
    finally:
        with open('user_list.json', 'w') as file:
            file.write(json.dumps(userList))
    return 0

def show_top10_users():
    temp = []
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
    except FileNotFoundError:
        return temp
    temp += sorted(userList['users'].items(), key=lambda x: x[1]['money'], reverse=True)
    return temp

def updateUserTime(userCode, ts):
    '''
        user code에 해당하는 사용자의 ts(timestamp) 정보를 갱신
        ex> updateUserTime('UEUMV8TR7', '20181220')
    '''
    userList = dict()
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                userList['users'][userCode]['ts'] = ts
            else:
                return -1
    except FileNotFoundError:
        return -1
    finally:
        with open('user_list.json', 'w') as file:
            file.write(json.dumps(userList))
    return 0

def updateUserbid(userCode, bid=0):
    '''
            user code에 해당하는 사용자의 bid 정보를 갱신
            ex> updateUserTime('UEUMV8TR7', 1000)
    '''
    userList = dict()
    try:
        with open('user_list.json', 'r') as file:
            userList = json.loads(file.read())
            if userCode in userList['users'].keys():
                if bid == 0:
                    userList['users'][userCode]['bid'] = 1000
                else:
                    userList['users'][userCode]['bid'] -= bid
            else:
                return -1
    except FileNotFoundError:
        return -1
    finally:
        with open('user_list.json', 'w') as file:
            file.write(json.dumps(userList))
    return 0

def main():
    pass


if __name__ == "__main__":
    main()
