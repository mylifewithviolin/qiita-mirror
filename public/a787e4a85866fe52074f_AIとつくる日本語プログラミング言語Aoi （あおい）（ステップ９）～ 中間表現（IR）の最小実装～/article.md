# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではIRの最小版を実装します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の途中です。今回は「中間表現（IR）」の最小版を実装します。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前々回記事以前で完了
**Phase 2. Parser タスク**
前々回記事以前で完了
**Phase 3. AST タスク**
前々回記事で完了
**Phase 4. 意味解析と名前解決**
前回記事で完了
### Phase 5. 中間表現（IR） タスク**
1. AST から後続ターゲットへ落とし込むための IR を追加する。
2. IR の設計例は以下の通り。
   - ProgramIR: namespace/import/class/method の集合
   - ClassIR: field と method の集合
   - MethodIR: parameter / local variable / body block
   - BlockIR: 文の列
   - StatementIR: assignment / call / if / while / for / return / break / continue
   - ExpressionIR: identifier / literal / binary / call / member access / array access / new
3. AST → IR の変換は「構文情報を保持したまま、バックエンド非依存の形に近づける」設計にする。
4. 生成器は IR を受け取って言語別に出力する構造に切り替える。

## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 5：中間表現（IR）の最小タスク化プロンプトを作成してください。
#### 生成レスポンス１
>🧩 タスク 2：StatementIR の派生ノードを追加
IR.cs に以下の StatementIR 派生ノードを差分として追加してください。
>
>- AssignmentIR
>- CallIR
>- IfIR
>- WhileIR
>- ReturnIR
>- BreakIR
>- ContinueIR
>
>プロパティの枠だけ追加し、ロジックは書かないでください。
既存コードは保持してください。
🧩 タスク 3：ExpressionIR の派生ノードを追加
IR.cs に以下の ExpressionIR 派生ノードを差分として追加してください。
>
>- IdentifierIR
>- LiteralIR
>- BinaryIR
>- CallExpressionIR
>- MemberAccessIR
>- ArrayAccessIR
>- NewExpressionIR
>
>プロパティの枠だけ追加し、ロジックは書かないでください。
既存コードは保持してください。
🧩 タスク 4：AST → IR 変換器（IRBuilder）の枠を作る
IRBuilder.cs を新規作成し、
AST → IR の変換を行うクラスの「枠（骨格）」だけを追加してください。
>
>必要な構造:
>- IRBuilder クラス
>- Build(CompilationUnit ast) メソッド
>- BuildStatement(Statement stmt) の枠
>- BuildExpression(Expression expr) の枠
>
>中身のロジックは書かず、枠だけ作成してください。
既存コードは保持してください。
🧩 タスク 5：AST → IR の最小変換（Identifier / Literal）
IRBuilder.cs に、
IdentifierExpression → IdentifierIR
LiteralExpression → LiteralIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 6：MemberAccess の最小変換
IRBuilder.cs に、
MemberAccessExpression → MemberAccessIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 7：Invocation の最小変換
IRBuilder.cs に、
InvocationExpression → CallExpressionIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 8：Assignment の最小変換
IRBuilder.cs に、
AssignmentStatement → AssignmentIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 9：If（◇）の最小変換
IRBuilder.cs に、
IfStatement → IfIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 10：Loop（〇） の最小変換
IRBuilder.cs に、
WhileStatement → WhileIR
への最小変換ロジックだけを差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
🧭 mylifewithviloinさんのプロジェクトに最適な実行順序（Phase 5）
1.IR の枠（骨格）を作る
2.StatementIR の派生ノード
3.ExpressionIR の派生ノード
4.IRBuilder の枠
5.Identifier / Literal の変換
6.MemberAccess の変換
7.Invocation の変換
8.Assignment の変換
9.If の変換
10.Loop の変換
この順番は AST → IR の依存関係に完全準拠しています。


## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 5の各タスクの実行プロンプトを逐次実行した結果、下記のソースコードが生成されました。IR.csのひな形は前回の記事で作成したものです。

