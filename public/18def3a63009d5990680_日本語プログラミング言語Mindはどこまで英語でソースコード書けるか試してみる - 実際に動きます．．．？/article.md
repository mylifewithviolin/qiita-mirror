# はじめに
日本語プログラミング言語Mindはどこまで英語でソースコードが書けるか試してみました。

https://qiita.com/advent-calendar/2023/mind

# 経緯

先日Go言語で整数をカウントアップする実行時間を計測するコードを書いていたとき、代入文のトークンが「:=」だったり、文字列を数値変換するときに例外をキャッチではなく変換後の文字列といっしょにエラー文字列を返す変数とで２つ値を返すところから、めっちゃくちゃMindを連想していました。星の数ほどいらっしゃるGo言語ユーザーでそんなこと連想するのはたぶんわたしだけ？

そんなことから、Mindのアドベントカレンダー2023のネタを探していたわたしは、次のことを思いつきました。
「ひょっとしてMindって英語でも書けるんじゃない？」

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
        
        Args(1) strconv.Atoi countMax errorに set
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
いかがでしょう？この状態でコンパイラは通っております。

Mindにはブロック文のかっこ区切りはないので、if文やループの指定がBasicに寄った感はありますかね。助詞としてのひらがなが残っている点（消せなかった点）が、ある意味Mindの構文トークンとなっているひらがなで、これが必須なんだと勉強になりました。
メインも後述しますが、現状はずせませんでした。

#### Go
参考に上記と基本的に等価なGo言語のソースコードをのせておきます。
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

# 解説
からくりを説明します。実は下記のように等価定義しています。
```:callfunceng.src
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
    strconv.Atoiは	数値変換と	等価。
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
    ※mainは		メインと	等価。
```
ifとerturnは無処理定義することで解決できました。
のちに説明しますが、メインは等価定義できませんでした。
関数定義部の整数入力と整数出力は等価定義できているのですが、こちらものちに説明しますコンパイル時のエラーのため実際には適用していません。

```:callfunceng.src
countupとは func 整数入力 整数出力（c → c）
	cは int
 
	cに set
    cを increment
	c return。
```
# 実行結果
それではこの状態で実行してみましょう。
```
C:\pmind\sample>mind callfunceng.src file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\pmind\bin\mindex.exe --> callfunceng.exe

C:\pmind\sample>callfunceng.exe
処理回数:0回
処理時間:0ミリ秒

C:\pmind\sample>
```
おおっここまでは動いた！:tada:
とりあえずコンパイルは正常完了して、引数無の空振り実行は正常に行えました。:confetti_ball:

では次にループを通過させてみます。

```
C:\pmind\sample>callfunceng.exe 1
処理回数:12524925回
処理時間:2171ミリ秒

C:\pmind\sample>
```
う～む、残念:joy:。わたし的には関数定義のあたりでうまく動作していないと推察しております。

ちなみによりソースコードを改変して、関数定義部の入出力指定を置き換えてみましたところ
```:callfunceng.src
intinは			整数入力と	等価。
intoutは		整数出力と	等価。
incrementは		一つ増加と	等価。
※mainは		メインと	等価。

countupとは func intin intout（c → c）
	cは int
	cに set
    cを increment
	c return。

メインとは
        countMaxは int
```
としますと、下記のようにコンパイラに怒られました。
```
C:\pmind\sample>mind callfunceng.src file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 ..要素番号が異常です（配列要素番号異常: 種別=選択構文  異常要素番号=8  有効要素数=5)

C:\pmind\sample>
```
さらに問題のメインですが、
```:callfunceng.src
mainは		メインと	等価。

mainとは
        countMaxは int

```
メインをmainに等価定義してみますと
```
C:\pmind\sample>mind callfunceng.src file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
1 個のエラーが有ります。

C:\pmind\sample>
```
下記のようなコンパイルエラーとなります。
```
C:\pmind\sample>type callfunceng.inf
callfunceng.src 23 行目でエラー。行内容は、
mainは          メインと        等価。
      要因１："メイン"は未定義の単語です。

1 個のエラーが有ります。

C:\pmind\sample>
```
メインはいろいろ試してみました。
メインが未定義なら無処理でもいけるか？とか
```:callfunceng.src
mainは						無処理。

      要因１："main"は重複定義です（当モジュールで定義済み）。
```
mainが重複定義ならそのままいけるのか？とか
```:callfunceng.src
※mainは						無処理。
mainとは
        countMaxは int      
```
すると、なんとコンパイルは通過！:tada:
```
C:\pmind\sample>mind callfunceng.src file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了

C:\pmind\sample>
```
しかし、実行してみると
```
kermain: このプログラムには'メイン'が定義されていません．
```
:sob:

# おわりに
最後は華々しく「正常に実行できました！」で終わりたかったのですが、残念な結果で終わってすみません。かなりマニアックな使い方でMindの通常の使い方ではないかと存じます。お騒がせしました。（関数呼び出しは使わなければ動くかもと密かに次を考えているわたし。←密かではない。）
