# gamer-lottery
<pre>
<場外抽獎程式>
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
1.抽獎人不含樓主(即使樓主在其他樓回覆)
2.被摺疊的抓得到 但刪除回覆的應該是抓不到
3.超過1000頁的話 請把程式碼裡的1000 改大
(1000頁不知道要跑多久 沒試過= =)


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


題外話:
(2020/10/7)
幹我以為巴哈文章沉了 但好像沒有= =
過好久，我懶得再回去修了
我覺得真的要做到方便大家使用
可能要架個網站直接讓大家線上弄
雖然其實自己用線上編譯器跑也不會太難
當初真的是隨便寫隨便弄
所以我才不大力推廣、宣傳，放著爛
甚至小屋也沒有放= =
看大家都用網路上找的抽獎亂數抽獎網站
心裡有點小失落，但其實也還好
我也不希望像深音那樣弄得太棒
我就是隨便寫寫 給一些有緣人用用
不要出什麼奇怪的事，其實也挺好的


(舊)
本來要寫多執行序 但requests好像是非線程安全的
線程好像會被鎖起來
開執行序還比直接跑慢
好像可以用多進程 但我不會= =

另外 寫這個程式時，我只是學店剛升大二的菜雞
主要是寫python 也不太會用這個github
(經過了半年多之後....)
我只有發一篇文宣傳 所以沒什麼人在用
那篇文也沉了 已經看不到內容了
程式還能跑 用線上編譯器實際操作起來 感覺還是很不錯

除非我之後有在更新 不然我不會重新發文
反正google搜尋 場外抽獎程式 還是找得到
</pre>
