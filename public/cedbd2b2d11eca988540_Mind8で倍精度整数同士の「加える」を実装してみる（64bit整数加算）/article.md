# はじめに
諸般の流れから日本語プログラミング言語Mindで固定小数点計算機能を書いてみようかなと思い立ち、Mind開発者の@killyさんからMind8に倍精度整数があると伺ったのを手掛かりにほぼ手探りで使ってみましたの続報です。

今回は倍精度整数（64bit整数）の変数同士の加算を実装してみます。Mind8は無償バージョンのためC定義関数のソースは公開されているのですが、予約されているダミー関数を実行可能に修正した後のMindワードテーブルを改修するツールは有償バージョンのMind7にしか添付されておりません。もしも本記事の内容をお試ししたい場合はMind7のライセンスが必要となりますのでご注意ください。

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
予約されているダミー関数が定義されているother.other_dummy_02( void )を下記のように修正します。decimal_add( void )	
Mind7のother.cはother.other_dummy_01から空いていましたが、Mind8のother.cはother.other_dummy_01が既にfamari( void )に置き換わっていましたので、02を使います。

```c:other.c
PRIVATE void
    decimal_add( void )	/* ;WORD テスト加える */
{
    	word64  long1;
		word64  long2;

        /* (long1, long2 → long1+long2) */

	long2 = pop_quad();
	long1 = pop_quad();

    long1 += long2;
    push_quad(long1);
}

PRIVATE void
    other_dummy_03( void )	/* ;DUMMYWORD */
{
}
```

## Mind7ツールでc_words修正ビルド
Mind8には修正ツールが入っていないので、Mind7のライセンスがあることを前提にMind7のbinフォルダからMind8のbinフォルダへ下記のファイルをコピーしておきます。


```
C:\developments\vscode\mind8\kernel>dir c:\pmind\bin\c2words.*
 c:\pmind\bin のディレクトリ

2004/10/02  18:33            45,056 c2words.exe
2004/10/02  18:33            46,742 c2words.mco
               2 個のファイル              91,798 バイト
               
C:\developments\vscode\mind8\kernel>dir c:\pmind\bin\mrunt008.*
 c:\pmind\bin のディレクトリ

2004/10/09  18:28           151,552 mrunt008.exe
               1 個のファイル             151,552 バイト               
```

ツールを実行します。mind8のbinフォルダにはパスが通っているものとします。
```
C:\developments\vscode\mind8\kernel>c2words kernel.c c_words
c2words 処理中・・kernel.c kerbody.c osdefine.def serialno.def common.def osfunc.h kernel.def ptrdef.c jumpbufmax.h ptrmacro.def wincons0.h dispatch.c kerhot.c compword.c 0ker.c dispword.c kermain.c array.c bunki.c 1ker.c 1kerF.c 1kerFunc.c 2ker0.c 2ker1.c 2ker2.c 2ker22.c 2ker3.c 2ker4.c 2kerU.c 3ker.c 4ker.c mktime.c ms_c.c chmod.c dosdep.c proccomm.c regquery_lib.h regquery.c other.c runtno.c 終り
```
## Mind8ツールでfile修正ビルド
fileライブラリをリビルドして開発環境のlibフォルダにコピーします。ここからはMind8のツール、コンパイラを使用します。
```
C:\developments\vscode\mind8\kernel>cd ../file      

C:\developments\vscode\mind8\file>mmake obj\file mind
..\kernel\c_words.wrdが新しい。
[再コンパイル] mind asmword ..\libY\yoyakugoG obj\asmword

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. serialno=42 終了

[再コンパイル] mind console obj\asmword obj\console -local

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了

[再コンパイル] mind file obj\console obj\file -local

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了

C:\developments\vscode\mind8\file>..\bin\mcpC -puv obj\file.mco obj\file.sym ..\lib
obj\file.mco -> ..\lib
obj\file.sym -> ..\lib
```

