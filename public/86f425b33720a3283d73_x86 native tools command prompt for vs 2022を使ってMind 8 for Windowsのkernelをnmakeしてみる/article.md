# はじめに
諸般の流れから日本語プログラミング言語Mind Windows版のkernelをnmakeしてみることを思いついたのでした。

# x86 native tools command prompt for vs 2022
マイクロソフトさんが提供してくれている、自力でコマンドラインコンパイラの環境つくるのが難儀なひとがめちゃくちゃ助かる環境です。

Visual Studio Community 2022のメニューグループには、下記の５つのコマンドラインツールが入っています。native toolsのネィティブの響きが.NETっぽくないので、Mind用にはx86 native tools でとりあえずトライしてみます。

**x86 native tools command prompt for vs 2022**
**x64 native tools command prompt for vs 2022**
**x86_x64 cross tools command prompt for vs 2022**
**x64_x86 cross tools command prompt for vs 2022**
**developer command prompt for vs 2022**

# とりあえず起動
とりあえず起動するとこんなプロンプトが開きます。
```
**********************************************************************
** Visual Studio 2022 Developer Command Prompt v17.4.4
** Copyright (c) 2022 Microsoft Corporation
**********************************************************************
[vcvarsall.bat] Environment initialized for: 'x86'

C:\Program Files\Microsoft Visual Studio\2022\Community>
```
Mindのカーネルのソースが格納されたフォルダへ移動して、コンパイラが動くか確認します。
```
C:\Program Files\Microsoft Visual Studio\2022\Community>cd C:\developments\mind8\kernel

C:\developments\mind8\kernel>cl
Microsoft(R) C/C++ Optimizing Compiler Version 19.34.31937 for x86
Copyright (C) Microsoft Corporation.  All rights reserved.

使い方: cl [ オプション... ] ファイル名... [ /link リンク オプション... ]
```
動いているようです。

# とりあえず0ker.cをコンパイル
１年前はubuntuでgccを適当に構成した後、いきなりmakeして大量の警告やエラーがシェルに流れ去るのをみて呆然とした記憶があるので、今回はとりあえず１ファイルコンパイルしてみます。
```
C:\developments\mind8\kernel>cl 0ker.c
Microsoft(R) C/C++ Optimizing Compiler Version 19.34.31937 for x86
Copyright (C) Microsoft Corporation.  All rights reserved.

0ker.c
0ker.c(49): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(50): error C2085: 'seisubuWoEru': 仮パラメーター リスト内にありません。
0ker.c(50): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(58): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(59): error C2085: 'syosubuWoEru': 仮パラメーター リスト内にありません。
0ker.c(59): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(67): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(68): error C2085: 'seisubuWoClear': 仮パラメーター リスト内にありません。
0ker.c(68): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(75): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(76): error C2085: 'seisuToSyosuWoPack': 仮パラメーター リスト内にありません。
0ker.c(76): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(88): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(89): error C2085: 'seisuToSyosuWoUnpack': 仮パラメーター リスト内にありません。
0ker.c(89): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(107): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(108): error C2085: 'mojiretuJyouhouBunkai': 仮パラメーター リスト内にありません。
0ker.c(108): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(121): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(122): error C2085: 'mojiretuJyouhouGousei': 仮パラメーター リスト内にありません。
0ker.c(122): error C2143: 構文エラー: ';' が '{' の前にありません。
0ker.c(132): error C2054: 'PRIVATE' の後に '(' が必要です。
0ker.c(133): error C2085: 'wordStore11': 仮パラメーター リスト内にありません。
0ker.c(133): error C2143: 構文エラー: ';' が '{' の前にありません。
```
gccでmakeしたときほどではないですが、けっこう出てますね。

# とりあえずmakefileをnmakeに認識させてみる

```
C:\developments\mind8\kernel>nmake

Microsoft(R) Program Maintenance Utility Version 14.34.31937.0
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
なんかちゃんと認識してるみたい。このあたりはLinux版で見覚えのあるusageですね。

# とりあえずnmake userkernelしてみる
せっかくなのでnmake userkernelしてみます。
```
C:\developments\mind8\kernel>nmake userkernel

Microsoft(R) Program Maintenance Utility Version 14.34.31937.0
Copyright (C) Microsoft Corporation.  All rights reserved.

        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\kernel.exe  obj\kernel.obj obj\startup.obj  obj\osfunc.obj obj\wincons0.obj  obj\regquery_lib.obj  WSOCK32.LIB advapi32.lib
Microsoft (R) Incremental Linker Version 14.34.31937.0
Copyright (C) Microsoft Corporation.  All rights reserved.

kernel.obj : error LNK2019: 未解決の外部シンボル _vsprintf が関数 _winprintf で参照されました
kernel.obj : error LNK2019: 未解決の外部シンボル _printf が関数 _c_test_push_quad で参照されました
startup.obj : error LNK2001: 外部シンボル _printf は未解決です
kernel.obj : error LNK2019: 未解決の外部シンボル ___iob_func が関数 _printStrinf で参照されました
kernel.obj : error LNK2019: 未解決の外部シンボル _sprintf が関数 _c_conv_to_string_quad で参照されました
kernel.obj : error LNK2019: 未解決の外部シンボル __snprintf が関数 _c_conv_to_string_fraction で参照されました
obj\kernel.exe : fatal error LNK1120: 5 件の未解決の外部参照
NMAKE : fatal error U1077: '"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\HostX86\x86\link.EXE"' : リターン コード '0x460'
Stop.

C:\developments\mind8\kernel>
```
gccでmakeしたときほどではないので、意外とエラーすくないです。これはmindの実行環境に影響を与えないようkernelフォルダだけ孤立して存在しているのが敗因でしょうか？

フォルダ構成はこんな感じです。いちどVisual Studio Community 2022でフォルダを開いています。
```
├─mind8
│  └─kernel
│      ├─.vs
│      │  └─kernel
│      │      ├─FileContentIndex
│      │      │  └─merges
│      │      └─v17
│      │          └─ipch
│      │              └─AutoPCH
│      │                  ├─8ed96e78fd484a8b
│      │                  ├─8fdb99d2fe173876
│      │                  ├─ec3e6dd585697c4c
│      │                  ├─f4ccbed58a3a6be1
│      │                  └─fe421fd58fcfa4c2
│      └─obj
```
# つづく
少し間があくかもしれませんがつづきます:sweat_smile:

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows

# 2024/02/07 追記
タイトルが若干異なりますが、本記事は下記の記事へ続きます。

https://qiita.com/mylifewithviolin/items/d039c83d359332d34caf
