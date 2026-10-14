# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の検証フェーズのステップ９になります。MVPのコード生成器はC#、VB.NET、Javaの３言語を想定していますが、ついにJavaの検証に進行します。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態でGitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro+版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

# 本記事のステップ
## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。下記の実装タスクから構成され実行完了しました。
　Phase 1. Lexer タスク
　Phase 2. Parser タスク
　Phase 3. AST タスク
　Phase 4. 意味解析と名前解決 タスク
　Phase 5. 中間表現（IR） タスク
　Phase 6. コード生成パイプライン タスク
　Phase 7. コア構文のトランスコンパイル実装
　Phase 8. Program.cs からの実行フロー統合の実装

### Phase 9: 検証と品質改善
前回、前々回のステップで定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つのVB.NETソースコードへのトランスコンパイル検証対応は完了しました。今回はJavaの生成ソースコードサンプルの対応に進行します。単純なサンプルで開始します。

## 簡単なサンプルと期待コード（答え）でJavaコード生成に対応する。
### あおいのソースコードサンプル
ターゲット言語がJavaの場合のあおいのソースコードサンプルでは、現状カバーする範囲の構文ではインポート文のみ異なる形となります。

インポート文がJavaのパッケージを指定する形となります。インポート文は将来的にはあおいのターゲット言語別ライブラリリソースとなります。

またクラス名とファイル名が同一という制約もありますので、生成ファイル名はフォルダ別に出力します。

**簡単なサンプル1**
**sourceFiles\helloworldjv.aoi**
<details open><summary>sourceFiles\helloworldjv.aoi</summary>

```aoi:sourceFiles\helloworldjv.aoi
▽名前空間 HelloWorld
    /**
    * Program
    */
    ▽public クラス プログラム型
        /**
        * main
        * @param 引数 args
        */
        ▽public static void メイン(string[] 引数)
            □コンソール.一行表示する("Hello World!")
        △
    △
△

■インポートする java.lang.System
▼public class コンソール PrintStream System.out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲
```
</details>

**sourceFiles\helloworldcs.aoi**
C#/VB.NET向けは[こちらの記事](
https://qiita.com/mylifewithviolin/items/41cdd6c2be00cb71792d)を参照してください。
「■インポートする」の違いに注目してください。

**簡単なサンプル2**
**sourceFiles\variablejv.aoi**

<details open><summary>sourceFiles\variablejv.aoi</summary>

```aoi:sourceFiles\variablejv.aoi
▽名前空間 Helloworld
    /**
    * Program
    */
    ▽public クラス プログラム型
    
        /** 
        * aisatsu1 
        */
        ・private static string 挨拶１


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

■インポートする java.lang.System
▼public class コンソール PrintStream System.out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲
```
</details>

**sourceFiles\variablecs.aoi**
C#/VB.NET向けは[こちらの記事](
https://qiita.com/mylifewithviolin/items/0c194fad2142bafaef79)を参照してください。

## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでその点でのMicrosoft Copilotとのやりとりはなかったです。ただし、あおいプロジェクトでJavaエクステンションが無効化されていなかったので、GitHub CopilotのJavacコンパイルやコンパイルクラスの起動に干渉している状況の確認や無効化の対処で方法ではやりとりしていました。
## GitHub Copilot
### プロンプト１
>sourceFiles\helloworldjv.aoi
sourceFiles\variablejv.aoi
は
sourceFiles\helloworldcs.aoi
sourceFiles\variablecs.aoi
を
Javaよりの表現で書いたソースです。
ターゲット言語によってあおい（Re:Mind）側の書き方をあまり変えたくないのですが
（今後クラスの概念がない対象言語を対応していくような場合は除く、
例えばクラスの概念のない対象言語であおい（Re:Mind）側でいまのように書いたら
エラーとするなどが今後の課題としてはありますが）
とりあえず
sourceFiles\helloworldjv.aoi
sourceFiles\variablejv.aoi
の書き方で
Javaのライブラリパスを表現するよい方法について考察し提案を
docs\C#的（.NET言語的）的ソースの書き方を維持してJavaのライブラリパスを指定する方法案.md
に出力してください。
#### 生成レスポンス１
**C#的（.NET言語的）的ソースの書き方を維持してJavaのライブラリパスを指定する方法案.md**
が生成されました。

