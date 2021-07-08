#!/usr/bin/python
# -*- coding: utf-8 -*-
# 執行時也可以直接將網址貼在11行的''內

import requests
from re import compile
from datetime import datetime
from bs4 import BeautifulSoup
from random import seed, shuffle

URL = ''

GET_HOST = compile(r'com\.tw/(.*)" class="username" target="_blank">(.*)</a>')
GET_USER = compile(r'tagUser\(.*\'(.*)\', \'(.*)\'\)')
GET_TIME = compile(r'留言時間 (.*)"')
GAMER = 'https://forum.gamer.com.tw/'
MORE_COMMEND = 'https://forum.gamer.com.tw/ajax/moreCommend.php?{}&returnHtml=1'
URL539 = 'https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/63.0.3239.132 Safari/537.36'
}

Authors = []
Deadline = ''


def deal_message():
    global Deadline
    req = requests.get(URL, headers=HEADERS)
    req.close()
    match = GET_HOST.search(req.text)
    host = '{} ({})'.format(match.group(2), match.group(1)).ljust(50)

    # 取得留言者 暱稱 + id
    url = MORE_COMMEND.format(URL[34:URL.find('&su')].replace('&sn', '&snB'))
    req = requests.get(url, headers=HEADERS)

    # 設定截止時間
    print("(格式範例:2021-07-08 21:06:00) (預設為當前時間)")
    while True:
        try:
            Deadline = input("請輸入截止時間:") or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            deadline = datetime.strptime(Deadline, '%Y-%m-%d %H:%M:%S')
            break
        except ValueError:
            print("<<< 時間格式錯誤，請重新輸入 >>>")

    authors_set = {host}  # 剔除樓主

    for s in req.json()['html']:
        match = GET_USER.search(s)
        author = '{} ({})'.format(match.group(2), match.group(1)).ljust(50)
        time_str = GET_TIME.search(s).group(1)
        time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        if time > deadline:
            break
        if author not in authors_set:
            authors_set.add(author)
            Authors.append(author + time_str)

    print("以下為抽獎名單:")
    for a in Authors:
        print(a)
    authors_len = len(Authors)
    print("共 %d 人\n" % authors_len)

    # 將名單保存成txt檔
    with open("抽獎名單.txt", 'w', encoding='UTF-8') as f:
        f.write("留言截止時間為: " + Deadline + "\n")
        f.write("抽獎人:\n\n")
        f.write('\n'.join(Authors))
        f.write("\n共 %d 人\n" % authors_len)
        # 紀錄文末指針 重複抽獎時才能重寫
        pointer = f.tell()

    return Authors, pointer


