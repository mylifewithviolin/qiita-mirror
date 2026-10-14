# はじめに
2023年の1月下旬よりQiita様へ参加させていただき、[自作言語 Re:Mind（リマインド）の企画趣旨をQiita内の記事](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)でご説明させていただいております。まだ実装がなにもないので、そろそろ試作に着手しようかと考えておりました。
本記事はその試作品の初版の実装情報で、ターゲット言語をJava,C#,Mindとしています。この状態ははっきり言っておもちゃにすぎません。おもちゃ状態をいつごろ脱せるかはわかりませんが、[仕様](https://qiita.com/mylifewithviolin/items/9a6abbab62c0f5e27d4b)としてはめちゃめちゃおもちゃというわけではないのでインクリメンタル開発を続行する所存でございます。

## この記事内容の作業目的
本試作範囲は[策定仕様](https://qiita.com/mylifewithviolin/items/9a6abbab62c0f5e27d4b)のごくごく一部です。ターゲット言語は一部のみ対応、言語の対応ソース構文も超限定的です。


日本語トランスコンパイラ言語 Re:Mind（リマインド）は[オープンな実装言語仕様](https://qiita.com/mylifewithviolin/items/9a6abbab62c0f5e27d4b)で、どなたでもコンパイラ・トランスコンパイラを実装することができます

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
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
"Hellow World!"がコンソール出力されるソースコードを入力して（インライン・リテラルコーディング）、ターゲット言語のソースコードを（双方だらだらと）コンソール出力する。（どれを出力するかは起動パラメータにする。）"Hello World!"じゃないの？というつっこみは無しで。C#で実装された試作品の名前空間はHelloWordl。

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
        static void main(String[] args)
        {
           out.println("Hellow World!");
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
               Console.WriteLine("Hellow World!");
            }
        }
    }
```

#### Mind
```mind:main.src
    メインとは
        「Hellow World!」を　一行表示する。

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
        ▽static メイン(string[] 引数)
            □コンソール.一行表示する(""Hellow World!"")
        △
    △

■import java.lang.System
▼public class コンソール PrintStream out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲";
```
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
        ▽static メイン(string[] 引数)
            □コンソール.一行表示する(""Hellow World!"")
        △
    △
△

■using System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲";
```

#### Mind

```cs:Re:Mind
        const String SOURCE_MIND=@"
        ▽メイン
            □コンソールへ一行表示する(""Hellow World!"")
        △
        ▼コンソールへ一行表示する(string value)
            ■一行表示する(string value)
        ▲
        ";
```

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
Key:プログラム型 Value:Program
Key:引数 Value:args
Key:メイン Value:Main
Key:コンソール Value:out
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
        static Main(string[] args)
        {

            out.println("Hellow World!");
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
        static Main(string[] args)
        {

            Console.WriteLine("Hellow World!");
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
            「Hellow World!」を 一行表示する。
```

# 実行結果の実行結果
[オンラインコンパイラCompiler](https://qiita.com/mylifewithviolin/items/bb2705e16347bbbefbb2)でソースエディタにサンプルソースコードイメージを貼り付けます。
エクゼキュータペインが更新されて下記の状態となりました。

#### Java
main関数に戻り値の指定がないと怒られました。これは内部設計ミスでvoidの出力値を返す記述が漏れていましたね。
```:
Executor jdk 20.0.0 (Java, Editor #1)

jdk 20.0.0
Compiler options...
Could not execute the program
Compiler returned: 1
Compiler stderr
<source>:13: error: invalid method declaration; return type required
        static Main(string[] args)
               ^
1 error
```
#### C#
main関数に戻り値の指定がないと怒られました。これは内部設計ミスでvoidの出力値を返す記述が漏れていました。
```:
Executor .NET 7.0.105 (C#, Editor #1)

.NET 7.0.105
Compiler options...
Could not execute the program
Compiler returned: 1
Compiler stdout
<source>(11,16): error CS1520: Method must have a return type [/app/CompilerExplorer.csproj]
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
Hellow World!

C:\pmind\sample>
```


# ソースコード
GitHub 鋭意準備中

# おわりに
超おもちゃながら、内部設計ミスでjavaとC#はまさかのvoid出力漏れという結果でした。Mindは無事に正常実行されたのが不幸中の幸いといいましょうか。Re:Mindの関数仕様としては戻り値無のvoidは割愛可としていたことが影響しています。
とりあえず、同じ内容で再度記事を更新したりするのはきついので、次の対応仕様を進める際に本件設計バグを訂正してまいります。その最に、本件対応仕様のロジック仕様記事についても追っかけで訂正します。

ほんとうは無事に実行成功だった場合、インポート文の仕様がターゲット言語別にはまだまとまっていないことに言及して絞める予定でしたが、まさかの実行エラーでした。（実行する前に気づけよというつっこみは無しということで(汗)）


## 補足 本試作の設計言語
・ロジック仕様記述言語 Re:Mind
[Re:Mindで内部設計する（基本構成）](https://qiita.com/mylifewithviolin/items/0ecfbfbaafcce6645d82)
[Re:Mindで内部設計する（ターゲット言語C#）](https://qiita.com/mylifewithviolin/items/a0754013787a513828a4)
[Re:Mindで内部設計する（ターゲット言語Java）](https://qiita.com/mylifewithviolin/items/abf5b4fa3b12b285935f)
[Re:Mindで内部設計する（ターゲット言語Mind）](https://qiita.com/mylifewithviolin/items/81d872c32358276cd88d)

日本語ロジック仕様記述言語 Re:Mind（リマインド）は[オープンな設計言語仕様](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)で、どなたでもこの記法を使いロジックを記述することができます。

**2026/09/09更新**
2026/08/11にプログラミング言語名をRe:Mind（リマインド）から Aoi （あおい）に変更しました。Re:Mindは開発プロジェクトコード名という位置づけといたします。基本的にはトランスコンパイラ言語として実装されますが、中間コードコンパイラとしての実装をさまたげるものでもないので「日本語プログラミング言語」とも呼称するとします。
