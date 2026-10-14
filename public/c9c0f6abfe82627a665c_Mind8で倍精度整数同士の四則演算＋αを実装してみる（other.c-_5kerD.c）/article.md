# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんからMind8に倍精度整数があると伺ったのを契機に、諸般の都合でMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)でother.cへの倍精度整数（64bit整数）の変数同士の四則演算と論理演算の一部（等しいと大きい）を実装してみましたので、今回はother.cで不足した単語一式を別ソースファイルで実装します。もしも本記事の内容をお試ししたい場合は諸般の事情でMind7のライセンスが必要となりますのでご注意ください。

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
スタックプッシュ関数push_quad2()が追加されています。[前回記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)を参照してください。

## other.c
other.cの直前に新しいソースファイルをインクルードするように追加しますので、other.cの内容をすべてダミー定義とします。正規のMind8ソースではｆ余りが定義されていますが、辞書の順序の関係からその単語は新規ソースファイルの冒頭にお引越しします。
```c:other.c
/*;GLOBAL*/

PRIVATE void
    other_dummy_01( void )	/* ;DUMMYWORD */
{
}
PRIVATE void
    other_dummy_02( void )	/* ;DUMMYWORD */
{
}
//～略～

PRIVATE void
    other_dummy_08( void )	/* ;DUMMYWORD */
{
}
/* end of 'other.c' */
```
## 5kerD.c
まことにややなんちゃってながら5kerD.cというソースコードファイルを追加します。浮動小数点演算用ソースの1kerF.cをかなり参考にさせていただいています。まだ[属性の扱い](https://qiita.com/killy/items/db2f1a935e6b00d23366)はよくわかっていないので、とりあえずこちら側だけの定義となっています。
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
    	_zero_divide_error( long1 , long2,  1 );
	}
    long1 =  long1 /  long2;
    push_quad2(long1);

}
//～略～

PRIVATE void
    qamari( void )		/* ;WORD ｑ余り ※属性はGENSYMにて */
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
    qtiisai( void )		/* ;WORD ｑ小さい ※属性はGENSYMにて */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1<long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 < long2), 0 );
}

PRIVATE void
    qijyou( void )		/* ;WORD ｑ以上 ※属性はGENSYMにて */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1>=long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	PUSH_Q( (long1 >= long2), 0 );
}

PRIVATE void
    qika( void )		/* ;WORD ｑ以下 ※属性はGENSYMにて */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1<=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 <= long2), 0 );
}

PRIVATE void
    qkotonaru( void )		/* ;WORD ｑ異なる ※属性はGENSYMにて */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1!=long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	PUSH_Q( (long1 != long2), 0 );
}

PRIVATE void
    qamari( void )		/* ;WORD ｑ余り ※属性はGENSYMにて */
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

32bit整数演算のソースの1ker.cも参考に実装させていただいております。0除算例外の処理のような例を発見しましたので、とりあえず書いてあります。スタックのサイズが合致しないかもしれませんので、別途_zero_divide_error64のような関数を実装した方がよいかもしれませんが、今回は32bit版の流用にとどまっています。

また余りもCの演算子の挙動のままなので、Mindの仕様に適合しているかは未確認です。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記します。
```c:kerbody.c
//～略～
/* ----------- includes other(2) ----------- */

  #if COMILERsKERNEL	/* ------ 以下はコンパイラ向けカーネル------- */
//～略～
  #else			/* -------- 以下は通常カーネル向け ---------- */
//～略～  
#include "5kerD.c"	  /* 倍精度変数　通貨変数の操作 */
#include "other.c"		/* アセンブラ定義語領域の予備 */

  #endif		/* ------------------------------------------ */
//～略～
```

## Mind7ツールでc_words修正ビルド
Mind8には単語定義修正ツールが入っていないので、Mind7のライセンスがあることを前提にMind7のbinフォルダからMind8のbinフォルダへツールをコピーしておきます。（前々回記事参照）

