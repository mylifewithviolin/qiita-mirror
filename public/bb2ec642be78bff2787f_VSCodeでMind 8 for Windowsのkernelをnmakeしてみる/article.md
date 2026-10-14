# はじめに
VSCodeでHelloWorldがmakefileを使ってビルドできたので、今回は調子にのってMind 8 for WindowsのKernelをVSCodeでビルドしてみます。

# 前提条件
VSCodeはなんらかのバージョンが既にインストールされていることが前提です。
MSCは2008バージョンのVisualStudioのVisualC++がインストールされていることが前提です。
今回は具体的には下記のバージョンを想定してお話が進みます。[前回の記事](https://qiita.com/mylifewithviolin/items/169ef33e012a210da71f)でVS Code Makefile Toolsを構成して[Makefile Tools]ビューでビルドできるようになったところからお話が進みます。

Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows

## VSCodeの拡張機能
VSCodeの拡張機能も下記の通り入っていることが前提です。

C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

# 参考情報

https://qiita.com/mylifewithviolin/items/d039c83d359332d34caf

# Makefile
Mind 8 for Windowsのmakefileを下図のように簡略化します。ビルド対象からはずしたモジュールに使用されていた変数も削除します。Mind 8 for Windowsのソースコードはオープンですが利用条件不明のため（本件開発者の@killyさんのご了解いただいている認識ですが）コピーライト記載させていただきます。

```make:makefile
# Copyright(C) 1985 Scripts Lab. Inc.

CC   = cl
OBJDIR = obj

WARNING = -W2
#OPT1    = -Ze    ←VC++ 9.0から抑制#
WINLIBS_FOR_NOT_GUI = WSOCK32.LIB advapi32.lib
CFLAGS_LINK     = $(WARNING) $(OPT1) /link
CFLAGS_NOLINK   = $(WARNING) $(OPT1)
#↑注："-c"は上位側で付けること#
LINKFLAGS        = /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86

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

userkernel:     $(OBJDIR)\$(USERKERNEL).exe $(OBJDIR)\$(MINDEXEC).exe

compilerkernel: $(OBJDIR)\$(COMPKERNEL).exe $(OBJDIR)\$(MINDEXEC).exe


# -- words -------------------- #
allwords:	userwords compilerwords

userwords: c_words.wrd
compilerwords: c_words2.wrd


#------------------------------------------------------#
#                       カーネル本体                   #
#------------------------------------------------------#
#--exe--#
$(OBJDIR)\$(USERKERNEL).exe:  \
		$(OBJDIR)\$(*B).obj $(OBJDIR)\$(STARTUP).obj \
		$(OBJDIR)\$(OSFUNC).obj $(OBJDIR)\$(WINCONSOLE_0).obj \
		$(OBJDIR)\regquery_lib.obj
	link $(LINKFLAGS) /OUT:$(OBJDIR)\$(*B).exe \
		$(OBJDIR)\$(*B).obj $(OBJDIR)\$(STARTUP).obj \
		$(OBJDIR)\$(OSFUNC).obj $(OBJDIR)\$(WINCONSOLE_0).obj \
		$(OBJDIR)\regquery_lib.obj \
		$(WINLIBS_FOR_NOT_GUI)

$(OBJDIR)\$(COMPKERNEL).exe:  \
		$(OBJDIR)\$(*B).obj $(OBJDIR)\$(STARTUP).obj \
		$(OBJDIR)\$(OSFUNC).obj \
		$(OBJDIR)\regquery_lib.obj
	link $(LINKFLAGS) /OUT:$(OBJDIR)\$(*B).exe \
		$(OBJDIR)\$(*B).obj $(OBJDIR)\$(STARTUP).obj \
		$(OBJDIR)\$(OSFUNC).obj \
		$(OBJDIR)\regquery_lib.obj \
		advapi32.lib


#--obj--#
$(OBJDIR)\$(USERKERNEL).obj:  $(*B).c \
		$(NOMIND_SOURCES) $(MINDWORD_SOURCES_NOT_DLL) \
		$(SRCRUNTNO).c c_words.def serialno.def \
		$(OSFUNC).h $(WINCONSOLE_0).h \
		regquery.c regquery_lib.h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\$(COMPKERNEL).obj:  $(*B).c \
		$(NOMIND_SOURCES) $(MINDWORD_SOURCES_COMPILER) \
		$(SRCRUNTNO2).c c_words2.def serialno2.def \
		$(OSFUNC).h \
		regquery.c regquery_lib.h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

#--共通ライブラリ--#
$(OBJDIR)\$(STARTUP).obj:     $(*B).c $(WINCONSOLE_0).h $(KERMAIN).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\$(WINSSTARTUP).obj: $(*B).c $(WINCONSOLE).h $(KERMAIN).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\$(OSFUNC).obj:      $(*B).c $(*B).h common.def
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\$(WINCONSOLE_0).obj:$(*B).c $(*B).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\$(WINCONSOLE_D).obj:$(WINCONSOLE).c $(WINCONSOLE).h
	$(CC) -c $(CFLAGS_NOLINK) $(WINCONSOLE).c /Fo$(OBJDIR)\$(*B).obj

$(OBJDIR)\regquery_lib.obj:   $(*B).c $(*B).h
	$(CC) -c $(CFLAGS_NOLINK) $(*B).c /Fo$(OBJDIR)\$(*B).obj


#------------------------------------------------------#
#                 カーネル起動プログラム               #
#------------------------------------------------------#
#--通常カーネル起動用--#
$(OBJDIR)\$(MINDEXEC).exe: $(*B).c $(EXECUTERSUB).c $(EXECUTERSUBSUB).c try_multipath_exec.c \
		common.def $(OSFUNC).h kernel.def filenamehandle.c
	$(CC) $(*B).c $(OBJDIR)\$(OSFUNC).obj /Fo$(OBJDIR)\$(*B).obj \
		$(CFLAGS_LINK) /OUT:$(OBJDIR)\$(*B).exe \
		advapi32.lib


#------------------------------------------------------#
#                        clean操作                     #
#------------------------------------------------------#

clean:
	$(RM) $(OBJDIR)\*.obj
	$(RM) $(OBJDIR)\*.exe

clean-userwords:
	$(RM) c_words.*

clean-compilerwords:
	$(RM) c_words2.*

clean-kernels:
	$(RM) $(OBJDIR)\$(USERKERNEL).exe
	$(RM) $(OBJDIR)\$(USERKERNEL).obj
	$(RM) $(OBJDIR)\$(COMPKERNEL).exe
	$(RM) $(OBJDIR)\$(COMPKERNEL).obj

#------------------------------------------------------#
#                        words操作                     #
#------------------------------------------------------#
c_words.wrd: \
		$(MINDWORD_SOURCES_NOT_DLL) kerbody.c \
		$(SRCRUNTNO).c
	echo "c2wordsかけますか?"
	pause
	c2words $(USERKERNEL).c c_words
	..\bin\incrserial u

c_words2.wrd: \
		$(MINDWORD_SOURCES_COMPILER) kerbody.c 
	c2words $(COMPKERNEL).c c_words2
	..\bin\incrserial 2

c_wordsg.wrd: \
		$(MINDWORD_SOURCES_NOT_DLL) kerbody.c \
		$(SRCRUNTNOCGI).c
	c2words $(CGIKERNEL).c c_wordsg
	..\bin\incrserial g


#------------------------------------------------------#
#                      install操作                     #
#------------------------------------------------------#
install: install-userkernel install-compilerkernel

#-----
install-userkernel:
	..\bin\copyrunt c_words.wrd obj ..\bin
	..\bin\mcpC  $(OBJDIR)\$(MINDEXEC).exe ..\bin\$(KICKEREXCUTABLE) -puvn

install-compilerkernel:
	..\bin\copyrunt c_words2.wrd obj ..\bin
	..\bin\mcpC  $(OBJDIR)\$(MINDEXEC).exe ..\bin\$(KICKEREXCUTABLE) -puvn

#EOF#

```
強烈に複雑であったMind8のmakefileも、ビルド対象のモジュールを２つに限定することで、構造が見えてくるものがあります。

下図のようなフォルダ構成でobjフォルダは空の状態とします。
Visual Studio 2008 command promptを開いて、mind8kernelをカレントディレクトリとしてcode .でVSCodeを起動します。
```
C:\developments\vscode\mind8kernel>tree
C:.
├─.vscode
└─obj
```
下図のような感じでVSCodeが開きます。

![vscodec11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4e44ebea-a683-9fbe-7fc0-8956737fa361.png)

# Make実行
[Makefile Tools]ビューで、「ターゲットのビルド」をクリックすると「all」が選択できますので、それを選択します。

[Makefile Tools]ビューのツールバーの左端の↓が凹にささっているみたいなアイコンをクリックするとmakeが開始されます。

```
Copyright (C) Microsoft Corporation.  All rights reserved.

kernel.c
c:\developments\vscode\mind8kernel\compword.c(2346) : warning C4047: '=' : 間接参照のレベルが 'char *' と 'ULONG' で異なっています。
c:\developments\vscode\mind8kernel\compword.c(2349) : warning C4047: '関 数' : 間接参照のレベルが 'char **' と 'char *' で異なっています。        
c:\developments\vscode\mind8kernel\compword.c(2349) : warning C4024: 'strtod' : の型が 2 の仮引数および実引数と異なります。
c:\developments\vscode\mind8kernel\dispword.c(273) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(357) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(365) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(376) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(384) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\3ker.c(303) : warning C4028: パラメー
タの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8kernel\3ker.c(309) : warning C4028: パラメー タの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8kernel\3ker.c(316) : warning C4028: パラメー
タの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8kernel\dosdep.c(888) : warning C4133: '関数' : 'int *' と 'char *' の間で型に互換性がありません。
        cl -c -W2  startup.c /Foobj\startup.obj
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

startup.c
        cl -c -W2  osfunc.c /Foobj\osfunc.obj
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

osfunc.c
        cl -c -W2  wincons0.c /Foobj\wincons0.obj
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

wincons0.c
        cl -c -W2  regquery_lib.c /Foobj\regquery_lib.obj
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

regquery_lib.c
        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\kernel.exe  obj\kernel.obj obj\startup.obj  obj\osfunc.obj obj\wincons0.obj  obj\regquery_lib.obj  WSOCK32.LIB advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        cl mindexec.c obj\osfunc.obj /Foobj\mindexec.obj  -W2  /link /OUT:obj\mindexec.exe  advapi32.lib
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

mindexec.c
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

/out:mindexec.exe
/OUT:obj\mindexec.exe
advapi32.lib
obj\mindexec.obj
obj\osfunc.obj 
        cl -c -W2  compker.c /Foobj\compker.obj
Microsoft(R) 32-bit C/C++ Optimizing Compiler Version 15.00.30729.01 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.

compker.c
c:\developments\vscode\mind8kernel\compword.c(2346) : warning C4047: '=' : 間接参照のレベルが 'char *' と 'ULONG' で異なっています。
c:\developments\vscode\mind8kernel\compword.c(2349) : warning C4047: '関 数' : 間接参照のレベルが 'char **' と 'char *' で異なっています。        
c:\developments\vscode\mind8kernel\compword.c(2349) : warning C4024: 'strtod' : の型が 2 の仮引数および実引数と異なります。
c:\developments\vscode\mind8kernel\dispword.c(273) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(357) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(365) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(376) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\dispword.c(384) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8kernel\3ker.c(303) : warning C4028: パラメー
タの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8kernel\3ker.c(309) : warning C4028: パラメー タの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8kernel\3ker.c(316) : warning C4028: パラメー
タの型 1 が関数宣言と一致しません。
        link /DEBUG:none /SUBSYSTEM:console /MACHINE:IX86 /OUT:obj\compker.exe  obj\compker.obj obj\startup.obj  obj\osfunc.obj  obj\regquery_lib.obj  advapi32.lib
Microsoft (R) Incremental Linker Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

けっこう警告はでていますが、すっからかんだったObjフォルダに下記のファイルができていますので、ビルドは成功したようです。
```
C:\developments\vscode\mind8kernel\obj>dir

 C:\developments\vscode\mind8kernel\obj のディレクトリ

2024/02/15  23:30    <DIR>          .
2024/02/15  22:50    <DIR>          ..
2024/02/15  23:30           181,760 compker.exe
2024/02/15  23:30           167,848 compker.obj
2024/02/15  23:30           291,840 kernel.exe
2024/02/15  23:30           239,452 kernel.obj
2024/02/15  23:30            74,752 mindexec.exe
2024/02/15  23:30             9,234 mindexec.obj
2024/02/15  23:30             1,785 osfunc.obj
2024/02/15  23:30               993 regquery_lib.obj
2024/02/15  23:30             1,166 startup.obj
2024/02/15  23:30               724 wincons0.obj
              10 個のファイル             969,554 バイト

```
# おわりに
とりあえずVSCodeエディタの環境からMind8のkernelがビルドできるようになったのでうれしいです。実はまだこの環境でデバッグ開始できるよう構成できていないのですが、近いうちにデバッグ実行できるようにして、Mind8コンパイラのインサイドな動きを勉強させていただきたいと妄想しております。
