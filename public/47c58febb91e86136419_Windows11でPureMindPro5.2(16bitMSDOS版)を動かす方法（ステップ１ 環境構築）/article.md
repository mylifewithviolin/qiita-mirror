# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/327b69e8d786c4f6832e)でおよそ40年前のPC環境について思いを馳せた結果、PureMindPro5.2(16bitMSDOS版)を今日のWindow11(64bit)で動かしてみたくなりました。16bitMSDOS環境としてMS-DOS Playerを使用してみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
puremind kihon 5.2　
MS-DOS Player

# MS-DOS Player

MS-DOS Playerは下記のサイトからダウンロードできます。

http://takeda-toshiya.my.coocan.jp/msdos/index.html

ダウンロードしたmsdos.7zを解凍するとbinaryフォルダの中にプロセッサ環境別のMS-DOSPlayerが格納されています。

```cmd:
C:\msdos>tree /f
C:.
└─msdos
    │  readme.txt
    │
    ├─binary
    │  ├─i286_x64
    │  │      msdos.exe
    │  │
    │  ├─i286_x86
    │  │      msdos.exe
    │  │
    │  ├─i386_x64
    │  │      msdos.exe
    │  │
    │  ├─i386_x86
    │  │      msdos.exe
    │  │
    │  ├─i486_x64
    │  │      msdos.exe
    │  │
    │  ├─i486_x86
    │  │      msdos.exe
    │  │
    │  ├─i86_x64
    │  │      msdos.exe
    │  │
    │  ├─i86_x86
    │  │      msdos.exe
    │  │
    │  ├─ia32_x64
    │  │      msdos.exe
    │  │
    │  ├─ia32_x86
    │  │      msdos.exe
    │  │
    │  ├─pentium4_x64
    │  │      msdos.exe
    │  │
    │  ├─pentium4_x86
    │  │      msdos.exe
    │  │
    │  ├─v30_x64
    │  │      msdos.exe
    │  │
    │  └─v30_x86
    │          msdos.exe
    │
    ├─license
    │  │  COPYING.txt
    
```


# puremind kihon 5.2　

PureMind-KIHON-and-DOSV.zipを下記のように解凍しています。KIHONSET\#1の構成を下記に示します。BINフォルダ内のPMIND.COMがコンパイラ本体にあたりますので、今回はこれの起動をめざします。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1>tree /f
C:.
│  INSTALL.COM
│  README.DOC
│
├─BIN
│      &CONSOLE.COM
│      &FILE.COM
│      CHKDELAY.COM
│      HISTORY.COM
│      MHELP.COM
│      MJOIN.COM
│      MPRINT.COM
│      PMAKE.COM
│      PMIND.COM
│      PTALK.COM
│      WORDS.COM
│
├─HELP
│      HELP.EXE
│
├─LIB
│      HCONSOLE.COM
│      HCONSOLE.SYM
│      HFILE.COM
│      HFILE.SYM
│      UCONSOLE.COM
│      UCONSOLE.SYM
│      UFILE.COM
│      UFILE.SYM
│
└─SAMPLE
        SAMPLE.EXE

```

#### 試しにそのままWindows11コマンドプロンプトで起動

試しにそのままWindows11コマンドプロンプトで起動してみます。もちろん動きません。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1>bin\pmind
このバージョンの C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\bin\PMIND.COM は、実行中の Windows のバージョンと互換性がありま せん。コンピューターのシステム情報を確認してから、ソフトウェアの発行元に問い合わせてください。
```

# MS-DOS Player配下での起動

MS-DOS Player配下での起動方法はこちらのサイトを参考にさせていただきました。

http://mezala.la.coocan.jp/vz/env/win/dosemu.html

#### ターゲット環境のMS-DOS Playerをbinフォルダにコピー

ターゲット環境のMS-DOS Player実行ファイルmsdos.exeをbinフォルダにコピーします。今回はmsdos\binary\i286_x86からコピーしました。

```cmd:
 C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\bin のディレクトリ

2024/12/21  10:07    <DIR>          .
2024/12/19  23:30    <DIR>          ..
2024/12/19  23:30            13,440 &CONSOLE.COM
2024/12/19  23:30            30,864 &FILE.COM
2024/12/19  23:30            33,648 CHKDELAY.COM
2024/12/19  23:30            33,680 HISTORY.COM
2024/12/19  23:30            39,856 MHELP.COM
2024/12/19  23:30            29,584 MJOIN.COM
2024/12/19  23:30            44,448 MPRINT.COM
2024/12/14  23:00           414,208 msdos.exe
2024/12/19  23:30            39,952 PMAKE.COM
2024/12/19  23:30            61,440 PMIND.COM
2024/12/19  23:30            64,736 PTALK.COM
2024/12/19  23:30            39,248 WORDS.COM
              12 個のファイル             845,104 バイト
```

#### MS-DOS Player(i286-x86)配下での起動

では起動してみます。最初に念のためmsdos.exeの起動確認です。下記のようなユーセージが表示されました。かなりいろいろなオプションがありますね。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1>bin\msdos
MS-DOS Player (i80286) for Win32 console

Usage:

MSDOS [-b] [-c[(new exec file)] [-p[P]]] [-d] [-e] [-i] [-m] [-n[L[,C]]]
      [-s[P1[,P2[,P3[,P4]]]]] [-sd] [-sc] [-vX.XX] [-wX.XX] [-x] [-a] [-l] [-h]
      (command) [options]

        -b      stay busy during keyboard polling
        -c      convert command file to 32bit execution file
        -p      record current code page when convert command file
        -d      pretend running under straight DOS, not Windows
        -e      use a reduced environment block
        -i      ignore invalid instructions
        -m      restrict free memory to 0x7FFF paragraphs
        -n      create a new buffer (25 lines, 80 columns by default)
        -s      enable serial I/O and set host's COM port numbers
        -sd     enable DTR/DSR flow control
        -sc     enable RTS/CTS flow control
        -v      set the DOS version
        -w      set the Windows version
        -x      enable LIM EMS and XMS
        -a      disable ANSI.SYS
        -l      draw box lines with ank characters
        -h      allow making cursor invisible

```

では、MS-DOS Player(i286-x86)配下でPureMind5.2(16bitMSDOS版)を起動します。binフォルダに移動しておきます。

```cmd:
C:\PureMind-KIHON-and-DOSV\KIHONSET\#1>cd bin

C:\PureMind-KIHON-and-DOSV\KIHONSET\#1\BIN>msdos pmind

日本語プログラミング言語  ＰｕｒｅＭｉｎｄＰＲＯ  Version 5.2
             Copyright(C)1989 Ｒigy Ｃorporation

　　　　　　　　 - 起動方法(例) -
　　　(ﾌﾟﾛｸﾞﾗﾑ名/ﾗｲﾌﾞﾗﾘ名には拡張子は付けません)

>PMIND ﾌﾟﾛｸﾞﾗﾑ名 ﾗｲﾌﾞﾗﾘ名    <--ｺﾝﾊﾟｲﾙ
>PTALK ﾌﾟﾛｸﾞﾗﾑ名             <--対話(ﾗｲﾌﾞﾗﾘとも対話可能)
```

起動しました！:tada::santa_tone2:

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。次回はソースコードをコンパイルしてみます。
