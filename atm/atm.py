# coding: utf-8
import pickle
import time
from prettytable import PrettyTable


def userInfo():    # 读取文件,生成用户字典
    userDict = {}
    with open('user_info.txt', 'r') as f:
        for line in f.xreadlines():
            Id, pwd, status = line.split('|')
            userDict[Id] = [pwd, status]
    return userDict


def login(card_id):    # 用户登录认证
    import getpass

    if card_id in userDict and userDict[card_id][1] != '1':
        for i in xrange(3):
            p = getpass.getpass('plz enter your password: ')
            if userDict[card_id][0] == p:
                return 1
            else:
                print 'password error.'
        else:
            print 'id locked!'
            userDict[card_id][1] = '1'
    else:
        print 'no card id or id locked.'


def operat(card_id):    # 功能菜单
    tag = True
    while tag:
        print u'''
                                    欢迎登录信用卡系统!


            可选操作:
                1. 取现: 不能超限额,手续费5%           4. 转账: 可转账到不同用户
                2. 查询: 查询余额和交易明细            5. 购物
                3. 还款: 现金还款                      6. 退出
        '''
        choose = raw_input('选择操作: ')
        if choose == '1':
            cash(card_id)
        elif choose == '2':
            showLog(card_id)
        elif choose == '3':
            repay(card_id)
        elif choose == '4':
            transfer(card_id)
        elif choose == '5':
            shopping(card_id)
        elif choose == '6':
            tag = False
            print 'Welcome to again!'
        else:
            print u'请输入正确的选项'


def getBalance(card_id):   # 获取用余额
    try:
        id_info = pickle.load(open('idInfo', 'rb'))
    except Exception:
        id_info = {card_id: [float(15000)]}
        pickle.dump(id_info, open('idInfo', 'wb'))
        return id_info[card_id][0]
    else:
        if card_id in id_info:
            return id_info[card_id][0]
        else:
            id_info[card_id] = [float(15000)]
            pickle.dump(id_info, open('idInfo', 'wb'))
            return id_info[card_id][0]


def insertBal(card_id, num):    # 插入用户余额
    id_info = pickle.load(open('idInfo', 'rb'))
    id_info[card_id] = [float(num)]
    pickle.dump(id_info, open('idInfo', 'wb'))


def repay(card_id):     # 还款
    num = raw_input('请输入金额: ')
    if len(num) != 0 and num.isdigit() and float(num) > 0:
        re_num = getBalance(card_id) + float(num)
        insertBal(card_id, float(re_num))
        log = 'repay %s' % num
        print log
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        genLog(card_id, 'repay', nowtime, getBalance(card_id), log)
    else:
        print u'请输入正确的金额'


def cash(card_id):      # 取现
    bal = getBalance(card_id)
    money = raw_input('请输入金额: ')
    if money.isdigit() and len(money) != 0 and float(money) + float(money) * 0.05 < bal:
        num = bal - (float(money) + float(money) * 0.05)
        insertBal(card_id, num)
        log = 'cash:%s,FEE:%s' % (money, float(money) * 0.05)
        print log
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        genLog(card_id, 'cash', nowtime, str(num), log)
    else:
        print u'余额不足或输入错误!'


def genLog(card_id, action, date, balance, description):    # 生成日志文件,用了picke
    msg = [date, action, description, str(balance)]
    try:
        log_info = pickle.load(open('logInfo', 'rb'))
    except Exception:
        log_info = {card_id: [msg]}
        pickle.dump(log_info, open('logInfo', 'wb'))
    else:
        if card_id in log_info:
            log_info[card_id].append(msg)
            pickle.dump(log_info, open('logInfo', 'wb'))
        else:
            log_info[card_id] = [msg]
            pickle.dump(log_info, open('logInfo', 'wb'))


def showLog(card_id):       # 输入日志
    try:
        log_info = pickle.load(open('logInfo', 'rb'))
    except:
        print u'之前没有过任何操作'
    else:
        x = PrettyTable(['datetime', 'action', 'log', 'balance'])
        for i in log_info[card_id]:
            x.add_row(i)
        print x


def transfer(card_id):      # 转账功能
    des_id = raw_input('请输入对方账号: ')
    if len(des_id) == 4 and des_id.isdigit() and des_id in userDict and des_id != card_id:
        money = raw_input('请输入金额: ')
        sor_bal = getBalance(card_id)
        if len(money) != 0 and money.isdigit() and 0 < float(money) < sor_bal:
            nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            des_bal = getBalance(des_id)
            des_bal += float(money)
            log = '%s transfer to you %s RMB.' % (card_id, money)
            genLog(des_id, 'transfer', nowtime, des_bal, log)
            insertBal(des_id, des_bal)
            sor_bal -= float(money)
            insertBal(card_id, sor_bal)
            log = 'transfer to %s, %sRMB' % (des_id, money)
            genLog(card_id, 'tramsfer', nowtime, sor_bal, log)
            print log
        else:
            print u'输入错误或余额不足'
    else:
        print u'输入错误或账号不存在'


def shopping(card_id):          # 购物功能
    tag = True
    while tag:
        print u'''
        商品列表:
            1. iphone       标价: 5000RMB
            2. MacBook      标价: 12000RMB
            3. iMac         标价: 20000RMB
            4. car          标价: 50000RMB
            5. 退出购物车
        '''
        choose = raw_input('输入商品标签: ')
        bal = getBalance(card_id)
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if choose == '1':
            if bal > 5000:
                log = 'Spend: 5000RMB'
                print log
                bal -= 5000
                insertBal(card_id, float(bal))
                genLog(card_id, 'shopping', nowtime, getBalance(card_id), log)
            else:
                print u'余额不足'
        elif choose == '2':
            if bal > 12000:
                log = 'Spend: 12000RMB'
                print log
                bal -= 12000
                insertBal(card_id, float(bal))
                genLog(card_id, 'shopping', nowtime, getBalance(card_id), log)
            else:
                print u'余额不足'
        elif choose == '3':
            if bal > 20000:
                log = 'Spend: 20000RMB'
                print log
                bal -= 20000
                insertBal(card_id, float(bal))
                genLog(card_id, 'shopping', nowtime, getBalance(card_id), log)
            else:
                print u'余额不足'
        elif choose == '4':
            if bal > 50000:
                log = 'Spend: 50000RMB'
                print log
                bal -= 50000
                insertBal(card_id, float(bal))
                genLog(card_id, 'shopping', nowtime, getBalance(card_id), log)
            else:
                print u'余额不足'
        elif choose == '5':
            tag = False
            print u'欢迎下次光临!'
        else:
            print u'请输入正确的选项'


if __name__ == '__main__':
    userDict = userInfo()
    cardId = raw_input('plz enter your card id: ').strip()
    if login(cardId):
        operat(cardId)