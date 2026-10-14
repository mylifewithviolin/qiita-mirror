# はじめに
「日本語トランスコンパイラ言語 Re:Mind（リマインド）」はオープンな実装言語仕様で、どなたでもどの実装言語でもコンパイラ・トランスコンパイラを実装することができます。本記事は仕様策定者の筆者がC#で実装しているステップバイステップな備忘録記事です。

# 本試作の実装言語
・C#
コンソールアプリケーションとして実装します。本試作範囲は策定仕様のごくごく一部です。ターゲット言語は一部のみ対応、言語の対応ソース構文も超限定的です。

## 本試作のターゲット言語
本試作のターゲット言語としては下記の4言語を想定しております、本記事はそのうちのC#に該当する内容です。
・**C#**　←本記事の対象言語
・Java
・VB.NET
・Mind

・想定稼働OS Windows
※C#は非Windows環境でも動作しますが、検証パワー不足のため動作環境をWindows限定とさせていただいております。

## 本試作のターゲット言語の対応仕様範囲
クラス内にメンバ変数を宣言して、関数内で使用できるようにします。クラスのインスタンス初期化構文非対応のためスタティック宣言を前提としています。

### お題のターゲット言語出力ソースコード
#### C#
```cs:targetSourceFiles\variable.cs
using System;
namespace HelloWorld
{

   /// <summary>プログラム型</summary>
   public class Program
   {
        /// <summary>挨拶１</summary>
       private static string? aisatsu1;
       
       /// <summary>メイン</summary>
       /// <param name=args>引数</param>
       static void Main(string[] args)
       {
           aisatsu1="Hello World one!";
           ConsoleOut(aisatsu1);
       }

       /// <summary>コンソール表示する</summary>
       /// <param name=args>引数</param>
       static void ConsoleOut(string args2)
       {
           Console.WriteLine(args2);
       }

   }

}

```

### お題のトランスコンパイラ言語 Re:Mind入力ソースコード(ターゲット言語一部依存)
#### C#
クラス内でメンバ変数を宣言しています。
関数内のローカル変数名や引数名のスコープに現状非対応のため、引数名に１，２をつけて重複をさけています。

Nullable指定（string?）などはC#依存です。

```mind:sourceFiles\variablecs.remind
▽名前空間 HelloWorld
    /**
    * Program
    */
    ▽public クラス プログラム型
    
        /** 
        * aisatsu1 
        */
        ・private static string? 挨拶１


        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            □挨拶１="Hello World one!"
 
            □コンソール表示する(挨拶１)
        △

        /**
        * ConsoleOut
        * @param 引数2 dispStr
        */
        ▽static void コンソール表示する(string 引数2)
            □コンソール.一行表示する(引数2)
        △
    △
△

■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲
```

インポート文の既存ライブラリを引用する記述は毎回書く必要をなくす想定ですが（ライブラリファイルとして分割想定）、まだライブラリのサンプルコードは皆無のため、本試作ではライブラリ引用ソースコードも明確に書いてもらう想定です。Systemは既定のusing文として明示不要であっても既定でない今後のusing文のため、出力するとしています。

### トランスコンパイラの内部構造

たいへんお手数ですがこちらの記事をご参照ください。細かい点は最新の試作実装を反映しておりませんが、基本的な構想を読み解くにはこちらのがよいかと思います。

https://qiita.com/mylifewithviolin/items/b3d921383aab4211dc84

日本語ロジック仕様記述言語 Re:Mind（リマインド）は[オープンな設計言語仕様](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)で、どなたでもこの記法を使いロジックを記述することができます。


### トランスコンパイラの言語仕様

たいへんお手数ですがこちらの記事をご参照ください。本試作が実装しているのは全体仕様の一部です。

https://qiita.com/mylifewithviolin/items/c3aff020a6831e6ae848

# 実行結果

## 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.99.3
C# 12 
dotnet-sdk-8.0.206-win-x64

### VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

## トランスコンパイラの出力コード
C#で実装されたソースをコンパイル実行します。ビルド（コンパイル）はVSCodeのタスクで実行しました。ターゲット言語のソースコードは実行時にファイルから読み込みます。

実行環境はWindows11上のVSCodeのターミナルです。
デバッグ用に最終トランスコンパイルソースコードの他、中間状態の分析結果も出力しています。実際はソースコードオリジナル出力というのが冒頭に出力されるのですが、そちらは記載を割愛しています。

