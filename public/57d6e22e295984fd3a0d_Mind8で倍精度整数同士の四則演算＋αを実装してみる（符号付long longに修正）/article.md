# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/bb4c77992ce5089b0cde)で倍精度整数（64bit整数）の四則演算処理にエラー処理を追加してみましたところ符号付64bit整数の最大値を超えてもオーバーフローが起きないことから、符号なしlong longで実装していたせいっぽいと推察。今回はスタック操作と演算を符号付long longに修正してみました。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows

MindはMind8のバージョンのパスが構成されていることを前提とします。もしも本記事の内容をお試ししたい場合は辞書修正ツールでMind7のライセンスが必要となりますのでご注意ください。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガはMind8のCカーネルアプリケーションをデバッグ実行するために使用しています。

# お題のソースコード　C関数
## compword.c
従来スタックプッシュ関数push_quad2()が追加されていましたが、今回の符号付long longへの修正に伴い独自ソースファイル5kerD.cに移設しました。今回記事よりcompword.cは正規版のままとなります。

## other.c
other.cの内容をすべてダミー定義とします。正規のMind8ソースでは「ｆ余り」が定義されていますが、辞書の順序の関係からその単語は5kerD.cの冒頭に引越ししています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記しています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## 5kerD.c
独自に追加しているソースファイルです。前回記事よりMind側で使用する処理単語の他に、それらの単語が呼び出すエラー処理関数も追加しており、c2word用のコメントは記述しなければ辞書の順序は変わらないことをつかんだので、こちらに独自関数や定義を集中します。

```c:5kerD.c
/*;GLOBAL*/
//～略～
typedef  __int64       LONG64;

PRIVATE void
    push_quad2( LONG64 qval )
{
        /* ([引数] → quad) */

		ULONG	hi32;
		ULONG	lo32;

	hi32 = qval >> 32;
	lo32 = qval & 0xffffffff;
	PUSH_Q( lo32, hi32 );
}

PRIVATE void
    c_test_push_quad2( void )		/* ;WORD c_test_push_quad2 */
{
		LONG64	qval;

        /* (quad → quad) */

	qval = pop_quad();

	printf("pop qvalした\n");
	printf("qval(16進表記)=%016llx\n", qval);
	printf("push qvalして再度戻す\n");

	push_quad2( qval );
}

PRIVATE void
    zzQuadHyouji2( void )		/* ;WORD クアド表示2 */
{
		LONG64	qval;
		
        /* (quad → .) */

	qval = pop_quad();
	printf("%016llx", qval);

}

PRIVATE void
    _qover_flow_error(
		LONG64   long1,	
        LONG64	 long2
                      )
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 2,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

PRIVATE void
    _qzero_divide_error(
		LONG64  dividend,		/* 引数1:非除数   */
        LONG64	divider        /* 引数2:除数     */
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
    	LONG64  long1;
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
	//if( *endptr != '\0' ){
	//	flg = 1;
	//}
	if(flg!=0){
		PUSH_S( addr, count );
		PUSH_Q( 1,  0 );	//エラー種別
		zzHot10();			/* 重大エラー処理に飛ぶ */
	}

    push_quad2(long1);
}
//～略～
/* end of '5kerD.c' */
```
符号付き64bit整数型のエイリアスをLONG64としました。この型名で定義済みの変数をすべて置換しました。

compword.cに定義していたpush_quad2をこちらに引っ越しました。32bitスタックにそれぞれプッシュする際の変数は符号なしを維持しました。

通常の１６進表示のクアド表示2を追加しました。これにより辞書の順序は変化しますが、リリースしているわけではないので開発時はいろいろ変動ありとします。

文字列初期化で、endptrを評価したエラー判定をやめました。マイナス符号付きの場合、NULL終端が返らないようでした。数値変換自体は成功していました。VCのバージョンやオプションが影響しているのかもしれません。

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

typedef  __int64       LONG64;

PRIVATE void
    push_quad2( LONG64 qval )
{
        /* ([引数] → quad) */

		ULONG	hi32;
		ULONG	lo32;

	hi32 = qval >> 32;
	lo32 = qval & 0xffffffff;
	PUSH_Q( lo32, hi32 );
}

PRIVATE void
    c_test_push_quad2( void )		/* ;WORD c_test_push_quad2 */
{
		LONG64	qval;

        /* (quad → quad) */

	qval = pop_quad();

	printf("pop qvalした\n");
	printf("qval(16進表記)=%016llx\n", qval);
	printf("push qvalして再度戻す\n");

	push_quad2( qval );
}

PRIVATE void
    zzQuadHyouji2( void )		/* ;WORD クアド表示2 */
{
		LONG64	qval;
		
        /* (quad → .) */

	qval = pop_quad();
	printf("%016llx", qval);

}

PRIVATE void
    _qover_flow_error(
		LONG64   long1,	
        LONG64	 long2
                      )
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 2,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

