# はじめに
諸般の流れからC言語を使う機会が増えてきたので、あらためてVSCodeでC言語プログラミングができる環境構築を再確認しておきます。世の中的にはGCCとかのがメジャーかもしれませんが、今回は諸般の事情でWindows＋MSCです。

# 前提条件
VSCodeはなんらかのバージョンがインストールされていることが前提です。
MSCもなんらかのバージョンのVisualStudioのVisualC++がインストールされていることが前提です。
今回は具体的には下記のバージョンを想定してお話が進みます。

Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Microsoft Visual C++ 2022 Community

## VSCodeの拡張機能
VSCodeの拡張機能も下記の通り入っていることが前提です。

C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

この記事に直接触れなくとも、はいっちゃっていますという意味で記載しているものもあります。
 
# 参考情報
定番のこれです。

https://code.visualstudio.com/docs/cpp/config-msvc

# tasks.json
これポイントですが、最初はVisualStudio(VSCodeではないやつ）の開発者コマンドプロンプトからVSCodeを起動するとあとでいろいろいじれるtasks.jsonをつくってくれるのでめっちゃラクです。

こんなフォルダを作成しておき開発者コマンドプロンプトで移動します。
```
C:\developments>tree
C:.
└─vscode
   └─helloworld
```

今回はVisual Studio 2008 command promptを起動してみました。
developer command prompt for vs 2022などでも基本はいっしょです。

```
Setting environment for using Microsoft Visual Studio 2008 x86 tools.

C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>cd C:\developments\vscode\helloworld

C:\developments\vscode\helloworld>
```
この状態からVSCodeを起動します。helloworldがカレントディレクトリというのがポイントです。codeのあとに半角空白はさんでピリオド。
```
C:\developments\vscode\helloworld>code .
```
helloworldフォルダを開いた状態でVSCodeが起動します。
helloworldフォルダに下記のようなCのソースコードファイルを作成します。参考情報はConfigure VS Code for Microsoft C++なのでC++のソースコードファイルが例示されていますが、本記事の課題はCの環境づくりなのでCのソースコードファイルを作成します。
```c:helloworld.c
#include <stdio.h>
 
int main(void)
{
	printf("Hello World !!\n");
 
	return 0;
}
```
このソースファイルをVSCodeのエディタで開くと下図のような状態となります。赤丸は既にブレークポイント設定している状態ですから気にしないでください。問題は、そこではなく、右上です。

![vscodec.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/631dc731-6609-67e0-9f6e-94b99ba5fb50.png)

右上左端の右三角に虫がひっついたようなアイコンにフォーカスすると、「C/C++ファイルのデバッグ」が、歯車アイコンにフォーカスすると「デバッグ構成の追加」がヒント表示されます。

右三角に虫がひっついたようなアイコンの右側の＾の逆向きのをクリックすると
「C/C++ファイルのデバッグ」
「C/C++ファイルの実行」
のメニューが表示されます。
「C/C++ファイルの実行」を選択してみます。下図の状態となりますので、「C/C++ cl.exe アクティブファイルのビルドとデバッグ」の方を選択します。こっちがMSCです。

![vscodec2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/800f26c2-aad6-beb2-0740-340691219797.png)

下図の状態となるとビルドと実行の成功です。
![vscodec3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ed2c5297-92ac-47e6-a31b-784deca29eea.png)

ターミナルに下記が出力されています。

Hello World !!
PS C:\developments\vscode\helloworld> 

この状態のフォルダを確認しますと、下図のように.vscodeフォルダが作成されて、tasks.jsonも作成されていることがわかります。
```
C:\DEVELOPMENTS\VSCODE
└─helloworld
   │  helloworld.c
   │  helloworld.exe
   │  helloworld.ilk
   │  helloworld.obj
   │  helloworld.pdb
   │  vc90.pdb
   │
   └─.vscode
           tasks.json
```
下図のようなtasks.jsonが生成されました。

```json:tasks.json
{
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: cl.exe アクティブなファイルのビルド",
            "command": "cl.exe",
            "args": [
                "/Zi",
                "/EHsc",
                "/nologo",
                "/Fe${fileDirname}\\${fileBasenameNoExtension}.exe",
                "${file}"
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": [
                "$msCompile"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "デバッガーによって生成されたタスク。"
        }
    ],
    "version": "2.0.0"
}
```
# launch.json
続いてlaunch.jsonの生成です。右上歯車アイコンをクリックすると下図の状態となります。

![vscodec4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/8f686e2c-1d71-c08a-6358-11ddf73d33c0.png)

既定となっている「C/C++ cl.exe アクティブファイルのビルドとデバッグ」の方を選択します。するとVSCodeは下図のようにlaunch.jsonを開いた状態となります。

![vscodec5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d706aa8d-c5d7-07fa-4acb-841734c4d011.png)

```json:launch.json
{
    "configurations": [
        {
            "name": "C/C++: cl.exe アクティブ ファイルのビルドとデバッグ",
            "type": "cppvsdbg",
            "request": "launch",
            "program": "${fileDirname}\\${fileBasenameNoExtension}.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "console": "integratedTerminal",
            "preLaunchTask": "C/C++: cl.exe アクティブなファイルのビルド"
        }
    ],
    "version": "2.0.0"
}
```
ここまでくれば、通常の[実行とデバッグ]からデバッグ開始できるようになります。

![vscodec6.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2a9c91c4-0af1-8141-7d52-91c779917265.png)

# つづく
今日はここまで。実はつづきがあります。VS Code Makefile Toolsを使ってみたいのでした。
