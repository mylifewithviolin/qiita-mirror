# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。前回シリーズ[^1]で実装完了した「最小セット（MVP）」の検証フェーズに入りました。本記事でそのステップ２になります。

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
前回は当初のサンプルコード（バブルソート相当）が完走しませんでしたので、今回はもう少し簡単なサンプルと期待コード（答え）も用意しそれが動くところまで検証->修正->再検証->再修正のサイクルをまわしてみます。

## 簡単なサンプルと期待コード（答え）を用意する。
**簡単なサンプル**
```aoi:sourceFiles\helloworldcs.aoi
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
            □コンソール.一行表示する("Hello World!")
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
**期待コード（答え）**
```cs:transcompiledFiles\helloworld.cs_
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
今回は分岐◇やループ○のない単純な実行文からなるターゲットサンプルです。「■インポートする」があおい的には重要構文で、これによりターゲット言語のライブラリを引用できるようにするものです。

## Microsoft Copilotとの事前準備
今回はMicrosoft Copilotとの対話は特にありません。
## GitHub Copilot
### プロンプト１
>sourceFiles\helloworldcs.aoiは現在のstring ReMindSourceCodeと
等価なソースコードファイルです。
ターゲット言語はC#
transcompiledFiles\helloworld.cs_
がトランスコンパイル後の期待結果です。
この期待結果となるための修正検証プランを作成してフォルダのdocsに出力してください。

「等価」というのはちょっと語弊がありました。元はバブルソートのロジックを記述していますのでだいぶ複雑でしたが、かなり単純にしたということを書き忘れました。

#### 生成レスポンス１
>helloworldcs.aoi と helloworld.cs_ を比較し、修正・検証計画を作成しました。

helloworld_csharp_transcompile_validation_plan.md

>主な内容:
>
>入力ソースと期待出力の差分
Lexer → Parser → AST → SemanticResolver → IR → C#生成の不足箇所
IRBuilder.Build() と CSharpCodeGenerator.Generate(ProgramIR) の実装計画
Console.WriteLine("Hello World!"); の名前解決
期待ファイルとの差分比較方法
生成 C# のコンパイル・実行検証
回帰テストと完了条件

生成された
helloworld_csharp_transcompile_validation_plan.mdの内容は
かなり緻密でいけそうな感じでした。
```text
## 8. 実装時の注意
- 今回の目的は HelloWorld の最小 E2E を通すこと。BubbleSort の全構文を同時に完成させない。
```
こういうところも気をつかっている感じがして好感が持てました。

### プロンプト２
>docs\helloworld_csharp_transcompile_validation_plan.mdを実行して
docs\helloworld_csharp_transcompile_validation_plan_executed.mdに
完了レポートを報告してください。

#### 生成レスポンス２
>計画を実行し、完了レポートを作成しました。

helloworld_csharp_transcompile_validation_plan_executed.md

>実施内容:
>
>HelloWorld 入力ファイルの優先読み込み
Parser の最小宣言・呼び出し解析
IRBuilder の最小 ProgramIR 変換
C# IR CodeGenerator の最小生成
ビルド成功を確認
ただし、端末連携上、実行時の標準出力と生成ファイルを取得できず、期待ファイルとの完全一致・生成 C# の実行確認は未完了です。Javadoc コメントや整形情報も IR 未保持のため、完全一致には追加対応が必要です。

## 実行中の様子
数回修正とリビルドを繰り返しているようでした。まさにこの開発フローの自動化が期待していた状況です。
### 実行結果
下記のファイルが生成されました。突合一致確認はできていないと言っていますが、内容的にはできているようです。
```cs:transcompiledFiles\helloworld.generated.cs
using System;

namespace HelloWorld
{
    public class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
        
    }
}
```

## VSCodeでデバッグ実行してみる
VSCodeでデバッグ実行もしてみます。
無事にCSのソースコードがデバッグコンソールに出力されました。
```
using System;

namespace HelloWorld
{
    public class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
        
    }
}

プログラム '[11368] astsample.dll' がコード 0 (0x0) で終了しました。
```
## 本ステップの評価
結果の状態としては初めてコード生成に到達しました。これは小さな一歩ですが日本語プログラミング言語あおいのAIドリブン開発上は大きなメルクマールとなりました。引き続き検証とバグ修正を行います。

また、次回も別のサンプルと期待コード（答え）を用意し動くところまで検証->修正->再検証->再修正のサイクルをまわしていきます。

# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。次回も検証とバグ修正の続きとなります。

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
