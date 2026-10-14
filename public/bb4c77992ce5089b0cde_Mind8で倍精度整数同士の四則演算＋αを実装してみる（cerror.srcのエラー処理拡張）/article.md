# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/8b87403646c2831fdaba)で倍精度整数（64bit整数）の変数初期化処理のエラー処理を実装しましたので、今回は過日実装していた四則演算処理にもエラー処理を追加してみます。もしも本記事の内容をお試ししたい場合は諸般の事情でMind7のライセンスが必要となりますのでご注意ください。

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
独自に追加しているソースファイルです。Mind側で使用する処理単語の他に、それらの単語が呼び出すエラー処理関数も追加します。c2word用のコメントは記述しないので、辞書の順序は変わらない想定です。
```c:5kerD.c
/*;GLOBAL*/
//～略～
PRIVATE void
    _qover_flow_error(
		word64   long1,	
        word64	 long2
                      )
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 2,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

PRIVATE void
    _qzero_divide_error(
		word64  dividend,		/* 引数1:非除数   */
        word64	divider        /* 引数2:除数     */
                      )
{
	push_quad2( dividend );
	push_quad2( divider );
	PUSH_Q( 0,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

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
		PUSH_Q( 1,  0 );	//エラー種別
		zzHot10();			/* 重大エラー処理に飛ぶ */
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

	_set_errno(0);
    long1 += long2;

	if(errno!=0){
		_set_errno(0);
    	_qover_flow_error( long1 , long2 );
	}
	_set_errno(0);
    push_quad2(long1);

}
//～略～
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
    	_qzero_divide_error( long1 , long2 );
	}
    long1 =  long1 /  long2;
    push_quad2(long1);

}
//～略～
/* end of '5kerD.c' */
```

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
    _qover_flow_error(
		word64   long1,	
        word64	 long2
                      )
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 2,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

PRIVATE void
    _qzero_divide_error(
		word64  dividend,		/* 引数1:非除数   */
        word64	divider        /* 引数2:除数     */
                      )
{
	push_quad2( dividend );
	push_quad2( divider );
	PUSH_Q( 0,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

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
		PUSH_Q( 1,  0 );	//エラー種別
		zzHot10();			/* 重大エラー処理に飛ぶ */
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

	_set_errno(0);
    long1 += long2;

	if(errno!=0){
		_set_errno(0);
    	_qover_flow_error( long1 , long2 );
	}
	_set_errno(0);
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

	_set_errno(0);
    long1 -= long2;
	if(errno!=0){
		_set_errno(0);
    	_qover_flow_error( long1 , long2 );
	}
	_set_errno(0);

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
	_set_errno(0);

    long1 =  long1 * long2;
	if(errno!=0){
		_set_errno(0);
    	_qover_flow_error( long1 , long2 );
	}
	_set_errno(0);

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
    	_qzero_divide_error( long1 , long2 );
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
    	_qzero_divide_error( long1 , long2 );
	}
    long1 =  long1%long2;
    push_quad2(long1);
}
/* end of '5kerD.c' */
```
</details>

四則演算にはオーバーフローのエラーチェックを追加（したつもりな）ので、若干処理にオーバーヘッドがかかったと思われます。

## Mind7ツールでc_words修正ビルド
[こちらの記事](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)をご参照ください。

## Mind8ツールでfile修正ビルド
前回の記事で追加したエラー処理HOT10の本定義を拡張します。

```mind:cerror.src
※～略～
$$HOT10とは　　　　　　　本定義　　　　　（倍精度変数関連エラー）
			＿バッファは　文字列実体　長さ　５１２桁
			エラー種別は　ワード変数
	エラー種別に　入れ
	エラー種別が　０に　等しい
	ならば
		「ゼロで除算しました。」を　＿バッファに　入れ
	さもなければ
		エラー種別が　１に　等しい
		ならば
			「倍精度変数を初期化できませんでした。初期化文字列（」を　＿バッファに　入れ
			＿バッファに　追加し
			「）」を　＿バッファに　追加し
		さもなければ
			エラー種別が　２に　等しい
			ならば
				「オーバーフローしました。」を　＿バッファに　入れ
			さもなければ
				「実行の継続が困難なエラーが発生しました。」を　＿バッファに　入れ	
			つぎに	
		つぎに
	つぎに
	＿バッファで　重大エラー。
※～略～
```
エラー種別は5kerD.c内でHot10を呼び出す直前にスタック積んでいるPUSH_Q( 2,  0 );の値です。左記の場合は2。

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
ちなみにcerror.srcに追記した記述内容に問題がある場合、コンパイルエラー情報はconsole.infに出力されます。

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
# お題のソースコードMindと実行結果
## お題のソースコード（１）　
初期化エラーとなる想定です。
```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"0abc"を　　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り ＄＄クアド表示し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```
今回リビルドしたfileライブラリを指定してコンパイルします。
[こちらの記事](https://qiita.com/mylifewithviolin/items/8b87403646c2831fdaba)をご参照ください。

## 実行結果（１）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
倍精度変数を初期化できませんでした。初期化文字列（0abc）
```
前回記事と同等の初期化エラーが出力されました。:tada:

## お題のソースコード（２）
0で除算エラーとなる想定です。
```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"0"を　　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り ＄＄クアド表示し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```

## 実行結果（２）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
int64_2 (ｑ文字列初期化)   00000000|00000000 0
int64とint64_2を　ｑ割り   ゼロで除算しました。
```
0で除算エラーとなりました。:tada::tada:


## お題のソースコード（３）
オーバーフローエラーとなる想定です。
```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"175921860444158"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"175921860444158"を　　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り ＄＄クアド表示し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```

## 実行結果（３）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
int64_2 (ｑ文字列初期化)   FFFFFFFE|00009FFF 175921860444158
int64とint64_2を　ｑ割り   00000001|00000000 1
int64にint64_2を　ｑ掛け   00000004|FFFD8000 -703687441776636
```
あああっれ！？オーバーフローせず負数側にいってしまいました？

# おわりに
なんども記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、まだまだ足踏みはつづく？
