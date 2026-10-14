# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではトランスコンパイルの実行フロー統合を実装します。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができて結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の途中ですが、今回の「Program.csからの実行フロー統合」の最小版実装が実装フェーズの最後です。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前々回記事以前で完了
**Phase 2. Parser タスク**
前々回記事以前で完了
**Phase 3. AST タスク**
前々回記事以前で完了
**Phase 4. 意味解析と名前解決 タスク**
前々回記事以前で完了
**Phase 5. 中間表現（IR） タスク**
前々回記事以前で完了
**Phase 6. コード生成パイプライン タスク**
前々回記事で完了
**Phase 7. コア構文のトランスコンパイル実装**
前回記事で完了
### Phase 8. Program.cs からの実行フロー統合の実装
1. Program.cs をオーケストレータとして再構成する。
2. 実行フローは次の順にする。
   - ReMindSourceCode を読み込む
   - Lexer でトークン化する
   - Parser で AST を生成する
   - SemanticResolver で名前解決・型解決を行う
   - IR へ変換する
   - 指定ターゲット言語の CodeGenerator でコードを生成する
   - 生成コードを標準出力またはファイルに書き出す
3. 既存の JSON 直列化・デシリアライズはデバッグ用途として残しつつ、本番フローでは不要なら段階的に外す。


## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 7: コア構文のトランスコンパイル実装は完了したようです。
Phase 8: Program.cs からの実行フロー統合のMVPタスクの最小プロンプトを作成してください
#### 生成レスポンス１
>Phase 7 まで完全に完了したので、
いよいよ Phase 8：Program.cs の実行フロー統合（MVP） に進む段階ですね。
ここは Re:Mind コンパイラの「本番パイプライン」を確立する最重要フェーズで、Program.csを正式なオーケストレーターとして再構成します。
>
>以下に、Phase 8 の MVPタスクを正しく進めるための CodeAgent 用最小プロンプトをまとめます。

>Program.cs を Re:Mind コンパイラのオーケストレーターとして再構成するため、
以下の実行フローを順番に実装する差分を追加してください。
>
>【実行フロー】
>1. ReMindSourceCode を読み込む（既存の const string を使用）
>2. Lexer でトークン化する
>3. Parser で AST を生成する
>4. SemanticResolver で名前解決・型解決を行う
>5. IRBuilder で AST → IR に変換する
>6. 指定ターゲット言語の CodeGenerator でコードを生成する
>7. 生成コードを標準出力に書き出す（必要ならファイル出力の枠だけ追加）
>
>【制約】
>- 既存コードは保持し、必要な部分だけ差分として修正する
>- 推論して新機能を追加しない
>- JSON 直列化・デシリアライズはデバッグ用途として残すが、本番フローでは呼び出さないようにする（コメントアウトまたは条件分岐）
>- ターゲット言語は C# をデフォルトとし、切り替えの枠だけ追加する
>
>【必要な最小構造】
>- var lexer = new Lexer(ReMindSourceCode);
>- var tokens = lexer.Tokenize();
>- var parser = new Parser(tokens);
>- var ast = parser.ParseCompilationUnit();
>- var resolver = new SemanticResolver(ast);
>- resolver.Resolve();
>- var irBuilder = new IRBuilder();
>- var programIR = irBuilder.Build(ast);
>- var generator = new CSharpCodeGenerator();
>- string output = generator.Generate(programIR);
>- Console.WriteLine(output);
>
>以上の条件で、Program.cs の実行フローを統合するための差分修正だけを生成してください。


## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 8タスクの実行プロンプトを実行した結果、下記のソースコードが生成されました。

```cs:Program.cs
using System;
using ReMindAst;
using ReMindBackend;
using ReMindParser;

class Program
{
    const string ReMindSourceCode = @"
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
";
static void Main(string[] args)
{
  var projectRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", ".."));
  var sourceFilePath = Path.Combine(projectRoot, "sourceFiles", "helloworldcs.aoi");
  var source = File.Exists(sourceFilePath)
      ? File.ReadAllText(sourceFilePath)
      : ReMindSourceCode;

  // 1. 字句解析
  var lexer = new Lexer(source);
    var tokens = lexer.Tokenize();

  // 2. 構文解析
    var parser = new Parser(tokens);
    var ast = parser.ParseCompilationUnit();

  // 3. 意味解析
    var resolver = new SemanticResolver(ast);
    resolver.Resolve();

  // 4. 中間表現の構築
    var irBuilder = new IRBuilder();
  var programIR = irBuilder.Build(ast);

  // 5. コード生成（既定ターゲット: C#）
    var generator = new CSharpCodeGenerator();
  string output = generator.Generate(programIR);

  // 6. 標準出力
  Console.WriteLine(output);
  File.WriteAllText(Path.Combine(projectRoot, "transcompiledFiles", "helloworld.generated.cs"), output);
}

}
```

## 本ステップの評価
ついに「最小セット（MVP）」の実装フェーズが完了しました。サンプルソースに対してトランスコンパイルが実行できるかどうかは検証フェーズに移行します。

# おわりに
以上です。次回はPhase 9: 検証と品質改善となります。「最小セット（MVP）」の最初の完成条件となりました。


