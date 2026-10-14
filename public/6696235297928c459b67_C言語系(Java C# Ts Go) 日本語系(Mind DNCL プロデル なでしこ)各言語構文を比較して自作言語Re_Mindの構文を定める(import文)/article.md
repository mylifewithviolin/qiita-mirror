# はじめに
Java C# Ts(TypeScrpt) GoといったC言語を由来とする新旧のプログラミング言語とMind なでしこ DNCLなどの日本語プログラミング言語の制御構文を比較して自作言語Re:Mindの構文を定めます。今回はimport文に関連する構文です。関連して名前空間の指定方法も検討します。

自作言語Re:Mindの詳しい利用シーンのイメージは[こちらへ](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)。すみません、[試作段階です。](https://qiita.com/mylifewithviolin/items/abae37afefb42ca8ef31)日本語プログラミング言語で、C言語を由来とする新旧言語へのトランスコンパイラ言語です。

## この記事内容の作業目的
今回は各言語のimport文の構文を比較検討します。関連して名前空間の指定方法も検討します。

今日のシステム開発に使われる有力言語は巨大なライブラリを保持しておりますが、利用の際には名前空間を指定したり、パッケージを指定したりして、予め利用する範囲を指定するのが一般的です。また言語によっては、利用する関数、変数単位でインポートするものもあります。
そこでRe:Mindはあらかじめタ－ゲット言語の全方位のライブラリをサポートすることはせず、一定のルールで利用可とできる構文を提供します。

プログラミング言語によっては、名前空間やimport処理をソースコードとしてはサポートしない場合がありますので、トランスパイラ言語としてはこのあたりをどうさばくかが問題となります。


## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（試作段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# Java C# Ts Goの新旧C言語系の構文イメージ
## Java
```java:Java
    package ConsoleApp;

    import java.lang.System;

    public class Program
    {
        static void main(String[] args)
        {
           out.println("Hello World!");
        }
    }

```
Javaは自身のクラスの名前空間をpackage文で、ライブラリのimport処理をimport文でサポートします。



## C#
```cs:C#
    using System;
    
    namespace ConsoleApp
    {
        class Program
        {
            static void Main(string[] args)
            {
                Console.Write("Hello World!");
            }
        }
    }
```

C#は自身のクラスの名前空間をnamespace文で、ライブラリのimport処理をusing文でサポートします。



## TypeScript
```ts:TypeScript
    import process from 'process'

    namespace ConsoleApp 
    {
        function main(args:string )
        {
           process.stdout.write("Hello World\n")
        }

    }
```

Tsは自身のクラスの名前空間をnamespace文で、ライブラリのimport処理をimport文でサポートします。


## Go
```go:Go
    package main
    
    import "fmt"

    func main() {
        fmt.Println("Hello World!")
    }

```

Goは自身のメソッドの名前空間をpackage文で、ライブラリのimport処理をimport文でサポートします。

# 英語を基調としたBASIC言語
BASIC言語は日本語ではありませんが、中かっこ「{}」を使って区切ることはなく、構文の表現も自然言語の英語に近いので、こちらの方に寄せました。

## VBA（Excel用）
```vb:VisualBasic for Application

```
VBAは名前空間とimport文をサポートしません。

## VB.NET
```vb:VB.NET
    Imports System
    
    Namespace ConsolApp
        Module Program
            Sub Main(args As String())
                Console.WriteLine("Hello World!")
            End Sub
        End Module
    End Namespace
```
VB.NETは名前空間をNamespace文で、ライブラリのimport処理をImports文とでサポートします。


# Mind DNCL の日本語プログラミング言語の構文イメージ
では、続いて日本語プログラミング言語のグループです。

## Mind
```mind:Mind
    メインとは
        「Hello World!」を　一行表示する。
```
Mindは名前空間とimport文をサポートしません。コンパイル時に指定された直下の下位ライブラリからさらに下位のライブラリへと使用可能単語を探索します。


## DNCL
```mind:DNCL
    「Hello World!」を表示する 
```
DNCLは名前空間とimport文をサポートしません。



# プロデル なでしこ 第2世代日本語プログラミング言語の構文イメージ（参考）
あまりと言いますかかなり詳しくはないのですが、参考にわたしの心の中での第2世代日本語プログラミング言語「プロデル」と「なでしこ」の構文も比較してみました。よくわかっていないので、間違っていたらごめんなさい。訂正します。「なでしこ」はV1を想定しています。
## プロデル


```mind:プロデル
    「ライブラリ.rdr」を参照する

```
プロデルはオブジェクト指向言語ではありますが名前空間は使えないらしい。プロデル専用ライブラリの参照方法は「参照する」を使用するようです。

## なでしこ
```mind:なでしこ
    !『test.nako』を取り込む
    test:A=30
    test:Aを言う
```

なでしこでは名前空間が使えるらしい。オブジェクト指向言語ではないので、グループという近い概念が存在し、それに近い概念に名前空間があるらしい。「取り込む」がimport文要素かもしれません。先頭の！になにか意味がありそう。

# 自作言語の構文イメージ
ここで自作言語の構文の開示です。Re:Mindはターゲット言語により構文が若干変化します。
## Re:Mind

### C#の場合
```mind:Re:Mind
    ▽名前空間 ConsoleApp
        /**
        * Program
        */
        ▽public クラス プログラム型
            /**
            * Main
            * @param 引数 args
            */
            ▽static メイン(string[] 引数)
               □コンソール.一行表示する("Hello World!")
            △
        △
    △

    ■インポートする System
    ▼public static class コンソール Console
        ▼public static 一行表示する(string? value)
              WriteLine (string? value)
        ▲
    ▲
```

### Javaの場合
```mind:Re:Mind
    □パッケージ consoleApp
        /**
        * Program
        */
        ▽public クラス プログラム型
            /**
            * main
            * @param 引数 args
            */
            ▽static メイン(string[] 引数)
               □コンソール.一行表示する("Hello World!")
            △
        △

    ■インポートする java.lang.System
    ▼public class コンソール PrintStream out
        ▼public static 一行表示する(string value)
              println (String value)
        ▲
    ▲
```

Re:Mindはターゲット言語が名前空間とライブラリのimport処理をサポートする場合はこれらを使ってターゲット言語のライブラリを引用し日本語名に対応付けします。

全角黒四角■に続いてインポート文を記述します。トランスコンパイラがターゲット言語のimport文に置換します。
全角下三角▼に続いてターゲット言語のターゲットクラスを宣言し、クラス名の直前に日本字のクラス名を記述します。
・通常のクラス定義と同様に全角上三角▲が定義の終了となります。
・この間に、ターゲット言語の利用対象のターゲット関数・変数を全角下三角▼と全角上三角▲挟んで宣言します。
・全角下三角▼に続いてターゲット言語の構文で関数、変数を宣言しますが、関数名・変数名は日本字を記述します。

### Mindの場合
```mind:Re:Mind
    ▽メイン
       □コンソールへ一行表示する("Hello World!")
    △

    ▼コンソールへ一行表示する(string value)
       ■一行表示する(string value)
    ▲

```
Mindの場合、現状■インポート文は指定しません。
Mind予約語の再定義記法としてはあまりにもC言語風の記法に寄ってしまっていますが、現時点ではこちらで暫定対応とします。

### TypeScriptの場合
鋭意加筆中
### Goの場合
鋭意加筆中

# おわりに


[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク

[Mind ６．サンプルプログラムのコンパイルと実行](http://www.scripts-lab.co.jp/mind/ver8/doc/operation-6-SamplePrograms.html#compile_all)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[日本語プログラミング言語なでしこ ネームスペースについて](https://www.nadesi.com/doc/reference/syntax/Z-3-namespace.htm)

[日本語プログラミング言語プロデル 言語仕様 参照する](https://docs.utopiat.net/rdr/manual/syntax/refer.htm)
