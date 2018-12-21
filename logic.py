from random import randint
from random import shuffle
from datetime import datetime
from collections import Counter
import time
import test2

def slot_test_play():
    result = [1,1,1,4,3,4,2,7,5]
    return result

# 유저가 돈을 빌린 시각과 현재 시각이 같은지 확인합니다.
# 현재 유저의 정보를 가져옵니다.
def bid_time_limit(userCode, inputbid):
    # 현재 시간을 가져옵니다.
    nowtime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    user = test2.getUserInfo(userCode)
    usertime = user['ts']
    inputbid = int(inputbid)
    if inputbid <= 0 :
        return "0 이하의 금액은 빌려올 수 없습니다."
    # 유저의 시간과 현재 시간이 같다면
    if str(nowtime) == usertime :
        if user['bid'] - inputbid < 0:
            return "일일 한도를 초과하는 액수입니다."
        else :
            test2.updateUserbid(userCode, inputbid)
            test2.updateUserMoney(userCode, inputbid)
            return "슬롯머신에게 {} 포인트를 빌렸습니다. \n".format(str(inputbid))
    # 다르다면
    else:
        test2.updateUserbid(userCode)
        test2.updateUserTime(userCode, nowtime)
        if user['bid'] - inputbid < 0 :
            return "일일 한도를 초과하는 액수입니다."
        else :
            test2.updateUserbid(userCode, inputbid)
            test2.updateUserMoney(userCode, inputbid)
            return "슬롯머신에게 {} 포인트를 빌렸습니다. \n".format(str(inputbid))


#랭킹을 사용자에게 보여줍니다.
def show_ranking():
    user_list = []
    temp = ""
    user_list = test2.show_top10_users()
    if len(user_list) == 0:
        return "등록된 사용자가 없습니다."
    for idx in range(0, len(user_list)):
        temp = temp + str(idx+1) + "등 : " + user_list[idx][1]['name'] + " / " +  str(user_list[idx][1]['money']) + "점 \n"
    return temp

# 돈을 넣은 슬롯머신을 돌립니다.
# 슬롯의 결과와 넣은 돈 * 획득 포인트를 리턴합니다.
def slot_playing(money):
    played = []
    result = ""
    point = 1
    played = slot_shuffle()
    # played = slot_test_play()
    point = slot_get_point(played)
    point = point * int(money)
    result = fruit_display_string(played)
    return result, point

# 슬롯머신을 돌립니다. int 형 숫자가 담긴 배열을 리턴합니다.
def slot_shuffle():
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 9):
        result[i] = randint(0, 8)
    temp = Counter(result)
    list1 = []
    max_val = 0
    max_key = 0
    min_val = 10
    min_key = 0
    for key, val in temp.items() :
        if max_val < val:
            max_val = val
            max_key = key
        if min_val > val:
            min_val = val
            min_key = key
        for i in range(0, val):
            list1.append(key)
    list1.append(max_key)
    list1.remove(min_key)
    shuffle(list1)
    return list1

# 슬롯머신의 배열을 받아 얼마의 득점을 하였는지 계산합니다.
def slot_get_point(slot_array):
    pow_point = 0
    #가로 아랫줄을 계산합니다.
    if slot_array[0] == slot_array[1] and slot_array[1] == slot_array[2]:
        pow_point = pow_point + slot_fruit_pow(slot_array[0])
    #가로 중간줄을 계산합니다.
    if slot_array[3] == slot_array[4] and slot_array[4] == slot_array[5]:
        pow_point = pow_point + slot_fruit_pow(slot_array[3])
    #가로 윗줄을 계산합니다.
    if slot_array[6] == slot_array[7] and slot_array[7] == slot_array[8]:
        pow_point = pow_point + slot_fruit_pow(slot_array[6])
    #세로 왼쪽줄을 계산합니다.
    if slot_array[0] == slot_array[3] and slot_array[3] == slot_array[6]:
        pow_point = pow_point + slot_fruit_pow(slot_array[0])
    #세로 중간줄을 계산합니다.
    if slot_array[1] == slot_array[4] and slot_array[4] == slot_array[7]:
        pow_point = pow_point + slot_fruit_pow(slot_array[1])
    #세로 오른쪽줄을 계산합니다.
    if slot_array[2] == slot_array[5] and slot_array[5] == slot_array[8]:
        pow_point = pow_point + slot_fruit_pow(slot_array[2])
    #왼쪽에서 오른쪽 위에서 아래의 대각선을 계산합니다.
    if slot_array[6] == slot_array[4] and slot_array[4] == slot_array[2]:
        pow_point = pow_point + slot_fruit_pow(slot_array[2])
    #왼쪽에서 오른쪽 아래에서 위의 대각선을 계산합니다.
    if slot_array[0] == slot_array[4] and slot_array[4] == slot_array[8]:
        pow_point = pow_point + slot_fruit_pow(slot_array[0])
    return pow_point

