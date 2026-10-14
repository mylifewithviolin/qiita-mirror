# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)で独自のソールファイル5kerD.cへの倍精度整数（64bit整数）の変数初期化処理を実装しましたので、今回はそのエラー処理です。もしも本記事の内容をお試ししたい場合は諸般の事情でMind7のライセンスが必要となりますのでご注意ください。
# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows

MindはMind8のバージョンのパスが構成されていることを前提とします。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガはMind8のCカーネルアプリケーションをデバッグ実行するために使用しています。

# お題のソースコード　C関数
## compword.c
スタックプッシュ関数push_quad2()が追加されています。[こちらの記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)を参照してください。

## other.c
other.cの内容をすべてダミー定義とします。正規のMind8ソースでは「ｆ余り」が定義されていますが、辞書の順序の関係からその単語は5kerD.cの冒頭に引越ししています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記しています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## 5kerD.c
独自に追加しているソースファイルです。「ｑ文字列初期化」を下記のように書き換えました。
```c:5kerD.c
/*;GLOBAL*/

//～略～

PRIVATE void
    qmojiretuShokika( void )	/* ;WORD ｑ文字列初期化 .S */
{
		ULONG	count;
		UCHAR  *addr;
    	word64  long1;
		int	flg;	
		char *endptr;
				
        /* (string → long1) */

	count = POP_C;
	addr  = POP_A;

	flg = 0;
	_set_errno(0);

	long1=_strtoi64(addr,&endptr,10);//_strtoi64 Microsoft 固有

	flg = errno;
	_set_errno(0);
	if( *endptr != '\0' ){
		flg = 1;
	}
	if(flg!=0){
		PUSH_S( addr, count );
		zzHot10();			/* 重大エラー処理に飛ぶ */
	}

    push_quad2(long1);
}

//～略～

/* end of '5kerD.c' */
```

### ソースコード全文
「ｑ文字列初期化」以外は変更ありませんので、[前回記事](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)をご参照ください。

## Mind7ツールでc_words修正ビルド
[前回記事](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)をご参照ください。

## Mind8ツールでfile修正ビルド
fileライブラリを修正ビルドする前に、下記のエラー定義ファイルにエラー処理を追記します。　HOT9とHOT4の間にHOT10の本定義を追加します。

```mind:cerror.src
※～略～
　　条件コンパイル　ＷｉｎｄｏｗｓＧＵＩ環境・非ＳＩＬＥＮＴ。
$$HOT9とは　　　　　　　本定義　　　　　（Tcl/Tk文法エラー）
	静かに重大エラー。
　　条件コンパイル終り。

$$HOT10とは　　　　　　　本定義　　　　　（倍精度変数初期化エラー）
			＿バッファは　文字列実体　長さ　５１２桁
	「倍精度変数を初期化できませんでした。初期化文字列（」を　＿バッファに　入れ
	＿バッファに　追加し
	「）」を　＿バッファに　追加し
	＿バッファで　重大エラー。

$$HOT4は　　　　　　　　本定義　　　　　（INDEX OVERFLOW）
※～略～
```

ここからはMind8のツール、コンパイラを使用します。
### シリアル番号チェッカーツール
Mind開発者の@killyさんからMind8ランタイムのシリアル番号チェッカーツールをご提供いただいています。（[この記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)参照）
今回は開発環境内での変更のため前回のカウントアップ値を保持しますので、ランタイムのシリアル番号チェッカツールは実行しません。
### fileライブラリをリビルド
fileライブラリをリビルドして開発環境のlibフォルダにコピーします。
```
C:\developments\vscode\mind8\kernel>cd ../file  
C:\developments\vscode\mind8\file>mmake obj\file mind
C:\developments\vscode\mind8\file>mcpC -puv obj\file.mco obj\file.sym ..\lib
obj\file.mco -> ..\lib
obj\file.sym -> ..\lib
```
### nmake all
nmake allをターミナルのタスクから実行します。
```
 *  実行するタスク: nmake all 
```
ここで追加した関数のC言語的に問題がある場合はエラーで終了することがありますので注意します。
### nmake install
nmake allが成功した場合はnmake installも実行しておきます。
```
 *  実行するタスク: nmake install 
```
### kernel.exeをmrunt010.exeにリネームしてbinフォルダコピー
開発環境のbinフォルダにkernel.exeをリネームしたmrunt010.exeに手動でコピーしておきます。
```
C:\developments\vscode\mind8>copy bin\kernel.exe bin\mrunt010.exe 
        1 個のファイルをコピーしました。
```

# お題のソースコード　Mind
今回はint64_2の方に符号付き64bit整数の最大値を超える数字を与えてみます。正常に実行されている部分も確認するため、int64の方には従来値を設定しておきます。

```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"9223372036854775808"を　　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	。
```

正規のMind8のfileライブラリではなく、今回リビルドしたfileライブラリを指定してコンパイルします。またMindコンパイラも正規のバージョンではなく、開発環境のbinパスのmindを実行します。
```
PS C:\developments\vscode\mind8> bin\mind sample\quaderr lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\developments\vscode\mind8\bin\mindex.exe --> sample\quaderr.exe
```

## 実行結果
正規のバージョンのMind8のランタイムとはシリアルNoが異なっていますので、開発環境のランタイムで動作するようbinフォルダに移動してから、ビルドされたquaderr.exeを実行します。
```
C:\developments\vscode\mind8>cd bin

C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
倍精度変数を初期化できませんでした。初期化文字列（9223372036854775808）
```
無事にエラーメッセージが表示されました！:tada::tada:

# おわりに
なんども記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、属性定義の件はオイオイ検証していくとして、次回はいよいよ倍精度変数を固定小数点型（小数部４桁固定の簡易通貨型のようなもの）に初期化する関数を対応してみます？
