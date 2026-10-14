# はじめに
日本語プログラミング言語 スミレ とJava C# とで整数カウントアップの反復実行時間を仲良く競い合わせてみます。コンソール出力は意外と重い処理のようで、もっとも単純な処理での結果を確認してみます。スミレはプロデルコンパイラ2.0で検証したソースコードをスミレコンパイラ1.9でコンパイルし、C#と同じ.NET Core 6で実行してみます。

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
[日本語プログラミング言語 プロデル Java C# で整数カウントアップ実行時間を仲良く競う](https://qiita.com/mylifewithviolin/items/b78c6809dcfbdebcbb70)

### スミレ とは
[日本語プログラミング言語 スミレ とは](https://qiita.com/mylifewithviolin/items/8f90f8452d65439fd825)

# お題のソースコード
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/b78c6809dcfbdebcbb70)をご参照ください。
#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/b78c6809dcfbdebcbb70)をご参照ください。

#### スミレ
```mind:count.rdr
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
    
    	count =count +1
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する
    
```

# 実行結果
#### Java
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/b78c6809dcfbdebcbb70)をご参照ください。

#### C#
お手数ですが[参考記事 プロデルの結果](https://qiita.com/mylifewithviolin/items/b78c6809dcfbdebcbb70)をご参照ください。

#### スミレ
```:
C:\sumire\evalution>\sumire\sumire.exe count.rdr 40
処理回数：40回
処理時間：26.1243ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 400
処理回数：400回
処理時間：31.4505ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 4000
処理回数：4000回
処理時間：35.1297ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 40000
処理回数：40000回
処理時間：86.2819ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 400000
処理回数：400000回
処理時間：458.9174ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 4000000
処理回数：4000000回
処理時間：3411.3683ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 40000000
処理回数：40000000回
処理時間：33558.2025ミリ秒

C:\sumire\evalution>\sumire\sumire.exe count.rdr 400000000
処理回数：400000000回
処理時間：342581.8545ミリ秒
```
スミレの公式サイトにある実行方法に準じて実行してみましたが、この方法ですと最初にソースコードを中間コードに事前コンパイルするオーバーヘッドが乗っかってしまいますので、中間コードファイルの生成オプションがないか確認してみましたが、なさそうでしたので、この結果を比較対象とします。前回のHelloWorld比較時は気づいていませんでした。

```
C:\sumire\evalution>\sumire\sumire.exe /?
日本語プログラミング言語「スミレ」 Ver.1.9.1191

使い方: dotnet sumire.dll [ソースファイル] [起動時引数]
  /? または /help       この使い方に関するメッセージを表示します。
  { [rdr1] [rdr2]... } [起動時引数]
　                              指定したソースファイルをすべて参照して実行します。
  - [初期ソースファイル] [起動時引数]   インタラクティブモードで起動します。
  /e プログラム文       指定した文を実行します。
  /pluginsdir プラグインパス            指定したディレクトリにあるプラグインを読み込みます。
  /v            バージョン情報を表示します。
  (パラメータなし)      標準入力からプログラムを取得して実行します。

C:\sumire\evalution>
```
# 実行結果まとめ
表2　整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | スミレ |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  26 |
| 400  | 0  | 6  | 31 |
| 4,000  | 0  | 7  | 35  |
| 40,000  | 0  | 6  | 86  |
| 400,000  | 3  | 7  | 458  |
| 4,000,000  | 3  | 23  | 3,411  |
| 40,000,000  | 3  | 139  | 33,558 |
| 400,000,000  | 3  | 1,341  | 342,581  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。4億を単純に数える処理にとくになんらかの実用性があるものでもないですが、Javaはなんだか他を圧倒する結果ですね。
スミレはプロデルより若干速くなっているようです。40回とか反覆少ない場合はプリコンパイルのオーバーヘッドが少し乗っているような気はしますが、ソースコード短いので大きな負荷にはなっていないようです。
