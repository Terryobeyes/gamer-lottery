#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from random import shuffle

print("巴哈抽獎程式")
# 線上編譯器網址
# https://repl.it/languages/python3
# 將網站上面的程式碼全選，貼上這個程式碼
# 並修改25行 將註解符號刪除 並貼上網址
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/63.0.3239.132 Safari/537.36"
}
# 輸入網址
while True:
    try:
        # 使用線上編譯的 可以把25行的# 去掉
        # 也就是把游標放在U左邊 按退格鍵兩下
        # 並填入網址，輸入網址時直接按Enter即可
        # (也可以把24行的U前面加上# 就不用按Enter了)
        URL = input("請輸入網址:")
        # URL = '網址打在引號裡面'

        # 修改網址 以利換頁
        index = URL.find('page=')
        if index == -1:
            URL = URL[:33] + 'page=&' + URL[33:]
        else:
            URL = URL[:38] + URL[URL[38:].index('&') + 38:]
        # 驗證網址
        home_req = requests.get(URL[:38] + '1' + URL[38:], headers=HEADERS)
        home_soup = BeautifulSoup(home_req.text, 'html.parser')

        # 取得文章頁數
        Total_Page = int(home_soup.select_one('.BH-pagebtnA > a:last-of-type').text)

        # 抓取樓主ID
        home_authors = home_soup.select('div.c-post__header__author a')
        Host = "%s(%s)" % (home_authors[1].text, home_authors[2].text)

    except ValueError:
        print("網址連接失敗")
    except (IndexError, AttributeError):
        print("網址錯誤 請重新輸入")
    except requests.exceptions.ConnectionError:
        print("連線問題")
    else:
        print("抓取中 請稍後...")
        break

# 建立回覆者字典 {名字(ID): 樓層}
Authors_dict = dict()

# 抓第一頁的人
for p in range(len(home_authors) // 3):
    f = home_authors[p * 3].text
    a = "%s(%s)" % (home_authors[p * 3 + 1].text, home_authors[p * 3 + 2].text)
    # 重複的不刷新
    if a not in Authors_dict:
        Authors_dict[a] = f

# 從第二頁開始 一頁一頁跑
for page in range(2, Total_Page + 1):
    url = URL[:38] + str(page) + URL[38:]
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.text, 'html.parser')
    authors = soup.select('div.c-post__header__author a')
    for i in range(len(authors) // 3):
        floor = authors[i * 3].text
        author = "%s(%s)" % (authors[i * 3 + 1].text, authors[i * 3 + 2].text)
        # 重複的不刷新
        if author not in Authors_dict:
            Authors_dict[author] = floor

# 剔除樓主
Authors_dict.pop(Host)

# 整理資料
Authors = [f + '-' + name for name, f in Authors_dict.items()]

# 用線上編譯器執行 順序會是亂的 這邊依據樓層做排序
# 不過字典本身應該就是無序的吧 = =
Authors.sort(key=lambda s: int(s.split()[0]))

# 印出名單
print("以下為抽獎名單:")
for a in Authors:
    print(a)
Authors_Len = len(Authors)
print("共 %d 人" % Authors_Len)

# 設定截止樓層
while True:
    number = input("請輸入截止樓層(該樓可抽 預設無截止):")
    if number == '':
        break
    index = -1
    for i in range(Authors_Len):  # 反過來找 通常比較快
        if Authors[Authors_Len - 1 - i].split()[0] == number:
            index = Authors_Len - 1 - i
    if index == -1:  # 沒找到
        print("樓層錯誤")
    else:
        Authors_Len = index + 1
        Authors = Authors[:Authors_Len]
        # 印出名單
        print("抽獎名單:")
        for a in Authors:
            print(a)
        print("共 %d 人\n" % Authors_Len)
        break

# 將名單保存成txt檔
with open("抽獎名單.txt", 'w', encoding='UTF-8') as f:
    f.write("抽獎人:\n\n")
    f.write('\n'.join(Authors))
    f.write("\n共 %d 人\n" % Authors_Len)
    # 紀錄文末指針 重複抽獎時才能重寫
    pointer = f.tell()


def shuffle_and_save(n):
    """打亂順序 並將中獎者寫入txt"""
    shuffle(Authors)
    print("<<< 以下為中獎者 >>>\n")
    with open("抽獎名單.txt", 'r+', encoding='UTF-8') as file:
        file.seek(pointer)
        file.write("\n中獎者:\n")
        # 取洗亂後的前n位 作為中獎者
        for winner in sorted(Authors[:n], key=lambda s: int(s.split()[0])):
            print(winner)
            file.write(winner + '\n')
        # 之前的得獎者的資料可能還在 要清除
        file.truncate()
    print()


# 開始抽獎
while True:
    try:
        number = int(input("請輸入抽獎人數:"))
        if number > Authors_Len or number < 1:
            raise ValueError
    except ValueError:
        print("人數錯誤 請重新輸入")
    else:
        shuffle_and_save(number)
        break

while True:
    buffer = input("輸入數字以該數字重抽，輸入任意內容重抽，直接按Enter則結束...")
    if buffer == '':
        exit()
    try:
        buffer = int(buffer)
        if buffer > Authors_Len or buffer < 1:
            print("數字無效!")
            raise ValueError
        number = buffer

    except ValueError:
        print("<<< 重抽 >>>")
    finally:
        shuffle_and_save(number)