```cs:IR.cs
using System.Collections.Generic;

namespace ReMindAst
{
    public class ProgramIR
    {
        public List<string> Namespaces { get; } = new();
        public List<string> Imports { get; } = new();
        public List<ClassIR> Classes { get; } = new();
    }

    public class ClassIR
    {
        public string Name { get; set; } = "";
        public List<string> Fields { get; } = new();
        public List<MethodIR> Methods { get; } = new();
    }

    public class MethodIR
    {
        public string Name { get; set; } = "";
        public string ReturnType { get; set; } = "void";
        public List<string> Parameters { get; } = new();
        public List<string> LocalVariables { get; } = new();
        public BlockIR Body { get; } = new();
    }

    public class BlockIR
    {
        public List<StatementIR> Statements { get; } = new();
    }

    public abstract class StatementIR
    {
    }

    public class AssignmentIR : StatementIR
    {
        public string Target { get; set; } = "";
        public ExpressionIR Value { get; set; } = null!;
    }

    public class CallIR : StatementIR
    {
        public string MethodName { get; set; } = "";
        public List<ExpressionIR> Arguments { get; } = new();
    }

    public class IfIR : StatementIR
    {
        public ExpressionIR Condition { get; set; } = null!;
        public BlockIR ThenBlock { get; } = new();
        public BlockIR? ElseBlock { get; set; }
    }

    public class WhileIR : StatementIR
    {
        public ExpressionIR Condition { get; set; } = null!;
        public BlockIR Body { get; } = new();
    }

    public class ReturnIR : StatementIR
    {
        public ExpressionIR? Value { get; set; }
    }

    public class BreakIR : StatementIR
    {
    }

    public class ContinueIR : StatementIR
    {
    }

    public abstract class ExpressionIR
    {
    }

    public class IdentifierIR : ExpressionIR
    {
        public string Name { get; set; } = "";
    }

    public class LiteralIR : ExpressionIR
    {
        public string Value { get; set; } = "";
    }

    public class BinaryIR : ExpressionIR
    {
        public ExpressionIR Left { get; set; } = null!;
        public string Operator { get; set; } = "";
        public ExpressionIR Right { get; set; } = null!;
    }

    public class CallExpressionIR : ExpressionIR
    {
        public string MethodName { get; set; } = "";
        public List<ExpressionIR> Arguments { get; } = new();
    }

    public class MemberAccessIR : ExpressionIR
    {
        public ExpressionIR Target { get; set; } = null!;
        public string MemberName { get; set; } = "";
    }

    public class ArrayAccessIR : ExpressionIR
    {
        public ExpressionIR Array { get; set; } = null!;
        public ExpressionIR Index { get; set; } = null!;
    }

    public class NewExpressionIR : ExpressionIR
    {
        public string TypeName { get; set; } = "";
        public List<ExpressionIR> Arguments { get; } = new();
    }
}
```
IRBuilder.csは前記の「タスク 4：AST → IR 変換器（IRBuilder）の枠を作る」以降のタスクで生成されました。

```cs:IRBuilder.cs
namespace ReMindAst
{
    public class IRBuilder
    {
        public ProgramIR Build(CompilationUnit ast)
        {
            throw new System.NotImplementedException();
        }

        public StatementIR BuildStatement(Statement stmt)
        {
            return stmt switch
            {
                AssignmentStatement assignment => new AssignmentIR
                {
                    Target = assignment.Left switch
                    {
                        IdentifierExpression identifier => identifier.NameEn,
                        MemberAccessExpression memberAccess => memberAccess.MemberName,
                        _ => ""
                    },
                    Value = BuildExpression(assignment.Right)
                },
                IfStatement ifStatement => BuildIfStatement(ifStatement),
                WhileStatement whileStatement => BuildWhileStatement(whileStatement),
                _ => throw new System.NotSupportedException()
            };
        }

        private IfIR BuildIfStatement(IfStatement ifStatement)
        {
            var result = new IfIR
            {
                Condition = BuildExpression(ifStatement.Condition),
                ElseBlock = new BlockIR()
            };

            foreach (var statement in ifStatement.ThenBody)
            {
                result.ThenBlock.Statements.Add(BuildStatement(statement));
            }

            foreach (var statement in ifStatement.ElseBody)
            {
                result.ElseBlock.Statements.Add(BuildStatement(statement));
            }

            return result;
        }

        private WhileIR BuildWhileStatement(WhileStatement whileStatement)
        {
            var result = new WhileIR
            {
                Condition = BuildExpression(whileStatement.Condition)
            };

            foreach (var statement in whileStatement.Body)
            {
                result.Body.Statements.Add(BuildStatement(statement));
            }

            return result;
        }

        public ExpressionIR BuildExpression(Expression expr)
        {
            return expr switch
            {
                IdentifierExpression identifier => new IdentifierIR
                {
                    Name = identifier.NameEn
                },
                LiteralExpression literal => new LiteralIR
                {
                    Value = literal.Value?.ToString() ?? ""
                },
                MemberAccessExpression memberAccess => new MemberAccessIR
                {
                    Target = BuildExpression(memberAccess.Expression),
                    MemberName = memberAccess.MemberName
                },
                InvocationExpression invocation => BuildInvocationExpression(invocation),
                _ => throw new System.NotSupportedException()
            };
        }

        private CallExpressionIR BuildInvocationExpression(InvocationExpression invocation)
        {
            var call = new CallExpressionIR
            {
                MethodName = invocation.Target switch
                {
                    IdentifierExpression identifier => identifier.NameEn,
                    MemberAccessExpression memberAccess => memberAccess.MemberName,
                    _ => ""
                }
            };

            foreach (var argument in invocation.Arguments)
            {
                call.Arguments.Add(BuildExpression(argument));
            }

            return call;
        }
    }
}

```

## 本ステップの評価
今回も基本的コメントがついていませんが、それは後で追記可能と踏んでいて、かなりよいと評価しています。先を急ぎます。サンプルソースに対してトランスコンパイルが実行できる状況づくりを目指します。

# おわりに
以上です。次回の方向性はPhase 6: コード生成パイプラインの実装の実行からとなります。「最小セット（MVP）」の完成条件にだいぶ近づいてきました。

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
