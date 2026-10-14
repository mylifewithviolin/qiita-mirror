# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんからMind8に倍精度整数があると伺ったのを契機に、諸般の都合でMind8のkernelの修正実行に挑戦。

前回で倍精度整数同士の加算のめぼしがつきましたので今回は倍精度整数（64bit整数）の変数同士の四則演算と論理演算の一部（等しいと大きい）を実装してみます。もしも本記事の内容をお試ししたい場合は諸般の事情でMind7のライセンスが必要となりますのでご注意ください。

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
Mind8標準のスタック操作内部関数push_quad()が64bitイメージのうち下位32bitの上位16bitを0でマスクする仕様のようでしたので、下位32bitをそのままMind8スタックにプッシュするpush_quad2()をcompword.c内のpush_quad()定義部の下に追記します。その下にはMind開発者の@killyさんからご紹介いたいだいたMind単語のスタック検査関数c_test_push_quadが定義されています。

```c:compword.c
PRIVATE void
    push_quad( word64 qval )
{
        /* ([引数] → quad) */

		ULONG	hi;
		ULONG	lo;

	hi = qval >> 32;
	lo = qval & 0xffff;
	PUSH_Q( lo, hi );
}

PRIVATE void
    push_quad2( word64 qval )
{
        /* ([引数] → quad) */

		ULONG	hi32;
		ULONG	lo32;

	hi32 = qval >> 32;
	lo32 = qval & 0xffffffff;
	PUSH_Q( lo32, hi32 );
}
```
このスタックプッシュ関数push_quad2()を使えば正常動作するだろうという想定で、予約されているダミー関数8つが定義されているother.c内の空いているダミー関数7つを下記のようにすべて使い切って四則演算と等しい、大きいを定義します。
また、push_quad2()用のテスト単語c_test_push_quad2を用意しておきます。

```c:other.c
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

/* end of 'other.c' */
```

## Mind7ツールでc_words修正ビルド
Mind8には単語定義修正ツールが入っていないので、Mind7のライセンスがあることを前提にMind7のbinフォルダからMind8のbinフォルダへツールをコピーしておきます。（前回記事参照）

今回はtasks.jsonに設定しておき、VSCodeターミナルのタスクで実行しました。
```
 *  実行するタスク: c2words 'kernel.c c_words' 

c2words 処理中・・kernel.c kerbody.c osdefine.def serialno.def common.def osfunc.h kernel.def ptrdef.c jumpbufmax.h ptrmacro.def wincons0.h dispatch.c kerhot.c compword.c 0ker.c dispword.c kermain.c array.c bunki.c 1ker.c 1kerF.c 1kerFunc.c 2ker0.c 2ker1.c 2ker2.c 2ker22.c 2ker3.c 2ker4.c 2kerU.c 3ker.c 4ker.c mktime.c ms_c.c chmod.c dosdep.c proccomm.c regquery_lib.h regquery.c other.c runtno.c 終り
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

## Mind8ツールでfile修正ビルド
ここからはMind8のツール、コンパイラを使用します。

前回記事でMind開発者の@killyさんからMind8ランタイムのシリアル番号チェッカーツールをご提供いただいたので、それをインストールしておきます。

```
c:\pmind\bin のディレクトリ

2024/03/09  19:42            57,344 incrserial.exe
2024/03/09  19:42            32,742 incrserial.mco
               2 個のファイル              90,086 バイト
2024/03/09  19:42           131,072 mrunt057.exe
               1 個のファイル             131,072 バイト
```
ランタイムのシリアル番号チェッカツールを下記のオプションで実行し、シリアル番号をカウントアップしておきます。
```
C:\developments\vscode\mind8\kernel>incrserial u
42 -> 43 | Generated: serialno.def
```

fileライブラリをリビルドして開発環境のlibフォルダにコピーします。
```
C:\developments\vscode\mind8\kernel>cd ../file  

C:\developments\vscode\mind8\file>mmake obj\file mind
..\kernel\c_words.wrdが新しい。
[再コンパイル] mind asmword ..\libY\yoyakugoG obj\asmword

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. serialno=43 終了

[再コンパイル] mind console obj\asmword obj\console -local

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了

[再コンパイル] mind file obj\console obj\file -local

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了

