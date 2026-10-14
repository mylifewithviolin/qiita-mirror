# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)でVSCodeでMind 8 for Windowsのkernelをデバッグ実行できる環境をつくりました。

今回はMind8の中間コードディスパッチャ（の一部）をCからC#に書き換えてみるという野望に進行するための第1歩として、C#とMind8を混在ビルドする環境をVSCodeで構築します。.NETCoreのバージョンは6から8にあげておきます。それに伴いC#のバージョンも10から12になります。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
C# 12 
dotnet-sdk-8.0.204-win-x64

このテーマでは処理単語の追加はなく、既存単語のMCode（の一部）を解釈実行する部分をCからC#に書き換えるというお題のため、辞書再構築ツールは使用しないので、Mind7ライセンスは不要です。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

C/C++のデバッガは直接使わないのですが、Cで実装されているMind8kernelの動作をデバッグ実行で探るために使用します。[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境となります。

# C#環境の構成
最初にC#のプロジェクトを作成してVSCodeを起動します。

```
C:\developments\vscode>dotnet --version
8.0.204

C:\developments\vscode>dotnet new console -o mind8dispatch
テンプレート "コンソール アプリ" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\mind8dispatch\mind8dispatch.csproj を復元しています:
  復元対象のプロジェクトを決定しています...
  C:\developments\vscode\mind8dispatch\mind8dispatch.csproj を復元しました (132 ms)。
正常に復元されました。

C:\developments\vscode>cd mind8dispatch
C:\developments\vscode\mind8dispatch>code .
```

下記のサンプルソースが生成されています。
```cs:Program.cs
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```

## デバッグ実行開始
VSCodeの実行とデバッグに「.NET Core Launch (console)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され
```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\mind8dispatch/mind8dispatch.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+b34f75857 (.NET)
  復元対象のプロジェクトを決定しています...
  復元対象のすべてのプロジェクトは最新です。

  復元対象のすべてのプロジェクトは最新です。
  mind8dispatch -> C:\developments\vscode\mind8dispatch\bin\Debug\net8.0\mind8dispatch.dll
```

デバッグコンソールにC#サンプルアプリの実行結果が表示されます。
```
Hello, World!
プログラム '[6636] mind8dispatch.dll' がコード 0 (0x0) で終了しました。
```

# Mind8環境の構成
つづいてMind8アプリがビルドできる環境を構成します。下記のサンプルソースファイルを作成します。

```mind:hello.src
メインとは
　　　　「Hello by mind8」を　表示すること。
```
ターミナルでコマンドプロンプトを開いてMind8の開発環境を設定します。
```
Microsoft Windows [Version 10.0.22621.3447]
(c) Microsoft Corporation. All rights reserved.

C:\developments\vscode\mind8dispatch>c:\pmind\usemind
myfolder=pmind\
myfolder=pmind
newpath=[]
Mindの開発環境を設定しました。

c:\pmind>
```
パスを元に戻して、正規のMind8コンパイラで正規のFileライブラリでサンプルソースをコンパイルします。
```
c:\pmind>cd c:\developments\vscode\mind8dispatch
c:\developments\vscode\mind8dispatch>mind hello file  

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> hello.exe
```
正常コンパイルされたMind8アプリを実行します。正常に実行できました。
```
c:\developments\vscode\mind8dispatch>hello
Hello by mind8
c:\developments\vscode\mind8dispatch>
```

今回はMind8側のコンパイル・実行・デバッグ環境構築にはほぼまったく力は入れません。下記に生成されたhello.mcoはしばらく再コンパイルしません。ひたすらこの中身を解釈していくことが本記事シリーズのお題です。

```
c:\developments\vscode\mind8dispatch>dir hello.mco

2024/04/18  20:53            43,544 hello.mco
               1 個のファイル              43,544 バイト
```

# つづく
ここに生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりがいま始まろうとしています。