#슬롯머신의 과일을 받아 검사 후 몇 포인트인트 짜리 과일인지 돌려줍니다.
def slot_fruit_pow(fruit):
    point = 0
    #사과와 메론은 2포인트를 얻습니다.
    if fruit == 0:
        point = 2
    elif fruit == 1:
        point = 2
    #포도와 귤은 3포인트를 얻습니다.
    elif fruit == 2:
        point = 3
    elif fruit == 3:
        point = 3
    #레몬과 사과는 5포인트를 얻습니다.
    elif fruit == 4:
        point = 5
    elif fruit == 5:
        point = 5
    #복숭아는 7포인트를 얻습니다.
    elif fruit == 6:
        point = 7
    #체리는 9포인트를 얻습니다.
    elif fruit == 7:
        point = 9
    #럭키세븐은 15포인트를 얻습니다.
    elif fruit == 8:
        point = 15
    return point

# 슬롯머신의 사용법을 나타냅니다.
def how_to_play():
    how_to = '''
        kpbot 슬롯머신 입니다.

        How to Play...
        slot\t\t\t\t\t   : 현재 페이지를 출력합니다.
        slot register\t\t : 사용자를 등록합니다.
        slot rank\t\t\t  : 사용자들의 랭킹을 보여줍니다.
        slot wallet           : 현재 자신의 돈이 얼마나 있는지 보여줍니다.
        slot del                : 파산신청을 하여 모든 정보를 삭제합니다.
        slot play 숫자     : 슬롯머신에 <숫자> 만큼의 돈을 넣고 돌립니다.
        slot bid 숫자       : 슬롯머신에게 <숫자> 만큼의 돈을 빌립니다.'''
    return how_to

# 게임의 결과를 출력합니다..
# 이긴 결과는 중간 줄이 하나로 통일되어야 합니다.
# 게임의 결과는 항상 int 형 숫자가 담긴 배열로 리턴합니다.
def game_win(win_cost):
    temp_array = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    shuffle(temp_array)
    # win_cost의 숫자에 따라. 게임판에 배열할 과일을 지정합니다.
    # win_cost가 0이면 진 게임입니다.
    if win_cost == 0:
        pass
    elif win_cost == 1:
        temp = randint(0, 5)
    elif win_cost == 2:
        temp = randint(5, 7)
    elif win_cost == 3:
        temp = 7
    else:
        temp = 8
    # 진 게임이 아니라면, 과일을 중앙에 배치합니다.
    if win_cost != 0:
        temp_array[3] = temp
        temp_array[4] = temp
        temp_array[5] = temp
    return temp_array

# 해당 값을 받으면 표시할 과일을 보내줍니다.
def fruit_number(number):
    temp = [':watermelon:', ':melon:', ':grapes:', ':tangerine:', ':lemon:', ':apple:', ':peach:', ':cherries:',
            ':lucky_seven:']
    return temp[number]

# 과일을 표시할 string을 만들어 보내줍니다.
def fruit_display_string(number_array):
    temp = ""
    idx = 0
    for j in number_array:
        if (idx % 3) == 2:
            temp = temp + fruit_number(j) + '\n'
            idx = idx + 1
        else:
            temp = temp + fruit_number(j)
            idx = idx + 1
    return temp


