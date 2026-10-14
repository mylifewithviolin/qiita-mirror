# はじめに
日本語プログラミング言語 スミレ とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。前回プロデルコンパイラ2.0で検証したソースコードをスミレコンパイラ1.9でコンパイルし、C#と同じ.NET Core 6で実行してみます。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
sumire Version 1.9.1191
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz

## この記事内容の保証
※この記事の実行結果は参考情報です。実行環境に大きく依存します。

## 参考記事
### プロデルの結果
[日本語プログラミング言語 プロデル Java C# でHello World実行時間を仲良く競う](https://qiita.com/mylifewithviolin/items/fdc00911a1600a4786c4)

### スミレ とは
[日本語プログラミング言語 スミレ とは](https://qiita.com/mylifewithviolin/items/8f90f8452d65439fd825)

# お題のソースコード
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/fdc00911a1600a4786c4)をご参照ください。

#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/fdc00911a1600a4786c4)をご参照ください。

#### スミレ
```mind:helloworld.rdr
※コンソール
    【count:整数】は、0
    【countMax:整数】は、0
    
    もしプログラムのコマンドライン引数が無なら
    　　countMax=0
    そうでなければ
       例外監視
    　　  countMax=プログラムのコマンドライン引数(1)
    　　発生した場合
     　　 countMax=0
        監視終わり
    もし終わり
    
    開始日時は、今日
    count < countMaxの間、繰り返す
    　 「Hello World!」をコンソールへ表示して改行する
    	count =count +1
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する
    
```
# 実行結果
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/fdc00911a1600a4786c4)をご参照ください。

#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/fdc00911a1600a4786c4)をご参照ください。

#### スミレ

```:
C:\sumire\evalution>\sumire\sumire.exe helloworld.rdr 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数：40000回
処理時間：6368.4163ミリ秒

C:\sumire\evalution>
```
# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | スミレ |
|-:|-:|-:|-:|
|  40 |  8 | 16  | 57 |
| 400  | 72  | 57  | 132  |
| 4,000  | 563  | 468  | 761  |
| 40,000  | 4,565  | 4,206  | 6,368  |
| 400,000  | 42,618  | 40,075  | 56,089  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
