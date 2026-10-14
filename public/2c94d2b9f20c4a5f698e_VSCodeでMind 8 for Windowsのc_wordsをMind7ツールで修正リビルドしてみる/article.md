# はじめに
VSCodeでMind 8 for WindowsのKernelを[デバッグ実行](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)して、dispatcherがC_Words_Addr[mcode]を介してC定義関数を実行する様子に迫りましたが、今回はC定義関数を試しに追加してみます。

タイトルにもありますが、Mind8は無償バージョンのためC定義関数のソースは公開されているのですが、予約されているダミー関数を実行可能に修正した後のMindワードテーブルを改修するツールは有償バージョンのMind7にしか添付されておりません。もしも本記事の内容をお試ししたい場合はMind7のライセンスが必要となりますのでご注意ください。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows

Mindはそれぞれのバージョンのパスが構成されていることを前提とします。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガは直接使わないのですが、Mind8のCカーネルアプリケーションをデバッグ実行でローンチするために流用しています。（今回は未使用）

# お題のソースコード
予約されているダミー関数が定義されているother.other_dummy_02( void )を下記のように修正します。decimal_add( void )	
Mind7のother.cはother.other_dummy_01から空いていましたが、Mind8のother.cはother.other_dummy_01が既にfamari( void )に置き換わっていましたので、02を使います。

```c:other.c
PRIVATE void
    decimal_add( void )	/* ;WORD テスト加える */
{
    	LONG  long1;
		LONG  long2;

        /* (long1, long2 → long1+long2) */

	long2 = POP_L_OF_Q;
	long1 = POP_L_OF_Q;

    long1 += long2;
    PUSH_Q(long1);

}

PRIVATE void
    other_dummy_03( void )	/* ;DUMMYWORD */
{
}
```

Mind7のother.cを使えば冒頭で述べたMindコンパイラバージョンのねじれはなくなるのですが、Mind7.5のリリースが2004年なのでVisual C++ 2008より手前になってしまうため、主にCコンパイラの環境を用意する手間を省くため従来記事の環境を引き続き使用させていただいております。


# Mind7ツールでc_words修正ビルド
Mind8には修正ツールが入っていないということを最初から認識していたわけではなく、やった順に書いていきますと、まず最初は素直にVSCodeのPowershellターミナルでnmake userwordsです。

いろいろいじり倒したMind8のmakefileですが、userwordsは残してあることを確認していました。
```
PS C:\developments\vscode\mind8\kernel> nmake userwords

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        echo "c2wordsかけますか?"
"c2wordsかけますか?"
        pause
続行するには何かキーを押してください . . . 
        c2words kernel.c c_words
'c2words' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
NMAKE : fatal error U1077: 'c2words' : リターン コード '0x1'
Stop.
PS C:\developments\vscode\mind8\kernel>
```

途中までは動いていますのでc2wordsのパスが足らないのかなと思い、Mind8の環境設定バッチを実行してみましたが、変わりませんでした。

※注意　以前の記事から読まれている方はご存じかと思いますが、恐らく稀かと。
Visual Studio 2008 command promptを開いて、mind8\kernelをカレントディレクトリとしてcode .でVSCodeを起動しています。Cコンパイラの環境設定はこの方法による一時的なものです。

```
PS C:\developments\vscode\mind8\kernel> c:\pmind\usemind
Mindの開発環境を設定しました。
PS C:\developments\vscode\mind8\kernel> nmake userwords 
略
```

この段階でMind8にはc2wordsが存在しないことを確認し、kernelやMindでセルフホストされたMindコンパイラの改修キット一式が完備したMind7の登場となります。

Mind7とMind8による混在ビルド環境の記事でも書きましたが、tasks.jsonにそれぞれのコンパイラの実パスを記述しているだけですので、ここでもVSCodeのPowershellターミナルでツールまでの実パスを指定して実行します。

```
PS C:\developments\vscode\mind8\kernel> c:\mind7\bin\c2words kernel.c c_words
c2words 処理中・・kernel.c kerbody.c osdefine.def serialno.def common.def osfunc.h kernel.def ptrdef.c jumpbufmax.h ptrmacro.def wincons0.h dispatch.c kerhot.c compword.c 0ker.c dispword.c kermain.c array.c bunki.c 1ker.c 1kerF.c 1kerFunc.c 2ker0.c 2ker1.c 2ker2.c 2ker22.c 2ker3.c 2ker4.c 2kerU.c 3ker.c 4ker.c mktime.c ms_c.c chmod.c dosdep.c proccomm.c regquery_lib.h regquery.c other.c runtno.c 終り
PS C:\developments\vscode\mind8\kernel>
```

無事に成功しました！:tada:

実は最初から成功していたわけではなく、MindコンパイラにMind単語として認識させる注釈部分の空白区切りが足らなくて下記のように怒られていました。:joy:

```
PS C:\developments\vscode\mind8\kernel> c:\mind7\bin\c2words kernel.c c_words 
c2words 処理中・・略
;WORD/;KWORDなどの右側に */ が有りません。
行内容＝"    decimal_add( void )        /* ;WORD テスト加える*/"
最後の関数名＝"famari"　最後の単語名＝"テスト加える*/"
```

これはわかりやすいエラーメッセージでしたので、すぐ直せました。

下記の３つのファイルが更新されました。
```
C:\developments\vscode\mind8\kernel>dir c_words.*
 C:\developments\vscode\mind8\kernel のディレクトリ

2024/03/03  10:42            27,185 c_words.def
2024/03/03  10:42            18,649 c_words.tbl
2024/03/03  10:42            33,178 c_words.wrd
               3 個のファイル              79,012 バイト
```