前回からtasks.jsonに設定してありますので、今回もVSCodeターミナルのタスクで実行しました。
```
 *  実行するタスク: c2words 'kernel.c c_words' 

c2words 処理中・・kernel.c kerbody.c osdefine.def serialno.def common.def osfunc.h kernel.def ptrdef.c jumpbufmax.h ptrmacro.def wincons0.h dispatch.c kerhot.c compword.c 0ker.c dispword.c kermain.c array.c bunki.c 1ker.c 1kerF.c 1kerFunc.c 2ker0.c 2ker1.c 2ker2.c 2ker22.c 2ker3.c 2ker4.c 2kerU.c 3ker.c 4ker.c mktime.c ms_c.c chmod.c dosdep.c proccomm.c regquery_lib.h regquery.c 5kerD.c other.c runtno.c 終り
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
ちょっと横スクロールで流れていてわかりずらいですが、今回のコンソール出力では　regquery.c 5kerD.c other.c runtno.c 終り　のようにother.cの直前に5kerD.cが出力されているのがポイントです。

## Mind8ツールでfile修正ビルド
ここからはMind8のツール、コンパイラを使用します。
Mind開発者の@killyさんからMind8ランタイムのシリアル番号チェッカーツールをご提供いただいたので、前回記事でそれをインストールしてあります。
ランタイムのシリアル番号チェッカツールを実行し、シリアル番号をカウントアップしておきます。（[前回記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)参照）

fileライブラリをリビルドして開発環境のlibフォルダにコピーします。（前回記事参照）

続いてtasks.jsonに設定してあるnmake allをターミナルのタスクから実行します。（前回記事参照）

警告が出ていますが実行には問題なさそうなので無視しています。
nmake installも実行しておきます。（前回記事参照）

開発環境のbinフォルダはパスを設定しておらず、正規のMind8にパスが通っていますが、前回正規の環境にkernel.exeをリネームしたmrunt010.exeに手動でコピーしましたが、今回は開発環境へのコピーとしておきます。
```
C:\developments\vscode\mind8>copy bin\kernel.exe bin\mrunt010.exe 
        1 個のファイルをコピーしました。
```

# お題のソースコード　Mind
[前回記事](https://qiita.com/mylifewithviolin/items/dc2272541ff438c6a63e)で追加した単語を使うソースを今回も流用します。今回追加した単語の実行は別途ということで、とりあえず前回版を下記のようにビルドします。

```mind:quad.src
//～略～　前回記事参照
```
正規のMind8のfileライブラリではなく、今回リビルドしたfileライブラリを指定してコンパイルします。またMindコンパイラも正規のバージョンではなく、開発環境のbinパスのを実行します。
```
PS C:\developments\vscode\mind8> bin\mind sample\quad lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\developments\vscode\mind8\bin\mindex.exe --> sample\quad.exe
```

## 実行結果
正規のバージョンのMind8のランタイムとはシリアルNoが異なっていますので、開発環境のランタイムで動作するようbinフォルダに移動してから、ビルドされたquad.exeを実行します。

```
PS C:\developments\vscode\mind8> cd bin
PS C:\developments\vscode\mind8\bin> ..\sample\quad
FFFFFFFE|00009FFF 175921860444158
00000002|00000000 2

00000000|0000A000 175921860444160
FFFFFFFC|00009FFF 175921860444156
FFFFFFFC|00013FFF 351843720888316
FFFFFFFF|00004FFF 87960930222079
00000000|00000000
00000001|00000000

FFFFFFFE|00009FFF 175921860444158
pop qvalした
qval(16進表記)=00009ffffffffffe
push qvalして再度戻す
pop qvalした
qval(16進表記)=00009ffffffffffe
push qvalして再度戻す
FFFFFFFE|00009FFF

