# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。前回シリーズ[^1]で実装完了した「最小セット（MVP）」の検証フェーズになります。本記事でそのステップ４になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。今回の検証改修ワークフローでフリー版のクレジットを消費しきったのでPro版にアップグレードしました。

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
前回は簡単なサンプルと期待コード（答え）を追加し、あおいのソースコードに記述されたJavaDoc形式のXMLコメントを日本語英語を交換してC＃のXMLコメントに出力するまで検証->修正->再検証->再修正のサイクルを回してみました。

今回は分岐◇とループ○のある構文サンプルとしてProgram.csが定数として保持していたバブルソートのアルゴリズムを記述したサンプルのC#コードが生成されるまで検証->修正->再検証->再修正のワークフローを回します。

## バブルソートのアルゴリズムを記述したサンプルに対応

**バブルソートのアルゴリズムを記述したサンプル**
```aoi:sourceFiles\bubblesortcs.aoi
▽名前空間 BubbleSort
    /**
    * Program
    */
    ▽public クラス プログラム型

        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            /** array */
            ・int[] 配列 = 15,13,9,6,4,1
           
            /** index */
            □バブルソートする(配列)

            〇int i=0,i<配列.Length,i++ 繰り返す
            　□コンソール表示する(配列[i])
            〇ここまで
        △
            
        /** BubbleSort
         * @param 配列 array
         */
        ▽public void バブルソートする(int[] 配列)
          /** i */
          ・int 外側 = 0
          〇外側 < 配列.Length の間は繰り返す
            /** j */
            ・int 内側 = 0
            〇内側 < 配列.Length - 外側 - 1 の間は繰り返す
              ◇配列[内側] > 配列[内側 + 1] の場合
                /** temp */
                ・int 一時 = 配列[内側]
                □配列[内側] = 配列[内側 + 1]
                □配列[内側 + 1] = 一時
              ◇ここまで
              □内側++
            〇ここまで
            □外側++
          〇ここまで
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
こちらのあおいのサンプルソースコードはあおいの言語仕様をMicrosoft Copilotが読み込んで生成したものです。
Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２１ バブルソート 実行可能形式 ターゲットJava C# VB.NET）](https://qiita.com/mylifewithviolin/items/94a8b69c9c467497e1e6)

一発でできたわけではなく、なかなかたいへんでした。
このときC#の対応ソースコードも生成していたようですが、すっかり忘れていました。今回は期待コードとの検証はなしで進めています。

## Microsoft Copilotとの事前準備
開始時のMicrosoft Copilotとの対話はなかったのですが、途中でフリー版のクレジットを消費しきったので、Pro版アップグレードの注意事項や止まったタスクの再開方法などを確認しています。
## GitHub Copilot
### プロンプト１
>Program.csのReMindSourceCodeは空列に書き換えました。（書き換え済）
代わりにその内容を
sourceFiles\bubblesortcs.aoi
に移しました。
期待ファイルは存在しませんのでいったんこのソースも読み込めるようにして
transcompiledFiles\bubblesort.generated.cs_
が生成されるところまでを実現する実行プランを作成してフォルダのdocsに出力してください。
docs\bubblesort_csharp_transcompile_plan.md
期待ファイルは存在しませんので検証の実施は不要です。こちらが目視で確認します。

#### 生成レスポンス１
詳しくは割愛しますが
docs\bubblesort_csharp_transcompile_plan.md
を生成して概要をまとめてくれました。

### プロンプト２
>docs\bubblesort_csharp_transcompile_plan.mdを実行して
完了レポート
docs\bubblesort_csharp_transcompile_plan_executed.mdを
出力してください。

#### 生成レスポンス２
詳しくは割愛しますが検証->修正->再検証->再修正のワークフローを何周かしたところでフリー版のクレジットが100％消費されてアップグレードダイアログが出てしまいました。
docs\bubblesort_csharp_transcompile_plan.mdはいったん完了していて残タスクの
docs\bubblesort_csharp_transcompile_remaining_tasks_plan.md
を実行中でした。

## Microsoft Copilot
### プロンプト
>VSCodeのチャットは下記の状態となっています。
You've reached your monthly credit limit. Upgrade to Copilot Pro or wait until your credits reset on 2026年10月1日 9:00.
GitHub Copilot Pro へのアップグレード

>どのようにすれば検証タスクを再開できますか？
検証タスクは
docs\bubblesort_csharp_transcompile_remaining_tasks_plan.md
として保存されており
完了レポート
docs\bubblesort_csharp_transcompile_remaining_tasks_plan_executed.mdを
出力するように指示していましたが、まだ出力されていません。

これはVSCodeの上記「GitHub Copilot Pro へのアップグレード」ボタンからアップグレードを完了し、GitHub Copilotからのサインアウト、サインインを行ってアップグレードを完了した後の状態からの質問です。
#### 生成レスポンス
下記のGitHub Copilotへのプロンプト３の内容を応答してもらいました。

## GitHub Copilot
### プロンプト３
>docs\bubblesort_csharp_transcompile_remaining_tasks_plan.md の続きから再開してください。
完了レポート docs\bubblesort_csharp_transcompile_remaining_tasks_plan_executed.md を出力してください。
#### 生成レスポンス３
>完了レポートを bubblesort_csharp_transcompile_remaining_tasks_plan_executed.md に出力しました。生成結果は bubblesort.generated.cs_ に更新されています。
検証: dotnet build 成功、エラー 0。既存の nullable 警告は残っています。


### 実行結果
下記のC#ソースコードがトランスコンパイルされました。
```cs:transcompiledFiles\bubblesort.generated.cs_
using System;

namespace BubbleSort
{
    /// <summary>プログラム型</summary>
    public class Program
    {
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static void Main(string[] args)
        {
            /// <summary>配列</summary>
            int[] array = new int[] { 15, 13, 9, 6, 4, 1 };
            BubbleSort(array);
            for (int i = 0; i < array.Length; i++)
            {
                ConsoleOut(array[i]);
            }
        }
        
        /// <summary>バブルソートする</summary>
        /// <param name="array">配列</param>
        static void BubbleSort(int[] array)
        {
            /// <summary>外側</summary>
            int outer = 0;
            while (outer < array.Length)
            {
                /// <summary>内側</summary>
                int inner = 0;
                while (inner < array.Length - outer - 1)
                {
                    if (array[inner] > array[inner + 1])
                    {
                        /// <summary>一時</summary>
                        int temp = array[inner];
                        array[inner] = array[inner + 1];
                        array[inner + 1] = temp;
                    }
                    inner++;
                }
                outer++;
            }
        }
        
        /// <summary>コンソール表示する</summary>
        /// <param name="dispStr">引数2</param>
        static void ConsoleOut(string dispStr)
        {
            Console.WriteLine(dispStr);
        }
        
    }
}
```

## 本ステップの評価
ついにバブルソートのアルゴリズムを記述したサンプルでコード生成に到達しました。定番アルゴリズムの線形探索法、二分探索法、バブルソートのあおい（Re:MInd）ソースコードとC#、Java、VB.NETのソースコードがありますので、漸次、他のアルゴリズムコード、他言語への展開を進めていきます。


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