ターゲット言語のトランスコンパイル後のソースコードはファイルでも出力されます。

#### C#
```mind:C#
************ソースコードノード判定出力*********************
名前空間 HelloWorld                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Program                              ND_JDC_MIDLE//JavaDoc備考途中
*/                              ND_JDC_END JavaDoc備考終了
public クラス プログラム型                              ND_DEF_BEGIN//定義開始
                              /**                              ND_JDC_BEGIN//JavaDoc備考開始
* aisatsu1                              ND_JDC_MIDLE//JavaDoc備考途中
*/                              ND_JDC_END JavaDoc備考終了
private static string? 挨拶１                              ND_STM_BEGIN//宣言開始
                                                            /**                              ND_JDC_BEGIN//JavaDoc備考開始
* Main                              ND_JDC_MIDLE//JavaDoc備考途中
* @param 引数 args                              ND_JDC_PARAM//JavaDoc備考変数
*/                              ND_JDC_END JavaDoc備考終了
static void メイン(string[] 引数)                              ND_DEF_BEGIN//定義開始
挨拶１="Hello World one!"                              ND_EXE_BEGIN//実行開始
                              コンソール表示する(挨拶１)                              ND_EXE_BEGIN//実行開始
                              ND_DEF_END//定義終了
                              /**                              ND_JDC_BEGIN//JavaDoc備考開始
* ConsoleOut                              ND_JDC_MIDLE//JavaDoc備考途中
* @param 引数2 dispStr                              ND_JDC_PARAM//JavaDoc備考変数
*/                              ND_JDC_END JavaDoc備考終了
static void コンソール表示する(string 引数2)                              ND_DEF_BEGIN//定義開始
コンソール.一行表示する(引数2)                              ND_EXE_BEGIN//実行開始
                              ND_DEF_END//定義終了
                              ND_DEF_END//定義終了
                              ND_DEF_END//定義終了
                              インポートする System                              ND_QAT_BEGIN//引用開始
public static class コンソール Console                              ND_QAD_BEGIN//引用定義開始
public static 一行表示する(string? value)                              ND_QAD_BEGIN//引用定義開始
WriteLine (string? value)                              ND_QAD_MIDLE//引用定義中
                              ND_QAD_END//引用定義終了
                              ND_QAD_END//引用定義終了

************nameDictionary出力***************************
Key:名前空間 Value:namespace
Key:クラス Value:class
Key:インポートする Value:using
Key:プログラム型 Value:Program
Key:挨拶１ Value:aisatsu1
Key:引数 Value:args
Key:メイン Value:Main
Key:引数2 Value:dispStr
Key:コンソール表示する Value:ConsoleOut
Key:コンソール Value:Console
Key:一行表示する Value:WriteLine

************トランスコンパイル後ソースコード出力************
using System;
namespace HelloWorld
{

   /// <summary>プログラム型</summary>
   public class Program
   {

        /// <summary>挨拶１</summary>
       private static string? aisatsu1;
       /// <summary>メイン</summary>
       /// <param name=args>引数</param>
       static void Main(string[] args)
       {

           aisatsu1="Hello World one!";
           ConsoleOut(aisatsu1);
       }

       /// <summary>コンソール表示する</summary>
       /// <param name=args>引数</param>
       static void ConsoleOut(string args2)
       {

           Console.WriteLine(args2);
       }

   }

}

プログラム '[3152] remind.dll' がコード 0 (0x0) で終了しました。
```
# 実行結果の実行結果

#### C#
C#の出力コードの実行結果はVSCodeのコンパイル環境でビルド・実行しました。デバッグコンソールに「Hello World one!」出力されています。
```:
Hello World one!
プログラム '[16896] HelloWorld.dll' がコード 0 (0x0) で終了しました。
```


# ソースコード
GitHub [Commit  a7ba5de](https://github.com/mylifewithviolin/remind/commit/a7ba5de668b3c5ed11037cb5f69d5129fa25ccfe)


# おわりに
いかがでしたでしょうか？完成までは自転車でアルファケンタウリや観測可能な宇宙の範囲の淵まで移動しようとしている気分です:joy:　とりあえずステップバイステップで進みます。:alarm_clock:
