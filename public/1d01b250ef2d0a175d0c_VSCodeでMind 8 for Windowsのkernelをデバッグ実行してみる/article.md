# はじめに
VSCodeでMind 8 for WindowsのKernelを[Makefileを使ってビルドできました](https://qiita.com/mylifewithviolin/items/bb2ec642be78bff2787f)ので、今度はデバッグ実行してみます。

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

# 参考情報
https://devblogs.microsoft.com/cppblog/now-announcing-makefile-support-in-visual-studio-code/
# Makefile
Mind 8 for Windowsのmakefileをさらに下図のように簡略化します。Objサブフォルダの変数と指定ヶ所を削除しました。これは学習目的で記述内容を理解しやすくするためです。Mindのコアなファンの方々との情報共有です。

```make:makefile
# Copyright(C) 1985 Scripts Lab. Inc.

CC   = cl
WARNING = -W2
#OPT1    = -Ze    ←VC++ 9.0から抑制#
OPT1 =  /nologo /Zi /Od
CFLAGS_LINK     = $(WARNING) $(OPT1) /link
CFLAGS_NOLINK   = $(WARNING) $(OPT1) 
#↑注："-c"は上位側で付けること#
LINKFLAGS        = /SUBSYSTEM:console /MACHINE:IX86

RM = del


USERKERNEL = kernel
COMPKERNEL = compker

OSFUNC     = osfunc
WINCONSOLE = wincons
WINCONSOLE_0 = wincons0
WINCONSOLE_D = winconsd

MINDEXEC    = mindexec
EXECUTERSUB = mindex
EXECUTERSUBSUB = mindex_readmcode
KICKEREXCUTABLE = mindex.exe

STARTUP = startup
KERMAIN = kermain

SRCRUNTNO = runtno
SRCRUNTNO2 = runtno2

MINDCOMPILER = mind

#------------------------------------------------------#
include sources
#------------------------------------------------------#
usage:
	@echo ''
	@echo Usage:
	@echo '-----------'
	@echo     make all                    ユーザ用カーネルとコンパイラ用カーネルのコンパイル
	@echo ''
	@echo     make userkernel             ユーザ用カーネル
	@echo     make compilerkernel         コンパイラ用カーネル
	@echo ''
	@echo '-----------'
	@echo     make install                ユーザ用カーネルとコンパイラ用カーネルのインストール
	@echo ''
	@echo     make install-userkernel     ユーザ用カーネルのインストール
	@echo     make install-compilerkernel コンパイラ用カーネルのインストール	@echo ''

# -- make --------------------- #
all:	userkernel compilerkernel
#	#↑これらを $(～) に置き換えないこと! #
userkernel:     $(USERKERNEL).exe $(MINDEXEC).exe
compilerkernel: $(COMPKERNEL).exe $(MINDEXEC).exe

# -- words -------------------- #
allwords:	userwords compilerwords

userwords: c_words.wrd
compilerwords: c_words2.wrd

#------------------------------------------------------#
#                       カーネル本体                   #
#------------------------------------------------------#
#--exe--#
$(USERKERNEL).exe:  $(*B).obj $(STARTUP).obj $(OSFUNC).obj $(WINCONSOLE_0).obj regquery_lib.obj
	link $(LINKFLAGS) /OUT:$(*B).exe $(*B).obj $(STARTUP).obj $(OSFUNC).obj $(WINCONSOLE_0).obj \
		regquery_lib.obj WSOCK32.LIB advapi32.lib

$(COMPKERNEL).exe: 	$(*B).obj $(STARTUP).obj $(OSFUNC).obj \
		regquery_lib.obj
	link $(LINKFLAGS) /OUT:$(*B).exe $(*B).obj $(STARTUP).obj $(OSFUNC).obj \
		regquery_lib.obj advapi32.lib


#--obj--#
$(USERKERNEL).obj:  $(*B).c $(SRCRUNTNO).c c_words.def serialno.def $(OSFUNC).h $(WINCONSOLE_0).h regquery.c regquery_lib.h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj

$(COMPKERNEL).obj:  $(*B).c  $(SRCRUNTNO2).c c_words2.def serialno2.def $(OSFUNC).h regquery.c regquery_lib.h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj


#--共通ライブラリ--#
$(STARTUP).obj:     $(*B).c $(WINCONSOLE_0).h $(KERMAIN).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj

$(WINSSTARTUP).obj: $(*B).c $(WINCONSOLE).h $(KERMAIN).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj

$(OSFUNC).obj:      $(*B).c $(*B).h common.def
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj

$(WINCONSOLE_0).obj:$(*B).c $(*B).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj

$(WINCONSOLE_D).obj:$(WINCONSOLE).c $(WINCONSOLE).h
	$(CC) -c $(CFLAGS_NOLINK) $(WINCONSOLE).c /Fo$(*B).obj

regquery_lib.obj:   $(*B).c $(*B).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(*B).obj


#------------------------------------------------------#
#                 カーネル起動プログラム               #
#------------------------------------------------------#
#--通常カーネル起動用--#
$(MINDEXEC).exe: $(*B).c $(EXECUTERSUB).c $(EXECUTERSUBSUB).c try_multipath_exec.c \
		common.def $(OSFUNC).h kernel.def filenamehandle.c
	$(CC) $(*B).c $(OSFUNC).obj /Fo$(*B).obj $(CFLAGS_LINK) /OUT:$(*B).exe 	advapi32.lib

#------------------------------------------------------#
#                        clean操作                     #
#------------------------------------------------------#
clean:
	$(RM) *.obj
	$(RM) *.exe

clean-userwords:
	$(RM) c_words.*

clean-compilerwords:
	$(RM) c_words2.*

clean-kernels:
	$(RM) $(USERKERNEL).exe
	$(RM) $(USERKERNEL).obj
	$(RM) $(COMPKERNEL).exe
	$(RM) $(COMPKERNEL).obj

#------------------------------------------------------#
#                        words操作                     #
#------------------------------------------------------#
c_words.wrd: $(MINDWORD_SOURCES_NOT_DLL) kerbody.c 	$(SRCRUNTNO).c
	echo "c2wordsかけますか?"
	pause
	c2words $(USERKERNEL).c c_words
	..\bin\incrserial u

c_words2.wrd: $(MINDWORD_SOURCES_COMPILER) kerbody.c 
	c2words $(COMPKERNEL).c c_words2
	..\bin\incrserial 2

c_wordsg.wrd: $(MINDWORD_SOURCES_NOT_DLL) kerbody.c $(SRCRUNTNOCGI).c
	c2words $(CGIKERNEL).c c_wordsg
	..\bin\incrserial g

#------------------------------------------------------#
#                      install操作                     #
#------------------------------------------------------#
install: install-userkernel install-compilerkernel
#-----
install-userkernel:
	copy c_words.wrd ..\bin
	copy  kernel.exe ..\bin
	copy  mindexec.exe ..\bin

install-compilerkernel:
	copy c_words2.wrd  ..\bin
	copy  compker.exe ..\bin
	copy  mindexec.exe ..\bin
#EOF#

```
強烈に複雑であったMind8のmakefileも、ビルド対象のモジュールを２つに限定し、さらに出力用のサブフォルダも無くすことで、かなり構造が見えてきました。
installはMindの実行ファイルツールから一般的なCopyコマンドに書き換えていますので、本来の動きと異なるかもしれません。

## フォルダ構成
下図のようなフォルダ構成でobjフォルダはなくし、kernelフォルダにbinフォルダを併存させました。今回はbinフォルダからではなく、カレントフォルダから実行します。

```
C:\developments\vscode\mind8>tree
C:.
├─bin
└─kernel
```
Visual Studio 2008 command promptを開いて、mind8\kernelをカレントディレクトリとしてcode .でVSCodeを起動します。

# Make実行
[Makefile Tools]ビューで、「ターゲットのビルド」をクリックして「all」が選択できますので、それを選択します。
[Makefile Tools]ビューのツールバーの左端の↓が凹にささっているみたいなアイコンをクリックするとmakeが開始されます。

```
 実行するタスク: nmake all 

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        cl -c -W2 /nologo /Zi /Od kernel.c /Fokernel.obj
kernel.c
c:\developments\vscode\mind8\kernel\compword.c(2346) : warning C4047: '=' : 間接参照のレベルが 'char *' 
と 'ULONG' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2349) : warning C4047: '関数' : 間接参照のレベルが 'char **' と 'char *' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2349) : warning C4024: 'strtod' : の型が 2 の仮引数および
実引数と異なります。
c:\developments\vscode\mind8\kernel\dispword.c(273) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(357) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(365) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(376) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(384) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\3ker.c(303) : warning C4028: パラメータの型 1 が関数宣言と一致しませ
ん。
c:\developments\vscode\mind8\kernel\3ker.c(309) : warning C4028: パラメータの型 1 が関数宣言と一致しませ ん。
c:\developments\vscode\mind8\kernel\3ker.c(316) : warning C4028: パラメータの型 1 が関数宣言と一致しませ ん。
c:\developments\vscode\mind8\kernel\dosdep.c(888) : warning C4133: '関数' : 'int *' と 'char *' の間で型
に互換性がありません。
        cl -c -W2 /nologo /Zi /Od startup.c /Fostartup.obj
startup.c
        cl -c -W2 /nologo /Zi /Od osfunc.c /Foosfunc.obj
osfunc.c
        cl -c -W2 /nologo /Zi /Od wincons0.c /Fowincons0.obj
wincons0.c
        cl -c -W2 /nologo /Zi /Od regquery_lib.c /Foregquery_lib.obj
regquery_lib.c
        link /SUBSYSTEM:console /MACHINE:IX86 /OUT:kernel.exe kernel.obj startup.obj osfunc.obj wincons0.obj  regquery_lib.obj WSOCK32.LIB advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        cl mindexec.c osfunc.obj /Fomindexec.obj -W2 /nologo /Zi /Od /link /OUT:mindexec.exe    advapi32.lib
mindexec.c
LINK : 前回のインクリメンタル リンクで mindexec.exe が見つからなかったか、ビルドされませんでした。フル リンクを行います。
        cl -c -W2 /nologo /Zi /Od compker.c /Focompker.obj
compker.c
c:\developments\vscode\mind8\kernel\compword.c(2346) : warning C4047: '=' : 間接参照のレベルが 'char *' 
と 'ULONG' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2349) : warning C4047: '関数' : 間接参照のレベルが 'char **' と 'char *' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2349) : warning C4024: 'strtod' : の型が 2 の仮引数および 実引数と異なります。
c:\developments\vscode\mind8\kernel\dispword.c(273) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(357) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(365) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(376) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(384) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\3ker.c(303) : warning C4028: パラメータの型 1 が関数宣言と一致しませ
ん。
c:\developments\vscode\mind8\kernel\3ker.c(309) : warning C4028: パラメータの型 1 が関数宣言と一致しませ ん。
c:\developments\vscode\mind8\kernel\3ker.c(316) : warning C4028: パラメータの型 1 が関数宣言と一致しませ ん。
        link /SUBSYSTEM:console /MACHINE:IX86 /OUT:compker.exe compker.obj startup.obj osfunc.obj  regquery_lib.obj advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
とりあえずmakeは成功です。下図のようにディレクトリを照会すると、exeとobjファイルが生成されていることがわかります。

```
C:\developments\vscode\mind8\kernel>dir *.exe

 C:\developments\vscode\mind8\kernel のディレクトリ

2024/02/16  23:18           181,760 compker.exe
2024/02/16  23:18           291,840 kernel.exe
2024/02/16  23:18            74,752 mindexec.exe
               3 個のファイル             548,352 バイト
```
```
C:\developments\vscode\mind8\kernel>dir *.obj

 C:\developments\vscode\mind8\kernel のディレクトリ

2024/02/16  23:18           167,844 compker.obj
2024/02/08  23:18           545,262 kernel.obj
2024/02/16  23:18             9,234 mindexec.obj
2024/02/16  23:18             1,781 osfunc.obj
2024/02/16  23:18               993 regquery_lib.obj
2024/02/16  23:18             1,162 startup.obj
2024/02/16  23:18               724 wincons0.obj
               7 個のファイル             727,000 バイト
```
またコンパイルオプションを調整していますので、デバッグ用のシンボルファイルも生成されています。
```
C:\developments\vscode\mind8\kernel>dir *.pdb

 C:\developments\vscode\mind8\kernel のディレクトリ

2024/02/16  23:18         1,264,640 mindexec.pdb
2024/02/16  23:18            94,208 vc90.pdb
               2 個のファイル           1,358,848 バイト
```
# mindexecを実行
とりあえずmindexecをターミナルから実行します。中間コードファイルがなにもないので怒られます。
```
C:\developments\vscode\mind8\kernel>mindexec
Can't open Mcode file(C:\developments\vscode\mind8\kernel\mindexec.mco)
```
mindexec.mcoはないですね。
```
C:\developments\vscode\mind8\kernel>dir mindexec.mco

 C:\developments\vscode\mind8\kernel のディレクトリ

ファイルが見つかりません
```

# mindexecをデバッグ実行

それではmindexecをデバッグ実行してみます。

ここからですが、実は[Makefile Tools]のデバッグ実行ではなく、[C/C++ for Visual Studio Code] の機能を使ってデバッグ実行してみます。[Makefile Tools]の構成を試みているのですが、いまのところ成功していませんので、使い慣れている方でとりあえずやってみます。

## tasks.json
デバッグ実行で使用するタスクはmake allだけです。[C/C++ for Visual Studio Code]が自動生成したビルドタスクも参考に残していますが、今回は使用できません。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "make all",
            "type": "shell",
            "command": "nmake",
            "args": [
                "all"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "make clean",
            "type": "shell",
            "command": "nmake",
            "args": [
                "clean"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "make install",
            "type": "shell",
            "command": "nmake",
            "args": [
                "install"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
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
            "group": "build",
            "detail": "デバッガーによって生成されたタスク。"
        }
    ]
}
```

この構成により「タスクの実行」からmake all、make cleanなどが実行できるようになりました。

## launch.json
今回はこれで動いています。

```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "kernel debug",
            "type": "cppvsdbg",
            "request": "launch",
            "program": "${workspaceFolder}/mindexec.exe",
            //"program": "${fileDirname}\\mindexec.exe",
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
//"program": "${fileDirname}\\mindexec.exe",の方とすると実行ファイルが.vscodeフォルダにあるかのようなエラーとなったため、上図のようにしています。

# デバッグ実行開始
mindexec.cはmindex.cをインクルードしているだけなので、下図のmindex.cの中のint main(int argc, char **argv)の中の適当なところ（なるべく手前、mcoファイルを開くより前）にブレークポイントを設定します。

![vscodec12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/94206373-59fe-311b-4770-19a8a62d1ddd.png)

では、通常の[実行とデバッグ]から[kernel debug]でデバッグ開始します。

![vscodec13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/a15f8ad0-3612-757f-0eb9-421c5268cb92.png)

無事にブレークしました！:tada::tada::tada::tada::confetti_ball:

# おわりに
少し間があくかもしれませんが、Mind8コンパイラをデバッグ実行できるようになったので、この後はMind8コンパイラのインサイドな動きを追跡レポートしてまいりたいと考えています。
