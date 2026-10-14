# はじめに
諸般の流れからTcl(Tool Command Language)を使う機会が増えてきたので、あらためてVSCodeでTclのC言語プログラミングができる環境構築を再確認しておきます。世の中的にはGCCとかのがメジャーかもしれませんが、今回も諸般の事情でWindows＋MSCです。

# 前提条件
VSCodeはなんらかのバージョンがインストールされていることが前提です。
MSCはバージョンのVisualStudioのVisualC++がインストールされていることが前提です。
今回は具体的には下記のバージョンを想定してお話が進みます。

Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.97.2
Microsoft Visual C++ 2022 Community
irontcl-win32-8.6.7


## VSCodeの拡張機能
VSCodeの拡張機能も下記の通り入っていることが前提です。

C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

この記事に直接触れなくとも、はいっちゃっていますという意味で記載しているものもあります。

# 参考情報
 VSCodeでC言語プログラミングができる環境構築はこちらを参考にしました。
 
https://qiita.com/mylifewithviolin/items/c7747d2616213be9b442

# irontclのダウンロード

ビルド済のTclのirontclを下記よりダウンロードします。

https://www.irontcl.com/index.html

x64とx86があります。両方ダウンロードしておくとよいでしょう。
irontcl-win32-8.6.7.zip
irontcl-amd64-8.6.7.zip

# irontcl-win32-8.6.7のフォルダ構成
今回はirontcl-win32-8.6.7を使用します。zipを解凍すると下記のフォルダが展開します。

```cmd:
C:\mind9-beta\irontcl-win32-8.6.7\IronTcl>tree
C:.
├─bin
├─doc
├─include
│  └─X11
└─lib
    ├─dde1.4
    ├─reg1.3
    ├─tcl8
    │  ├─8.4
    │  │  └─platform
    │  ├─8.5
    │  └─8.6
    ├─tcl8.6
    │  ├─encoding
    │  ├─http1.0
    │  ├─msgs
    │  ├─opt0.4
    │  └─tzdata
    │      ├─Africa
    │      ├─America
    │      │  ├─Argentina
    │      │  ├─Indiana
    │      │  ├─Kentucky
    │      │  └─North_Dakota
    │      ├─Antarctica
    │      ├─Arctic
    │      ├─Asia
    │      ├─Atlantic
    │      ├─Australia
    │      ├─Brazil
    │      ├─Canada
    │      ├─Chile
    │      ├─Etc
    │      ├─Europe
    │      ├─Indian
    │      ├─Mexico
    │      ├─Pacific
    │      ├─SystemV
    │      └─US
    └─tk8.6
```

# プロジェクトの構成
上記フォルダのbinフォルダからtcl86t.dllを、libフォルダからtcl86t.libを、includeフォルダからヘッダファイルを、下記のようにプロジェクトフォルダにコピーします。

```cmd:
C:\developments\vscode\tcl>tree /F
C:.
│  sample.c
│  tcl.decls
│  tcl.h
│  tcl86t.dll
│  tcl86t.lib
│  tclDecls.h
│  tclOO.h
│  tclOODecls.h
│  tclPlatDecls.h
│  tclTomMath.h
│  tclTomMathDecls.h
│  tk.h
│  tkDecls.h
│  tkIntXlibDecls.h
│  tkPlatDecls.h
│  tommath_class.h
│  tommath_superclass.h
│
└.vscode
      c_cpp_properties.json
      launch.json
      tasks.json
```
# お題のソースコード

sample.cを下記のように記述します。

```c:sample.c
#include <tcl.h>

int main() {
    Tcl_Interp *interp = Tcl_CreateInterp();
    Tcl_Eval(interp, "puts {Hello from Tcl!}");
    Tcl_DeleteInterp(interp);
    return 0;
}

```
# お題のソースコードの実行

x86 Native Tools Command Prompt for vs 2022を起動します。カレントフォルダをプロジェクトフォルダに移動します。

```
**********************************************************************
** Visual Studio 2022 Developer Command Prompt v17.12.5
** Copyright (c) 2022 Microsoft Corporation
**********************************************************************
[vcvarsall.bat] Environment initialized for: 'x86'

C:\Program Files\Microsoft Visual Studio\2022\Community>cd C:\developments\vscode\tcl

C:\developments\vscode\tcl>code .
```

この状態からVSCodeを起動します。ビルドを開始します。

```
ビルドを開始しています...
cmd /c chcp 65001>nul && cl.exe /Zi /EHsc /nologo /IC:\developments\vscode\tcl /FeC:\developments\vscode\tcl\sample.exe C:\developments\vscode\tcl\sample.c C:\developments\vscode\tcl\tcl86t.lib
sample.c

ビルドが正常に完了しました。
```
ターミナルに下記の出力が出れば成功です。

```powershell:
Hello from Tcl!
```

# おわりに
いかがでしたでしょうか？なにかのお役にたてれば幸いです。
