# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事では意味解析と名前解決をまず実装するか、中間表現（IR）を実装するかを検討します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の途中です。ASTの最小版の実装まで完了しました。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前々回記事以前で完了
**Phase 2. Parser タスク**
前々回記事で完了
**Phase 3. AST タスク**
前回記事で完了

ここで「Re:Mind コンパイラ全体設計」のPhase 4は
意味解析と名前解決　(IR タスクはPhase 5)
となっていますが、「1. 最小セット（MVP）」の実装タスク詳細では
4. IR タスク
となっているため、ここで念のため今回はステップの方向性を再確認します。

## Microsoft Copilotとの事前準備
### プロンプト１
>Ast.csの更新が完了しました。現在は最小セット（MVP）を実装していますね。ASTの次のステップはIRですか？それとも　意味解析と名前解決　ですか？

#### 生成レスポンス１
>結論
**Phase 3（AST 拡張）が終わったら、次は Phase 4：意味解析と名前解決です。
次に進むべきフェーズは IR ではなく「意味解析と名前解決（Semantic Analysis）」です。
>
>これは言語処理系の王道の順番であり、
あなたの Re:Mind の構文仕様（□ / ◇ / 〇 / 日本語識別子 / AliasClass / AliasMember）を考えると
意味解析 → IR → CodeGen の順が最も安定します。
>
>① IR は「意味が確定した AST」を前提にする
IR は「言語非依存の中間表現」なので、
AST の曖昧な部分（型・スコープ・メンバー名）が残っていると作れません。
これらは 名前解決（Symbol Table）を通さないと意味が確定しません。
>
>② Re:Mind は「日本語 → 英語」変換が必須
AST には日本語名が残っていますが、
IR は ターゲット言語の名前（Console.WriteLine） を使います。
つまり：
AST：日本語名
Semantic：名前解決（AliasClass → AliasMember）
IR：英語名（ターゲット言語名）
この順番でないと CodeGen が壊れます。
>
>③ IR は「型情報」が必要
Re:Mind の構文は型推論が多いです。
例：コード
□年齢 = 20
□コンソール.一行表示する(年齢)
AST だけでは「年齢」が int なのか string なのか分かりません。
意味解析で型を決めてから IR に渡す必要があります。
>
>④ IR は「構文の意味」を表す
AST は「構文の形」
IR は「意味の構造」
例：
>
>AST（構文）コード
>
>InvocationExpression
  Target: MemberAccessExpression
    Target: Identifier("コンソール")
    Member: Identifier("一行表示する")
  Arguments: [Identifier("年齢")]
>
>IR（意味）コード
>
>CallIR
  TargetClass: "Console"
  TargetMethod: "WriteLine"
  Arguments: [VariableIR("age")]
>
>AST のままでは CodeGen が困難です。

#### 生成レスポンス１の評価
Re：Mind（あおい）固有の情報を例示して、これでもかと詳しく説明してきましたので、「意味解析と名前解決」に進行することに同意します。実際は前後しますが、「意味解析と名前解決」最小タスクプロンプト作成した後、これに該当するクラスは以前のプロジェクトには存在しないことに気づきます。

### プロンプト2
>SemanticResolver.csはまだ存在しません。枠を作成するプロンプトを最初に作成してください。

#### 生成レスポンス2
>SemanticResolver.cs がまだ存在しない状態で Phase 4（意味解析と名前解決）を開始するための「枠（骨格）だけを CodeAgent に生成させるプロンプト」を作成します。
>
>これは SemanticResolver.cs の最小構造（クラス定義・コンストラクタ・Resolve メソッドの枠・SymbolTable の枠）だけを作るためのプロンプトです。
中身のロジックは一切生成させず、後続の最小タスク化プロンプトで差分追加していく方式です。
>
>Re:Mind 言語処理系の Phase 4（意味解析と名前解決）を開始するため、
SemanticResolver.cs の「枠（骨格）」だけを新規作成してください。
>
>条件:
>- まだ SemanticResolver.cs は存在しません。
>- 中身のロジックは一切書かず、クラス定義とメソッドの枠だけ作成してください。
>- 後続フェーズで差分追加できるように、最小構造にしてください。
>- 以下の構造を含めてください。
>
>必要な構造:
>- namespace ReMindParser
>- public class SemanticResolver
>- コンストラクタ（AST の CompilationUnit を受け取る）
>- Resolve() メソッド（AST 全体を意味解析する枠）
>- ResolveExpression() メソッドの枠
>- ResolveStatement() メソッドの枠
>- SymbolTable の枠（クラス定義だけ）
>- Scope の枠（BlockScope / MethodScope / ClassScope のクラス定義だけ）
>
>既存コードは保持し、新規ファイルとして最小構造だけ生成してください。

#### 生成レスポンス2の評価
Copilotが「CodeAgent は次のような「枠だけ」を生成します」として、丁寧に散布労ソースも開示してきました。

