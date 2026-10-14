# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)でおよそ40年前のPC環境について思いを馳せた結果、PureMindPro5.2(16bitMSDOS版)を今日のWindow11(64bit)で動かしてみたくなりました。[前回記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)で16bitMSDOS環境としてMS-DOS Playerを使用してコンパイラの起動に成功しましたので、今回はなにかソースのコンパイルを行ってみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
puremind kihon 5.2　
MS-DOS Player

# MS-DOS Player

MS-DOS Playerは下記のサイトからダウンロードできます。

http://takeda-toshiya.my.coocan.jp/msdos/index.html

ダウンロードしたmsdos.7zを解凍するとbinaryフォルダの中にプロセッサ環境別のMS-DOSPlayerが格納されています。フォルダ構成はたいへんお手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)を参照してください。

# puremind kihon 5.2　

PureMind-KIHON-and-DOSV.zipを解凍してできるKIHONSET\#1の構成もたいへんお手数ですがはたいへんお手数ですが[前回記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)を参照してください。

#### ターゲット環境のMS-DOS Playerをbinフォルダにコピー

BINフォルダ内のPMIND.COMがコンパイラ本体にあたりますので、前回はここにターゲット環境i286_x86のMS-DOS Player実行ファイルmsdos.exeをコピーしてあります。

#### SAMPLE.EXEの解凍

KIHONSET\#1フォルダ配下には下記のサンプルソースのアーカイブがありますのでこれを解凍します。

```cmd:
 C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\SAMPLE のディレクトリ

2024/12/19  23:30    <DIR>          .
2024/12/19  23:30    <DIR>          ..
2024/12/19  23:30            41,542 SAMPLE.EXE
               1 個のファイル              41,542 バイト
```

これは当時の16bitアプリでアーカイブされているようでしたので、Windows11コマンドプロンプトでは解凍できませんでした。これもMS-DOS Player配下で解凍します。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\SAMPLE>sample
このバージョンの C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\SAMPLE\SAMPLE.EXE は、実行中の Windows のバージョンと互換性があ りません。コンピューターのシステム情報を確認してから、ソフトウェアの発行元に問い合わせてください。
```
無事に解凍できましたが、フォルダ構成を間違ってbinフォルダにソースを展開してしまいました。これはこれでパスの記述が減るのでこのままでよしといたします。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos ..\sample\sample.exe
LHa's SFX 2.10S (c)1991, Yoshi

BIORHY.SRC .
BIORHY.DOC .
DENTAKU.SRC .
DENTAKU.DOC .
HANOI.SRC .
HANOI.DOC .
HELLO.SRC .
KONGETU.SRC .
KONGETU.DOC .
NIKOCHAN.SRC .
NIKOCHAN.DOC .
OMIKUJI.SRC .
RPN.SRC .
RPN.DOC .
TOKEI.SRC .
TOKEI.DOC .
NIBAI.SRC .
NIBAIASM.ASM .
NIBAIASM.LST .
COPY1.SRC .
COPY2.SRC .
COPY3.SRC .
COPY4.SRC .
FIND1.SRC .
REPLACE.SRC .
DELPROMT.SRC .
WORDS.SRC .
DIR1.SRC .
BROWSE.SRC .
EDUMP.SRC .
KIRIDASI.SRC .
KEISEN.SRC .
MDBASE.SRC .
KENSAKU.SRC .
TOUROKU.SRC .
COMMON.SRC .
BUKKEN.DAT .
追加登録.TXT .
```

#### MS-DOS Player(i286-x86)配下でのコンパイル実行

では、とりあえずHELLO.SRCをコンパイルしてみます。
```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>type hello.src
メインとは
　　　　「こんにちは、Ｍｉｎｄです。」を　表示して　改行すること。
```

コンパイラは起動しましたが、どうもライブラリの指定がよろしくないようです。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos pmind hello ..\lib\file

日本語プログラミング言語  ＰｕｒｅＭｉｎｄＰＲＯ  Version 5.2
             Copyright(C)1989 Ｒigy Ｃorporation

コンパイル中 -
コンパイルエラー：ライブラリのファイルが見付かりません。
```

当時のFILEライブラリはHFILEライブラリだったようです。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>dir ..\lib\hfile.com
 C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\lib のディレクトリ

2024/12/19  23:30            31,696 HFILE.COM
               1 個のファイル              31,696 バイト
```

ライブラリの指定をfileからhfileに変更して無事にコンパイル成功しました！:santa_tone2:

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos pmind hello ..\lib\hfile

日本語プログラミング言語  ＰｕｒｅＭｉｎｄＰＲＯ  Version 5.2
             Copyright(C)1989 Ｒigy Ｃorporation

コンパイル中 - 終了。

C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>dir hello.*

2024/12/21  11:05            31,744 HELLO.COM
2024/12/21  11:05                71 HELLO.HIS
2024/12/21  11:05                46 HELLO.INF
1989/10/10  17:49                80 HELLO.SRC
2024/12/21  11:05            13,952 HELLO.SYM
               5 個のファイル              45,893 バイト
```

続いて実行してみます。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos hello
こんにちは、Ｍｉｎｄです。
```

実行成功しました！:tada:

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。これで往年の名器PureMindPro5.2のコンパイル実行環境が手に入りました。次回は最近のMind8で書いたソースコードをコンパイルしてみます。
