# はじめに
トランスコンパイル言語を作りたいが、コンパイラさえ作ったことないので、とりあえず有名自作Cコンパイラ四則演算版の書き換えで試しに日本語コンパイラ言語Mindのソースを出力してみた。その結果の検証環境をつくっています。
ちなみにUbuntu上ではダウンロードした状態のバイナリのMindコンパイラは動きま~~せんで~~した。2023/01/28訂正

## この記事内容の作業目的
[トランスコンパイラの作り方 Ｃ言語を日本語プログラミング言語Mindにトランスコンパイルしてみる（四則演算版）](https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c)で出力させたMindのソースコードをコンパイル検証したい、その検証環境を構築したい。
## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu 22.04.1 LTS）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
gcc 9,10,11,12
Mind 8 for Linux　mind-for-linux-8.0.08.tgz
## この記事内容の保証
※この記事には環境構築の手順的な情報が含まれます。本記事に書かれた手順の妥当性は保証されません。~~（というか、まだmakeできてません。）~~　2023/01/28訂正
# 基本情報
[Mindオペレーションマニュアル（インストール方法など）](http://www.scripts-lab.co.jp/mind/ver8/doc/operation-1b-Install-linux.html#binary_in_package)より引用
``Mindカーネルのmake方法（もし必要なら）``
>[gcc関連のパッケージ確認１]
>64bitOSの場合、glibc.i386～glibc.i686 のいずれかが（glibc.x86_64 ではなく）
>インストール済みであるか確認し、無ければインストールしてください（これが無いと、ヘッダファイル不足で、make時に stubs.h が無いなどのエラーが出ます）。
>$ yum list installed glibc         ←インストール済みであるか確認

>[gcc関連のパッケージ確認２]
>64bitOSの場合、libgcc.i386～libgcc.i686 のいずれかが（libgcc.x86_64 ではなく）インストール済みであるか確認し、無ければインストールしてください。
>$ yum list installed libgcc        ←インストール済みであるか確認

ここはつまり、恐らく「.x86_64 ではなく」がポイントで、32bitっぽいライブラリを入れてくれというように解釈。

とりえず現状の環境をチェック
# 環境をチェック
Ubuntuのバージョンです。念のため。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
```
$ cat /etc/os-release
PRETTY_NAME="Ubuntu 22.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.1 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
```
glibcは32bit版らしきものを確認できませんでした。下図は例です。
```
$ sudo apt search glibc
Sorting... Done
Full Text Search... Done
glibc-source/jammy-updates,now 2.35-0ubuntu3.1 all [installed]
  GNU C Library: sources
```
libgccは32bit版らしきものを確認できました。下図は例です。
```
$ sudo apt search libgcc
Sorting... Done
Full Text Search... Done
lib32gcc-11-dev/jammy-updates,jammy-security,now 11.3.0-1ubuntu1~22.04 amd64 [installed,automatic]
  GCC support library (32 bit development files)
```
gccは9,10,11,12をインストールしてあります。下記のコマンドで数字を入力して切り替えます。
```
$ sudo update-alternatives --config gcc
There are 4 choices for the alternative gcc (providing /usr/bin/gcc).

  Selection    Path             Priority   Status
------------------------------------------------------------
  0            /usr/bin/gcc-12   120       auto mode
  1            /usr/bin/gcc-10   100       manual mode
* 2            /usr/bin/gcc-11   60        manual mode
  3            /usr/bin/gcc-12   120       manual mode
  4            /usr/bin/gcc-9    90        manual mode

Press <enter> to keep the current choice[*], or type selection number: 

```

## 参考 32bit版glibcのインストールで試みたこと

こちらの記事を参考にしました。やりたいことはまさしくこれ。
[How to install 32 bit glibc on 64 bit ubuntu](
https://stackoverflow.com/questions/23970684/how-to-install-32-bit-glibc-on-64-bit-ubuntu#:~:text=This%20command%20will%20install%20the%2032bit%20glibc%20libraries,file%20should%20not%20appear%20on%20GCC%27s%20command%20line.)

既に入れてある状態からのインストール再実行結果です。
```
$ sudo apt install gcc-multilib
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
gcc-multilib is already the newest version (4:11.2.0-1ubuntu1).
0 upgraded, 0 newly installed, 0 to remove and 29 not upgraded.
```
参考記事のベストアンサーのコマンドの実行結果。
```
$ gcc -m32 objectfile.o -o executablefile
/usr/bin/ld: cannot find objectfile.o: No such file or directory
collect2: error: ld returned 1 exit status
```
他に、Ubuntuのバージョンが低いですが、こちらの記事とか。
[Ubuntu 14.04 64bit で 32bit アプリを動作させる方法](https://agekuno.hatenablog.com/entry/2014/10/22/190712)

```
$ sudo dpkg --add-architecture i386
$ sudo apt install libc6:i386 libncurses5:i386 libstdc++6:i386
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
E: Unable to locate package libc6:i386
E: Unable to locate package libncurses5:i386
E: Unable to locate package libstdc++6:i386
```


# make実行

```
$ make clean
rm -f mindexec
rm -f kernel
rm -f compker
rm -f cgiker
rm -f mindexeccgi
rm -f *.o

$ make all
```


gcc9,10,11,12いずれでも大量の警告が出力され、下図は最後の終わったところの内容です。上からgcc11、gcc10,9,12です。
```:gcc11
In file included from /usr/include/features.h:486,
                 from /usr/include/bits/libc-header-start.h:33,
                 from /usr/include/stdio.h:27,
                 from osfunc.c:55:
/usr/include/bits/string_fortified.h:92:1: note: expected ‘const char * __restrict__’ but argument is of type ‘UCHAR *’ {aka ‘unsigned char *’}
   92 | __NTH (strncpy (char *__restrict __dest, const char *__restrict __src,
      | ^~~~~
osfunc.c:281:15: warning: pointer targets in assignment from ‘char *’ to ‘UCHAR *’ {aka ‘unsigned char *’} differ in signedness [-Wpointer-sign]
  281 |         token = strtok( (char *)envBuffer, " ,:");  /* NULL   ֤    Ȥ⤢   */
      |               ^
osfunc.c: In function ‘sysReadFixedSize’:
osfunc.c:187:20: warning: ‘resultBytes’ may be used uninitialized [-Wmaybe-uninitialized]
  187 |                 if ( resultBytes != requestBytes )
      |                    ^
osfunc.c:178:27: note: ‘resultBytes’ was declared here
  178 |                 size_t    resultBytes;
      |                           ^~~~~~~~~~~
gcc -m32 -DLINUX -D_GNU_SOURCE   -Wall -O6 -funsigned-char -ansi \
        kernel.o \
        startup.o osfunc.o \
        -o kernel -lm -ldl
```

```:gcc10
In file included from /usr/include/features.h:486,
                 from /usr/include/bits/libc-header-start.h:33,
                 from /usr/include/stdio.h:27,
                 from osfunc.c:55:
/usr/include/bits/string_fortified.h:92:1: note: expected ‘const char * __restrict__’ but argument is of type ‘UCHAR *’ {aka ‘unsigned char *’}
   92 | __NTH (strncpy (char *__restrict __dest, const char *__restrict __src,
      | ^~~~~
osfunc.c:281:15: warning: pointer targets in assignment from ‘char *’ to ‘UCHAR *’ {aka ‘unsigned char *’} differ in signedness [-Wpointer-sign]
  281 |         token = strtok( (char *)envBuffer, " ,:");  /* NULL   ֤    Ȥ⤢   */
      |               ^
osfunc.c: In function ‘sysReadFixedSize’:
osfunc.c:187:20: warning: ‘resultBytes’ may be used uninitialized in this function [-Wmaybe-uninitialized]
  187 |                 if ( resultBytes != requestBytes )
      |                    ^
gcc -m32 -DLINUX -D_GNU_SOURCE   -Wall -O6 -funsigned-char -ansi \
        kernel.o \
        startup.o osfunc.o \
        -o kernel -lm -ldl
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/10/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/10/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
collect2: error: ld returned 1 exit status
make: *** [makefile:212: kernel] Error 1
```
```:gcc9
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/9/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/9/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
collect2: error: ld returned 1 exit status
make: *** [makefile:212: kernel] Error 1
```
```:gcc12
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/12/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
/usr/bin/ld: skipping incompatible /usr/lib/gcc/x86_64-linux-gnu/12/libgcc.a when searching for -lgcc
/usr/bin/ld: cannot find -lgcc: No such file or directory
collect2: error: ld returned 1 exit status
make: *** [makefile:212: kernel] Error 1
```
x86_64-linux-gnu/9(10)/libgcc.aと互換性がないのでスキップしたとか、gccが見つからないと言っているようです。
gcc9,10,12はエラーとなっていますが、gcc11は警告だけなのでいけたかと思ったので
gcc11でmake installまで実行してみました。
```
$ make install
'kernel' -> '../bin/mrunt010'
'mindexec' -> '../bin/mindex'
'mindexec' -> '../bin/cmpstamp'
'mindexec' -> '../bin/euc2sjis'
'mindexec' -> '../bin/getCGIruntime'
'mindexec' -> '../bin/mcp'
'mindexec' -> '../bin/mgrep'
'mindexec' -> '../bin/mhist'
'mindexec' -> '../bin/mind'
'mindexec' -> '../bin/mindC'
'mindexec' -> '../bin/mmake'
'mindexec' -> '../bin/showargs'
'mindexec' -> '../bin/shownewpath'
'mindexec' -> '../bin/sjis2euc'
'mindexec' -> '../bin/stamp'
'compker' -> '../bin/mrunt060'
'cgiker' -> '../bin/mrunt160'
'mindexeccgi' -> '../bin/mindexcgi'
```
いちおうできてるっぽい。
```
$ cd ../bin
$ ls -l
total 1540
-rwxr-xr-x 1 puremind puremind  16676 Jan 28 00:37 mind
-rwxr-xr-x 1 puremind puremind 147294 Nov 30  2018 mind.mco
-rwxr-xr-x 1 puremind puremind  16676 Jan 28 00:37 mindC
-rwxr-xr-x 1 puremind puremind 118724 Jun 22  2016 mindC.mco
-rwxr-xr-x 1 puremind puremind  16676 Jan 28 00:37 mindex
-rwxr-xr-x 1 puremind puremind  16688 Jan 28 00:37 mindexcgi
```
# mind実行

mindコンパイラを実行してみます。
```
~/pmind/bin$ mind
Command 'mind' not found, did you mean:
  command 'mina' from deb mina (0.3.7-1.1)
  command 'minc' from deb mblaze (1.1-1)
  command 'find' from deb findutils (4.8.0-1ubuntu3)
Try: sudo apt install <deb name>
```
動きませんでした。(涙)
```
~/pmind/bin$ ./mind
���ܸ�ץ�����ߥ󥰸��� �ͣ��� Version 8.07 for UNIX
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (���ץ����ܺ٤�ɽ��)
Usage(1): mind source library [objectdir/][objfile]
```
動きました。(涙) 2023/01/28訂正
起動の仕方が間違っていただけでgcc11の下記32bit互換ライブラリの元ではコンパイラ初期エコーの出力までは確認できました。

## 原因考察

現状では/usr/lib/gcc配下にはx86_64版しか構成されておらず、
```
/usr/lib/gcc$ ls -l
total 4
drwxr-xr-x 6 root root 4096 Jan 27 22:41 x86_64-linux-gnu
```
gcc11用だけにはx86_64の32bit互換ライブラリみたいなのが構成されているので
```
/usr/lib/gcc$ tree -d
.
└── x86_64-linux-gnu
    ├── 10
    │   ├── include
    │   │   └── sanitizer
    │   └── plugin
    ├── 11
    │   ├── 32
    │   ├── include
    │   │   └── sanitizer
    │   ├── plugin
    │   └── x32
    ├── 12
    │   ├── include
    │   │   └── sanitizer
    │   └── plugin
    └── 9
        ├── include
        │   └── sanitizer
        └── plugin
```
gcc11でmakeすると、コンパイル(make)は警告のみで完走するが、実行時は~~互換性ないため動かない模様~~いまのところ初動することを確認。2023/1/28訂正
このあと、Mind開発元のスクリプツ・ラボさま（以下敬称略）よりご支援いただいた内容を確認してまいります。


# スクリプツ・ラボ推奨手順（2023/1/28追記）
再度ダウンロードしたアーカイブを解凍してMindコンパイラバイナリの状態で初期化します。
```
$ tar xzpf mind-for-linux-8.0.08.tgz
$ cd pmind/bin
~/pmind/bin$ ls -l
total 1360
-rwxr-xr-x 1 puremind puremind  12862 Dec  2  2018 mind
-rwxr-xr-x 1 puremind puremind 147294 Nov 30  2018 mind.mco
-rwxr-xr-x 1 puremind puremind  12862 Dec  2  2018 mindC
-rwxr-xr-x 1 puremind puremind 118724 Jun 22  2016 mindC.mco
-rwxr-xr-x 1 puremind puremind  12862 Dec  2  2018 mindex
```
この状態で実行確認します。
```
~/pmind/bin$ ./mind
���ܸ�ץ�����ߥ󥰸��� �ͣ��� Version 8.07 for UNIX
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (���ץ����ܺ٤�ɽ��)
Usage(1): mind source library [objectdir/][objfile]
```
動きました！ということはmake不要かも？
```
~/pmind/bin$ echo $LANG
ja_JP.EUC-jp
```
文字コードはEUC-jpになっているはずですが、文字化けしてます。

## make kicker実行

```
~/pmind/bin$ cd ../kernel
~/pmind/kernel$ make kicker
make: *** No rule to make target 'kicker'.  Stop.
```
あれ？動きませんでした。usageを見ると該当オプションないようでした。
```
~/pmind/kernel$ make

Usage:
    make all                     �����ͥ룳��򤹤٤ƥ���ѥ���
    make install-all             �����ͥ룳��򤹤٤ƥ��󥹥ȡ���
    make compilerkernel          Mind�ġ����ѥ����ͥ�Υ���ѥ���
    make userkernel              �桼���ѥ����ͥ�Υ���ѥ���
    make cgikernel               CGI�ѥ����ͥ�Υ���ѥ���
    make install-compilerkernel  Mind�ġ����ѥ����ͥ�򥤥󥹥ȡ���
    make install-userkernel      �桼���ѥ����ͥ�򥤥󥹥ȡ���
    make install-cgikernel       CGI�ѥ����ͥ�򥤥󥹥ȡ���
```
makeのソースには kicker のワードが若干出現します。
```shell:makefile
clean-kicker:
	$(RM) $(KICKEXECUTABLE)

install-compilerkernel:
	@cp -puv $(COMPEXECUTABLE) ../bin/$(COMPILERMRUNTINSTALL)
	@cp -puv $(KICKEXECUTABLE) ../bin/$(KICKERINSTALL)
```
## /kernel配下のmindexec実行
makeはやりなおせていませんが、とりあえずアーカイブバイナリの状態で
これが動けば大丈夫とのことのmindexecを実行してみます。
```
~/pmind/kernel$ ./mindexec
M-code file() not exist
```
動いているみたいです！
とりあえず本記事の課題としてはmakeすることでしたが、本来の目的はコンパイラが動く環境の構築ですので、次の段階へ進みます。
makeすること自体も参考情報として追加更新します。

# 次の段階
下記の記事にて、無事にコンパイルして、生成コードを実行することができました。
[VSCode [WSL:Ubuntu] で日本語プログラミング言語Mindのソースをビルドしてみた](https://qiita.com/mylifewithviolin/items/366d1e3b0fea9485acdb)

VSCodeの文字コードをeucJPにしUbuntuの文字コードもeucJPに変更しましたが、VSCodeの統合bashターミナルの設定がわからず、VSCodeが出力する日本語は正常ですがMindコンパイラのエコーの日本語が化けているという謎状態です

# 参考リンク
https://qiita.com/killy/items/ccec1fbb81c4432757f5

https://qiita.com/killy/items/8987fe06f675300b852b

https://qiita.com/killy/items/ee7740693161a42140dc

[Ubuntu Manpage: libc - Linux の標準 C ライブラリの概要](https://manpages.ubuntu.com/manpages/jammy/ja/man7/libc.7.html)

[How to install 32 bit glibc on 64 bit ubuntu](
https://stackoverflow.com/questions/23970684/how-to-install-32-bit-glibc-on-64-bit-ubuntu#:~:text=This%20command%20will%20install%20the%2032bit%20glibc%20libraries,file%20should%20not%20appear%20on%20GCC%27s%20command%20line.)

[Ubuntu 14.04 64bit で 32bit アプリを動作させる方法](https://agekuno.hatenablog.com/entry/2014/10/22/190712)

https://qiita.com/mylifewithviolin/items/366d1e3b0fea9485acdb