# Mind8ツールでfile修正ビルド
この後からはMindのシンボルファイルのリメイクとなるため、mmakeというMindで書かれたmakeツールを使いますが、それを所定の起動パラメータで起動するbatがMindインストールフォルダのfileフォルダにある場合があるので、どちらを使うか、そのまま使えるか、あるいは改修して使うかを検討するため、両者を比較してみました。


## Mind7
```:c:\mind7\file\cflle.bat
@mmake obj\file
```
## Mind8
```:c:\pmind\file\cflle.bat
@mmake obj\file mindF
@echo ..\lib に複写しますか？
@pause
@..\bin\mcpC -puv obj\file.mco obj\file.sym ..\lib
@rem ..\bin\mcpC -puv obj\file.mco obj\file.sym obj\file.his ..\lib
```

実はよくわかっていないのですが、Mind8はmcpCというMindで書かれたツールでさらになにかやっているようです。とりあえずMind8のOther.cから改修していますので、たぶんそこに書かれていたfamari( void )に対応する処理が書かれていると思われますで、こちらと同じ相対フォルダで本当のバージョンを上書きしないよう実行してみます。

つまりここからはMind8のツール（Mind8で書かれたバージョン）を使用します。
下記の開発環境のfileフォルダ（Mind8）に移動してcflle.batを実行します。
```
C:\developments\vscode\mind8>tree
C:.
├─bin
├─file
│  └─obj
└─kernel
    └─.vscode
```

VSCodeのターミナルをコマンドプロンプトに切り替えてfileフォルダに移動してMind8ツールのパス環境を設定しmmakeとmcpCが認識されるのを確認します。
```
C:\developments\vscode\mind8\kernel>cd ..
C:\developments\vscode\mind8>cd file
C:\developments\vscode\mind8\file>c:\pmind\usemind
Mindの開発環境を設定しました。
c:\pmind>cd C:\developments\vscode\mind8\file 
C:\developments\vscode\mind8\file>mind

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (オプション詳細を表示)
Usage(1): mind source library [objectdir\][objfile]

C:\developments\vscode\mind8\file>mmake
Usage: mmake [dir\]objectname [compiler]   (デフォルトのコンパイラ=mind)
 (objectnameには拡張子は付けません(.hisを参照します)

C:\developments\vscode\mind8\file>mcpC
Usage: mcp [-puvn] FILE [FILE..] DIRECTORY[\]|TARGETNAME [-xNOCPYNAME] [-xNOCPYNAME ..]
　 FILE..     複写元ファイル名(ワイルドカード指定可)
　 DIRECTORY  複写先ディレクトリ名(末尾パス記号有っても良い)
　 TARGETNAME 複写先ファイル名(-nオプションと共に使う)
　　　　-p　　タイムスタンプを継承(UNIXのみ,DOSではデフォルト)
        -u　　更新のあったファイルのみ処理
　　　　-v　　処理中ファイル名を表示する
　　　　-n　　複写先ファイル名(TARGETNAME)を指定
　　　　-x　　複写しないファイル名(NOCPYNAME)を指定(複数指定可)
```

cflle.batを実行します。
```
C:\developments\vscode\mind8\file>cfile
ライブラリ '..\libY\yoyakugoG' が有りません。
..\lib に複写しますか？
続行するには何かキーを押してください . . .
```
なんか警告がでています。あとあと問題になると紛らわしいので、libYも開発環境に確保してリトライします。コピー先のlibも確保しました。
```
C:\developments\vscode\mind8>tree
C:.
├─bin
├─file
│  └─obj
├─kernel
│  └─.vscode
├─lib
└─libY
```

ターミナルをコマンドプロンプトは強制終了しましたので前記Mindツールを認識させる手順もう一度行いcflle.batを実行します。すると今度は下記のようなエラーまたは警告が出ています。
```
:\developments\vscode\mind8\file>cfile
リンク先ライブラリ(..\libY\yoyakugoG.sym)が新しい。
mindコンパイラが見つかりません
mindコンパイラが見つかりません
mindコンパイラが見つかりません
..\lib に複写しますか？
続行するには何かキーを押してください . . .
```
..\lib に複写しますか？の前に出ているので、mmakeが出しているエラーと思われますが、mindコンパイラ自体は起動を確認できてきているのになぜ？的な感じ。

とりあえず、もうここは続行してみます。
```
続行するには何かキーを押してください . . .
obj\file.mco -> ..\lib
obj\file.sym -> ..\lib

C:\developments\vscode\mind8\file>
```
とりあえず完走したようですが、実際はfileのmcodeは更新されていないようです。

```
C:\developments\vscode\mind8\lib>dir file.*
 C:\developments\vscode\mind8\lib のディレクトリ

2023/01/22  16:36            43,504 file.mco
2023/01/22  16:36            30,376 file.sym
               2 個のファイル              73,880 バイト

C:\developments\vscode\mind8\file\obj>dir file.*
 C:\developments\vscode\mind8\file\obj のディレクトリ

2023/01/22  16:36             2,263 file.his
2023/01/22  16:36            43,504 file.mco
2023/01/22  16:36            30,376 file.sym
               3 個のファイル              76,143 バイト
```

う～む、残念。mmakeからMindコンパイラを起動できなかったのが効いているようです。

# つづく
fileライブラリのmcodeファイルの更新までは進行できませんでしたが、その手前のc_words.tblの更新まではうまくいったようです。時期をみて続きをリトライしてみます。
