#### gamer-lottery
## 巴哈抽獎程式
<pre>
這個是給場外人做抽獎的程式
由於巴友可能重複發文
造成抽獎人公平抽獎的困難
看到好像沒什麼人寫 就自己來寫

大家可以下載exe檔 或
把程式碼貼到線上編譯器上執行
我自己是用這個網站(原本用online gdb但後來發現有問題2020/10/7)
</pre>
https://repl.it/languages/python3
<pre>

但輸入的部分 好像一樣不能用貼上的
所以要在程式碼那邊改
程式碼前面幾行有說明

執行後會在exe檔目錄下產生
抽獎名單.txt 的檔案
裡面會有抽獎名單 最後會有得獎者

注意事項:
1.抽獎人不含樓主(即使樓主在其他樓回覆)(留言的樓主即為該文的作者)
2.被摺疊的抓得到 但刪除回覆的應該是抓不到
3.抽留言的網址是按下該樓層鈕後的網址 應包含 &subbsn
4.539的程式就是利用當下最新一期的 今彩539
獲取亂數種子，作為抽獎順序
輸出順序在當期是固定的，並沒有其他的隨機影響
因此更有公平性，可以多加利用

2021/1/18
參考 https://blog.jiatool.com/posts/gamer_commend_spider/
獲取頁數的方法來修改我的程式碼
並新增了抽留言的程式

2019/8/17 新增 抽獎程式(539)
是透過 台灣彩券的 今彩539 的號碼
得到一個 0 ~ 約7千萬 的大數當種子
並以人數 對種子取餘數 得到中獎者
如果我的想法沒錯的話 機率應該是平均的
只是前面的樓層中獎率會稍微高一點

2020/10/7
online gdb 的連線有問題
改用 repl.it
只有修改539的程式碼

備註 (2021/1/18):
現在的我是學店資工大三生
我沒有很認真檢查、確認這些程式
以上.py 及 .exe檔皆為本人的創作，
僅供教學用途及有需要的巴友使用
本人不負任何法律責任...
</pre>
