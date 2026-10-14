# はじめに
未完の大器 日本語プログラミング言語「なでしこ」Version2でV1,V３のコードがどのくらいビルドできるのか試してみました。[前回の記事](https://qiita.com/mylifewithviolin/items/a55c9411d5329bf013f1)では昨年実行時間検証用に記述した「なでしこ」v1のコードは　「[ERROR] インデントレベルが間違っています。」と怒られてしまったので、とりあえず一番シンプルなHellowWorldで実行してみました。今回はこのエラーの回避策を探り、さらにその先へちょこっと進んでみようと思います。


# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
nadesiko2 2014/04/22リリース版(β版)
C# 12 ※直接関係ないかもしれませんが入っているので
dotnet-sdk-8.0.206-win-x64 ※直接関係ないかもしれませんが入っているので monoは入れてないです。

# 日本語プログラミング言語「なでしこ」Version2とは

.NETCore統合前のmono版.NETのCLR中間コードにコンパイルするバージョンで現時点では開発中断しています。開発リポジトリ上の最終マージは2018年11月ごろ。今回実行しているバージョンは下記サイトに掲示されている 2014/04/22リリース版(β版)です。

https://nadesi.com/dev/wiki/index.php?%E3%81%AA%E3%81%A7%E3%81%97%E3%81%932.0

# プロジェクトフォルダ構成

たいへんお手数ですが[前回の記事](https://qiita.com/mylifewithviolin/items/a55c9411d5329bf013f1)をご参照ください。


# お題のソースコード
今回V2でビルド実行を試みたのは下記の記事のV1,V3ソ－スコードです。単純に整数をカウントアップして実行時間を出力します。

https://qiita.com/mylifewithviolin/items/83bc75d70a7a102d268a

https://qiita.com/mylifewithviolin/items/e8528eaced83894422a2

#### なでしこV1

コマンドライン引数の処理コードがコメントアウトされている箇所で、インデントがなくなっているのは、　「[ERROR] インデントレベルが間違っています。」を解消しようとした試みの後です。V1は下記の状態で実行できました。行頭のインデントは関係ないようでした。

```mind:count.nako
※【なでしこ実行モード】cnako
countとは整数
countMaxとは整数

count=0
countMax=10

※もし コマンドラインの配列要素数 < 2 ならば
※countMax=0
※違えば
※エラー監視
※countMax=コマンドライン[1]を整数変換
※エラーならば
※countMax=0
※ここまで
※ここまで

開始日時は、システム時間

（count < countMax）の間
   count = count + 1
※ここまで

終了日時は、システム時間
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する
```

#### なでしこV3
V3も実行できたのは下記の状態から「もし」の行をコメントアウトした状態でV1と実質同じ状態でした。

```mind:count3.nako
※【なでしこ実行モード】cnako3

count=0
countMax=0
sizeArgs=コマンドラインの配列要素数
もし (sizeArgs < 4) ※ならば
　　countMax=0
※違えば
※   エラー監視
※　    countMax=コマンドライン[3] //を整数変換
※　　エラーならば
※ 　　 countMax=0
※    ここまで
※ここまで

開始日時は、システム時間ミリ秒

（count < countMax）の間
	count = count + 1
※ここまで

終了日時は、システム時間ミリ秒
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する


```

# 実行結果
#### なでしこV1
上記ソースコードの状態での実行結果です。
```:
C:\nadesiko2\vscode>bin\cnako2 count.nako
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
処理回数：10回
処理時間：2ミリ秒
```
「（count < countMax）の間」の終端「ここまで」があった場合では下記のエラーとなっていました。
```mind:count.nako
（count < countMax）の間
   count = count + 1
ここまで
```
ということはV2ではここの構文の変更があったのかもしれません。

```:
C:\nadesiko2\vscode>bin\cnako2 count.nako         
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
[ParseError]無効な式か値があります。(余剰スタックのチェック)::[WORD:ここ{まで}(22)]
```
countMax=コマンドライン[1]を整数変換だけ復活させると、処理回数0で実行されたので、ここは動いているっぽいので、コマンドライン引数に数字をセットしてみましたところ
```mind:count.nako
countMax=コマンドライン[1]を整数変換
```

```:
C:\nadesiko2\vscode>bin\cnako2 count.nako
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
処理回数：0回
処理時間：1ミリ秒

C:\nadesiko2\vscode>bin\cnako2 count.nako 1 2 3 4
[ERROR] ファイル 'C:\nadesiko2\vscode\4' が見つかりませんでした。
```
最後の引数をファイルと認識するようでした。このあたりは仕様をわかっていないのであてずっぽです。引数１つ、２つでも最後の引数に対して同じメッセージがでました。

#### なでしこV3
V3はV2の後方バージョンなので動かないことが前提ですが、あくまでどんな挙動を示すか見てみたくビルド実行してみました。

前記記載のソースコード状態は下記の状態からエラーメッセージの解消を試みた途中状態となります。

```mind:count3.nako
もし (sizeArgs < 4) ならば
　　countMax=0
※違えば
※   エラー監視
※　    countMax=コマンドライン[3] //を整数変換
※　　エラーならば
※ 　　 countMax=0
※    ここまで
ここまで
```
上記の状態。
```:
C:\nadesiko2\vscode>bin\cnako2 count3.nako
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
[ParseError]無効な式か値があります。(余剰スタックのチェック)::[WORD:ここ{まで}(15)]
```
ループの終端のように「ここまで」をコメントアウトしてみる。
```:
C:\nadesiko2\vscode>bin\cnako2 count3.nako
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
[ParseError]無効な式か値があります。(余剰スタックのチェック)::[WORD{ならば}(7)]
```
もしかして「ならば」の扱いが変わったのか？と思っていちおう切り分けのためとってみる（というのが前記フル掲載状態）
```:
C:\nadesiko2\vscode>bin\cnako2 count3.nako
C:\nadesiko2\vscode\bin
C:\nadesiko2\vscode\bin\plug-ins
[SystemError]オブジェクト参照がオブジェクト インスタンスに設定されていません。   場所 NakoPlugin.NakoValueConveter.ToDouble(Object value)
   場所 Libnako.Interpreter.NakoInterpreter.calc_method_sub(Object a, Object b)
   場所 Libnako.Interpreter.NakoInterpreter.exec_calc(CalcMethodType f)
   場所 Libnako.Interpreter.NakoInterpreter.Run_NakoIL(NakoILCode code)
   場所 Libnako.Interpreter.NakoInterpreter._run()
   場所 Libnako.Interpreter.NakoInterpreter.Run(NakoILCodeList list)
   場所 Libnako.Interpreter.NakoInterpreter.Run()
   場所 cnako2.CNako2Executor.RunFileMode(String sourcefile)
   場所 cnako2.CNako2Executor.Run()
```
おおっ、例外がスローされてスタックトレースが出力されました。V2の実行のメカニズムがかいま見られたような感じでした。（わたしの中ではまったくわるいイメージはなく、こんな感じで動いているんだということがすこしイメージ化できてうれしい感じ？）

このエラーは「システム時間ミリ秒」をV1状態の「システム時間」に訂正することで解消されました。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。V2はあくまでβ版です。C#実装ということから親近感を感じております興味本位の記事でもありますのでご容赦ください。
