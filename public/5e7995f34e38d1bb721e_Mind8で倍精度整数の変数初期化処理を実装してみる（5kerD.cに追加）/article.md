# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)で独自のソールファイル5kerD.cへの倍精度整数（64bit整数）の変数同士の四則演算と論理演算を実装してみましたので、今回は倍精度整数の変数初期化処理を実装します。もしも本記事の内容をお試ししたい場合は諸般の事情でMind7のライセンスが必要となりますのでご注意ください。

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
スタックプッシュ関数push_quad2()が追加されています。[前々回記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)を参照してください。

## other.c
other.cの内容をすべてダミー定義とします。正規のMind8ソースでは「ｆ余り」が定義されていますが、辞書の順序の関係からその単語は5kerD.cの冒頭に引越ししています。[前回記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記しています。前回記事を参照してください。


## 5kerD.c
独自に追加しているソースファイルです。今回はc_test_push_quad2と「ｑ加え」の間に「ｑ文字列初期化」という単語を追加しました。これが本記事お題の倍精度整数の変数初期化処理です。前回以前に追加されている単語の属性定義はまだ追記していませんが、「ｑ文字列初期化」には「.S」を記述してみています。前回本体記事のソース全文の追加単語で「※属性はGENSYMにて」とあった点は削除されています。
```c:5kerD.c
/*;GLOBAL*/

//～略～

PRIVATE void
    qmojiretuShokika( void )	/* ;WORD ｑ文字列初期化 .S */
{
		ULONG	count;
		UCHAR  *addr;
    	word64  long1;
		USHORT	flg;	
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
		PUSH_Q( addr, count );
		zzHot9();			/* 重大エラー処理に飛ぶ */
	}

    push_quad2(long1);
}

//～略～

/* end of '5kerD.c' */
```
「ｑ文字列初期化」ではいちおう数値変換できなかった場合のエラー処理を記述していますが、未検証です。またVC++の_strtoi64が符号付64ビット整数の最大値、最小値を超える数字文字列を変換しようとしたときにerrnoにエラーコードをセットするのかとかも未検証です。オイオイ検証してまいります。（下記の参考情報ではオーバーフローの場合は最大値定数、最小値定数を返すとありますが、errnoにエラーコードをセットするという明示は発見できませんでした。）

https://learn.microsoft.com/ja-jp/cpp/c-runtime-library/reference/strtoi64-wcstoi64-strtoi64-l-wcstoi64-l?view=msvc-170

<details><summary>ソースコード全文</summary>

```c:5kerD.c
/*;GLOBAL*/

PRIVATE void
    famari( void )		/* ;WORD ｆ余り 実数入力 実数出力 */
{
		double	float1;
		double	float2;

        /* (float1, float2 → float) */

	float2 = pop_float();
	float1 = pop_float();

	float1 = fmod( float1, float2 );

	push_float( float1 );
}

PRIVATE void
    c_test_push_quad2( void )		/* ;WORD c_test_push_quad2 */
{
		word64	qval;

        /* (quad → quad) */

	qval = pop_quad();

	printf("pop qvalした\n");
	printf("qval(16進表記)=%016llx\n", qval);
	printf("push qvalして再度戻す\n");

	push_quad2( qval );
}

PRIVATE void
    qmojiretuShokika( void )	/* ;WORD ｑ文字列初期化 .S */
{
		ULONG	count;
		UCHAR  *addr;
    	word64  long1;
		USHORT	flg;	
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
		PUSH_Q( addr, count );
		zzHot9();			/* 重大エラー処理に飛ぶ */
	}

    push_quad2(long1);
}

PRIVATE void
    qkuwae( void )	/* ;WORD ｑ加え */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1+long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    long1 += long2;
    push_quad2(long1);

}


PRIVATE void
    qhiku( void )	/* ;WORD ｑ引く */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1-long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    long1 -= long2;
    push_quad2(long1);

}

PRIVATE void
    qkake( void )	/* ;WORD ｑ掛け */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1*long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    long1 =  long1 * long2;
    push_quad2(long1);

}

PRIVATE void
    qwaru( void )	/* ;WORD ｑ割る */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1/long2) */

	long2 = pop_quad();
	long1 = pop_quad();
	if ( long2 == 0 )
	{
    	_zero_divide_error( long1 , long2,  1 );
	}
    long1 =  long1 /  long2;
    push_quad2(long1);

}
/* --------- 以下は32bit整数値返しなので注意のこと --------- */
/*							*/
PRIVATE void
    qhitosii( void )	/* ;WORD ｑ等しい */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1==long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    PUSH_Q( (long1 == long2), 0 );

}

PRIVATE void
    qookii( void )	/* ;WORD ｑ大きい */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1>long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    PUSH_Q( (long1 > long2), 0 );


}
PRIVATE void
    qtiisai( void )		/* ;WORD ｑ小さい  */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1<long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 < long2), 0 );
}

PRIVATE void
    qijyou( void )		/* ;WORD ｑ以上  */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1>=long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 >= long2), 0 );
}

PRIVATE void
    qika( void )		/* ;WORD ｑ以下  */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1<=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 <= long2), 0 );
}

PRIVATE void
    qkotonaru( void )		/* ;WORD ｑ異なる  */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1!=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 != long2), 0 );
}

PRIVATE void
    qamari( void )		/* ;WORD ｑ余り  */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1%long2) */

	long2 = pop_quad();
	long1 = pop_quad();
	if ( long2 == 0 )
	{
    	_zero_divide_error( long1 , long2,  2 );
	}
    long1 =  long1%long2;
    push_quad2(long1);
}
/* end of '5kerD.c' */
```
</details>

## Mind7ツールでc_words修正ビルド
Mind8には単語定義修正ツールが入っていないので、Mind7のライセンスがあることを前提にMind7のbinフォルダからMind8のbinフォルダへツールをコピーしておきます。（[「加える」初実装記事参照](https://qiita.com/mylifewithviolin/items/cedbd2b2d11eca988540)）

VSCodeターミナルのタスクでtasks.jsonに設定してある下記のタスクを実行します。結果出力は割愛。前回記事を参照してください。
```
 *  実行するタスク: c2words 'kernel.c c_words' 
```


## Mind8ツールでfile修正ビルド
ここからはMind8のツール、コンパイラを使用します。
### シリアル番号チェッカーツール
Mind開発者の@killyさんからMind8ランタイムのシリアル番号チェッカーツールをご提供いただいています。（[前々回記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)参照）
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
今回は実行結果を少し見やすくするため、クアッド表示の直前になにを処理したかを文字列表示しておくことにしました。そのため、ソースコードは少しごちゃごちゃしました。
```mind:quad.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"2"を　　ｑ文字列初期化し　int64_2に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し

    改行し
	"int64にint64_2を　ｑ加え   "を　表示し
	int64に　int64_2を ｑ加え ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ加え ＄＄倍精度表示し　改行し 
	"int64からint64_2をｑ引き   "を　表示し
	int64から　int64_2を ｑ引き ＄＄クアド表示し　" "を　表示し 
    int64から　int64_2を ｑ引き ＄＄倍精度表示し　改行し 
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り ＄＄クアド表示し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64とint64_2の　ｑ余り   "を　表示し
	int64と int64_2の ｑ余り ＄＄クアド表示し　" "を　表示し 	
	int64と int64_2の ｑ余り ＄＄倍精度表示し 　改行し 	
	改行し
	"int64とint64_2が　ｑ等しい "を　表示し
	int64と　int64_2が ｑ等しい ＄＄クアド表示し　　改行し
	"int64がint64_2よりｑ大きい "を　表示し
	int64が int64_2より ｑ大きい ＄＄クアド表示し 　改行し 
	"int64がint64_2よりｑ小さい "を　表示し
	int64が int64_2より ｑ小さい ＄＄クアド表示し 　改行し 
	"int64がint64_2　　ｑ以上   "を　表示し
	int64が int64_2より ｑ以上 ＄＄クアド表示し 　改行し 
	"int64がint64_2　　ｑ以下   "を　表示し
	int64が int64_2より ｑ以下 ＄＄クアド表示し 　改行し 
	"int64がint64_2と　ｑ異なる "を　表示
	int64が int64_2と ｑ異なる ＄＄クアド表示し 　改行し 
	改行し		
	。
```

今回のソースは前回追加した単語の実行も追加されていますが、今回のポイントはお題の初期化単語です。
```mind:quad.src
メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"2"を　　ｑ文字列初期化し　int64_2に　入れ
```
前回記事では割愛していましたが、最初にサンプルから倍精度変数の初期化処理を発見した状態のままでした。
```mind:quad.src
メインとは
	0fffffffeHと　000009FFFHを　無処理し　文字列情報合成し　int64に　入れ
	000000002Hと　000000000Hを　無処理し　文字列情報合成し　int64_2に　入れ
```
正規のMind8のfileライブラリではなく、今回リビルドしたfileライブラリを指定してコンパイルします。またMindコンパイラも正規のバージョンではなく、開発環境のbinパスのmindを実行します。
```
PS C:\developments\vscode\mind8> bin\mind sample\quad lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\developments\vscode\mind8\bin\mindex.exe --> sample\quad.exe
```

ここでC環境でデバッグ実行できるようにコンパイルされたmcodeファイルをmindexec.mcoにリネームしてkernelフォルダにコピーしておきます。
```
C:\developments\vscode\mind8>copy sample\quad.mco kernel\mindexec.mco 
kernel\mindexec.mco を上書きしますか? (Yes/No/All): Y
        1 個のファイルをコピーしました。
```

## デバッグ実行結果
kernelをビルド・デバッグ実行する環境でデバッグ実行開始します。

![vscodec35.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d30d6f29-f9a4-1c72-d502-32b5513b5ed4.png)

厳密にはエラー処理に課題が残っていますが、正常系は動作しました。
zzHot9はkerhot.cに下記のように定義されてままです。
```mind:kerhot.c
PRIVATE void                    /* $$HOT9 */
    zzHot9( void )
{                               /* 空き */
        executeHotWord( 9 );
}
```
mindランタイムのエラー処理はまだよくわかっておらず、スタックを元に戻して上記の関数群を呼び出すような慣習と認識していますが、まだ検証していません。

## 実行結果
正規のバージョンのMind8のランタイムとはシリアルNoが異なっていますので、開発環境のランタイムで動作するようbinフォルダに移動してから、ビルドされたquad.exeを実行します。

```
PS C:\developments\vscode\mind8> cd bin
PS C:\developments\vscode\mind8\bin> ..\sample\quad
int64   (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
int64_2 (ｑ文字列初期化)   00000002|00000000 2

int64にint64_2を　ｑ加え   00000000|0000A000 175921860444160
int64からint64_2をｑ引き   FFFFFFFC|00009FFF 175921860444156
int64にint64_2を　ｑ掛け   FFFFFFFC|00013FFF 351843720888316
int64とint64_2を　ｑ割り   FFFFFFFF|00004FFF 87960930222079
int64とint64_2の　ｑ余り   00000000|00000000 0

int64とint64_2が　ｑ等しい 00000000|00000000
int64がint64_2よりｑ大きい 00000001|00000000
int64がint64_2よりｑ小さい 00000000|00000000
int64がint64_2　　ｑ以上   00000001|00000000
int64がint64_2　　ｑ以下   00000000|00000000
int64がint64_2と　ｑ異なる 00000001|00000000
```

# おわりに
前々回の記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、とりあえず属性定義の件はオイオイ検証していくとして、今回は倍精度変数の初期化単語が実装できましたので、倍精度変数を固定小数点型（小数部４桁固定の簡易通貨型のようなもの）に初期化する関数を次回対応してみます。

# 2024/03/24 訂正
投稿した後に記事を読み直しているときに、ソースコードでC/C++一般のグローバル変数のerrnoの型がなんだったか気になりだしたので確認してみますと、intっぽいようです。当初flgとerrnoは別建てで扱っていたのですが途中でいっしょに扱うようにしたので、USHORTで宣言したflgの方の長さが足らないようです。次回記事でいっしょに修正しておきます。