00000002|00000000 2
pop qvalした
qval(16進表記)=0000000000000002
push qvalして再度戻す
pop qvalした
qval(16進表記)=0000000000000002
push qvalして再度戻す
00000002|00000000
PS C:\developments\vscode\mind8\bin>
```
正常動作したようです。:tada:今回は前回記事のデバッグ実行と同じ結果であればミニマムサクセスです。追加された単語の検証は次回以降行います。

# Mind7ツールc2wordsが更新したファイル
Mind7ツールc2wordsが更新したファイルを確認しました。追加した単語のmcodeが対応していることが確認できます。
```:c_words.wrd
～略～
c_get_registry_valueは　アセンブラ定義の処理単語。
グローバル。
ｆ余りは　アセンブラ定義の処理単語　実数入力 実数出力。
c_test_push_quad2は　アセンブラ定義の処理単語。
ｑ加えは　アセンブラ定義の処理単語。
ｑ引くは　アセンブラ定義の処理単語。
ｑ掛けは　アセンブラ定義の処理単語。
ｑ割るは　アセンブラ定義の処理単語。
ｑ等しいは　アセンブラ定義の処理単語。
ｑ大きいは　アセンブラ定義の処理単語。
グローバル。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
アセンブラ定義のダミー。
$$mrunt010は　アセンブラ定義の処理単語。
```

```:c_words.def
～略～
PRIVATE void c_get_registry_value( void );
PRIVATE void famari( void );
PRIVATE void c_test_push_quad2( void );
PRIVATE void qkuwae( void );
PRIVATE void qhiku( void );
PRIVATE void qkake( void );
PRIVATE void qwaru( void );
PRIVATE void qhitosii( void );
PRIVATE void qookii( void );
PRIVATE void other_dummy_01( void );
PRIVATE void other_dummy_02( void );
PRIVATE void other_dummy_03( void );
PRIVATE void other_dummy_04( void );
PRIVATE void other_dummy_05( void );
PRIVATE void other_dummy_06( void );
PRIVATE void other_dummy_07( void );
PRIVATE void other_dummy_08( void );
PRIVATE int mrunt_no( void );
```
```:c_words.tbl
～略～
/*02EE*/ c_get_registry_value,
/*02EF*/ famari,
/*02F0*/ c_test_push_quad2,
/*02F1*/ qkuwae,
/*02F2*/ qhiku,
/*02F3*/ qkake,
/*02F4*/ qwaru,
/*02F5*/ qhitosii,
/*02F6*/ qookii,
/*02F7*/ other_dummy_01,
/*02F8*/ other_dummy_02,
/*02F9*/ other_dummy_03,
/*02FA*/ other_dummy_04,
/*02FB*/ other_dummy_05,
/*02FC*/ other_dummy_06,
/*02FD*/ other_dummy_07,
/*02FE*/ other_dummy_08,
```

famariのMCodeは02EFが維持されてMind8コンパチブルであることが確認できます。今回はこのあたりの検証が目標でした。

細かいお話では、実は5kerD.cのMind単語定義のコメント部で「※属性はGENSYMにて」と書いた単語は追加されていないようです。このあたりも次回以降検証という扱いとさせていただきます。

# おわりに
前回の記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、まだ[属性定義の記述](https://qiita.com/mylifewithviolin/items/58853c548798b309a601)はよくわかっていないので、少し倍精度変数の試作実装で足踏みするかもしれません。次回はそのあたりということで。


## 2024/03/24 訂正
「※属性はGENSYMにて」の記述を削除して c2wordsでc_words修正ビルドをして、「※属性はGENSYMにて」の記述有だった単語のmcodeが追加された後、再度「※属性はGENSYMにて」の記述を追加して c2wordsでc_words修正ビルドをしても、「※属性はGENSYMにて」の記述有単語のmcodeが維持されるのを確認しました。「※属性はGENSYMにて」の記述はc2wordsの単語テーブル生成処理には無関与でした。たいへんお騒がせしました。
