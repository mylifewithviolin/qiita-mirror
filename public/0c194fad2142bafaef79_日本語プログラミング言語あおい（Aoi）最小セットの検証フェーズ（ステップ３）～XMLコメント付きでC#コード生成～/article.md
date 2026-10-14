# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。前回シリーズ[^1]で実装完了した「最小セット（MVP）」の検証フェーズに入りました。本記事でそのステップ３になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

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
前回はかなり簡単なサンプルと期待コード（答え）も用意しそれが動くところまで検証->修正->再検証->再修正のサイクルをまわしてみました。

残課題としてはjavadoc仕様のあおい上のコメントをC#のコメント形式に変換するところが未実装でした。その点はそもそも最小セット（MVP）では想定しておりませんでしたが、以前の手書き実装の結果を期待コード（答え）としていたため、C#のコメント形式がそちらにあったためAIが課題認識しました。

## 簡単なサンプルと期待コード（答え）を追加しXMLコメントに対応する。
**簡単なサンプル1**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/41cdd6c2be00cb71792d)を参照してください。
**簡単なサンプル2**
```aoi:sourceFiles\variablecs.aoi
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
**期待コード（答え）2**
```cs:transcompiledFiles\variable.cs_
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
今回はクラス内変数の定義と、ローカルメンバ関数を定義してMainから引用するというサンプルパターンです。

## Microsoft Copilotとの事前準備
Microsoft Copilotとの対話はなかったわけではないのですが、長くなるので今回は割愛しています。
## GitHub Copilot
### プロンプト１
>helloworld_csharp_transcompile_validation_plan.mdを参考に
sourceFiles\helloworldcs.aoi
sourceFiles\variablecs.aoi
が
transcompiledFiles\helloworld.cs_
transcompiledFiles\variable.cs_
の
期待結果となるための修正検証プランを作成してフォルダのdocsに出力してください。
helloworldandvariable_csharp_transcompile_validation_plan.md

#### 生成レスポンス１
割愛します。docs\helloworldandvariable_csharp_transcompile_validation_plan.mdを作成して概要を教えてくれています。
### プロンプト２
>docs\helloworldandvariable_csharp_transcompile_validation_plan.mdを実行して
完了レポート
docs\helloworldandvariable_csharp_transcompile_validation_plan_executed.mdを
出力してください。
#### 生成レスポンス２
割愛します。planを実行し、docs\helloworldandvariable_csharp_transcompile_validation_executed_plan.mdを作成して概要を教えてくれています。
ここでXMLコメントの扱いが残課題として再提示されます。
### プロンプト３
docs\xml_comment_transcompile_plan_executed.mdの
7. 残課題
1.期待結果に合わせ、コメント概要に NameJa を使うか、Javadoc の Summary を使うかを仕様として確定する。
は
コメント概要に NameJa を使う
として残課題を実行するプランを作成してフォルダのdocsに出力してください。
docs\xml_comment_transcompile_remaining_tasks_plan.md
#### 生成レスポンス３
残課題が実行され完了レポートが生成されます。

#### docs\xml_comment_transcompile_remaining tasks plan_executed.md
```text
残る差分
完全な期待ファイル一致はまだ未達である。

空行とインデントが期待ファイルと異なる。
期待ファイルの <param name=args> に対し、生成結果は正しい XML 形式の <param name="args"> である。
Variable の代入文で空白の有無が異なる。
CompareGeneratedOutput() は空実装のままで、比較結果ファイルは判定結果を記録していない。
```
基本的に問題なしです。インデントの差異は許容です。XMLコメントに対応できたのは、人間が読むソースコードをトランスコンパイルすることが主眼なのでまずは対応第１歩が進んでよかったです。

### 実行結果
下記のC#ソースコードがトランスコンパイルされました。
```cs:transcompiledFiles\helloworld.generated.cs_
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
```cs:transcompiledFiles\variable.generated.cs_
using System;

namespace HelloWorld
{
    /// <summary>プログラム型</summary>
    public class Program
    {
        /// <summary>挨拶１</summary>
        private static string? aisatsu1;
        
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static void Main(string[] args)
        {
            aisatsu1 = "Hello World one!";
            ConsoleOut(aisatsu1);
        }
        
        /// <summary>コンソール表示する</summary>
        /// <param name="dispStr">引数2</param>
        static void ConsoleOut(string args2)
        {
            Console.WriteLine(args2);
        }
        
    }
}

```

## 本ステップの評価
結果の状態としてはXMLコメント付きでコード生成に到達しました。引き続き検証とバグ修正を行います。

また、次回はバブルソートのサンプルが動くところまで検証->修正->再検証->再修正のサイクルをまわしていきます。バブルソートのサンプルのソースコードの要件は一部「最小セット（MVP）」の範囲を超える恐れがありますが（小さなプログラムが通せるとはどの程度かによる）、インクリメンタルに「最小セット（MVP）」を拡張改修していく事例になるかもしれません。

# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
記事リストです。（ステップ降順）
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[ステップ１１ コア構文のトランスコンパイルの最小実装](
https://qiita.com/mylifewithviolin/items/d66a707c8ae7419f001c)
[ステップ１０ コード生成パイプラインの最小実装](
https://qiita.com/mylifewithviolin/items/c02b35b762aa11b42540)
[ステップ９ 中間表現（IR）の最小実装](
https://qiita.com/mylifewithviolin/items/a787e4a85866fe52074f)
[ステップ８ 中間表現（IR）の最小実装 ひな形](
https://qiita.com/mylifewithviolin/items/b8b142c4046c6df2654b)
[ステップ７ 「意味解析と名前解決」の最小実装](https://qiita.com/mylifewithviolin/items/4c2a0811b824402ea177)
[ステップ６ 「意味解析と名前解決」か「中間表現（IR）」か](https://qiita.com/mylifewithviolin/items/13a90dec5eefaf9bd1b5)
[ステップ５ AST最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/1ce67bdee49bcdf052e6)
[ステップ４ Parser最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/c35fed8a80254eb7c1a6)
[ステップ３ Lexer最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/34a4872e17869824a3f3)
[ステップ２ PlanAgent計画細分化](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)
[ステップ１ Copilotが生成した日本語トランスコンパイラ言語 Re:Mindの原型をGitHub CopilotのPlanエージェントで再計画](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