# お題のソースコード　Mind
```mind:decimal.src
int64は　倍精度変数。
int64_2は　倍精度変数。
int64_3は　倍精度変数。

メインとは
	0ffffffffHと　000009FFFHを　無処理し　文字列情報合成し　int64に　入れ
	000000001Hと　000000000Hを　無処理し　文字列情報合成し　int64_2に　入れ
	int64を　＄＄倍精度表示し　改行し
	int64_2を　＄＄倍精度表示し　改行し

	改行し		
	int64に　int64_2を　テスト加え　＄＄クアド表示し　改行し
	int64_2に　int64を　テスト加え　＄＄倍精度表示し　改行し
	int64を int64_3に　入れ　int64_3を　＄＄クアド表示し　改行し
	。
```
正規のMind8のfileライブラリではなく、今回リビルドしたfileライブラリを指定してコンパイルします。
```
C:\developments\vscode\mind8>mind sample\decimal lib\file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> sample\decimal.exe
```

少し結論から申しますと、現状のお題のCソースではスタックへのPUSHが正常動作しておらず、まだ実行結果は正常ではありません。
とりあえず途中のスタックからのPOP状況などを確認するため、Mind8コンパイラが生成した上記のお題ソースのmcodeファイルをデバッグ環境のkernelフォルダに下記のようにリネームしてコピーします。

```
C:\developments\vscode\mind8>copy sample\decimal.mco kernel\mindexec.mco 
kernel\mindexec.mco を上書きしますか? (Yes/No/All): Y  
        1 個のファイルをコピーしました。
```

# VSCodeでお題のC関数をデバッグ実行
## デバッグ実行の前提条件

こちらの記事と同じです。dispatcherのC単語呼び出し部分をブレークさせたところまでがレポートされています。

https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c

## デバッグ実行中のご様子

dispatch.c内のdispatcher()がC_Words_Addr()を介して追加単語を最初に呼びだしたところでブレークした状態が下図です。ターミナルにはそれぞれの変数の倍精度表示が実行されています。

![vscodec29.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9c541f80-6560-4e20-8e73-c6a398d948da.png)

ウォッチ式にlong1とlong2を追加し、スタックからPOPするところまで実行しました。正常に64bit値がPOPできているようです。

![vscodec30.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ebdb2e0b-977c-af40-6547-43c356f7d950.png)

加算も正常に実行されました。

![vscodec31.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4e5c98dc-7d67-3d1f-8e89-fbfae19cb0db.png)

しかし、スタックにPUSHした後のクアッド表示や倍精度表示はうまくいきませんでした。ステップインするとpush_quadではなくpush_floatの方に入ってしまいました。現状のビルドの場合はデバッグ実行でもランタイム実行でも表示結果はいっしょですので、何かソースとアセンブリとで不整合があるかもしれません。実はお題のソースはpush_quadにする直前はpush_floatと書いていました。

![vscodec32.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/fb588ef7-e9d0-f655-358d-15a7c2c197f3.png)

## 実行結果

```
175921860444159
1

42E40000|00000000
1122238464
FFFFFFFF|00009FFF
```

# おわりに
かなり惜しい感じでタイムアウトです。JavaやC#でも差分ビルドだけですとデバッグ中のソースの見た感じと実行されるアセンブリが一致しないということがたまにありますので、Cでもあるのかもしれません。リビルドをしっかりやってみます。

# 2024/03/09 追記
c2words kernel.c c_wordsをkernelのデバッグ環境でやりなおして、デバッグ実行再開しましたところpush_quad()に正常進行するようになり、「テスト加える」の後の「クアド表示」「倍精度表示」ともに加算された値を出力するようになりました。

![vscodec33.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2a23fac3-4d9e-a1ae-e3bb-76c2cb7155a6.png)

##　コンソールへの実行結果（記事本体のお題ソース）
```
175921860444159
1

00000000|0000A000
175921860444160
FFFFFFFF|00009FFF
```
※注意　実行結果の妥当性保証は本例の値限定です。

##　ランタイム環境での実行の注意点
下記のリビルドされたkernel.exeをmrunt010.exeにリネームしてMind8パスのとおったbinフォルダへ配置する必要があります。
```
C:\developments\vscode\mind8\kernel>dir kernel.exe
 C:\developments\vscode\mind8\kernel のディレクトリ

2024/03/09  00:22           444,928 kernel.exe
               1 個のファイル             444,928 バイト
```
下記の_mrunt010.exeは正規のMind8ランタイムを退避したものです。
```
C:\developments\vscode\mind8\kernel>dir c:\pmind\bin\*runt010.exe
 c:\pmind\bin のディレクトリ

2024/03/09  00:22           444,928 mrunt010.exe
2023/01/22  16:36           291,840 _mrunt010.exe
               2 個のファイル             736,768 バイト
```
