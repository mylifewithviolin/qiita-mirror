# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

[前回](https://qiita.com/mylifewithviolin/items/57d6e22e295984fd3a0d)で倍精度整数（64bit整数）の四則演算処理のスタック操作と演算を符号付long longに修正してみました。C言語の符号付整数の四則演算オーバーフローは未定義動作であることを再確認。今回は四則演算オーバーフローチェックを実装してみます。

# 参考情報
四則演算オーバーフローチェックの実装にあたっては下記の情報を参考にさせていただいております。

https://www.jpcert.or.jp/sc-rules/c-int32-c.html

https://hiroyukichishiro.com/arithmetic-overflow-in-c-language/

https://teratail.com/questions/95465

当初JPCERTの事前条件のみのチェックを実装してみましたが、加算と減算はサンプル条件でオーバーフロー検出しましたが、乗算は検出できませんでした。

つづいて、hiroyukichishiro.comの事前、事後条件を実装してみましたが、加算と減算はサンプル条件でオーバーフロー検出しましたが，乗算は検出しませんでした。こちらに記載の乗算事後条件の実装は参考記事の記述内容どおりかは保証されません。
>符号ありの場合は，以下のようにチェックします．
p の上位32ビットがすべて 0 あるいはすべて 1 の場合は正常
それ以外はオーバーフロー

この「p」は乗算結果の「c」の誤記と解釈していますが、その場合の文意の64bit整数の場合の妥当性は確認できませんでした。

乗算は最終的にteratail.comにあった乗算結果を乗数の片方で除算して復元するかどうかで検出というロジックで実装してみたところ、サンプル条件でオーバーフロー検出しました。

除算はhiroyukichishiro.comには符号付での記述はないため、JPCERTの事前条件を保持しています。これはオーバーフロー発生条件が限定的で、マイナス側最小値を-1で割るとマイナス側最小値の絶対値がプラス側最大値より1大きいことからのチェックとなり、JPCERTの事前条件は妥当と判定しております。

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
## other.c
other.cの内容をすべてダミー定義とします。正規のMind8ソースでは「ｆ余り」が定義されていますが、辞書の順序の関係からその単語は5kerD.cの冒頭に引越ししています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記しています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## 5kerD.c
独自に追加しているソースファイルです。[こちらの記事](https://qiita.com/mylifewithviolin/items/bb4c77992ce5089b0cde)よりMind側で使用する処理単語の他に、それらの単語が呼び出すエラー処理関数も追加しており、c2word用のコメントは記述しなければ辞書の順序は変わらないことをつかんだので、こちらに独自関数や定義を集中します。

```c:5kerD.c
//～略～
typedef  __int64       LONG64;

#define LONG64_MAX +9223372036854775807
#define LONG64_MIN -9223372036854775808

PRIVATE void push_quad2( LONG64 qval )
{
        /* ([引数] → quad) */

		ULONG	hi32;
		ULONG	lo32;

	hi32 = qval >> 32;
	lo32 = qval & 0xffffffff;
	PUSH_Q( lo32, hi32 );
}

/* エラー種別オーバーフローで重大エラー処理に飛ぶ */
PRIVATE void _qover_flow_error(LONG64 long1,LONG64 long2)
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 2,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}
/* エラー種別ゼロ除算で重大エラー処理に飛ぶ */
PRIVATE void _qzero_divide_error(LONG64 long1,LONG64 long2)
{
	push_quad2( long1 );
	push_quad2( long2 );
	PUSH_Q( 0,  0 );	//エラー種別
	zzHot10();			/* 重大エラー処理に飛ぶ */
}

/* 加算オーバーフロー事前チェック JPCERT/CC INT32-C.*/
PRIVATE void _check_over_flow_add(LONG64 long1, LONG64 long2)
{
  	if (((long2 > 0) && (long1 > (LONG64_MAX - long2))) ||
      ((long2 < 0) && (long1 < (LONG64_MIN - long2)))) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */ 
	}
}
/* 減算オーバーフロー事前チェック JPCERT/CC INT32-C.*/
PRIVATE void _check_over_flow_sub(LONG64 long1, LONG64 long2)
{
  	if ((long2 > 0 && long1 < LONG64_MIN + long2) ||
      (long2 < 0 && long1 > LONG64_MAX + long2)) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */
	}
}
/* 乗算オーバーフロー事前チェック JPCERT/CC INT32-C.*/
PRIVATE void _check_over_flow_multiply(LONG64 long1, LONG64 long2)
{
	if (long1 > 0) {  /* long1 は正 */
		if (long2 > 0) {  /* long1 と long2 は正 */
			if (long1 > (LONG64_MAX / long2)) {
				_qover_flow_error( long1 , long2 ); /* エラー処理 */
			}
		} else { /* long1 は正、 long2 はゼロ以下 */
			if (long2 < (LONG64_MIN / long1)) {
				_qover_flow_error( long1 , long2 );/* エラー処理 */
			}
		} /* long1 は正、long2 はゼロ以下 */
	} else { /* long1 はゼロ以下 */
		if (long2 > 0) { /* long1 is nonpositive, long2 is positive */
			if (long1 < (LONG64_MIN / long2)) {
				_qover_flow_error( long1 , long2 );/* エラー処理 */
			}
		} else { /* long1 と long2 はゼロ以下 */
			if ( (long1 != 0) && (long2 < (LONG64_MAX / long1))) {
				_qover_flow_error( long1 , long2 );/* エラー処理 */
			}
		}
	}
}
/* 除算オーバーフロー事前チェック JPCERT/CC INT32-C.（ゼロ除算チェック含む） */
PRIVATE void _check_over_flow_divid(LONG64 long1, LONG64 long2)
{
	if (long2 == 0) {
    	_qzero_divide_error( long1 , long2 );/* エラー処理 */
	}else if(long1 == LONG64_MIN && long2 == -1){
			_qover_flow_error( long1 , long2 );/* エラー処理 */
	}
}

/* 加算オーバーフロー事前チェック hiroyukichishiro.com/ */
PRIVATE void _check_over_flow_before_add(LONG64 long1, LONG64 long2)
{
  	if (
		((long1 >= 0 && long2 >= 0) && ((LONG64_MAX - long1) < long2 )) ||
      	((long1 < 0 && long2 < 0) && (long1 < (LONG64_MIN - long2)))
	  ) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */ 
	}
}
/* 加算オーバーフロー事後チェック hiroyukichishiro.com/ */
PRIVATE void _check_over_flow_after_add(LONG64 long1, LONG64 long2, LONG64 long3)
{
  	if (
		((long1 >= 0) && (long3 < long2 )) ||
      	((long1 < 0) && (long3 > long2))
		) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */ 
	}
}
/* 減算オーバーフロー事前チェック hiroyukichishiro.com/ */
PRIVATE void _check_over_flow_before_sub(LONG64 long1, LONG64 long2)
{
  	if (
		((long1 > 0 && 0 > long2) && long1 > (LONG64_MAX + long2)) ||
        ((long2 > 0 && 0 > long1) && long1 < (LONG64_MIN + long2)) ||
		(long1 == 0  && long2 == LONG64_MIN) 
		)  {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */
	}
}

/* 減算オーバーフロー事後チェック hiroyukichishiro.com/ */
PRIVATE void _check_over_flow_after_sub(LONG64 long1, LONG64 long2, LONG64 long3)
{
  	if (
		((long2 >= 0) && (long3 > long1 )) ||
      	((long2 < 0) && (long3 < long1))
		) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */ 
	}
}
/* 乗算オーバーフロー事前チェック hiroyukichishiro.com/*/
PRIVATE void _check_over_flow_before_multi(LONG64 long1, LONG64 long2)
{
  	if (
		((long1 > 0 && long2 > 0) && ((LONG64_MAX / long2) < long1 )) ||
      	((long1 > 0 && long2 <= 0) && ((LONG64_MIN / long1 >long2)))  ||
		((long1 <= 0 && long2 > 0) && ((LONG64_MIN / long2) > long1 )) ||
      	((long1 <= 0 && long2 <= 0) && (long1!=0 && (LONG64_MAX / long1 > long2)))
	  ) {
    	_qover_flow_error( long1 , long2 );/* エラー処理 */ 
	}
}
/* 乗算オーバーフロー事後チェック teratail.com/questions/95465/ */
PRIVATE void _check_over_flow_after_multi(LONG64 long1, LONG64 long2, LONG64 long3)
{
  	if(long1==0 || long2==0) {
		//long1,long2いずれか0はオーバーフローしない
	}else{
		if(long1!=0){//0でない方の乗数で結果を除して被乗数と等しくない場合はオーバーフロー
			if(long2 !=(long3 / long1)) _qover_flow_error( long1 , long2 );/* エラー処理 */ 
		}
		if(long2!=0){
			if(long1 !=(long3 / long2)) _qover_flow_error( long1 , long2 );/* エラー処理 */
		}
	}
}

//～略～

PRIVATE void
    qkuwae( void )	/* ;WORD ｑ加え */
{
    	LONG64  long1;
		LONG64  long2;
		LONG64  long3;
        /* (long1, long2 → long1+long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	_check_over_flow_before_add(long1, long2);/* 加算オーバーフロー事前チェック*/
	long3 = long1 + long2;
	_check_over_flow_after_add(long1, long2, long3);/* 加算オーバーフロー事後チェック*/

    push_quad2(long3);

}


PRIVATE void
    qhiku( void )	/* ;WORD ｑ引く */
{
    	LONG64  long1;
		LONG64  long2;
		LONG64  long3;

        /* (long1, long2 → long1-long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	_check_over_flow_before_sub(long1,long2);/* 減算オーバーフロー事前チェック */
	long3 = long1 - long2;
	_check_over_flow_after_sub(long1, long2, long3);/* 減算オーバーフロー事後チェック*/

    push_quad2(long3);

}

PRIVATE void
    qkake( void )	/* ;WORD ｑ掛け */
{
    	LONG64  long1;
		LONG64  long2;
		LONG64  long3;

        /* (long1, long2 → long1*long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	//_check_over_flow_before_multi(long1,long2);/* 乗算オーバーフロー事前チェック */
    long3 =  long1 * long2;
	_check_over_flow_after_multi(long1, long2, long3);/* 乗算オーバーフロー事後チェック*/

    push_quad2(long3);

}

PRIVATE void
    qwaru( void )	/* ;WORD ｑ割る */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1/long2) */

	long2 = pop_quad();
	long1 = pop_quad();


	_check_over_flow_divid(long1,long2);/* 除算オーバーフロー事前チェック（ゼロ除算チェック含む） */

    long1 =  long1 /  long2;
    push_quad2(long1);

}
//～略～

PRIVATE void
    qamari( void )		/* ;WORD ｑ余り  */
{
    	LONG64  long1;
		LONG64  long2;

        /* (long1, long2 → long1%long2) */

	long2 = pop_quad();
	long1 = pop_quad();

	_check_over_flow_divid(long1,long2);/* 除算オーバーフロー事前チェック（ゼロ除算チェック含む） */

    long1 =  long1%long2;
    push_quad2(long1);
}
/* end of '5kerD.c' */

```
足し算と引き算には参考情報hiroyukichishiro.comの事前、事後条件チェックを実装しています。事前チェック関数の定義としてはJPCERTの事前条件も残してあります。
乗算は参考情報teratail.comの事後条件チェックのみを実装しています。事前チェック関数の定義としてはJPCERTとhiroyukichishiro.comの事前条件も残してあります。
除算と余りは参考情報JPCERTの事前条件チェックのみを実装しています。

### ソースコード全文
四則演算と余り以外は前回と同じです。[前回記事](https://qiita.com/mylifewithviolin/items/57d6e22e295984fd3a0d)をご参照ください。


## Mind7ツールでc_words修正ビルド
[こちらの記事](https://qiita.com/mylifewithviolin/items/5e7995f34e38d1bb721e)をご参照ください。

## Mind8ツールでfile修正ビルド
### cerror.src
これはMind側のfileライブラリの依存ライブラリのconsoleソースコードです。C側のエラー処理関数から呼ばれる単語になります。[こちらの記事](https://qiita.com/mylifewithviolin/items/bb4c77992ce5089b0cde)をご参照ください。

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
cerror.srcに追記した記述内容に問題がある場合、コンパイルエラー情報はconsole.infに出力されます。

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
符号付き64bit整数の最大値と最小値+1で初期化して、それぞれの変数で割り算と掛け算を実行します。
```mind:quaderr.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"-9223372036854775807"を　ｑ文字列初期化し　int64_2に　入れ   
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
int64_2 (ｑ文字列初期化)   8000000000000001 -9223372036854775807
int64とint64_2を　ｑ割り   ffffffffffffffff -1
int64にint64_2を　ｑ掛け   オーバーフローしました。
```
## お題のソースコード（２）
割り算のオーバーフロー条件、マイナス側最小値を-1で割ります。掛け算も直前に行います。
```mind:quaderr.src
※～略～
メインとは
	"-9223372036854775808"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"-1"を　ｑ文字列初期化し　int64_2に　入れ
※～略～
```
## 実行結果（２）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   8000000000000000 -9223372036854775808
int64_2 (ｑ文字列初期化)   ffffffffffffffff -1
int64とint64_2を　ｑ割り   オーバーフローしました。
```
## お題のソースコード（３）
マイナス側最小値を-1で加算します。
```mind:quaderr.src
※～略～
メインとは
	"-9223372036854775808"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"-1"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ加え   "を　表示し
	int64と　int64_2を ｑ加え クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ加え ＄＄倍精度表示し　改行し
※～略～
```
## 実行結果（３）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   8000000000000000 -9223372036854775808
int64_2 (ｑ文字列初期化)   ffffffffffffffff -1
int64とint64_2を　ｑ加え   オーバーフローしました。
```
## お題のソースコード（４）
マイナス側最小値を1で減算します。
```mind:quaderr.src
※～略～
メインとは
	"-9223372036854775808"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"1"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ加え   "を　表示し
	int64と　int64_2を ｑ加え クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ加え ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ引き   "を　表示し
 	int64に　int64_2を ｑ引き クアド表示2し　" "を　表示し 
    int64に　int64_2を ｑ引き ＄＄倍精度表示し　改行し 
    。
```
## 実行結果（４）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   8000000000000000 -9223372036854775808
int64_2 (ｑ文字列初期化)   0000000000000001 1
int64とint64_2を　ｑ加え   8000000000000001 -9223372036854775807
int64にint64_2を　ｑ引き   オーバーフローしました。
```
## お題のソースコード（５）
プラス側最大値を1で加算します。
```mind:quaderr.src
メインとは
	"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ
	"int64   (ｑ文字列初期化)   "を　表示し
	int64を　クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　改行し
 	"1"を　ｑ文字列初期化し　int64_2に　入れ   
	"int64_2 (ｑ文字列初期化)   "を　表示し
	int64_2を クアド表示2し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	"int64とint64_2を　ｑ加え   "を　表示し
	int64と　int64_2を ｑ加え クアド表示2し　" "を　表示し 
    int64と　int64_2を ｑ加え ＄＄倍精度表示し　改行し
	"int64にint64_2を　ｑ引き   "を　表示し
 	int64に　int64_2を ｑ引き クアド表示2し　" "を　表示し 
    int64に　int64_2を ｑ引き ＄＄倍精度表示し　改行し 
    。
```
## 実行結果（５）
```
C:\developments\vscode\mind8\bin>..\sample\quaderr
int64   (ｑ文字列初期化)   7fffffffffffffff 9223372036854775807
int64_2 (ｑ文字列初期化)   0000000000000001 1
int64とint64_2を　ｑ加え   オーバーフローしました。
```
# おわりに
もう少しいろいろな境界値でテストしてみないとなんとも言えませんが、基本的なパターンではオーバーフローチェック動作しているようです。
なんども記事のおわりで「いよいよ本丸の固定小数点に迫っていきます。」とか書きましたが、いよいよかも？課題は課題として残しつつ少し本題の実装イメージを具体化してみたい願望は強まっています。
