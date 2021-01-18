import requests
from re import compile
from datetime import datetime
from bs4 import BeautifulSoup

GET_HOST = compile(r'com\.tw/(.*)" class="username" target="_blank">(.*)</a>')
GET_USER = compile(r'tagUser\(.*\'(.*)\', \'(.*)\'\)')
GET_TIME = compile(r'留言時間 (.*)"')
MORE_COMMEND = 'https://forum.gamer.com.tw/ajax/moreCommend.php?{}&returnHtml=1'

URL539 = "https://www.taiwanlottery.com.tw/lotto/DailyCash/history.aspx"

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
print("(格式範例:2020-01-08 20:11:00) (預設為當前時間)")
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
