# はじめに
日本語プログラミング言語Mindはどこまで英語でソースコードが書けるか試してみました。前回記事で動きましたが、今回はMind開発者の@killyさんのアドバイスをいただき、よりいっそうコトの発端となったGo言語のソース風となりました。:tada::tada:

https://qiita.com/advent-calendar/2023/mind

# 経緯

先日Go言語で整数をカウントアップする実行時間を計測するコードを書いていたとき、Mindを連想していました。（何を連想したかは[前々回記事](https://qiita.com/mylifewithviolin/items/18def3a63009d5990680)をご参照ください。）
「ひょっとしてMindって英語でも書けるんじゃない？」
てなことから、書いてみました。前々回記事のバージョンでは動きませんでした。
その後の[前回記事の調整版](https://qiita.com/mylifewithviolin/items/8156ab2e5775429a18ed)で動きましたが、エントリポイントの「メイン」が残っていました。

# お題のソースコード

#### Go
コトの発端となったGo言語のソースコードは下記の感じ。
```go:callfunc.go
// メイン
func main() {
	countMax := 0
	count := 0

	if len(os.Args) <= 1 {
		countMax = 0
	} else {
		var err error
		countMax, err = strconv.Atoi(os.Args[1])
		if err != nil {
			countMax = 0
		}
	}

	startTime := time.Now()

	for count < countMax {
		count = countup(count)
	}

	stopTime := time.Now()
	spanTime := stopTime.Sub(startTime)
	fmt.Println("処理回数: ", count, "回")
	fmt.Println("処理時間: ", int64(spanTime/time.Millisecond), "ミリ秒")

}

func countup(c int) int {
	return c + 1
}
```
日本語プログラミング言語Mindによる英語表記のソースコードです。シンタックスハイライトはGoを指定しています。

#### Mind
```go:callfunceng3.src
mainは func
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
		count countup countに set
	    
        loop

		[stopTime := clock]
        [spanTime := stopTime - startTime]

        "処理回数:" count strconv append "回" append Printf
        "処理時間:" spanTime strconv append "ミリ秒" append Printf。

countupは func 
	cは int

    cに set
    cを increment
    c return
    
```
# 解説
からくりを説明していますが、大筋はお手数ですが[前々回記事](https://qiita.com/mylifewithviolin/items/18def3a63009d5990680)をご参照ください。
[前回記事](https://qiita.com/mylifewithviolin/items/8156ab2e5775429a18ed)からの差異は下記の点です。
```
countupは				　仮定義。
mainは					　仮定義。
funcは			本定義と	等価。
メインは		mainする。
```
@killyさんに「仮定義」の存在を教えていただきました。これにより前回記事のコメントのやりとりで「メイン」問題はいったんの解決を見たのですが、わたしの中ではcountupの定義がmainの前に来てしまうのが気になっていたのです。（Mindはワンパスコンパイラ？）
しかし、仮定義することで手前にエントリポイントを宣言しておいて、実装定義を後にもっていけましたので、funcを「本定義」と等価定義することで、よりいっそうGo言語風にすることができました。

# 実行結果
それでは実行してみましょう。
```
(上書き保存) 
(コンパイル)
コンパイル中 .. 終了

(起動引数付き実行)
処理回数:40000回
処理時間:16ミリ秒
```
無事に動作していますね！:tada::tada:
## 参考情報
<details><summary>ソースコード全文</summary>

```go:callfunceng3.src
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
functionは			関数と		等価。
intinは			整数入力と	等価。
intoutは		整数出力と	等価。
incrementは		一つ増加と	等価。
countupは				仮定義。
mainは					仮定義。
funcは			本定義と	等価。
メインは		mainする。



mainは func
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
		count countup countに set
	    
        loop

		[stopTime := clock]
        [spanTime := stopTime - startTime]

        "処理回数:" count strconv append "回" append Printf
        "処理時間:" spanTime strconv append "ミリ秒" append Printf。

countupは func 
	cは int

    cに set
    cを increment
    c return
```
</details>
