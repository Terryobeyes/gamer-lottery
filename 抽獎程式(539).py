#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

""" 線上編譯器網址
https://repl.it/languages/python3
將網站上面的程式碼全選，貼上這個程式碼
並修改23行 將註解符號刪除 並貼上網址
"""
URL539 = "https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx"

# 輸入網址
while True:
    try:
        """
        使用線上編譯的 可以把23行的# 去掉
        也就是把游標放在U左邊 按退格鍵兩下
        並填入網址，輸入網址時直接按Enter即可
        (也可以把22行的U前面加上# 就不用按Enter了)
        """
        URL = input("請輸入網址:")
        # URL = "網址打在引號裡面"

        # 修改網址 以利換頁
        index = URL.find("page=")
        if index == -1:
            URL = URL[:33] + "page=&" + URL[33:]
        else:
            URL = URL[:38] + URL[URL[38:].index('&') + 38:]

        # 驗證網址
        home_req = requests.get(URL[:38] + '1' + URL[38:])
        home_soup = BeautifulSoup(home_req.text, "html.parser")
        # 取得文章頁數
        code = home_soup.select("p a")[4].text
        if code.isdigit():
            code = int(code)
            # 只有2頁會抓到 看板代碼(?) (場外是7533)
            if code > 1000:  # 但如果是大於1000頁 會被判定為只有2頁
                Last_Page = 2
            elif code == 2:
                Last_Page = 3
            elif code == 1:
                Last_Page = 4
            else:
                Last_Page = code
        # 只有1頁會抓到 歡迎加入 或 Google Chrome
        else:
            Last_Page = 1
        # 抓取樓主ID
        home_authors = home_soup.select("div.c-post__header__author a")
        Host = "%s(%s)" % (home_authors[1].text, home_authors[2].text)

    except ValueError:
        print("網址連接失敗")
    except IndexError:
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
for page in range(2, Last_Page + 1):
    url = URL[:38] + str(page) + URL[38:]
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    authors = soup.select("div.c-post__header__author a")
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
print("目前名單:")
for a in Authors:
    print(a)
Authors_Len = len(Authors)
print("共 %d 人\n" % Authors_Len)

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


def transform(sequence):
    """
    新的序列 Bn = An - 1 - count(An > Ai for i:1~n-1)
    也就是原序列 -1 再減掉前面有幾個比他小的數
    """
    new = []
    for i in range(5):
        value = int(sequence[i]) - 1
        for j in range(i):
            if sequence[i] > sequence[j]:
                value -= 1
        new.append(value)
    return new


def get539():
    req539 = requests.get(URL539)
    soup539 = BeautifulSoup(req539.text, "html.parser")
    lucky_numbers = []
    ball = "D539Control_history1_dlQuery_SNo"
    for n in range(1, 6):
        lucky_numbers.append(soup539.find("span", id=ball + str(n) + "_0").text)
    print("最新一期539 號碼為:")
    print(lucky_numbers)
    sequence = transform(lucky_numbers)
    # a1*38*37*36*35 + a2*37*36*35 + a3*36*35 + a4*35 + a5
    # 69,090,840‬
    seed = sequence[0] * 1771560 + sequence[1] * 46260 + sequence[2] * 1260 + sequence[3] * 35 + sequence[4]
    print("種子號碼為:", seed)
    return seed


SEED = get539()

# 印出抽獎順序
order = []
# SEED % 人數 = 中獎者
for i in range(Authors_Len):
    order.append(Authors.pop(SEED % (Authors_Len - i)))
    """
    種子範圍為 0 ~ 69090839 (39*38*37*36*35 - 1)
    若人數無法整除 69090840 (2^3 * 3^3 * 5*7*13*19*37)
    會導致樓層前面的人 抽到機率稍微高一點點
    故這邊進行反轉
    """
    Authors.reverse()

print("<<< 以下為中獎順序 >>>\n")
with open("抽獎名單.txt", 'a', encoding='UTF-8') as file:
    file.write("\n中獎順序:\n")
    for i in range(Authors_Len):
        output = "(%d) %s" % (i + 1, order[i])
        print(output)
        file.write(output + '\n')

input("\n按Enter結束...")
exit()
