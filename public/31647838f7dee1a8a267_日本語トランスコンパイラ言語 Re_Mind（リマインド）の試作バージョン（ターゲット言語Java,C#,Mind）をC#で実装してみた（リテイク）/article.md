# はじめに

[前回記事](https://qiita.com/mylifewithviolin/items/abae37afefb42ca8ef31)はRe:Mind試作品の初号機の実装情報で、ターゲット言語をJava,C#,Mindとしていましたが、トランスコンパイル後のソースコードで、Java,C#ではまさかの実行時エラーという結果でございました。これはRe:Mindの構文仕様で関数の戻り値ない場合は省略可としていた点の考慮を内部設計時に忘れていたというオチでしたが、いろいろ考えた末にとりあえず冒険するのはやめて、構文仕様として戻り値ない場合はvoidを明記というように仕様訂正させていただきます。これに伴い過去設計情報・仕様情報も漸次訂正を行って舞います。

## この記事内容の作業目的
本試作範囲は[策定仕様](https://qiita.com/mylifewithviolin/items/9a6abbab62c0f5e27d4b)のごくごく一部です。ターゲット言語は一部のみ対応、言語の対応ソース構文も超限定的です。


日本語トランスコンパイラ言語 Re:Mind（リマインド）は[オープンな実装言語仕様](https://qiita.com/mylifewithviolin/items/9a6abbab62c0f5e27d4b)で、どなたでもコンパイラ・トランスコンパイラを実装することができます

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Compiler Explorer(Execution モード)
Mind Version 8.07 for Windows


## この記事内容の保証
※この記事には実装・仕様的な情報が含まれます。本記事に開示された実装・仕様は次バージョンの仕様においては予告なく変更される場合があります。また、このバージョンの仕様内で訂正や追加がなされる場合があります。


# 試作概要・試作目的
本試作では日本語トランスコンパイラ言語 Re:Mind（リマインド）の原型を検証し、いろいろな問題点を洗い出します。ターゲット言語のソースコード入力は実装言語のソースコードのインライン記述にとどまります。試作範囲は段階的に拡張してまいります。



## 本試作の実装言語
・C#
コンソールアプリケーションとして実装します。

## 本試作のターゲット言語
本試作のターゲット言語としては下記の3言語を想定しております。
・Java
・C#
・Mind

・想定稼働OS Windows

## 本試作のターゲット言語の対応仕様範囲
"Hello World!"がコンソール出力されるソースコードを入力して（インライン・リテラルコーディング）、ターゲット言語のソースコードを（双方だらだらと）コンソール出力する。（どれを出力するかは起動パラメータにする。）
※出力値を"Hellow World!"から一般的にな"Hello World!"に訂正しました。

### お題のターゲット言語出力ソースコード
すなわち、下記のようなターゲット言語別のソースコードを出力できるようにします。

#### Java
```Java:main.java
    package HelloWorld;

    import java.lang.System;
    /**
    * プログラム型
    */
    public class Program
    {
        /**
        * メイン
        * @param args 引数
        */
        public static void main(string[] args)
        {
           System.out.println("Hello World!");
        }
    }

```
#### C#
```cs:main.cs
    using System;

    namespace HelloWorld
    {
        /// <summary>プログラム型</summary>
        public class Program
        {
            /// <summary>メイン</summary>
            /// <param name="args">引数</param>
            static void Main(string[] args)
            {
               Console.WriteLine("Hello World!");
            }
        }
    }
```

#### Mind
```mind:main.src
    メインとは
        「Hello World!」を　一行表示する。

```

### お題のトランスコンパイラ言語 Re:Mind入力ソースコード(ターゲット言語依存)
下記のソースコードは試作品実装言語C#のリテラル文字列です。class Program内に実装されています。

#### Java

```cs:Re:Mind
        const String SOURCE_JAVA=@"
□パッケージ HelloWorld
    /**
    * Program
    */
    ▽public クラス プログラム型
        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            □コンソール.一行表示する(""Hello World!"")
        △
    △

■インポートする java.lang.System
▼public class コンソール PrintStream System.out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲";
```
メインの戻り値はvoidを明示に訂正しています。
■importは■インポートするに訂正しています。
PrintStreamのインスタンス名をoutではなくSystem.outに訂正しています。

#### C#

```cs:Re:Mind
        const String SOURCE_CS=@"
▽名前空間 HelloWorld
    /**
    * Program
    */
    ▽public クラス プログラム型
        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            □コンソール.一行表示する(""Hello World!"")
        △
    △
△

■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲";
```
メインの戻り値はvoidを明示に訂正しています。
■usingは■インポートするに訂正しています。

#### Mind

```cs:Re:Mind
        const String SOURCE_MIND=@"
        ▽メイン
            □コンソールへ一行表示する(""Hello World!"")
        △
        ▼コンソールへ一行表示する(string value)
            ■一行表示する(string value)
        ▲
        ";
```
Mindのメインの戻り値は基本的にvoidのような気がしますので、ソース仕様はこのままとしています。

# 実行結果
## トランスコンパイラの出力コード
C#をコンパイル実行します。ビルド（コンパイル）はVSCodeのタスクで実行しました。
それぞれ起動パラメータとして"java","cs","mind"を与えると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。
*ソースコードオリジナル出力
デバッグ用に最終トランスコンパイルソースコードの他、中間状態の分析結果も出力しています。実際はソースコードオリジナル出力というのが冒頭に出力されるのですが、そちらは記載を割愛しています。

#### Java
```mind:java
************ソースコードノード判定出力************
                              パッケージ HelloWorld                              /**                              ND_JDC_BEGIN//JavaDoc備考開始
* Program                              ND_JDC_MIDLE//JavaDoc備考途中
*/                              ND_JDC_END JavaDoc備考終了
public クラス プログラム型                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Main                              ND_JDC_MIDLE//JavaDoc備考途中
* @param 引数 args                              ND_JDC_PARAM//JavaDoc備考変数
*/                              ND_JDC_END JavaDoc備考終了
static メイン(string[] 引数)                              ND_DEF_BEGIN//定義開始
コンソール.一行表示する("Hellow World!")                              ND_EXE_BEGIN//実行開始
2
                              ND_DEF_END//定義終了
                              import java.lang.System                              ND_QAT_BEGIN//引用開始
public class コンソール PrintStream out                              ND_QAD_BEGIN//引用定義開始
public static 一行表示する(string value)                              ND_QAD_BEGIN//引用定義開始
println (String value)                              ND_QAD_MIDLE//引用定義中
2
                              ND_QAD_END//引用定義終了

************nameDictionary出力************
Key:パッケージ Value:package
Key:クラス Value:class
Key:インポートする Value:import
Key:string Value:String
Key:プログラム型 Value:Program
Key:引数 Value:args
Key:メイン Value:main
Key:コンソール Value:System.out
Key:一行表示する Value:println

************トランスコンパイル後ソースコード出力************
package HelloWorld;
import java.lang.System;
    /**
    * プログラム型
    */
    public class Program
    {

        /**
        * メイン
        @param args 引数
        */
        public static void main(String[] args)
        {

            System.out.println("Hello World!");
        }

    }
```
#### C#
```mind:cs
************ソースコードノード判定出力************
                              名前空間 HelloWorld                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Program                              ND_JDC_MIDLE//JavaDoc備考途中
*/                              ND_JDC_END JavaDoc備考終了
public クラス プログラム型                              ND_DEF_BEGIN//定義開始
/**                              ND_JDC_BEGIN//JavaDoc備考開始
* Main                              ND_JDC_MIDLE//JavaDoc備考途中
* @param 引数 args                              ND_JDC_PARAM//JavaDoc備考変数
*/                              ND_JDC_END JavaDoc備考終了
static メイン(string[] 引数)                              ND_DEF_BEGIN//定義開始
コンソール.一行表示する("Hellow World!")                              ND_EXE_BEGIN//実行開始
3
                              ND_DEF_END//定義終了
                              using System                              ND_QAT_BEGIN//引用開始
public static class コンソール Console                              ND_QAD_BEGIN//引用定義開始
public static 一行表示する(string? value)                              ND_QAD_BEGIN//引用定義開始
WriteLine (string? value)                              ND_QAD_MIDLE//引用定義中
2
                              ND_QAD_END//引用定義終了

************nameDictionary出力************
Key:名前空間 Value:namespace
Key:クラス Value:class
Key:インポートする Value:using
Key:プログラム型 Value:Program
Key:引数 Value:args
Key:メイン Value:Main
Key:コンソール Value:Console
Key:一行表示する Value:WriteLine

************トランスコンパイル後ソースコード出力************
using System;
namespace HelloWorld
{

    /// <summary>プログラム型</summary>
    public class Program
    {

        /// <summary>メイン</summary>
        /// <param name=args>引数</param>
        static void Main(string[] args)
        {

            Console.WriteLine("Hello World!");
        }

    }
}
```

#### Mind
```mind:main
************ソースコードノード判定出力************
                              メイン                              ND_DEF_BEGIN//定義開始
コンソールへ一行表示する("Hellow World!")                              ND_EXE_BEGIN//実行開始
                              ND_DEF_END//定義終了
コンソールへ一行表示する(string value)                              ND_QAD_BEGIN//引用定義開始
一行表示する(string value)                              ND_QAD_MIDLE//引用定義中
                              ND_QAD_END//引用定義終了
                              
************nameDictionary出力************
Key:コンソールへ一行表示する Value:一行表示する

************トランスコンパイル後ソースコード出力************
        メインとは
            「Hello World!」を 一行表示する。
```

# 実行結果の実行結果
[オンラインコンパイラCompiler Explorer](https://qiita.com/mylifewithviolin/items/bb2705e16347bbbefbb2)でソースエディタにサンプルソースコードイメージを貼り付けます。
エクゼキュータペインが更新されて下記の状態となりました。

#### Java
```:
Executor jdk 20.0.0 (Java, Editor #1)

jdk 20.0.0
Could not execute the program
Compiler returned: 1
Compiler stderr
<source>:6: error: class Program is public, should be declared in a file named Program.java
    public class Program
           ^
1 error
```
JavaでオンラインコンパイラCompiler Explorerの場合、そのままではソースコードを実行できなかったため、別途コマンドライン環境で実行します。

出力ソースコードをProgram.javaというファイル名をテキストエディタで開いてコピー貼り付けして、HelloworldサブフォルダにUTF-8で保存し、コマンドラインからコンパイルして実行しました。
```:
C:\developments\java20>javac Helloworld/Program.java

C:\developments\java20>java -cp . HelloWorld/Program
Hello World!

C:\developments\java20>
```

#### C#
C#は前回状態よりオンラインコンパイラCompiler Explorerで「Hello World!」出力されています。
```:
Executor .NET 7.0.105 (C#, Editor #1)
.NET 7.0.105
Program returned: 0
Program stdout
Hello World!
```

#### Mind
mindは出力ソースコードをtest.srcというファイル名をテキストエディタで開いてコピー貼り付けしてSJISで保存し、コマンドラインからコンパイルして実行しました。
```:
C:\pmind\sample>mind test file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\pmind\bin\mindex.exe --> test.exe

C:\pmind\sample>test
Hello World!

C:\pmind\sample>
```


# ソースコード
GitHub 鋭意準備中

# おわりに
超おもちゃながら、今回は無事に実行成功にこぎつけました。インポート文の仕様は前回実行の後、比較検討記事をあげて、各言語に対して■インポートする　で揃えてimport/using/import/Inportsなどにトランスコンパイルすることとしております。今回はその仕様が反映されています。


## 補足 本試作の設計言語
・ロジック仕様記述言語 Re:Mind
[Re:Mindで内部設計する（基本構成）](https://qiita.com/mylifewithviolin/items/0ecfbfbaafcce6645d82)
[Re:Mindで内部設計する（ターゲット言語C#）](https://qiita.com/mylifewithviolin/items/a0754013787a513828a4)
[Re:Mindで内部設計する（ターゲット言語Java）](https://qiita.com/mylifewithviolin/items/abf5b4fa3b12b285935f)
[Re:Mindで内部設計する（ターゲット言語Mind）](https://qiita.com/mylifewithviolin/items/81d872c32358276cd88d)

日本語ロジック仕様記述言語 Re:Mind（リマインド）は[オープンな設計言語仕様](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)で、どなたでもこの記法を使いロジックを記述することができます。


**2026/09/09更新**
2026/08/11にプログラミング言語名をRe:Mind（リマインド）から Aoi （あおい）に変更しました。Re:Mindは開発プロジェクトコード名という位置づけといたします。基本的にはトランスコンパイラ言語として実装されますが、中間コードコンパイラとしての実装をさまたげるものでもないので「日本語プログラミング言語」とも呼称するとします。