ここで示された「長期案」とは

>本体ソースとライブラリAliasを分離し、ターゲット言語ごとの標準ライブラリ定義を再利用可能なライブラリパッケージとして管理する。

「第一候補: Re:Mind側のライブラリ別名を共通記法で表現する」（下記プロンプト３で引用）
とは
>Re:Mind側では、C#/.NETとJavaでライブラリパスの書き方を変えず、`■インポートする`とAliasClass/AliasMemberでターゲット名を定義する。

という内容でした。あまりに自分の構想どおりのこと（かなずしも仕様に文書化されていない範囲）を提案してきたので少し感動しました。

### プロンプト２
>docs\C#的（.NET言語的）的ソースの書き方を維持してJavaのライブラリパスを指定する方法案.md
の長期案ですが
もともと現状のサンプルはC#のUsing句を解決するためのインポートするは
大量の使用するライブラリの仕様情報を書いておく必要があるため
外部ファイルとしてかつ、このソースは人間が書くのではなくAIなどで機械的に
書いておき、人間ユーザまたはAIも含むはこれを個別に書くことは想定していません。
（参照仕様には書いてませんが、トランスコンパイラとして対象言語の大量のライブラリを
日本語環境で利用可能とすることが言語の企画目的です。）
というわけで、長期的にはこうするとして今回はソースコードをjavaでわけます。
ただし、パッケージという表現は名前空間に統一します。

>docs\C#的（.NET言語的）的ソースの書き方を維持してJavaのライブラリパスを指定する方法案.md
第一候補: Re:Mind側のライブラリ別名を共通記法で表現する
>
>sourceFiles\helloworldjv.aoi
sourceFiles\variablejv.aoi
をそのように書き換えましたので、まずはこの２つを変換する
docs\基礎２サンプルをJavaでトランスコンパイルできるようにするための修正フロー.md
に出力してください。
続けてそれを実行開始して
docs\基礎２サンプルをJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
に出力してください。
#### 生成レスポンス２
docs\基礎２サンプルをJavaでトランスコンパイルできるようにするための修正フロー.md
docs\基礎２サンプルをJavaでトランスコンパイルできるようにするための修正フロー完了レポート.md
が生成されます。
途中Javaエクステンションが介入してGitHub CopilotのJavacコンパイルやコンパイルクラスの起動に干渉してしまいましたが、Javaエクステンションを当プロジェクトでは無効化することで難を逃れました。

### トランスコンパイル後のJavaソースコード
コンパイル検証済コードとなります。
**transcompiledFiles\java\helloworld\Program.java**

```java:transcompiledFiles\java\helloworld\Program.java
package helloworld;

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
    public static void main(String[] args)
    {
        System.out.println("Hello World!");
    }
    
}
```
**transcompiledFiles\java\variable\Program.java**

```java:transcompiledFiles\java\variable\Program.java
package helloworld;

import java.lang.System;

/**
 * プログラム型
 */
public class Program
{
    private static String aisatsu1;
    /**
     * メイン
     * @param args 引数
     */
    public static void main(String[] args)
    {
        aisatsu1 = "Hello World one!";
        System.out.println(aisatsu1);
    }
    
    /**
     * コンソール表示する
     * @param dispStr 引数2
     */
    public static void consoleOut(String dispStr)
    {
        System.out.println(dispStr);
    }
    
}
```

## 本ステップの評価
簡単なサンプルのJavaの生成ソースコード対応が完了しました。あおいのXMLコメントはJavaDoc形式なので、あおいの英語コメントがJava側本名となります。より複雑なソースコードとして定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つがありますが、次回はバブルソートを変換します。


# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
