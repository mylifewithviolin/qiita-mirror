# はじめに
この記事のお題はCのdllをCのコンソールアプリケーションから呼び出す際のヘッダファイルの書き方の備忘録です。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022


# お題のソースコード
Cのコンソールアプリケーション
```c:consoleApp.c
#include<stdio.h>

#include "dllMain.h"

__declspec(dllimport) void exec();

void main() {
	exec();
}
```

Cのdll（ダイナミックリンクライブラリ）
```c:dllMain.c
#include<stdio.h>

#define _EXPORTING

#include "dllMain.h"

__declspec(dllexport) void exec(){
	printf("Hello World!\n");
}
```

Cのdll（ダイナミックリンクライブラリ）のヘッダファイル
```c:dllMain.h
#pragma once

#ifdef _EXPORTING
#define FUNC_DECLSPEC    __declspec(dllexport)
#else
#define FUNC_DECLSPEC    __declspec(dllimport)
#endif

FUNC_DECLSPEC void exec();
```
当初VS2022のプロジェクトひな形にC++のDLLを指定したので、ヘッダファイルにC++のプリプロセッサディレクティブ#pragma onceが残っています。細かいことは気にしない。


 # ビルド結果
 それではビルドしてみます。ビルド成功のための構成は後でご説明いたします。
```
 リビルドを開始しました...
1>------ すべてのリビルド開始: プロジェクト:mssqlodbc32, 構成: Debug Win32 ------
1>dllMain.c
1>   ライブラリ C:\developments\dllMain\Debug\dllMain.lib とオブジェクト C:\developments\dllMain\Debug\dllMain.exp を作成中
1>dllMain.vcxproj -> C:\developments\dllMain\Debug\dllMain.dll
2>------ すべてのリビルド開始: プロジェクト:ConsoleApp, 構成: Debug Win32 ------

2>consoleApp.c
2>ConsoleApp.vcxproj -> C:\developments\dllMain\Debug\ConsoleApp.exe
========== すべて再構築: 2 正常終了、0 失敗、0 スキップ ==========
=========== 経過時間 00:07.608 ==========
```

 # 実行結果
 それでは実行してみます。
```
Hello World!

C:\developments\dllMain\Debug\ConsoleApp.exe (プロセス 15144) は、コード 0 で終了しました。
デバッグが停止したときに自動的にコンソールを閉じるには、[ツール] -> [オプション] -> [デバッグ] -> [デバッグの停止時に自 動的にコンソールを閉じる] を有効にします。
このウィンドウを閉じるには、任意のキーを押してください...
```

無事にdll経由でHello World!できました。

 # 配置情報
 このビルドを成功させるためのソリューション、プロジェクトの配置についてご説明します。
 こんな感じです。dllMain.hはConsoleApp側にもコピーして配置しています。
```
 C:.
│  dllMain.sln
│
├─ConsoleApp
│  │  ConsoleApp.vcxproj
│  │  consoleApp.c
│  │  dllMain.h
│  └─Debug
│
├─Debug
│      ConsoleApp.exe
│      ConsoleApp.pdb
│      dllMain.dll
│      dllMain.exp
│      dllMain.lib
│      dllMain.pdb
│
└─dllMain
    │  dllMain.vcxproj
    │  dllMain.c
    │  dllMain.h
    └─Debug
```
dll側のCソースには下記の定義があるため
```c
#define _EXPORTING
```
dll側のヘッダファイルdllMain.hでは
```c
#define FUNC_DECLSPEC    __declspec(dllexport)
```
が処理され、
コンソールアプリ側のCソースにはこの定義がないため
コンソールアプリ側のヘッダファイルdllMain.hでは
```c
#define FUNC_DECLSPEC    __declspec(dllimport)
```
が処理され、
```c
FUNC_DECLSPEC void exec();
```
は、それぞれの意味となって、双方で共通のヘッダファイルとしてインクルードできるようになります。

 # よくあるビルドエラー


 C:\developments\dllMain\Debug\dllMain.libのパスをコンソールアプリ側のプロジェクトのプロパティの
 リンカー->入力->追加の依存ファイル
 に設定し忘れているとConsoleApp側のビルドが下記のように失敗します。
```
2>consoleApp.c
2>consoleApp.obj : error LNK2019: 未解決の外部シンボル __imp__exec が関数 _main で参照されました
2>C:\developments\dllMain\Debug\ConsoleApp.exe : fatal error LNK1120: 1 件の未解決の外部参照
2>C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Microsoft\VC\v170\Microsoft.CppCommon.targets(1096,5): error MSB6006: "link.exe" はコード 1120 を伴って終了しました。
2>プロジェクト "ConsoleApp.vcxproj" のビルドが終了しました -- 失敗。
```

 # おわりに
C言語でのdll作成の情報は少ないので何かの参考になれば幸いです。
