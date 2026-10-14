# はじめに
諸般の流れからC言語を使う機会が増えてきたので、あらためてVSCodeでC言語プログラミングができる環境構築を再確認しておきます。諸般の事情でWindows＋MSCです。今回はmakefileを使ってHelloWorldがビルドできる状況を確認します。HelloWorld単体をビルドするのにmakefileを使うことはあまり意味のないことかもしれませんが、シンプルな環境でなにか見えてくるものもあるかもしれないということで。

# 前提条件
VSCodeはなんらかのバージョンが既にインストールされていることが前提です。
MSCもなんらかのバージョンのVisualStudioのVisualC++がインストールされていることが前提です。
今回は具体的には下記のバージョンを想定してお話が進みます。[前回の記事](https://qiita.com/mylifewithviolin/items/c7747d2616213be9b442)でtasks.jsonとlaunch.jsonを生成して通常の[実行とデバッグ]からデバッグ開始できるようになったところからお話が進みます。

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
https://marketplace.visualstudio.com/items?itemName=ms-vscode.makefile-tools

# 前回の状態からVSCodeを起動
前回の記事の作業で下図のようになっているhelloworldにVisual Studio 2008 command promptを起動して移動します。
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
           launch.json
```
developer command prompt for vs 2022などでも基本はいっしょですがtasks.jsonなどに記述されたcl.exeなどの起動するバージョンが変化します。

```cmd:
Setting environment for using Microsoft Visual Studio 2008 x86 tools.

C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC>cd C:\developments\vscode\helloworld

C:\developments\vscode\helloworld>code .
```
helloworldがカレントディレクトリの状態からVSCodeを起動します。codeのあとに半角空白はさんでピリオド。下図のような状態のVSCodeが起動します。

![vscodec7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/1c1071b9-4005-f999-9e09-fa4e5229c306.png)

# Makefile
下図のようなmakefileをhelloworldフォルダに作成します。変数名は少しわたしの趣味がはいります。

```make:makefile
# コンパイラ・コンパイラオプションの指定
CC = cl
CFLAGS =/Zi /EHsc /nologo
# ターゲット・ソース・オブジェクトの指定
EXEC = helloworld.exe
SRCS = helloworld.c
OBJS = $(SRCS:.c=.obj)
# ターゲットファイル生成
$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) /Fe$(EXEC) 
# オブジェクトファイル生成
$(OBJS): $(SRCS)
	$(CC) $(CFLAGS) /c $(SRCS) /Fo$(OBJS) 
# all
all: $(OBJS) $(EXEC)
# clean
clean:
	rm -f $(OBJS) $(EXEC) *.d
```
# VS Code Makefile Tools
VS Code Makefile Toolsを構成していきます。
VS Codeの［ファイル］メニューから［ユーザー設定］－［設定］の順にクリックし、［拡張機能］の［makefile］を選択します。

今回はmakefileはプロジェクトルートにあるため、とくにパス指定は行っていません。MakeツールがMSのnmake.exeになりますので、そこは書き換える必要があります。

下図ではフルパスで書いてしまっていますが、開発者コマンドプロンプトのバージョンを変えて起動したとき、そのバージョンのnmakeを起動するためには実行ファイル名だけを記述します。

![vscodec8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9795493f-f69a-a9a3-06db-12adfa6edbbb.png)

続いて、コマンドパレットを開いて、makefileとタイプします。するといくつか候補が表示されますが、最初に出てくる「メイクファイル：クリーン構成」を選択するとなんだか構成が中途半端な感じとなります。

なにかを見たわけではないのですが、コマンド名を読んでみた感じいけそうでしたので選択するとよかったのは「メイクファイル：メイクファイル ツール拡張機能ワークスペースの状態をリセットする(トラブルシューティング)」です。

![vscodec9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/81527f10-5591-dcbc-6063-635a2ca2151a.png)

「メイクファイル：メイクファイル ツール拡張機能ワークスペースの状態をリセットする(トラブルシューティング)」を選択するとVSCodeが再起動して、下図のような[Makefile Tools]ビューが追加されます。

![vscodec10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/e8f7d3b7-52b4-5dcf-7ed4-9d0efe42b5f2.png)

# Make実行
[Makefile Tools]ビューで、「ターゲットのビルド」をクリックすると「all」が選択できますので、それを選択します。

[Makefile Tools]ビューのツールバーの左端の↓が凹にささっているみたいなアイコンをクリックするとmakeが開始されます。

ちょっとスクショが小さくて見づらいですが、下記のようにターミナルに出力されています。
```:ターミナル
Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        cl /Zi /EHsc /nologo /c helloworld.c /Fohelloworld.obj
helloworld.c
        cl /Zi /EHsc /nologo helloworld.obj /Fehelloworld.exe
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。
```
出力は下記のようになっています。
```:出力
Saving opened files before build.
Building target "all" with command: 'nmake.exe all'
Target "all" built successfully.
```

# つづく
今日はここまで。いちおうつづきがあります。
