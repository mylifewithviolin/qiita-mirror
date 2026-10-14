# はじめに
日本語プログラミング言語 プロデル とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。スミレはプロデルコンパイラ2.0で検証したソースコードをスミレコンパイラ1.9でコンパイルし、C#と同じ.NET Core 6で実行してみます。プロデルの２つの手順呼び出しの構文の違いで有意差があり、スミレでも影響はあるようでしたので代入式構文で再計測しました。


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
[日本語プログラミング言語 プロデル Java C# で関数を介した整数カウントアップ実行時間を仲良く競う](https://qiita.com/mylifewithviolin/items/d7f8b5b94ce1d40ee904)

### スミレ とは
[日本語プログラミング言語 スミレ とは](https://qiita.com/mylifewithviolin/items/8f90f8452d65439fd825)
# お題のソースコード
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/d7f8b5b94ce1d40ee904)をご参照ください。

#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/d7f8b5b94ce1d40ee904)をご参照ください。

#### スミレ
```mind:callfunc.rdr
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
    
       	//countをカウントアップしたものをcountに代入する
    	count =　countをカウントアップする
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する

【c:整数】をカウントアップする手順
     c = c +1
     cを返す
終わり

```
プロデルと同一のソースコードです。
代入文形式の
```
count =　countをカウントアップする
```
の方です。

# 実行結果
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/d7f8b5b94ce1d40ee904)をご参照ください。

#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/d7f8b5b94ce1d40ee904)をご参照ください。

#### スミレ

```:
C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 40
処理回数：40回
処理時間：40.673ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 400
処理回数：400回
処理時間：43.7571ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 4000
処理回数：4000回
処理時間：58.7187ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 40000
処理回数：40000回
処理時間：220.2294ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 400000
処理回数：400000回
処理時間：1235.7707ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 4000000
処理回数：4000000回
処理時間：10316.0762ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 40000000
処理回数：40000000回
処理時間：106097.3538ミリ秒

C:\sumire\evalution>\sumire\sumire.exe callfunc.rdr 400000000
処理回数：400000000回
処理時間：1041675.9982ミリ秒

C:\sumire\evalution>
```
スミレの公式サイトにある実行方法に準じて実行してみましたが、この方法ですと最初にソースコードを中間コードに事前コンパイルするオーバーヘッドが乗っかってしまいますので、中間コードファイルの生成オプションがないか確認してみましたが、なさそうでしたので、この結果を比較対象とします。

# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | スミレ |
|-:|-:|-:|-:|
|  40 |  0 | 6  | 40 |
| 400  | 0  | 6  | 43 |
| 4,000  | 0  | 6  | 58  |
| 40,000  | 0  | 6  | 220  |
| 400,000  | 2  | 11 | 1,235  |
| 4,000,000  | 3  | 62  | 10,316  |
| 40,000,000  | 5  | 538  | 283,792  |
| 400,000,000  | 6  | 5,304  | 1,041,675  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