[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
「Re:Mindをいじりたおす」の記事リストです。（ステップ降順）
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[ステップ２５ ターゲット言語C#へのASTからの生成処理](https://qiita.com/mylifewithviolin/items/13d78530f2b7d8895502)
[ステップ２４ ASTを生成するサンプル実装をC#で生成](https://qiita.com/mylifewithviolin/items/e9589fc28b077ab46fa5)
[ステップ２３ マッピングルール生成](https://qiita.com/mylifewithviolin/items/f446a20ee2f6a71b65c4)
[ステップ２２ AST（抽象構文木）風の構造化表示](https://qiita.com/mylifewithviolin/items/9079f80873875fbedd44)
[ステップ２１ バブルソート 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/94a8b69c9c467497e1e6)
[ステップ２０ 二分探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/2902026b161c10bfb6a3)
[ステップ１９ 線形探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/5d2466574f9d6fbbaa59)
[ステップ１８ バブルソート １案件づつやりなおし](
https://qiita.com/mylifewithviolin/items/d1e346f83d98381c3a9e)
[ステップ１７ 二分探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/baeb565cf8378106b5c2)
[ステップ１６ 線形探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/b503e16aacbdba6c59c4)
[ステップ１５ ３つの定番アルゴリズムソースの忘却原因調査](https://qiita.com/mylifewithviolin/items/2859b860bc96a5887f83)
[ステップ１４ バブルソートソースの忘却発生再確認](https://qiita.com/mylifewithviolin/items/4e0761c28d91ff66a507)
[ステップ１３ 二分探索法ソースの忘却発生](https://qiita.com/mylifewithviolin/items/11d9f898474eb895c049)
[ステップ１２ 線形探索法の６言語変換](https://qiita.com/mylifewithviolin/items/bff13bbeb71163fcf2d7)
[ステップ１１ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/2fb2909efbbfe9ee20f9)
[ステップ１０ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/3c5467b0b6b59e6d8c01)
[ステップ９ バージョン情報付きで３定番アルゴリズムソースの生成](
https://qiita.com/mylifewithviolin/items/55fdb18e72bac7e99c1d)
[ステップ８ バージョニングが可能か確認](
https://qiita.com/mylifewithviolin/items/fbc80e45d927000af85a)
[ステップ７ Re:Mindの詳しい言語仕様の学習結果をバブルソートで確認](https://qiita.com/mylifewithviolin/items/99b52bcba7a41b459d31)
[ステップ６ Re:Mindの詳しい言語仕様の学習結果を二分探索法で確認](https://qiita.com/mylifewithviolin/items/cf41523b54887e638363)
[ステップ５ Re:Mindの詳しい言語仕様の学習結果を線形探索法で確認](https://qiita.com/mylifewithviolin/items/c0e912c98375ab72f09e)
[ステップ４ Re:Mindの詳しい言語仕様の学習成果を保持するスコープを確認](https://qiita.com/mylifewithviolin/items/d17dbd2daff7486bc034)
[ステップ３ Re:Mindの詳しい言語仕様を学習できる方法を確認](https://qiita.com/mylifewithviolin/items/79c7be1247521f1a8eed)
[ステップ２ Re:Mindの言語仕様の認知度を確認](https://qiita.com/mylifewithviolin/items/edebd6042808892f50af)
[ステップ１ Re:Mindの認知度を確認](https://qiita.com/mylifewithviolin/items/68376e6375b63e361b51)
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
「Re:MindのASTパーサが動作するまで」の記事リストです。（ステップ降順）
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[ステップ１１](
https://qiita.com/mylifewithviolin/items/9c891cdcc8d2bd78f36f)
[ステップ１０ 生成済コードの伝達完了](
https://qiita.com/mylifewithviolin/items/a0b5747e40e7b545175a)
[ステップ９](
https://qiita.com/mylifewithviolin/items/f34548d50a974fb4420e)
[ステップ８](
https://qiita.com/mylifewithviolin/items/cb8f54f87329d7e62c9a)
[ステップ７](https://qiita.com/mylifewithviolin/items/1e05c80a0cad0580f073)
[ステップ６ 生成済コードの伝達開始](https://qiita.com/mylifewithviolin/items/31e8413e0789e5433705)
[ステップ５](https://qiita.com/mylifewithviolin/items/2af14676b1c267af22a2)
[ステップ４ Program.csが動作](https://qiita.com/mylifewithviolin/items/b037019608d6b5d068a7)
[ステップ３](https://qiita.com/mylifewithviolin/items/7c9568d238550b997e21)
[ステップ２](https://qiita.com/mylifewithviolin/items/076e1a792b8545fae7a6)
[ステップ１ 検証環境構築](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)
[^3]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
「Re:MindのC#コード生成が動作するまで」の記事リストです。（ステップ降順）
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
[ステップ３](https://qiita.com/mylifewithviolin/items/9f8082ae6629c9d8e35a)
[ステップ２](https://qiita.com/mylifewithviolin/items/bcb4b56688101463937c)
[ステップ１](https://qiita.com/mylifewithviolin/items/54e3c7cdd2757b694f79)