```cs:SemanticResolver.cs
namespace ReMindParser
{
    public class SemanticResolver
    {
        private readonly CompilationUnit _root;
        private readonly SymbolTable _symbols;

        public SemanticResolver(CompilationUnit root)
        {
            _root = root;
            _symbols = new SymbolTable();
        }

        public void Resolve()
        {
            // AST 全体の意味解析を行う（後で実装）
        }

        private void ResolveStatement(Statement stmt)
        {
            // 後で実装
        }

        private void ResolveExpression(Expression expr)
        {
            // 後で実装
        }
    }

    public class SymbolTable
    {
        // 後で実装
    }

    public class BlockScope
    {
        // 後で実装
    }

    public class MethodScope
    {
        // 後で実装
    }

    public class ClassScope
    {
        // 後で実装
    }
}
```
めんどくさがらずこれでプロジェクトにファイルを作成すればよかったのですが、いちおう上記生成プロンプトをGithub Copilotに投げてみました。クレジットが少し消費されたので後悔しました。

## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのSemanticResolver.csひな形作成タスクの実行プロンプトを実行した結果、下記のソースコードが生成されました。
```cs:SemanticResolver.cs
using System;
using System.Collections.Generic;
using ReMindAst;

namespace ReMindParser
{
    /// <summary>
    /// 意味解析と名前解決を行うクラス
    /// AST に対してシンボルテーブルを構築し、型チェックと名前解決を実行する
    /// </summary>
    public class SemanticResolver
    {
        private CompilationUnit _ast = null!;
        private SymbolTable _symbolTable = null!;
        private Scope _currentScope = null!;

        /// <summary>
        /// コンストラクタ
        /// </summary>
        /// <param name="ast">解析対象の CompilationUnit</param>
        public SemanticResolver(CompilationUnit ast)
        {
            _ast = ast;
            _symbolTable = new SymbolTable();
            _currentScope = _symbolTable.GlobalScope;
        }

        /// <summary>
        /// AST 全体を意味解析する
        /// </summary>
        public void Resolve()
        {
            // TODO: AST 全体を走査して意味解析を実行
        }

        /// <summary>
        /// 式を意味解析する
        /// </summary>
        /// <param name="expression">解析対象の式</param>
        public void ResolveExpression(Expression expression)
        {
            // TODO: 式の型チェックと名前解決を実行
        }

        /// <summary>
        /// ステートメントを意味解析する
        /// </summary>
        /// <param name="statement">解析対象のステートメント</param>
        public void ResolveStatement(Statement statement)
        {
            // TODO: ステートメントの意味解析を実行
        }
    }

    /// <summary>
    /// シンボルテーブル
    /// 変数・メソッド・クラス・名前空間などのシンボル情報を管理する
    /// </summary>
    public class SymbolTable
    {
        private Scope _globalScope;

        public Scope GlobalScope { get { return _globalScope; } }

        public SymbolTable()
        {
            _globalScope = new GlobalScope();
        }
    }

    /// <summary>
    /// スコープの基底クラス
    /// 変数やメソッドのシンボル情報を保持する
    /// </summary>
    public abstract class Scope
    {
        protected Dictionary<string, Symbol> _symbols = new();
        protected Scope? _parentScope;

        public Scope(Scope? parentScope = null)
        {
            _parentScope = parentScope;
        }

        /// <summary>
        /// シンボルを登録する
        /// </summary>
        public void DefineSymbol(string name, Symbol symbol)
        {
            // TODO: シンボルを登録
        }

        /// <summary>
        /// シンボルを検索する
        /// </summary>
        public Symbol? LookupSymbol(string name)
        {
            // TODO: シンボルを検索（スコープチェーンをたどる）
            return null;
        }
    }

    /// <summary>
    /// グローバルスコープ
    /// プログラム全体の名前空間・クラス・グローバル関数を管理
    /// </summary>
    public class GlobalScope : Scope
    {
        public GlobalScope() : base(null)
        {
        }
    }

    /// <summary>
    /// ブロックスコープ
    /// if / while / for などのブロック内のローカル変数を管理
    /// </summary>
    public class BlockScope : Scope
    {
        public BlockScope(Scope parentScope) : base(parentScope)
        {
        }
    }

    /// <summary>
    /// メソッドスコープ
    /// メソッド内のパラメータとローカル変数を管理
    /// </summary>
    public class MethodScope : Scope
    {
        public MethodScope(Scope parentScope) : base(parentScope)
        {
        }
    }

    /// <summary>
    /// クラススコープ
    /// クラスのフィールドとメソッドを管理
    /// </summary>
    public class ClassScope : Scope
    {
        public ClassScope(Scope parentScope) : base(parentScope)
        {
        }
    }

    /// <summary>
    /// シンボル
    /// 変数・メソッド・クラスなどの情報を保持
    /// </summary>
    public class Symbol
    {
        public string Name { get; set; } = "";
        public string Type { get; set; } = "";
        public SymbolKind Kind { get; set; }

        public Symbol(string name, string type, SymbolKind kind)
        {
            Name = name;
            Type = type;
            Kind = kind;
        }
    }

    /// <summary>
    /// シンボルの種類
    /// </summary>
    public enum SymbolKind
    {
        Variable,
        Parameter,
        Method,
        Class,
        Namespace,
        Field,
        Constant
    }
}

```
## 本ステップの評価
かなりよいと評価しています。クレジットは若干は消費するのでSemanticResolver.csが生成したひな形コードでよかったかもしれません。サンプルソースに対してトランスコンパイルが実行できる状況づくりを急ぎます。

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
