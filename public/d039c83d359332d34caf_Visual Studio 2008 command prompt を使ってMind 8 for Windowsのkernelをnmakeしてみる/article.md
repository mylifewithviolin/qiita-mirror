# はじめに
諸般の流れから日本語プログラミング言語Mind8 Windows版のkernelをmakeしてみることを思いついたのでした。前記事で無謀にもVisual Studio Community 2022のx86 native tools command prompt for vs 2022でnmakeを行うもみごとに失敗。Mind開発者の@killyさんよりMind8 Windows版の開発環境はVisual Studio 2008 との情報共有をいただき、さっそくのリトライです。

# Visual Studio 2008 command prompt
マイクロソフトさんが提供してくれている、自力でコマンドラインコンパイラの環境つくるのが難儀なひとがめちゃくちゃ助かる環境です。ある意味、Visual Studio 2022のx86 native tools command prompt for vs 2022の祖先みたいなものですね。パス設定とかもちろんできないわけではありませんが、お時間の制約上なるべくはしょれる工程があると助かります。

# とりあえず起動
とりあえず起動するとこんなプロンプトが開きます。
```
Setting environment for using Microsoft Visual Studio 2008 x86 tools.

C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>
```
x86 native tools command prompt for vs 2022に比べるとちょっと地味。

Cコンパイラとnmakeが動くか確認します。
```
C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>cl
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

使い方: cl [ オプション... ] ファイル名... [ /link リンク オプション... ]

C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>nmake

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

NMAKE : fatal error U1064: MAKEFILE が見つかりません、またターゲットが指定されていません。
Stop.

```
動いています！いけそうな予感。
ではMind8のkernelのソースコード一式が格納されているフォルダへ移動して、makefileが認識されるか確認します。
```
C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>cd C:\developments\mind8\kernel

C:\developments\mind8\kernel>cd C:\developments\mind8\kernel

C:\developments\mind8\kernel>nmake

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

''
Usage:
'-----------'
make all コンパイラ用カーネル以外のすべてのコンパイル
''
make userkernel ユーザ用カーネル
make cgikernel CGI用カーネル
make winkernel Windows-GUIカーネル
make winskernel サイレントWinカーネル
make compilerkernel コンパイラ用カーネル
''
'-----------'
make install コンパイラ用カーネル以外のすべてのインストール
''
make install-userkernel ユーザ用カーネルのインストール
make install-cgikernel CGI用カーネルのインストール
make install-winkernel Windows-GUIカーネルのインストール
make install-winskernel サイレントWinカーネルのインストール
make install-compilerkernel コンパイラ用カーネルのインストール @echo ''
```
認識しています！よりいっそういけそうな予感。

# とりあえずnmake userkernelしてみる
では、いけそうなのでいきなりnmake userkernelしてみます。
```
C:\developments\mind8\kernel>nmake userkernel

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\kernel.exe  obj\kernel.obj obj\startup.obj  obj\osfunc.obj obj\wincons0.obj  obj\regquery_lib.obj  WSOCK32.LIB advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.


C:\developments\mind8\kernel>
```
ああっ、ほんとにいけた！:tada:かなりうれしいです。killyさん、ありがとうございます。

# つづいてnmake compilerkernelしてみる
ここからは失敗する要素が感じられないので、どんどんいけいけムードです。
```
C:\developments\mind8\kernel>nmake compilerkernel

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\compker.exe  obj\compker.obj obj\startup.obj  obj\osfunc.obj  obj\regquery_lib.obj  advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.


C:\developments\mind8\kernel>
```
昨日までの警告とエラーの嵐がうそのようにキレイに成功しました。
※といってもLinux版をgccでmakeしたときの暴風雨のようなエラーの嵐に比べればだいぶ静かではありましたが:sweat_smile:

# そしてnmake allしてみる
```
C:\developments\mind8\kernel>nmake all

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\cgiker.exe  obj\cgiker.obj obj\startup.obj  obj\osfunc.obj obj\wincons0.obj  obj\regquery_lib.obj  WSOCK32.LIB advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

NMAKE : fatal error U1073: 'runtnows.c' のビルド方法が指定されていません。
Stop.

C:\developments\mind8\kernel>
```
おおっここでついにfatal errorが。なにかオプションを要求されているような。

# つづく
とりあえず基本的なビルド環境はできたみたいな感じ。少し間があくかもしれませんがつづきます:sweat_smile:

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