C:\developments\vscode\mind8\file>mcpC -puv obj\file.mco obj\file.sym ..\lib
obj\file.mco -> ..\lib
obj\file.sym -> ..\lib
```
続いて以前の記事でtasks.jsonに設定してあるnmake allをターミナルのタスクから実行します。
```
 *  実行するタスク: nmake all 


Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        cl -c -W2 /nologo /Zi /Od kernel.c /Fokernel.obj
kernel.c
c:\developments\vscode\mind8\kernel\compword.c(2359) : warning C4047: '=' : 間接参照のレベルが 'char *' と 'ULONG' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2362) : warning C4047: '関数' : 間接参照の
レベルが 'char **' と 'char *' で異なっています。
c:\developments\vscode\mind8\kernel\compword.c(2362) : warning C4024: 'strtod' : の型が 2 の仮引数および実引数と異なります。
c:\developments\vscode\mind8\kernel\dispword.c(273) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(357) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(365) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(376) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\dispword.c(384) : warning C4090: '関数' : 異なる 'const' 修飾子です。
c:\developments\vscode\mind8\kernel\3ker.c(303) : warning C4028: パラメータの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8\kernel\3ker.c(309) : warning C4028: パラメータの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8\kernel\3ker.c(316) : warning C4028: パラメータの型 1 が関数宣言と一致しません。
c:\developments\vscode\mind8\kernel\dosdep.c(888) : warning C4133: '関数' : 'int *' と 'char *' の間で型に互換性がありません。
        cl /SUBSYSTEM:console /MACHINE:IX86 /nologo /Zi /Od /OUT:kernel.exe kernel.obj startup.obj osfunc.obj wincons0.obj  regquery_lib.obj WSOCK32.LIB advapi32.lib
cl : コマンド ライン warning D9025 : '/Od' より '/Ox' が優先されます。
cl : コマンド ライン warning D9002 : 不明なオプション '/SUBSYSTEM:console' を無視します   
cl : コマンド ライン warning D9002 : 不明なオプション '/MACHINE:IX86' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/OU' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/OT' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/O:' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Ok' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Oe' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Or' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/On' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Oe' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Ol' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/O.' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Oe' を無視します
cl : コマンド ライン warning D9002 : 不明なオプション '/Oe' を無視します
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
警告が出ていますが実行には問題なさそうなので無視しています。
nmake installも実行しておきます。
```
 *  実行するタスク: nmake install 

Microsoft(R) Program Maintenance Utility Version 9.00.30729.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        copy c_words.wrd ..\bin
        1 個のファイルをコピーしました。
        copy  kernel.exe ..\bin
        1 個のファイルをコピーしました。
        copy  mindexec.exe ..\bin
        1 個のファイルをコピーしました。
        copy c_words2.wrd  ..\bin
        1 個のファイルをコピーしました。
        copy  compker.exe ..\bin
        1 個のファイルをコピーしました。
        copy  mindexec.exe ..\bin
        1 個のファイルをコピーしました。
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
開発環境のbinフォルダはパスを設定しておらず、正規のMind8にパスが通っていますので、kernel.exeをリネームしたmrunt010.exeに手動でコピーします。
```
C:\developments\vscode\mind8>copy bin\kernel.exe c:\pmind\bin\mrunt010.exe 
c:\pmind\bin\mrunt010.exe を上書きしますか? (Yes/No/All): Y
        1 個のファイルをコピーしました。
```
# お題のソースコード　Mind
今回追加した単語をすべて使うソースを下記のように記述してビルドします。

```mind:quad.src
int64は　倍精度変数。
int64_2は　倍精度変数。

メインとは
	0fffffffeHと　000009FFFHを　無処理し　文字列情報合成し　int64に　入れ
	000000002Hと　000000000Hを　無処理し　文字列情報合成し　int64_2に　入れ
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し

    改行し
	int64に　int64_2を ｑ加え ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ加え ＄＄倍精度表示　改行し 
	int64から　int64_2を ｑ引き ＄＄クアド表示し　" "を　表示し 
    int64から　int64_2を ｑ引き ＄＄倍精度表示　改行し 
	int64に　int64_2を ｑ掛け ＄＄クアド表示し　" "を　表示し 
    int64に　int64_2を ｑ掛け ＄＄倍精度表示　改行し 
	int64と　int64_2を ｑ割り ＄＄クアド表示し　" "を　表示し 
    int64と　int64_2を ｑ割り ＄＄倍精度表示　改行し
	int64と　int64_2を ｑ等しい ＄＄クアド表示し　　改行し
	int64が int64_2より ｑ大きい ＄＄クアド表示し 　改行し 
	改行し		
	int64を　＄＄クアド表示し　" "を　表示し int64を　＄＄倍精度表示し　改行し
	int64に　c_test_push_quad2 　c_test_push_quad2 ＄＄クアド表示し　改行し　改行し
	int64_2を ＄＄クアド表示し　" "を　表示し　int64_2を ＄＄倍精度表示し　改行し
	int64_2を c_test_push_quad2 　c_test_push_quad2 ＄＄クアド表示し　改行し 
	。

```
前回の記事ではあまりはっきり書いておりませんでしたが、kernelをビルド・デバッグ実行する環境はVisual Studio 2008 command promptを開いて、vscode\mind8\kernelをカレントディレクトリとしてcode .でVSCodeを起動しています。
それに対して、Mindのソースを編集してMindコンパイラでコンパイルする環境は通常のコマンドプロンプトを開いて、vscode\mind8をカレントディレクトリとしてcode .で別のVSCodeインスタンスを起動しています。

正規のMind8のfileライブラリではなく、今回リビルドしたfileライブラリを指定してコンパイルします。
```
C:\developments\vscode\mind8>mind sample\quad lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> sample\quad.exe
```
ここでC環境でデバッグ実行できるようにコンパイルされたmcodeファイルをmindexec.mcoにリネームしてkernelフォルダにコピーしておきます。
```
C:\developments\vscode\mind8>copy sample\quad.mco kernel\mindexec.mco 
kernel\mindexec.mco を上書きしますか? (Yes/No/All): Y
        1 個のファイルをコピーしました。
```

## 実行結果
kernelをビルド・デバッグ実行する環境でデバッグ実行開始します。
下記はVSCodeのターミナルに出力された実行結果です。

```
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
PS C:\developments\vscode\mind8\kernel>
```
正常動作したようです。:tada:演算結果もあっている模様。:tada::tada::tada:
スタック検査単語での結果もOKのようです。:confetti_ball:

ここでC環境で実行したランタイムのシリアル番号チェッカツールでアップデートしたシリアル番号と異なるライブラリでビルドされたmindexec.mcoを実行しようとすると、デバッグ実行時にエラーがでました。

# おわりに
今回はいい感じで終われました。本来ならばテストツールでがらがら諸条件を検証しなければならないところですが、本件は学習目的なのでそこは割愛させていただきます。次回は少し調子にのって、いよいよ本丸の固定小数点に迫っていきます。変数の宣言や初期化どうするか（わたしにとっての）難題が山積していますが、（少し納税期限が迫ってきておりますので）少しお休みします。

# 2024/03/11追記
Mind7ツールc2wordsが更新したファイルを確認しました。追加した単語のmcodeが対応していることが確認できます。
```:c_words.wrd
～略～
グローバル。
ｆ余りは　アセンブラ定義の処理単語　実数入力 実数出力。
c_test_push_quad2は　アセンブラ定義の処理単語。
ｑ加えは　アセンブラ定義の処理単語。
ｑ引くは　アセンブラ定義の処理単語。
ｑ掛けは　アセンブラ定義の処理単語。
ｑ割るは　アセンブラ定義の処理単語。
ｑ等しいは　アセンブラ定義の処理単語。
ｑ大きいは　アセンブラ定義の処理単語。
$$mrunt010は　アセンブラ定義の処理単語。
```

```:c_words.def
～略～
PRIVATE void famari( void );
PRIVATE void c_test_push_quad2( void );
PRIVATE void qkuwae( void );
PRIVATE void qhiku( void );
PRIVATE void qkake( void );
PRIVATE void qwaru( void );
PRIVATE void qhitosii( void );
PRIVATE void qookii( void );
PRIVATE int mrunt_no( void );
```
```:c_words.tbl
～略～
/*02EF*/ famari,
/*02F0*/ c_test_push_quad2,
/*02F1*/ qkuwae,
/*02F2*/ qhiku,
/*02F3*/ qkake,
/*02F4*/ qwaru,
/*02F5*/ qhitosii,
/*02F6*/ qookii,
```