def deal_reply():
    global URL, Authors
    # 修改網址 以利換頁
    URL = URL[:33] + 'page=&' + URL[URL.find('bsn'):]
    # 驗證網址
    home_req = requests.get(URL[:38] + '1' + URL[38:], headers=HEADERS)
    home_soup = BeautifulSoup(home_req.text, 'html.parser')

    # 取得文章頁數
    total_page = int(home_soup.select_one('.BH-pagebtnA > a:last-of-type').text)

    # 抓取樓主ID
    home_authors = home_soup.select('div.c-post__header__author a')
    host = "%s(%s)" % (home_authors[1].text, home_authors[2].text)

    # 建立回覆者字典 {名字(ID): 樓層}
    authors_dict = dict()

    # 抓第一頁的人
    for p in range(len(home_authors) // 3):
        f = home_authors[p * 3].text
        a = "%s(%s)" % (home_authors[p * 3 + 1].text, home_authors[p * 3 + 2].text)
        # 重複的不刷新
        if a not in authors_dict:
            authors_dict[a] = f

    print("抓取中，請稍後...")
    # 從第二頁開始 一頁一頁跑
    for page in range(2, total_page + 1):
        url = URL[:38] + str(page) + URL[38:]
        req = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(req.text, 'html.parser')
        Authors = soup.select('div.c-post__header__author a')
        for i in range(len(Authors) // 3):
            floor = Authors[i * 3].text
            author = "%s(%s)" % (Authors[i * 3 + 1].text, Authors[i * 3 + 2].text)
            # 重複的不刷新
            if author not in authors_dict:
                authors_dict[author] = floor

    # 剔除樓主
    authors_dict.pop(host)

    # 整理資料
    Authors = [f + '-' + name for name, f in authors_dict.items()]

    # 用線上編譯器執行 順序會是亂的 這邊依據樓層做排序
    # 不過字典本身應該就是無序的吧 = =
    Authors.sort(key=lambda s: int(s.split()[0]))
    # 印出名單
    print("\n以下為抽獎名單:")
    for a in Authors:
        print(a)
    authors_len = len(Authors)
    print("共 %d 人\n" % authors_len)

    # 設定截止樓層
    while True:
        indices = input("請輸入樓層範圍(默認無限制):").split()
        if not indices:
            break
        if len(indices) > 2 or not indices[0].isdigit() or not indices[-1].isdigit():
            print("<<< 樓層格式錯誤>>>")
            continue
        if len(indices) == 1:
            indices = ['1', indices[0]]
        for i, floor_num in enumerate(indices):
            for j in range(authors_len):
                if Authors[j][:Authors[j].find(' ')] == floor_num:
                    indices[i] = j
                    break
            else:  # 沒找到
                print("<<< 樓層錯誤 >>>")
                break
        else:
            Authors = Authors[indices[0]:indices[1] + 1]
            break

    # 跟樓主的留言一起抽
    if input("若要與一樓的留言一併抽取，請輸入任意內容:"):
        URL = GAMER + home_authors[0]['href']
        original_len = len(Authors)
        deal_message()
        # 需剔除留言與回覆重複的部分
        accounts = {s[s.find('-') + 1:] for s in Authors[:original_len]}
        message_authors = Authors[original_len:]
        del Authors[original_len:]
        for s in message_authors:
            info = s.split()
            account = info[0] + info[1]
            if account not in accounts:
                Authors.append(s)
                accounts.add(account)

    # 印出名單
    print("抽獎名單:")
    for a in Authors:
        print(a)
    authors_len = len(Authors)
    print("共 %d 人\n" % authors_len)

    # 將名單保存成txt檔
    with open("抽獎名單.txt", 'w', encoding='UTF-8') as f:
        if Deadline:
            f.write("留言截止時間為: " + Deadline + "\n")
        f.write("抽獎人:\n\n")
        f.write('\n'.join(Authors))
        f.write("\n共 %d 人\n" % authors_len)
        # 紀錄文末指針 重複抽獎時才能重寫
        pointer = f.tell()

    return Authors, pointer


while True:
    URL = URL or input("請輸入網址:")
    # 取得樓主 暱稱 + id
    try:
        if '&subbsn' in URL:
            Pointer = deal_message()
        else:
            Pointer = deal_reply()
        break
    except requests.exceptions.ConnectionError:
        print("<<< 連線問題，請檢查網路 >>>")
    except (IndexError, AttributeError):
        print("<<< 網址錯誤，請重新輸入 >>>")
    except:
        print("<<< 發生錯誤，請重新輸入 >>>")
    URL = ''


def get539():
    req539 = requests.get(URL539, headers=HEADERS)
    soup539 = BeautifulSoup(req539.text, "html.parser")
    ball = "D539Control_history1_dlQuery_SNo"
    lucky_numbers = []
    for n in range(1, 6):
        lucky_numbers.append(soup539.find("span", id=ball + str(n) + "_0").text)

    print("最新一期539 號碼為:")
    print(*lucky_numbers)
    seed539 = ''.join(lucky_numbers)
    print("種子碼為:", seed539)
    return int(seed539)


while True:
    SEED = input('請輸入亂數種子，若不輸入將利用今彩539抓取:')
    if SEED and not SEED.isdigit():
        print('<<< 輸入的種子錯誤，種子應為整數 >>>')
    else:
        SEED = int(SEED) if SEED else get539()
        break

seed(SEED)
shuffle(Authors)
print("<<< 以下為中獎順序 >>>\n")
with open("抽獎名單.txt", 'a', encoding='UTF-8') as file:
    file.write(f"\n種子碼: {SEED}\n中獎順序:\n")
    for i in range(len(Authors)):
        output = "(%d) %s" % (i + 1, Authors[i])
        print(output)
        file.write(output + '\n')

input("\n按Enter結束...")
exit()
