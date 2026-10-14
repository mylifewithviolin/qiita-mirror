# はじめに
日本語プログラミング言語 Mind とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。

ただし[前回の記事](https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)ではMindの場合、関数で比較といっても関数形式ではない処理単語形式で実行しておりましたので、今回念のため関数形式に書き換えて再計測してみました。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Mind Version 8.07 for Windows
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz


## この記事内容の保証
※この記事の実行結果は参考情報です。実行環境に大きく依存します。

# お題のソースコード
#### Java
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)をご参照ください。
#### C#
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)をご参照ください。

#### Mind
```mind:callfunc.src
カウントアップとは　関数　整数入力　整数出力（c　→　c）
	cは　変数
	cに　入れ
    cを　一つ増加し
	cを　返す。

メインとは
        countMaxは　変数
        countは　変数
        合否は　変数

        startTimeは　変数
        stopTimeは　変数
        spanTimeは　変数
        
        起動引数個数が　ゼロ？
        ならば　[countMax := 0]
        つぎに
        起動引数（1）を　数値変換し　countMaxと　合否に　入れ
        合否が　偽？
        ならば　[countMax := 0]
        つぎに


        [startTime := クロック]
        [count := 0]
        ここから
        　　[count >= countMax]　ならば　打ち切り
        　　　　　　　　つぎに
            ※countを　カウントアップし　countに　入れ
	        [count :=  カウントアップ(count)]
        繰り返し

        [stopTime := クロック]
        [spanTime := stopTime - startTime]

        「処理回数: 」と　countを　文字列変換し　合成し 「回」を　合成し
        一行表示し
        「処理時間: 」と　spanTimeを　文字列変換し　合成し 「ミリ秒」を　合成し
        一行表示すること。
```
今回、カウントアップの下記の処理単語を
```mind:main.src
    カウントアップとは　（c　→　c）
    	cは　変数
     
    	cに　入れ
        cを　一つ増加し
    	cを　返す
```  
下記のように関数定義に書き換えています。関数定義の場合は引数型、戻り値型も指定できますね。
```mind:callfunc.src
カウントアップとは　関数　整数入力　整数出力（c　→　c）
	cは　変数
 
	cに　入れ
    cを　一つ増加し
	cを　返す。
```
 そして、カウントアップの実行部の記述を下記の日本語構文から
```mind:main.src
    countを　カウントアップし　countに　入れ
```
下記の代入構文に書き換えています。
```mind:callfunc.src
	[count :=  カウントアップ(count)]
```
他に下記のような変数の初期化も
```mind:main.src
countに　0を　入れ
```
下記の代入構文に書き換えています。
```mind:callfunc.src
[count := 0]
```
前回このように書かなかったのは、代入形式の場合はかぎかっこで囲わなければならないとか、すっかり忘れていたためでした:sweat_smile:
かぎかっこで囲わない場合は下記のように怒られますのでみなさん注意しましょう（忘れていた≒ほぼ知らない状態となっていた）のは私だけ？
```
    　count := 0
      要因１：":="は誤った引用です。
```
# 実行結果
#### Java
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)をご参照ください。

#### C#
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)をご参照ください。

#### Mind

```:
C:\pmind\sample>callfunc.exe 40
処理回数: 40回
処理時間: 0ミリ秒

C:\pmind\sample>callfunc.exe 400
処理回数: 400回
処理時間: 0ミリ秒

C:\pmind\sample>callfunc.exe 4000
処理回数: 4000回
処理時間: 0ミリ秒

C:\pmind\sample>callfunc.exe 40000
処理回数: 40000回
処理時間: 0ミリ秒

C:\pmind\sample>callfunc.exe 400000
処理回数: 400000回
処理時間: 93ミリ秒

C:\pmind\sample>callfunc.exe 4000000
処理回数: 4000000回
処理時間: 562ミリ秒

C:\pmind\sample>callfunc.exe 40000000
処理回数: 40000000回
処理時間: 5754ミリ秒

C:\pmind\sample>callfunc.exe 400000000
処理回数: 400000000回
処理時間: 56387ミリ秒

C:\pmind\sample>
```
# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | Mind |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 0  |
| 40,000  | 0  | 6  | 0  |
| 400,000  | 2  | 11 | 93  |
| 4,000,000  | 3  | 62  | 562  |
| 40,000,000  | 5  | 538  | 5,754  |
| 400,000,000  | 6  | 5,304  | 56,387  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？4万回がJavaと同じく0ミリ秒となったので（前回処理単語時は15ミリ秒）もしかしたら速くなった！？とぬか喜びしてしまいましたが、その後の結果は有意差なさそうでした。
整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
