# はじめに
[前回記事](https://qiita.com/mylifewithviolin/items/c52c3af4d4be565c0ebb)で16bitMSDOS環境としてMS-DOS Playerを使用してPureMindPro5.2コンパイラによりMind8ソースのコンパイル実行を行ってみましたが、非互換単語でコンパイルエラーとなりましたので、今回はその解消の試みです。

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

KIHONSET\#1フォルダ配下にはsampleフォルダにサンプルソースのアーカイブがあります。前回無事に解凍できましたが、binフォルダにソースを展開してしまいました。これはこれでパスの記述が減るのでこのままでよしといたします。今回のお題のMind8ソースファイルもここにコピーしてコンパイルしております。

# お題のソースコード
今回のお題のMind8ソースファイルは昨年のMindアドベントカレンダー2023の下記の記事で使ったコードですが、これはこのままではコンパイルできませんでした。

https://qiita.com/mylifewithviolin/items/17c8263636c7bbab220c

#### MS-DOS Player(i286-x86)配下でのコンパイル実行の結果

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

# お題のソースコード改定版
実は今回のお題のゴールは、中間コードコンパイラのMind8とネイティブコンパイラのMind5の実行速度の比較にあります。なので、あまり大きく書き換えたくはなく、とりあえずループ内の処理は互換コンパイルできているので、ループ外の前処理と後処理をコンパイル実行可能なよう、下記のとおり書き換えました。

```mind:countup.src
    メインとは
        countMaxは　変数
        countは　変数
        合否は　変数

        startTimeは　変数
        stopTimeは　変数
        spanTimeは　変数
        起動引数は　文字列
        
        起動パラメータから　単語切り出しし　起動引数に　入れ
        起動引数が　空列？
        ならば　countMaxに　0を　入れ
        つぎに
        起動引数を　数値変換し　countMaxと　合否に　入れ
        合否が　偽？
        ならば　countMaxに　0を　入れ
        つぎに

        ※開始時間（秒）
        時刻を得て　時に 60を 掛け 分に 60を 掛け 秒を 加え　startTimeに　入れる
        countに　0を　入れ
        ここから
        　　countが　countMax　以上　ならば　打ち切り
        　　　　　　　　つぎに

            countを　一つ増加し
        繰り返し
        
        ※終了時間（秒）
        時刻を得て　時に 60を 掛け 分に 60を 掛け 秒を 加え　stopTimeに　入れる
        stopTimeから　startTimeを　引き　1000を　掛け　spanTimeに　入れる
        「処理回数: 」と　countを　文字列変換し　合成し 「回」を　合成し
        表示し　改行し
        「処理時間: 」を　表示し　spanTimeを　文字列変換し 表示し
        「ミリ秒」を　表示し　改行すること。
```

spanTimeを文字列変換するの前後で、合成するを使った場合、正常に出力されませんでしたので、とりあえずつど表示するで逃げています。spanTimeを文字列変換して表示した後も「ミリ秒」が表示されませんでした。


#### MS-DOS Player(i286-x86)配下でのコンパイル実行


```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos pmind countup ..\lib\hfile

日本語プログラミング言語  ＰｕｒｅＭｉｎｄＰＲＯ  Version 5.2
             Copyright(C)1989 Ｒigy Ｃorporation

コンパイル中 - 終了。
```

とりあえずコンパイル成功しました！:tada:つづいて実行してみます。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos countup 1000000
処理回数: 1000000回
処理時間: 2000
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos countup 10000000
処理回数: 10000000回
処理時間: 11000
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos countup 40000000
処理回数: 40000000回
処理時間: 46000
```
100万回と1000万回を繰り返した実行時間です。単位は秒計測ですが1000倍してミリ秒単位にしています。spanTimeを文字列変換して表示した後の「ミリ秒」が表示されない謎現象は前述のとおりです。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。これで往年の名器PureMindPro5.2のコンパイル実行環境が手に入りました:santa_tone2:
