# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではASTの最小版を実装します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の途中です。今回はASTの最小版を実装します。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前々回記事で完了
**Phase 2. Parser タスク**
前回記事で完了
## 3. AST タスク
- AST ノードの基本構造を定義する
- 変数宣言ノードを追加する
- 定数宣言ノードを追加する
- 関数宣言ノードを追加する
- 関数呼び出しノードを追加する
- クラス宣言ノードを追加する
- クラスメンバノードを追加する
- 条件分岐ノードを追加する
- 繰り返しノードを追加する
- 例外処理ノードを追加する
- 既存の Ast.cs を拡張して、Re:Mind 構文に対応させる

## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 2：Parserが完了しました。Phase 3: AST モデルの拡張の最小タスク化プロンプト（CodeAgent 用）を作成してください。

#### 生成レスポンス１
>AST モデルの拡張は Re:Mind 言語処理系の「データ構造の中核」であり、後続フェーズ（意味解析 → IR → CodeGen）の品質を左右する重要フェーズです。
以下に、Phase 3 の AST 拡張を CodeAgent 用に完全最小タスク化したプロンプト集をまとめます。
カテゴリ A：宣言系ノード（Declaration）
① ConstantDeclaration の追加
以下は AST の仕様です。
Ast.cs に「ConstantDeclaration ノード」を差分として追加してください。
必要なプロパティ（名前・型・初期値）だけを追加し、既存コードは保持してください。
② FieldDeclaration の追加
Ast.cs に「FieldDeclaration ノード」を差分として追加してください。
フィールド名・型・初期値を保持する最小構造だけ追加してください。
既存コードは保持してください。


AI的にはきっちり反復的にプロンプトを生成していますが、本記事的には以下同様で内容割愛しています。
>③ NamespaceDeclaration の追加
④ ImportDeclaration / AliasClass / AliasMember の追加
🧩 カテゴリ B：文系ノード（Statement）
⑤ ReturnStatement の追加
⑥ BreakStatement / ContinueStatement の追加
⑦ TryCatchStatement の追加
⑧ SwitchStatement の追加
🧩 カテゴリ C：式系ノード（Expression）
⑨ NewExpression の追加
⑩ NullLiteralExpression の追加
⑪ ConditionalExpression（条件演算子）
⑫ AssignmentExpression の追加
⑬ ArrayCreationExpression の追加
🧩 カテゴリ D：メタ情報（Metadata）
⑭ JavadocComment の追加
⑮ Parameter の追加
⑯ TypeReference の追加


## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 3の各タスクの実行プロンプトを逐次実行した結果、下記のソースコードが生成されました。


