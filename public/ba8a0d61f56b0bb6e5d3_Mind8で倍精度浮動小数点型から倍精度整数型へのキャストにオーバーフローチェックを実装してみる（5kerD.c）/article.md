# はじめに
Mind開発者の@killyさんよりコメントでAndroid版Mindには倍精度整数へのキャスト単語があることを情報共有いただきましたので、[前回記事](https://qiita.com/mylifewithviolin/items/239bf87bf05c48f5391d)で32bit整数型変数と64bit浮動小数点型変数から64bit整数型変数への型変換を実装してみました。64bit浮動小数点型変数からの型変換ではオーバーフローが発生する余地があるため、今回はそのチェック処理を実装してみることにします。

# 参考情報
64bit浮動小数点型変数から64bit整数型変数への型変換オーバーフローチェックの実装にあたっては下記の情報を参考にさせていただいております。

https://www.jpcert.or.jp/sc-rules/c-flp34-c.html

https://marycore.jp/prog/c-lang/compare-floating-point-number/

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
## 5kerD.c
独自に追加しているソースファイルです。[こちらの記事](https://qiita.com/mylifewithviolin/items/bb4c77992ce5089b0cde)以降からはMind側で使用する処理単語の他に、それらの単語が呼び出すエラー処理関数も追加しており、c2word用のコメントは記述しなければ辞書の順序は変わらないことをつかんだので、こちらに独自関数や定義を集中します。

符号付64bit浮動小数点変数「小数変数」からの型変換「ｑ小数からのキャスト」にオーバーフローチェックを実装してみました。
DBL_EPSILON 2.2204460492503131E-16は「計算機イプシロン(machine epsilon)」です。float.hをインクルードしていないため、本ファイル内で宣言しています。

```c:5kerD.c
//～略～

typedef  __int64       LONG64;

#define LONG64_MAX +9223372036854775807
#define LONG64_MIN -9223372036854775808
#define DBL_MIN = -1.797693E+308
#define DBL_MAX = 1.797693E+308
#define DBL_EPSILON 2.2204460492503131E-16

//～略～

/* 倍精度浮動小数点から倍精度整数キャストオーバーフロー事前チェック JPCERT/CC FLP34-C.改 */
PRIVATE void _check_over_flow_cast_d2ll(double float64)
{
	 if ( (float64 >=0.0 && (float64 - (double)(LONG64_MAX -1.0)) > -1.0*DBL_EPSILON)
	   	|| (float64 <0.0 && (float64 + (double)(LONG64_MIN +1.0)) < DBL_EPSILON)) {
	 		_fover_flow_error(float64);/* エラー処理 */
	 }
}
//～略～

PRIVATE void
    qcast_f( void )		/* ;WORD ｑ小数からキャスト */
{
		double		float1;
    	LONG64  	long1;

        /* (float1 → long1) */

	float1 = pop_float();
	_check_over_flow_cast_d2ll(float1);

	long1 = (LONG64)float1;

    push_quad2(long1);
}

//～略～
```

### ソースコード全文
「ｑ小数からのキャスト」とオーバーフローチェック関数、定数定義以外は前回と同じです。[前回記事](https://qiita.com/mylifewithviolin/items/239bf87bf05c48f5391d)をご参照ください。


## other.c
other.cの内容をすべてダミー定義とします。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。

## kerbody.c
kerbody.cでother.cのインクルードの直前に5kerD.cをインクルードするように追記しています。[こちらの記事](https://qiita.com/mylifewithviolin/items/c9c0f6abfe82627a665c)を参照してください。


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
最初は文字列で64bit整数最大値9223372036854775807で初期化しています。
次に9223372036854774000の近似値で初期化しています。
次に9223372036854775000の近似値で初期化しています。
最後の9223372036854776000の近似値で初期化しています。これはオーバーフローを検出する想定です。

```mind:varinit3.src
float64は　小数変数。
int64は　倍精度変数。

メインは
"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
9.223372036854774e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　14桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
9.223372036854775e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　14桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
9.223372036854776e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　14桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
。
```
## 実行結果（１）
```
PS C:\developments\vscode\mind8\biN> mind ..\sample\varinit3 ..\lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> ..\sample\varinit3.exe
PS C:\developments\vscode\mind8\biN> ..\sample\varinit3 
7fffffffffffffff 9223372036854775807
fffffffe43dfffff 9.22337203685477e+018
7ffffffffffff800 9223372036854773760
ffffffff43dfffff 9.22337203685477e+018
7ffffffffffffc00 9223372036854774784
0000000043e00000 9.22337203685478e+018
オーバーフローしました。
```

9223372036854774000の近似値9.223372036854774e18で初期化された倍精度浮動小数点変数を「ｑ小数からのキャスト」すると9223372036854773760にキャストされました。

9223372036854775000の近似値9.223372036854775e18で初期化された倍精度浮動小数点変数を「ｑ小数からのキャスト」すると9223372036854774784にキャストされました。

9223372036854776000の近似値9.223372036854776e18で初期化された倍精度浮動小数点変数を「ｑ小数からのキャスト」すると、オーバーフローを検出しました。:tada:

このとき、float64 - (double)(LONG64_MAX -1.0)の値は0.0000000000000000となっており、double型定数0.0とは正常に大小比較できなかったため、計算機イプシロン値のマイナス値-1.0*DBL_EPSILONと比較判定しています。

## お題のソースコード（２）
最初は文字列で64bit整数最小値-9223372036854775808で初期化しています。
次に-9223372036854774000の近似値で初期化しています。
次に-9223372036854775000の近似値で初期化しています。
最後の-9223372036854776000の近似値で初期化しています。これはオーバーフローを検出する想定です。
```mind:varinit3.src
float64は　小数変数。
int64は　倍精度変数。


メインは
"-9223372036854775808"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
-9.223372036854774e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
-9.223372036854775e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
-9.223372036854776e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　13桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
。
```

## 実行結果（２）
```
PS C:\developments\vscode\mind8\biN> mind ..\sample\varinit3 ..\lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> ..\sample\varinit3.exe
PS C:\developments\vscode\mind8\biN> ..\sample\varinit3                 
8000000000000000 -9223372036854775808
fffffffec3dfffff -9.2233720368547738e+
8000000000000800 -9223372036854773760
ffffffffc3dfffff -9.2233720368547748e+
8000000000000400 -9223372036854774784
00000000c3e00000 -9.2233720368548e+018
オーバーフローしました。
```
-9223372036854776000の近似値-9.223372036854776e18で初期化初期化された倍精度浮動小数点変数を「ｑ小数からのキャスト」すると、オーバーフローを検出しました。:tada:

このときの符号付き64bit整数のマイナス側最大値に1加算してdoubleにキャストした値との差異は非常に小さな値のため、計算機イプシロン値DBL_EPSILONと比較判定しています。

# おわりに
固定小数点型へのキャストに倍精度浮動小数点型変数から倍精度整数へのキャストがあった方がよいかなと思い軽い気持ちで実装してみましたが、オーバーフローチェックは意外と煩雑でした。近似値扱いのアプローチが必要で、JPCERTの参考ロジックはそのままでは動作しなかったので、もうひとつの参考情報の計算機イプシロン値DBL_EPSILONを使った比較判定というのはたいへん勉強になりました。