PRIVATE void
    _qzero_divide_error(
		LONG64  dividend,		/* 引数1:非除数   */
        LONG64	divider        /* 引数2:除数     */
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
    	LONG64  long1;
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
	//if( *endptr != '\0' ){
	//	flg = 1;
	//}
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
    	LONG64  long1;
		LONG64  long2;
	
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
    	LONG64  long1;
		LONG64  long2;

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
    	LONG64  long1;
		LONG64  long2;

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
    	LONG64  long1;
		LONG64  long2;

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
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1==long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    PUSH_Q( (long1 == long2), 0 );

}

PRIVATE void
    qookii( void )	/* ;WORD ｑ大きい */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1>long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    PUSH_Q( (long1 > long2), 0 );


}
PRIVATE void
    qtiisai( void )		/* ;WORD ｑ小さい  */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1<long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 < long2), 0 );
}

PRIVATE void
    qijyou( void )		/* ;WORD ｑ以上  */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1>=long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 >= long2), 0 );
}

PRIVATE void
    qika( void )		/* ;WORD ｑ以下  */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1<=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 <= long2), 0 );
}

PRIVATE void
    qkotonaru( void )		/* ;WORD ｑ異なる  */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1!=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 != long2), 0 );
}

PRIVATE void
    qamari( void )		/* ;WORD ｑ余り  */
{
    	LONG64  long1;
		LONG64  long2;

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

## Mind7ツールでc_words修正ビルド
[こちらの記事](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)をご参照ください。

## Mind8ツールでfile修正ビルド
### cerror.src
[前回記事](https://qiita.com/mylifewithviolin/items/bb4c77992ce5089b0cde)をご参照ください。

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
これ重要です。バージョンチェッカーツールでシリアルNoをあげていれば、コピー忘れは実行時に検知されます。あげていない場合でこのコピーを忘れた場合は古いバージョンの動作となります。

# お題のソースコードMindと実行結果
今回リビルドしたfileライブラリを指定してコンパイルします。
[こちらの記事](https://qiita.com/mylifewithviolin/items/8b87403646c2831fdaba)をご参照ください。
## お題のソースコード（１）
符号付き64bit整数の最大値と最小値で初期化して、それぞれの変数で割り算と掛け算を実行してみます。
```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"-9223372036854775808"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け クアド表示2し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```
## 実行結果（１）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   7fffffffffffffff 9223372036854775807
int64_2 (ｑ文字列初期化)   8000000000000000 -9223372036854775808
int64とint64_2を　ｑ割り   0000000000000000 0
int64にint64_2を　ｑ掛け   8000000000000000 -9223372036854775808
```
初期化は正常に行われました。これよりそれぞれ1大きい、-1小さい場合は初期化失敗するのを確認しました。掛け算はオーバーフローは起きずに掛けた方の値を維持しました。割り算、掛け算ともにプログラマー電卓と結果は同じです。オーバーフローが起きている動作としてはあっていそう。

## お題のソースコード（２）
マイナス値の絶対値をプラス側の最大値にしました。

```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"-29223372036854775807"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け クアド表示2し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```

## 実行結果（２）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   7fffffffffffffff 9223372036854775807
int64_2 (ｑ文字列初期化)   8000000000000001 -9223372036854775807
int64とint64_2を　ｑ割り   ffffffffffffffff -1
int64にint64_2を　ｑ掛け   ffffffffffffffff -1
```
割り算は正常値を返しました。掛け算はプログラマー電卓と結果は同じです。オーバーフローが起きている動作としてはあっていそう。

## お題のソースコード（３）
最大値に対して2で割り算掛け算してみます。

```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"2"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ割り   "を　表示し
	int64と　int64_2を ｑ割り クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ掛け   "を　表示し
	int64に　int64_2を ｑ掛け クアド表示2し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示し　改行し 
	。
```

## 実行結果（３）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   7fffffffffffffff 9223372036854775807
int64_2 (ｑ文字列初期化)   0000000000000002 2
int64とint64_2を　ｑ割り   3fffffffffffffff 4611686018427387903
int64にint64_2を　ｑ掛け   fffffffffffffffe -2。
```
割り算は正常値っぽいです。掛け算はプログラマー電卓と結果は同じでした。オーバーフローした状態としてはあっているっぽい。

# おわりに
掛け算や加減算がオーバーフローしないのは符号なし整数であったことの他、そもそもここで「オーバーフローしない」という表現は_strtoi64のようにerrnoに0以外の値をセットすることを期待していましたが、そのような動作はしないということのようです。しかし、計算の結果としてはオーバーフローした状態ですので、このあたりのチェックをどうするかは今後の課題のようですね。
なんども記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、まだまだ足踏みはつづく？課題は課題として残しつつ少し本題の実装イメージを具体化してみたい願望は強まっています。

## 2024/03/28 参考情報追記
https://www.jpcert.or.jp/sc-rules/c-int32-c.html
