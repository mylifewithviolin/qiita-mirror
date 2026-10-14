# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。前回シリーズ[^1]で「最小セット（MVP）」の実装が完了しましたので、本記事では検証フェーズの最初のステップになります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装が完了しました。今回はその実装の最初の検証となります。

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
1. 既存のビルド・実行を継続的に確認する。
2. 各フェーズごとにサンプル入力を用意し、期待コードが出力されることを確認する。
3. 追加する検証サンプルを用意する。
   - 変数宣言 + 代入 + console 出力
   - if / while / for のハンドリング
   - import / alias class の解決
   - class / method / member access
4. 未対応構文は明示的にエラーまたはプレースホルダーとして出力する。
### 完了条件
1. Re:Mind の代表的なサンプルコードが Lexer と Parser を通過する

## とりあえず現状有姿で実行してみる。
今回実装が完了した最小セット（MVP）のProgram.csにはあおいのサンプルソースコードが文字列変数として定義されています。こちらをCSソースに変換できるか実行してみます。

```cs:Program.cs
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
Program.csのあおいのサンプルソースコードはバブルソートのロジックを記述したもので意外と複雑なことが書いてあります。これをいきなり成功させるのはむずかしいかも。（最初に逃げ前置き）

## Microsoft Copilotとの事前準備
今回はMicrosoft Copilotとの対話は特にありません。
## GitHub Copilot
### プロンプト１
>下記の実行エラーを適切に解消するプランを作成してフォルダのdocsに出力してください。
Unhandled exception. System.InvalidOperationException: Unexpected character '▽' at line 2, column 1.
   at ReMindParser.Lexer.NextToken() in C:\developments\cs12\astsample\Lexer.cs:line 303
   at ReMindParser.Lexer.Tokenize() in C:\developments\cs12\astsample\Lexer.cs:line 92
   at Program.Main(String[] args) in C:\developments\cs12\astsample\Program.cs:line 74
#### 生成レスポンス１
>実行エラーの原因と修正方針を計画書として追加しました。
>
>lexer_runtime_error_fix_plan.md
>
>内容には以下を含めています。
>
>▽ が未対応である根本原因
>Lexer に追加すべき記号トークン
TokenType / NextToken() の修正方針
Parser との切り分け
Lexer 単体・パイプライン検証手順
完了条件と次工程
今回は計画書のみ作成し、ソースコードは変更していません。

### プロンプト２
>docs\lexer_runtime_error_fix_plan.mdを実行して
docs\lexer_runtime_error_fix_plan_executed.mdに
修正内容と実行結果を、
完走した場合、コンソール出力の内容を評価して
を報告してください。
   
#### 生成レスポンス２
>計画を実行し、Lexer の修正と検証結果を以下に記録しました。
>
>lexer_runtime_error_fix_plan_executed.md
>
>結果:
>
>▽ の Lexer エラーを解消
全角空白など、入力中の追加記号にも対応
ビルド成功
実行は Parser の Unsupported statement start: '▽' で停止
コード生成には未到達のため、生成コードの標準出力はありません
変更ファイルは Lexer.cs のみです。

### lexer_runtime_error_fix_plan_executed.md
```text
# Lexer 実行エラー解消計画 実行報告
## 1. 実行日
2026-09-06
## 2. 実施内容
`docs/lexer_runtime_error_fix_plan.md` に従い、Lexer の入力文字処理を修正した。

### `Lexer.cs` の修正
- `▽` を `DeclarationStart` としてトークン化
- `△` を `DeclarationEnd` としてトークン化
- `・` を `DeclarationBullet` としてトークン化
- `■` を `ImportStart` としてトークン化
- `▼` を `AliasStart` としてトークン化
- `▲` を `AliasEnd` としてトークン化
- `<` / `>` を `Operator` としてトークン化
- `:` / `?` / `;` を `Symbol` としてトークン化
- 全角空白 `　` を空白としてスキップ
- 識別子の継続文字に数字と `_` を許可
既存の Parser、AST、IR、CodeGenerator の宣言解析ロジックは今回変更していない。

## 3. ビルド結果
実行コマンド:
C:\Program Files\dotnet\dotnet.EXE build C:\developments\cs12\astsample/astsample.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign

結果:
- ビルド成功
- `astsample.dll` を生成
- 既存コード由来の nullable 警告は残存
- Lexer.cs 自体のエラーはなし

## 4. 実行結果
実行コマンド:
C:\Program Files\dotnet\dotnet.EXE run --no-build --project .\astsample.csproj

結果:
Unhandled exception. System.InvalidOperationException:
Unsupported statement start: '▽'.
   at ReMindParser.Parser.ParseStatement()
   at ReMindParser.Parser.ParseCompilationUnit()
   at Program.Main(String[] args)

## 5. 結果評価
### Lexer
Lexer の当初エラーである次の例外は解消した。
Unexpected character '▽' at line 2, column 1.
`ReMindSourceCode` は Lexer を通過し、`▽` 以外の構造記号、比較演算子、全角空白も入力処理できた。

### Parser 以降
コンパイラ全体は完走していない。Lexer の次の段階である Parser が、名前空間・クラス・メソッド宣言の開始記号 `▽` を文の開始として処理できず停止した。

現時点ではコード生成まで到達していないため、生成コードの標準出力は存在しない。コンソールに出力されたのは Parser の未対応構文を示す例外だけである。

## 6. 残課題
次工程として Parser に宣言構文の解析を追加する必要がある。
- `▽名前空間 ...`
- `▽public クラス ...`
- `▽static void ...`
- `△` による宣言終了
- `・` による変数宣言
- `■`、`▼`、`▲` による import / Alias 定義

Parser が AST を生成できるようになった後、SemanticResolver、IRBuilder、CSharpCodeGenerator の実行結果を改めて確認する。

## 7. 完了判定
- Lexer の `▽` 実行エラー解消: 完了
- Lexer の全入力トークン化: 実行経路上は完了
- ビルド: 成功
- Parser から CodeGenerator までの完走: 未完了
- 生成コードのコンソール出力評価: 未実施。Parser で停止したため生成コードは出力されていない
```

## 本ステップの評価
最初の検証フェーズが完了しました。結果の状態としてはまだコード生成に到達していません。引き続き検証とバグ修正を行います。次回はもう少し単純なのから始めてみます。

また、次回は期待コード（答え）も用意し動くところまで検証->修正->再検証->再修正のサイクルをまわしてみます。

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