def play_main(text, slack_user_code):
    # 들어온다고 가정하는 명령입니다.
    # text = "<@MENSIONNAME> slot bid 123\n"
    result = ""
    # 들어오는 text를 보기좋게 가공합니다.
    text = text.split()

    # 사용자가 명령한 문장을 가공합니다.
    # cmd 는 커맨드 이름, args 는 모든 인자를 받습니다.
    cmd = ""
    args = []

    # 로직에 쓰일 객체를 선언합니다.
    played = 0  # 랜덤함수로 나온 플레이 값입니다.
    game_result = 0  # 슬롯머신이 플레이 된 결과값을 정수로 받습니다.

    # 일단 모든 인자를 args 에 저장합니다.
    args = text[:]

    # args 인자의 2번째 텍스트는 사용자의 명령어입니다. cmd 에 저장합니다.
    if len(args) == 1:
        print('how_to_play')
        result = how_to_play()
        return result
    cmd = args[1]

    # 해당 명령어가 정확한지 검사합니다.
    if cmd != "slot" or len(args) > 4:
        result = "잘못된 명령이거나 들어오는 매개변수가 부정확합니다."
        return result  # 슬롯머신 루틴을 종료시켜야 합니다.
    else:
        # 명령어를 좀 더 다듬습니다. 뒤에 오는 개행문자를 제거합니다.
        args[-1] = args[-1].replace('\n', "")

        # 슬롯머신을 시작합니다..
        # 사용자에게 어떻게 사용하는지 보여줍니다.
        if len(args) == 2:
            print('how_to_play')
            result = how_to_play()
            return result
        #사용자에게 현재 랭킹을 보여줍니다.
        elif args[2] == 'rank' :
            return show_ranking()
        # 사용자를 등록합니다.# by jun
        elif args[2] == 'register':
                ret = test2.addUser(slack_user_code)
                if ret == 0:
                    user = test2.getUserInfo(slack_user_code)
                    result = '<@{}> 님 성공적으로 등록되었습니다.\n잔액 : {}     일일대출한도 : {}'.format(slack_user_code, user['money'], user['bid'])
                elif ret == -2:
                    user = test2.getUserInfo(slack_user_code)
                    result = '이미 등록된 사용자 입니다.\n<@{}> 님\n잔액 : {}     일일대출한도 : {}'.format(slack_user_code, user['money'], user['bid'])
                else:
                    result = '등록에 실패하였습니다.'
                return result
        # 사용자가 가진 돈이 얼마인지 보여줍니다.
        elif args[2] == 'wallet':
            if test2.getUserInfo(slack_user_code) == None:
                result = '등록되지 않은 사용자입니다.'
                return result
            print('wallet')
            user = test2.getUserInfo(slack_user_code)
            result = '<@{}> 님\n잔액 : {}     일일대출한도 : {}'.format(slack_user_code, user['money'], user['bid'])
            return result# by jun
        # 사용자가 파산신청을 하여 슬롯머신에서 사용자를 삭제합니다.
        elif args[2] == 'del':
            if test2.getUserInfo(slack_user_code) == None:
                result = '등록되지 않은 사용자입니다.'
                return result
            test2.delUser(slack_user_code)
            print("del user")
            result = "<@{}> 님, 파산신청이 정상적으로 접수되었습니다. :pepe:".format(slack_user_code)
            return result
        # 슬롯머신을 플레이 하거나 돈을 빌리기 전, 사용자의 명령을 검사합니다.
        elif len(args) != 4:
            print('error : args[] len is not 4')
            result = "잘못된 명령이거나 들어오는 매개변수가 부정확합니다."
            return result
        # 슬롯머신을 돈을 걸고 돌립니다. 돈은 0 이상의 정수로 지정되야 합니다.
        elif args[2] == 'play' and int(args[3]) > 0:
            if test2.getUserInfo(slack_user_code) == None:
                result = '등록되지 않은 사용자입니다.'
                return result
            if int(args[3]) > 100 :
                result = "<@{}> 님, 베팅 한도를 넘은 금액입니다. 베팅 한도는 100 입니다.".format(slack_user_code)
                return result
            user = test2.getUserInfo(slack_user_code)
            if int(args[3]) > user['money']:
                result = "잔액이 부족합니다.\n"
            else:
                result, point = slot_playing(args[3])
                test2.updateUserMoney(slack_user_code, -int(args[3]))
                if point == 0:
                    result = result + "안타깝습니다! \n"
                else :
                    result = result + "축하합니다! {}를 획득했습니다. \n".format(point)
                    test2.updateUserMoney(slack_user_code, point)
            user = test2.getUserInfo(slack_user_code)
            result = result + '<@{}> 님\n잔액 : {}     일일대출한도 : {}'.format(slack_user_code, user['money'], user['bid'])
        # 슬롯머신에게 돈을 빌립니다. 돈은 0 이상의 양수로 지정되어야 합니다.
        elif args[2] == 'bid' and int(args[3]) > 0:
            if test2.getUserInfo(slack_user_code) == None:
                result = '등록되지 않은 사용자입니다.'
                return result
            result = bid_time_limit(slack_user_code, args[3])
            # test2.updateUserMoney(slack_user_code,int(args[3]))
            user = test2.getUserInfo(slack_user_code)
            # result = "슬롯머신에게 {} 포인트를 빌렸습니다. \n".format(args[3])
            result = result + '<@{}> 님\n잔액 : {}     일일대출한도 : {}'.format(slack_user_code, user['money'], user['bid'])

        else:
            result = "잘못된 명령이거나 들어오는 매개변수가 부정확합니다."
    return result