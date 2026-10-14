# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんのご支援をいただきつつMind8のkernelの修正実行に挑戦中の続きです。

既に[こちらの記事](https://qiita.com/mylifewithviolin/items/d5d65042ca02477a680c)で4桁スケーリング固定小数点型の通貨変数を実装してみていますが、ベースとしております倍精度変数(符号付き64bit整数)の初期化の際に、他の変数型からの型変換キャストができるとうれしいなと思い、[前回記事](https://qiita.com/mylifewithviolin/items/e41d0b6b9e70a3d277da)で他の整数型変数からの代入による暗黙の型変換の挙動を調査しましたところ、@killyさんよりコメントでAndroid版Mindには倍精度整数へのキャスト単語があることを情報共有いただきましたので、近い感じのものを実装してみることにします。

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

符号付32bit整数変数「変数」から符号付64bit整数変数「倍精度変数」への型変換「ｑキャスト」の他、符号付64bit浮動小数点変数「小数変数」からの型変換「ｑ小数からのキャスト」を実装してみました。

```c:5kerD.c
//～略～
PRIVATE void
    qcast( void )	/* ;WORD ｑキャスト .N */
{
		LONG		int32;
    	LONG64  	long1;

	/* (int32 → long1) */

	int32 = POP_L_OF_Q;

	long1 = (LONG64)int32;

    push_quad2(long1);
}

PRIVATE void
    qcast_f( void )		/* ;WORD ｑ小数からキャスト */
{
		double		float1;
    	LONG64  	long1;

        /* (float1 → long1) */

	float1 = pop_float();

	long1 = (LONG64)float1;

    push_quad2(long1);
}
//～略～
```
上記の他にオーバーフローチェック付きの「ｑ一つ加え」、「ｑ二つ加え」、「ｑ一つ引き」、「ｑ二つ引き」を実装しています。

<details><summary>ソースコード全文</summary>

```c:5kerD.c

```
</details>

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
符号付32bit整数変数「変数」の最大値と最小値から符号付64bit整数変数「倍精度変数」への型変換「ｑキャスト」を実行します。また、参考に[前回記事](https://qiita.com/mylifewithviolin/items/e41d0b6b9e70a3d277da)で行った直接代入の結果も併記しました。

```mind:varinit2.src
int32は　      変数。
int64は　倍精度変数。


メインは
2147483647を　int32に　入れ　int32を クアド表示2し　" "を　表示し int32を　数値表示し　　改行し
int32を　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
int32を ｑキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
"2147483647"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
改行し
-2147483648を　int32に　入れ　int32を クアド表示2し　" "を　表示し int32を　数値表示し　　改行し
int32を　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
int32を ｑキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
"-2147483648"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
改行し
。
```
## 実行結果（１）
```
PS C:\developments\vscode\mind8\bin> mind ..\sample\varinit2 ..\lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> ..\sample\varinit2.exe
PS C:\developments\vscode\mind8\bin> ..\sample\varinit2
000000007fffffff 2147483647
000000007fffffff 2147483647
000000007fffffff 2147483647
000000007fffffff 2147483647

0000000080000000 -2147483648
0000000080000000 2147483648
ffffffff80000000 -2147483648
ffffffff80000000 -2147483648
```
直接代入で符号が反転したマイナス値も無事にキャストして代入できました。:tada:（プラス側ブロック、マイナス側ブロックそれぞれの2行目が直接代入の結果です。）

## お題のソースコード（２）
符号付64bit浮動小数点変数「小数変数」の最大値と最小値から符号付64bit整数変数「倍精度変数」への型変換「ｑ小数からキャスト」を実行します。Mindの「小数」の仮数部桁数は15桁、指数部は±308です。この範囲で「倍精度変数」の最大値、最小値に近い値の変換を狙ってみます。


```mind:varinit2.src
float64は　小数変数。
int64は　倍精度変数。

メインは
9.223372036854775e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　14桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
"9223372036854775807"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
改行し
-9.223372036854775e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　13桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
"-9223372036854775808"を　ｑ文字列初期化し　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
。
```
「指数形式で表示」は符号と小数点、指数記号eを含めて21文字を超えると指数部が文字切れしてましたので、桁数指定を実際の指定値より少ない指定14桁としています。

## 実行結果（２）
```
PS C:\developments\vscode\mind8\bin> mind ..\sample\varinit2 ..\lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> ..\sample\varinit2.exe
PS C:\developments\vscode\mind8\bin> ..\sample\varinit2
ffffffff43dfffff 9.22337203685477e+018
7ffffffffffffc00 9223372036854774784
7fffffffffffffff 9223372036854775807

ffffffffc3dfffff -9.2233720368548e+018
8000000000000400 -9223372036854774784
8000000000000000 -9223372036854775808
```
仮数部桁数は15桁の範囲内で最大値、最小値を指定した結果は、マイナス値も無事にキャストして代入できました。:tada:

## お題のソースコード（３）
指数部の指定によってはオーバーフローが起きえますが、
Mindの「小数変数」の仮数部桁数の正常範囲を超えて「倍精度変数」の最大値、最小値を指数形式でも設定してみます。Mindの「小数変数」の仮数部桁数がオーバーフローしている状態。
Mindの「小数変数」の仮数部桁数の正常範囲内で「倍精度変数」の最大値、最小値を超える値を指数形式でも設定してみます。Mindの「倍精度変数」がオーバーフローしている状態。

```mind:varinit2.src
float64は　小数変数。
int64は　倍精度変数。

メインは

9.223372036854775807e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
9.223372036854776e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
改行し
-9.223372036854775808e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
-9.223372036854776e18を　float64に　入れ　float64を クアド表示2し　" "を　表示し float64を　16桁で　指数形式で表示し　　改行し
float64を ｑ小数からキャストし　int64に　入れ　int64を クアド表示2し　" "を　表示し int64を　＄＄倍精度表示し　　改行し
改行し
。
```
「指数形式で表示」は符号と小数点、指数記号eを含めて21文字を超えると指数部が文字切れしますが、境界値の動きがわかるように桁数指定を16桁としています。（指数部は文字切れします。）
## 実行結果（３）
```
PS C:\developments\vscode\mind8\bin> mind ..\sample\varinit2 ..\lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> ..\sample\varinit2.exe
PS C:\developments\vscode\mind8\bin> ..\sample\varinit2
0000000043e00000 9.2233720368547758e+0
8000000000000000 -9223372036854775808
0000000043e00000 9.2233720368547758e+0
8000000000000000 -9223372036854775808

00000000c3e00000 -9.2233720368547758e+
8000000000000000 -9223372036854775808
00000000c3e00000 -9.2233720368547758e+
8000000000000000 -9223372036854775808
```
まず、Mindの「小数変数」のプラス値の仮数部オーバーフローは9.223372036854775807e18と指定しても16桁目で丸められて9.223372036854776e18と同じ状態になるようでした。いずれも「倍精度変数」の最大値を超えていて、「倍精度変数」へのキャストはマイナスの最大値に変換されました。

マイナス値の仮数部オーバーフローは、Mindの「小数変数」の仮数桁数としてはオーバーフローしていない-9.223372036854776e18を指定しても、「指数形式で表示」の16桁指定の表示が-9.2233720368547758e+となっているためちょっとわかりにくいですが、仮数桁数としてはオーバーフローしている-9.223372036854775808e18とは16進数表示も同じなので、オーバーフローしている方はオーバーフローしていない方に丸められていると推察されます。
-9.223372036854776e18は「倍精度変数」の最小値を超えていて、「倍精度変数」へのキャストはマイナスの最大値に変換されました。
-9.223372036854775808e18は「倍精度変数」の最小値と同じですが、Mindの「小数変数」としてはオーバーフローして「倍精度変数」の最小値を超えた状態に丸められて「倍精度変数」へのキャストはオーバーフローしたと推定されます。

# おわりに
浮動小数点の扱いは仮数指定の限界あたりの扱いがめんどうですね。固定小数点型へのキャストにあった方がよいかなと思い実装してみました。
