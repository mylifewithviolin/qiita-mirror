# はじめに

日本語プログラミング言語 Mind とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。前回の記事では筆者の知見不足によりMindは秒単位で計測していましたので、今回Mindだけミリ秒計測のやり直しです。

https://qiita.com/advent-calendar/2023/mind

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
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/6182b9822524dd0709db)をご参照ください。
#### C#
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/6182b9822524dd0709db)をご参照ください。
#### Mind
```mind:main.src
    メインとは
        countMaxは　変数
        countは　変数
        合否は　変数

        startTimeは　変数
        stopTimeは　変数
        spanTimeは　変数
        
        起動引数個数が　ゼロ？
        ならば　countMaxに　0を　入れ
        つぎに
        起動引数（1）を　数値変換し　countMaxと　合否に　入れ
        合否が　偽？
        ならば　countMaxに　0を　入れ
        つぎに

        ※開始時間（ミリ秒）
        クロックを　startTimeに　入れる
        countに　0を　入れ
        ここから
        　　countが　countMax　以上　ならば　打ち切り
        　　　　　　　　つぎに
            「Hello World!」を　一行表示する
            countを　一つ増加し
        繰り返し
        
        ※終了時間（ミリ秒）
        クロックを　stopTimeに　入れる
        stopTimeから　startTimeを　引き　spanTimeに　入れる
        「処理回数: 」と　countを　文字列変換し　合成し 「回」を　合成し
        一行表示し
        「処理時間: 」と　spanTimeを　文字列変換し　合成し 「ミリ秒」を　合成し
        一行表示すること。

```

前回記事では現在の日時を秒単位の３２ビット整数に換算する「日時を値で得る」を使っていましたが、今回は@killyさんのご支援をいただき、ミリ秒単位の内部カウンタを参照する「クロック」を使っています。この処理単語はWindows版のみ有効です。
# 実行結果
#### Java
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/6182b9822524dd0709db)をご参照ください。
#### C#
お手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/6182b9822524dd0709db)をご参照ください。
#### Mind

```:
C:\pmind\sample>hello3.exe 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 7777ミリ秒

C:\pmind\sample>
```
# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | Mind |
|-:|-:|-:|-:|
|  40 |  8 | 16  |  15 |
| 400  | 72  | 57  | 78  |
| 4,000  | 563  | 468  | 807  |
| 40,000  | 4,565  | 4,206  | 7,777  |
| 400,000  | 42,618  | 40,075  | 73,936  |

前回の計測ではMindの1秒未満の世界が不明でしたが、今回計測してみると400回くらいまでの反復では各言語有意差がない感じですね。

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
