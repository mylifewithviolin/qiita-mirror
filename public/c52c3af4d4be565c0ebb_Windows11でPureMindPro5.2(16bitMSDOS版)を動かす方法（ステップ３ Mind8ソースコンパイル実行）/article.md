# はじめに
[前回記事](https://qiita.com/mylifewithviolin/items/ad44f96c0a96ef2d76ca)で16bitMSDOS環境としてMS-DOS Playerを使用してPureMindPro5.2コンパイラによるサンプルソースのコンパイルと実行に成功しましたので、今回はMind8ソースのコンパイル実行を行ってみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
puremind kihon 5.2　
MS-DOS Player

# MS-DOS Player

MS-DOS Playerは下記のサイトからダウンロードできます。

http://takeda-toshiya.my.coocan.jp/msdos/index.html

ダウンロードしたmsdos.7zを解凍するとbinaryフォルダの中にプロセッサ環境別のMS-DOSPlayerが格納されています。フォルダ構成はたいへんお手数ですが[初回記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)を参照してください。

# puremind kihon 5.2　

PureMind-KIHON-and-DOSV.zipを解凍してできるKIHONSET\#1の構成もたいへんお手数ですがはたいへんお手数ですが[初回記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)を参照してください。

#### ターゲット環境のMS-DOS Playerをbinフォルダにコピー

BINフォルダ内のPMIND.COMがコンパイラ本体にあたりますので、ここにターゲット環境i286_x86のMS-DOS Player実行ファイルmsdos.exeをコピーしてあります。

#### サンプルソースをbinフォルダに解凍

KIHONSET\#1フォルダ配下にはsampleフォルダにサンプルソースのアーカイブがあります。前回無事に解凍できましたが、binフォルダにソースを展開してしまいました。これはこれでパスの記述が減るのでこのままでよしといたします。今回のお題のMind8ソースファイルもここにコピーしてコンパイルしてみます。

# お題のソースコード
今回のお題のMind8ソースファイルは昨年のMindアドベントカレンダー2023の下記の記事で使ったコードです。

https://qiita.com/mylifewithviolin/items/17c8263636c7bbab220c

こちらのソースコードではC#とJavaとMindの実行時間を計測していますが、ソースコードの書き味や各言語のdefaultの最適化状態はさほど気にしておりませんので、あくまで参考値として公開しておりました。

```mind:countup.src
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

        ※開始時間（秒）
        日時を値で得る　startTimeに　入れる
        countに　0を　入れ
        ここから
        　　countが　countMax　以上　ならば　打ち切り
        　　　　　　　　つぎに

            countを　一つ増加し
        繰り返し
        
        ※終了時間（秒）
        日時を値で得る　stopTimeに　入れる
        stopTimeから　startTimeを　引き　1000を　掛け　spanTimeに　入れる
        「処理回数: 」と　countを　文字列変換し　合成し 「回」を　合成し
        一行表示し
        「処理時間: 」と　spanTimeを　文字列変換し　合成し 「ミリ秒」を　合成し
        一行表示すること。
```

では、このコードをKIHONSET\#1\binフォルダにコピーしてコンパイル実行してみます。Mind7とMind8で確か処理単語の引数の書き方に非互換があったかと思いますが、上記記事は一本書きなのでたぶんだいじょうぶ。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>dir countup.src

2024/12/21  12:37             1,020 countup.src
               1 個のファイル               1,020 バイト
```

#### MS-DOS Player(i286-x86)配下でのコンパイル実行

では、とりあえずcountup.srcをコンパイルしてみます。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos pmind countup ..\lib\hfile

日本語プログラミング言語  ＰｕｒｅＭｉｎｄＰＲＯ  Version 5.2
             Copyright(C)1989 Ｒigy Ｃorporation

コンパイル中 - 終了。
6 個のエラーが有ります。
```

うっうう、思ったよりエラーがでました。

```
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>type countup.inf
COUNTUP.SRC 10 行目でエラー。 行内容は、
        起動引数個数が　ゼロ？
      要因１："起動引数個数"は未定義の単語です。

COUNTUP.SRC 13 行目でエラー。 行内容は、
        起動引数（1）を　数値変換し　countMaxと　合否に　入れ
      要因１：かっこ表記に誤りが有ります。
      要因２："起動引数"は未定義の単語です。

COUNTUP.SRC 19 行目でエラー。 行内容は、
        日時を値で得る　startTimeに　入れる
      要因１："日時を値で得"は未定義の単語です。

COUNTUP.SRC 29 行目でエラー。 行内容は、
        日時を値で得る　stopTimeに　入れる
      要因１："日時を値で得"は未定義の単語です。

COUNTUP.SRC 32 行目でエラー。 行内容は、
        一行表示し
      要因１："一行表示"は未定義の単語です。

6 個のエラーが有ります。
Next code addr=7DB0H  Next data addr=1A60H
```

# つづく
次回で、非互換の処理単語をMind5互換単語に書き換えてみます。
