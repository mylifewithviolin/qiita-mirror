# はじめに
日本語プログラミング言語Mindはどこまで英語でソースコードが書けるか試してみました。[前回記事](https://qiita.com/mylifewithviolin/items/18def3a63009d5990680)では動きませんでしたが、今回は動きました！！:tada::tada:


https://qiita.com/advent-calendar/2023/mind

# 経緯

お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/18def3a63009d5990680)をご参照ください。

# お題のソースコード
てなことから、書いてみました。日本語プログラミング言語Mindによる英語表記のソースコードです。シンタックスハイライトはGoを指定しています。

#### Mind
```go:callfunceng.src
メインとは
        countMaxは int
        countは    int
        errorは    int

        startTimeは int
        stopTimeは  int
        spanTimeは  int
        
        if Args.size zero?
        then [countMax := 0]
        endif
        
        Args(1) strconv.Atoi countMaxと errorに set
        if error false?
        then [countMax := 0]
        endif

        [startTime := clock]
        [count := 0]
        do
        	if [count >= countMax] then break
            endif
    	    [count :=  countup(count)]
        loop

		[stopTime := clock]
        [spanTime := stopTime - startTime]

        "処理回数:" count strconv append "回" append Printf
        "処理時間:" spanTime strconv append "ミリ秒" append Printf
        
```
いかがでしょう？この状態でコンパイラは通っており、今回は動作しています。

#### Go
参考に上記と基本的に等価なGo言語のソースコードがあるのですが、お手数ですが前回記事をご参照ください。


# 解説
からくりを説明していますが、お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/18def3a63009d5990680)をご参照ください。

# 実行結果
それでは実行してみましょう。
```
C:\pmind\sample>counteng.exe 4000
処理回数:4000回
処理時間:0ミリ秒

C:\pmind\sample>counteng.exe 40000
処理回数:40000回
処理時間:15ミリ秒

C:\pmind\sample>counteng.exe 400000
処理回数:400000回
処理時間:62ミリ秒

C:\pmind\sample>counteng.exe 4000000
処理回数:4000000回
処理時間:906ミリ秒

C:\pmind\sample>counteng.exe 40000000
処理回数:40000000回
処理時間:8256ミリ秒

C:\pmind\sample>
```
無事に動作していますね！

# おわりに
今回はなんとか「正常に実行できました！」で終わりました。前回動かなかった原因にお気づきの方はいらっしゃいますでしょうか？
実は
<details><summary>答え</summary>

```
Args(1) strconv.Atoi countMax-->と<-- errorに set
```
</details>
でした。

## 参考情報
<details><summary>ソースコード全文</summary>

```go:callfunceng.src
intは			変数と		等価。
ifは						無処理。
thenは			ならばと	等価。
endifは			つぎと		等価。
doは			ここと		等価。
loopは			繰り返すと	等価。
returnは					無処理。
Printfは		一行表示と	等価。
breakは			打ち切りと	等価。
clockは			クロックと	等価。
false?は		偽？と		等価。
strconv.Atoiは		数値変換と	等価。
strconvは		文字列変換と	等価。
Args.sizeは		起動引数個数と	等価。
zero?は			ゼロ？と	等価。
Argsは			起動引数と	等価。
setは			入れと		等価。
appendは		合成と		等価。
funcは			関数と		等価。
intinは			整数入力と	等価。
intoutは		整数出力と	等価。
incrementは		一つ増加と	等価。
※mainは						無処理。

countupとは func 整数入力 整数出力（c → c）
	cは int

	cに set
    	cを increment
	c return。

メインとは
        countMaxは int
        countは    int
        errorは    int

        startTimeは int
        stopTimeは  int
        spanTimeは  int
        
        if Args.size zero?
        then [countMax := 0]
        endif
        
        Args(1) strconv.Atoi countMaxと errorに set
        if error false?
        then [countMax := 0]
        endif

        [startTime := clock]
        [count := 0]
        do
        	if [count >= countMax] then break
	        endif
		    [count :=  countup(count)]
	    
        loop

	[stopTime := clock]
        [spanTime := stopTime - startTime]

        "処理回数:" count strconv append "回" append Printf
        "処理時間:" spanTime strconv append "ミリ秒" append Printf

```
</details>
