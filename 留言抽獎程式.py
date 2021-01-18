import requests
from re import compile
from datetime import datetime
from random import shuffle

GET_HOST = compile(r'com\.tw/(.*)" class="username" target="_blank">(.*)</a>')
GET_USER = compile(r'tagUser\(.*\'(.*)\', \'(.*)\'\)')
GET_TIME = compile(r'留言時間 (.*)"')
MORE_COMMEND = 'https://forum.gamer.com.tw/ajax/moreCommend.php?{}&returnHtml=1'

while True:
    URL = input("請輸入網址:")
    # 取得樓主 暱稱 + id
    try:
        if '&subbsn' not in URL:
            print("請檢查網址 (應包含 &subbsn)")
            continue
        req = requests.get(URL)
        req.close()
        match = GET_HOST.search(req.text)
        host = '{} ({})'.format(match.group(2), match.group(1)).ljust(50)
        break
    except requests.exceptions.ConnectionError:
        print("<<< 連線問題 >>>")
    except ValueError:
        print("<<< 請檢查網址 >>>")

# 取得留言者 暱稱 + id
url = MORE_COMMEND.format(URL[34:URL.find('&su')].replace('&sn', '&snB'))
req = requests.get(url)

# 設定截止時間
print("(格式範例:2087-08-07 20:07:00) (預設為當前時間)")
while True:
    try:
        deadline_str = input("請輸入截止時間:") or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M:%S')
        break
    except ValueError:
        print("時間格式錯誤，請重新輸入")

Authors_set = {host}  # 剔除樓主
Authors = []

for s in req.json()['html']:
    match = GET_USER.search(s)
    author = '{} ({})'.format(match.group(2), match.group(1)).ljust(50)
    time_str = GET_TIME.search(s).group(1)
    time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    if time > deadline:
        break
    if author not in Authors_set:
        Authors_set.add(author)
        Authors.append(author + time_str)

print("以下為抽獎名單:")
for a in Authors:
    print(a)
Authors_Len = len(Authors)
print("共 %d 人\n" % Authors_Len)

# 將名單保存成txt檔
with open("抽獎名單.txt", 'w', encoding='UTF-8') as f:
    f.write("截止時間為: " + deadline_str + "\n")
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
        for winner in Authors[:n]:
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
