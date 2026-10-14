# はじめに
日本語プログラミング言語Mindの開発元@killyさんの御厚意により日本語プログラミング言語Mindのバージョン９βをご提供いただいたので、さっそくインストールしてMind8のソースコードをビルドしてみました。


# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6　

# インストールフォルダ構成
mind version8.08のpmindフォルダをC:\mind9-betaの下にコピーしてフォルダ名をmind9-betaとして、version9-BETA-6のフォルダを上書きコピーしました。

```cmd:
C:\mind9-beta>dir

 C:\mind9-beta のディレクトリ
2025/01/10  00:04    <DIR>          mind9-beta
2025/01/09  23:34    <DIR>          mind9-beta-1
2025/01/09  23:39    <DIR>          mind9-beta-2b
2025/01/09  23:40    <DIR>          mind9-beta-3
2025/01/09  23:42    <DIR>          mind9-beta-4
2025/01/09  23:44    <DIR>          mind9-beta-5
2025/01/10  00:04    <DIR>          mind9-beta-6
```
## 参考 mind9-beta-6のフォルダ構成
現バージョンが保持しているフォルダは下記に含まれていないものがあります。

```cmd:
C:\mind9-beta\mind9-beta-6>tree
C:.
├─bin
├─doc
│  └─image
├─lib
├─samplew
│  ├─image
│  └─obj
├─tclruntime
│  ├─dde1.4
│  ├─itcl4.2.3
│  ├─nmake
│  ├─reg1.3
│  ├─sqlite3.40.0
│  ├─tcl8
│  │  ├─8.4
│  │  │  └─platform
│  │  ├─8.5
│  │  └─8.6
│  │      └─tdbc
│  ├─tcl8.6
│  │  ├─encoding
│  │  ├─http1.0
│  │  ├─msgs
│  │  ├─opt0.4
│  │  └─tzdata
│  │      ├─Africa
│  │      ├─America
│  │      │  ├─Argentina
│  │      │  ├─Indiana
│  │      │  ├─Kentucky
│  │      │  └─North_Dakota
│  │      ├─Antarctica
│  │      ├─Arctic
│  │      ├─Asia
│  │      ├─Atlantic
│  │      ├─Australia
│  │      ├─Brazil
│  │      ├─Canada
│  │      ├─Chile
│  │      ├─Etc
│  │      ├─Europe
│  │      ├─Indian
│  │      ├─Mexico
│  │      ├─Pacific
│  │      ├─SystemV
│  │      └─US
│  ├─tdbc1.1.5
│  ├─tdbcmysql1.1.5
│  ├─tdbcodbc1.1.5
│  ├─tdbcpostgres1.1.5
│  ├─tdbcsqlite31.1.5
│  ├─thread2.8.8
│  └─tk8.6
│      ├─demos
│      │  └─images
│      ├─images
│      ├─Img1.4.16
│      ├─msgs
│      └─ttk
└─testdir
    ├─フォルダー1
    └─空白を 含む ディレクトリ
```

tdbcとかはtclのodbcランタイムっぽいですね。

内部バージョンは8.11でしたので念のためMind8(mind-for-windows-8.0.08)も起動しています。

```cmd:
C:\mind9-beta\mind9-beta>bin\mind

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (オプション詳細を表示)
Usage(1): mind source library [objectdir\][objfile]

C:\mind9-beta\mind9-beta>c:\pmind\bin\mind

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (オプション詳細を表示)
Usage(1): mind source library [objectdir\][objfile]
```

## 参考 サンプルの格納フォルダ構成
下記のフォルダにMind7/8互換サンプルソースを格納しました。 callfunc.srcはMind9βでビルド済です。

```cmd:
C:\developments\vscode\mind9>dir

2025/01/10  00:12            74,752 callfunc.exe
2025/01/10  00:12                85 callfunc.his
2025/01/10  00:12            43,746 callfunc.mco
2024/03/16  21:59             1,280 callfunc.src
2025/01/10  00:12            30,432 callfunc.sym
2023/11/23  11:32             1,057 count2.src
2023/11/20  23:36               990 hello3.src
2024/03/18  00:24             7,095 mssqlodbc.src
               8 個のファイル             159,437 バイト
```

# VSCodeのターミナルで無事ビルド成功

VSCodeのターミナルで無事ビルド成功しました。

![mind9beta1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/e8ed7feb-b643-8ef4-25c4-d3cf8ed30dfc.png)


つづいて実行してみます。

```cmd:
C:\developments\vscode\mind9>callfunc.exe 40000
処理回数: 40000回
処理時間: 0ミリ秒

C:\developments\vscode\mind9>callfunc.exe 400000
処理回数: 400000回
処理時間: 63ミリ秒

C:\developments\vscode\mind9>callfunc.exe 4000000
処理回数: 4000000回
処理時間: 531ミリ秒
```

気のせいかもしれませんが、Mind8より若干速いような気がしますね。
この環境ですこしづつ新機能を評価してまいります。

# おわりに
いかがでしたでしょうか？まだほんのさわりの部分でものたりなかったかもしれません。今年で生誕４０周年を迎える日本語プログラミング言語Mind、ついにベールに包まれた新バージョンの全貌があかされはじめます！