```cs:Ast.cs
using System;
using System.Collections.Generic;

namespace ReMindAst
{
    // ベースノード
    public abstract class AstNode
    {
    }

    // ルート
    public class CompilationUnit : AstNode
    {
        public List<NamespaceDeclaration> Namespaces { get; } = new();
        public List<ImportDeclaration> Imports { get; } = new();
        public List<Statement> Statements { get; } = new();
    }

    public class NamespaceDeclaration : AstNode
    {
        public string Name { get; set; } = "";
        public List<ClassDeclaration> Classes { get; } = new();
    }

    public class ClassDeclaration : AstNode
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = ""; // transpiledName
        public List<string> Modifiers { get; } = new();
        public JavadocComment? Javadoc { get; set; }
        public List<MethodDeclaration> Methods { get; } = new();
    }

    public class JavadocComment
    {
        public string? Summary { get; set; }
        public List<JavadocParam> Params { get; } = new();
    }

    public class JavadocParam
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    public class MethodDeclaration : AstNode
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public string ReturnType { get; set; } = "void";
        public List<string> Modifiers { get; } = new();
        public JavadocComment? Javadoc { get; set; }
        public List<Parameter> Parameters { get; } = new();
        public List<Statement> Body { get; } = new();
    }

    public class FieldDeclaration : AstNode
    {
        public JavadocComment? Javadoc { get; set; }
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public Expression? Initializer { get; set; }
        public List<string> Modifiers { get; } = new();
    }

    public class Parameter : AstNode
    {
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    // --- ステートメント基底 ---

    public abstract class Statement : AstNode
    {
    }

    public class LocalVariableDeclaration : Statement
    {
        public JavadocComment? Javadoc { get; set; }
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public Expression? Initializer { get; set; }
    }

    public class ConstantDeclaration : Statement
    {
        public JavadocComment? Javadoc { get; set; }
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public Expression? Initializer { get; set; }
        public List<string> Modifiers { get; } = new();
    }

    public class ExpressionStatement : Statement
    {
        public Expression Expression { get; set; } = null!;
    }

    public class ForStatement : Statement
    {
        public LocalVariableDeclaration? Initializer { get; set; }
        public Expression? Condition { get; set; }
        public Expression? Iterator { get; set; }
        public List<Statement> Body { get; } = new();
    }

    public class WhileStatement : Statement
    {
        public Expression Condition { get; set; } = null!;
        public List<Statement> Body { get; } = new();
    }

    public class IfStatement : Statement
    {
        public Expression Condition { get; set; } = null!;
        public List<Statement> ThenBody { get; } = new();
        public List<Statement> ElseBody { get; } = new();
    }

    public class BlockStatement : Statement
    {
        public List<Statement> Statements { get; } = new();
    }

    public class AssignmentStatement : Statement
    {
        public Expression Left { get; set; } = null!;
        public Expression Right { get; set; } = null!;
    }

    public class ReturnStatement : Statement
    {
        public Expression? Value { get; set; }
    }

    public class BreakStatement : Statement
    {
    }

    public class ContinueStatement : Statement
    {
    }

    public class TryCatchStatement : Statement
    {
        public List<Statement> TryBody { get; } = new();
        public List<CatchClause> CatchClauses { get; } = new();
        public List<Statement> FinallyBody { get; } = new();
    }

    public class CatchClause : AstNode
    {
        public string ExceptionType { get; set; } = "";
        public string VariableName { get; set; } = "";
        public List<Statement> Body { get; } = new();
    }

    public class SwitchStatement : Statement
    {
        public Expression Expression { get; set; } = null!;
        public List<SwitchCase> Cases { get; } = new();
    }

    public class SwitchCase : AstNode
    {
        public Expression? Value { get; set; }
        public List<Statement> Body { get; } = new();
    }

    // --- 式基底 ---

    public abstract class Expression : AstNode
    {
    }

    public class IdentifierExpression : Expression
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    public class LiteralExpression : Expression
    {
        public object? Value { get; set; }
    }

    public class BinaryExpression : Expression
    {
        public string Operator { get; set; } = "";
        public Expression Left { get; set; } = null!;
        public Expression Right { get; set; } = null!;
    }

    public class UnaryExpression : Expression
    {
        public string Operator { get; set; } = "";
        public Expression Operand { get; set; } = null!;
    }

    public class MemberAccessExpression : Expression
    {
        public Expression Expression { get; set; } = null!;
        public string MemberName { get; set; } = "";
    }

    public class ElementAccessExpression : Expression
    {
        public Expression ArrayExpression { get; set; } = null!;
        public Expression IndexExpression { get; set; } = null!;
    }

    public class InvocationExpression : Expression
    {
        public Expression Target { get; set; } = null!;
        public List<Expression> Arguments { get; } = new();
    }

    public class ArrayLiteralExpression : Expression
    {
        public string ElementType { get; set; } = "";
        public List<Expression> Elements { get; } = new();
    }

    public class NewExpression : Expression
    {
        public string TypeName { get; set; } = "";
        public List<Expression> Arguments { get; } = new();
    }

    public class NullLiteralExpression : Expression
    {
    }

    public class ConditionalExpression : Expression
    {
        public Expression Condition { get; set; } = null!;
        public Expression ThenExpression { get; set; } = null!;
        public Expression ElseExpression { get; set; } = null!;
    }

    public class AssignmentExpression : Expression
    {
        public Expression Left { get; set; } = null!;
        public Expression Right { get; set; } = null!;
    }

    public class ArrayCreationExpression : Expression
    {
        public string ElementType { get; set; } = "";
        public List<Expression> Initializers { get; } = new();
    }

    // --- import / System.Console マッピング ---

    public class ImportDeclaration : AstNode
    {
        public string Name { get; set; } = "";
        public List<AliasClass> AliasClasses { get; } = new();
    }

    public class AliasClass
    {
        public string OriginalName { get; set; } = "";
        public string TranspiledName { get; set; } = "";
        public List<AliasMember> Members { get; } = new();
    }

    public class AliasMember
    {
        public string OriginalName { get; set; } = "";
        public string TranspiledName { get; set; } = "";
        public List<Parameter> Parameters { get; } = new();
    }

    public class TypeReference : AstNode
    {
        public string Name { get; set; } = "";
        public List<TypeReference> TypeArguments { get; } = new();
    }
}

```
## 本ステップの評価
かなりよいと評価しています。コメントは後でつけていきます。このくらいの量ならばCopilotで十分対応できそうです。サンプルソースに対してトランスコンパイルが実行できる状況づくりを急ぎます。

# おわりに
以上です。次回の方向性はPhase 4: 意味解析と名前解決の実装の実行からとなります。

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
