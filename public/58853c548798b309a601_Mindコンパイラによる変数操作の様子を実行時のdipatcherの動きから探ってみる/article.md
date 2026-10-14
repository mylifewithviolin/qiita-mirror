# はじめに
Mind開発者の@killyさんからMind8の変数操作単語の特別な動きについて重要な情報共有をいただきましたので、念のためその様子を実行時のdipatcherの動きから探ってみることにしました。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.07 for Windows

MindはMind8のバージョンのパスが構成されていることを前提とします。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガはMind8のCカーネルアプリケーションをデバッグ実行するために使用しています

# お題のソースコード　Mind
Mind8で定義されているすべての数値型に対して「一つ増加」を下記のように記述してビルドします。

```mind:varincr.src
int8は　　　バイト変数。
int16は　　 ワード変数。
int32は　   変数。
float64は　 小数変数。
int64は　   倍精度変数。

メインは
    int8を　一つ増加し
    int16を　一つ増加し
    int32を　一つ増加し
    float64を　一つ増加し
    int64を　一つ増加し

    int8を　＄＄クアド表示し　改行し
    int16を　＄＄クアド表示し　改行し
    int32を　＄＄クアド表示し　改行し
    float64を　＄＄クアド表示し　改行し
    int64を　＄＄クアド表示し　改行し
    。
```

デバッグ実行の都合上、正規のMind8のfileライブラリではなく、前回リビルドしたfileライブラリを指定してコンパイルします。
```
C:\developments\vscode\mind8>mind sample\varincr lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> sample\varincr.exe
```
このソースから呼び出されるランタイム関数をC環境でデバッグ実行できるようにコンパイルされたmcodeファイルをmindexec.mcoにリネームしてkernelフォルダにコピーしておきます。
```
C:\developments\vscode\mind8>copy sample\varincr.mco kernel\mindexec.mco 
kernel\mindexec.mco を上書きしますか? (Yes/No/All): Y
        1 個のファイルをコピーしました。
```
## 実行結果
kernelをビルド・デバッグ実行する環境でデバッグ実行開始します。
下記はVSCodeのターミナルに出力された実行結果です。

```
00000001|00000000
00000001|00000000
00000001|00000000
00000000|000000FF
00000001|00000000
PS C:\developments\vscode\mind8\kernel> 
```

4行目だけ浮動小数点なのでフォーマットが異なりますが、他の4つの整数型は1がセットされている（整数型初期値の0から1カウントアップされている）ことがわかります。


# お題のソースコード　C関数
前回の記事でpush_quad2を追加したcompword.cが今回の深堀テーマです。@killyさんから情報共有により、関数型関数の引数型違いの同名関数のような動きをする処理単語がここには定義されています。詳しくは[killyさんの記事](https://qiita.com/killy/items/db2f1a935e6b00d23366)をご参照ください。

少し行数を減らすためオリジナルより改行を減らしています。
```c:compword.c
/*-------   変数を一つ増加　------------------------------------*/
    /*** 注意:以下の4単語は定義順序を変えてはならない **/
    /*    (コンパイラが連続したコードを想定している為) */

PRIVATE void
    zzIncBvar( void )           /* ;WORD $$INC_BVAR */
{
        (*AccessPointer.b)++;
}

PRIVATE void
    zzIncWvar( void )           /* ;WORD $$INC_WVAR */
{
        (*AccessPointer.w)++;
}

PRIVATE void
    zzIncDvar( void )           /* ;WORD $$INC_DVAR */
{
        (*AccessPointer.l)++;
}

PRIVATE void
    zzIncLvar( void )           /* ;WORD $$INC_LVAR */
{
        (*AccessPointer.ll)++;
}

```
上記の4関数のそれぞれのポインタ構造体のメンバをカウントアップしている箇所にブレークポイントを設定しました。

# VSCodeでお題のC関数をデバッグ実行
## デバッグ実行の前提条件

[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)と同じです。dispatcherのC単語呼び出し部分をブレークさせたところまでがレポートされています。

## デバッグ実行中のご様子
下図は「int64を　一つ増加し」が実行したときの様子です。左側のウォッチ式にMCodeのポインタとは別に変数アクセスポインタの値が出力されています。最初ソースコードだけ読んでいたときはAccessPointerのメンバ構成がMCodeポインタと同じだったので、これをMCodeポインタの別の参照変数なのかと誤認していましたが、そうではなさそうです。（値がそれぞれ異なっている。）

この後、「zzQuadHyouji( void )		/* ;WORD ＄＄クアド表示 */」内に設定したブレークポイントに4回ブレークして実行終了します。

![vscodec34.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/e1a293ae-9cae-0866-8129-0e3bb6834972.png)

「int64を　一つ増加し」が実行されるその手前ですが「int8を　一つ増加し」が実行されて「zzIncBvar( void )           /* ;WORD $$INC_BVAR */」内のアクセスポインタのインクリメントにブレークする前に、「zzIncDvar( void )           /* ;WORD $$INC_DVAR */」が25回くらい呼び出されていました。

ユーザーソースコードとしては「一つ増加し」始める前は変数宣言しかないはずなのですが、Mindのランタイムがスタートアップでワード変数のインクリメントを数十回繰り返しているのかもしれません。

# おわりに
@killyさんのご説明のとおり、変数型に応じてMindソースコード上は同じ処理単語名でも内部では別の関数が呼び出されていることが確認できました。たいへん貴重な情報共有ありがとうございました。
