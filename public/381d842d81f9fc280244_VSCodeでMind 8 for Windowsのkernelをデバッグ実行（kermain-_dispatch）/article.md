# はじめに
VSCodeでMind 8 for WindowsのKernelを[デバッグ実行できました](https://qiita.com/mylifewithviolin/items/96168b67c59ff03bf236)ので、今回も引き続きそのデバッグ途中のご様子のレポートです。※注 デバッグの言い回しですが、もちろんデバッグが目的ではなく、学習目的でステップ実行しているだけです。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

# デバッグ実行の前提条件
Mind開発者の@killyさんからの前回記事コメントでのさらなる情報共有で、mrunt010.exeがkernel.exeがリネームされたランタイムであることが判明。今回は前回に続きmcodeファイルはhello.mcoを使い（mindexc.mcoに逆リネーム）kernel.exeの実質メインソースのkermain.cがステップ実行できる環境を構築します。
kernel.cがkerbody.cをインクルードしてkerbody.cがkermain.cをインクルードするという複雑な入れ子構造をなしています。
## mindex.c
mindex.cの下記のヶ所mrunt010.exeをローンチする直前で、プログラム名をオリジナルのkernel.exeのまま起動するように細工します。

```diff_c:mindex.c
	//strcat( FullpathRuntname, RuntimeProgname );
+	strcat( FullpathRuntname, "kernel.exe" );

 	retcode = spawnv( P_WAIT, FullpathRuntname, &(Argv[0]) );
 ```
 この修正はmindexec.exeからkernel.exeのファイル名状態でのローンチを確認するためだけのもので、VSCodeのlaunch.jsonを下記のように修正した後は不要です。
 
## launch.json
VSCodeのデバッグローンチのファイル名をkernel.exeに変更します。

```diff_json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "kernel debug",
            "type": "cppvsdbg",
            "request": "launch",
            //"program": "${workspaceFolder}/mindexec.exe",            
+            "program": "${workspaceFolder}/kernel.exe",
            "args": [
                "mindexec.mco"
            ],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "console": "integratedTerminal",
            "preLaunchTask": "make all"
        }
    ]

```
## Makefile
makefileも下記のkernel.exeをビルドするヶ所のコマンドをlinkからclに変更してデバッグシンボルの生成オプションを追加します。

```diff_make:makefile
# Copyright(C) 1985 Scripts Lab. Inc.
CC   = cl
OPT1 =  /nologo /Zi /Od

#------------------------------------------------------#
#                       カーネル本体                   #
#------------------------------------------------------#
#--exe--#
$(USERKERNEL).exe:  $(*B).obj $(STARTUP).obj $(OSFUNC).obj $(WINCONSOLE_0).obj regquery_lib.obj
	$(CC) $(LINKFLAGS) $(OPT1) /OUT:$(*B).exe $(*B).obj $(STARTUP).obj $(OSFUNC).obj $(WINCONSOLE_0).obj \
		regquery_lib.obj WSOCK32.LIB advapi32.lib
```

# デバッグ実行中のご様子
最初から下図の状態までいったわけではありませんが、makefileの構成でkernel.exeのデバッグシンボルkernel.pdbが生成されるようになってからは無事にkermain.cにブレークするようになりました。

![vscodec18.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ff5cc423-0e23-3cb3-7981-ae71275e7ca5.png)

上図はkermain.cのexecute_main_wordという関数内のsetupForDispatchという関数でブレークしているところです。

setupForDispatch関数内のcheckMyEndian、openMcodeFile、strcmpNocaseなどを経て、同じくexecute_main_word関数内からdispatch.c内のdispatcher()という関数が実行されます。下図はその関数内の実行の様子です。


![vscodec19.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/569b93e5-2e45-384e-b260-597be44f5319.png)

このループの中でMコードが評価されて対応関数が実行されるようでした。このループを抜けたところで
「こんにちは、Ｍｉｎｄです。」
がコンソール出力されます。

# おわりに
またまたタイムアウトしてしまいました。（出かけます。）次回はこの「こんにちは、Ｍｉｎｄです。」がコンソール出力されるdispatcher()の様子を深堀します。
