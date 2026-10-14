# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりましたところ、ほぼ「棚ぼた」でRe:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその続きとも言える検証編の第４ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編[^1]第２６ステップの後にはサインアウトがあります。

# 第４ステップ
前回ステップでProgram.csの中身はぐっと現実に近づきました。ただし、下記のコード部分は以前生成されたReMindParserクラスの実装と異なっているため、この点は（下記のコードスタイルのがよさそうとも言えるのですが）現状実装に沿って修正しました。（プロンプトに貼り付けた状態が現状のソースコードとなります。）

```cs:
        // 1. Re:Mind → AST
        var parser = new ReMindParser();
        var ast = parser.Parse(ReMindSourceCode);
```

## プロンプト
パーサーは以前ReMindBubbleSortAstGeneratorクラスを生成していただいていましたので、下記のように調整してパーサー部分は問題なく引数整合させましたが、CSharpCodeGeneratorクラスのGenerateメソッドの引数のCompilationUnit型ast2にnull参照可能性の警告がでています。nullの場合のエラー処理またはnullセーフ―チェーンを構成できますか？
```cs:
using System;
using System.Text.Json;
using ReMindAst;
using ReMindBackend;
using ReMindParser;

class Program
{
    static void Main()
    {
        const string ReMindSourceCode = @"
▽名前空間 BubbleSort
    /** Program */
    ▽public クラス プログラム型
        ...
";

        // 1. Re:Mind → AST
        var parser = new ReMindBubbleSortAstGenerator(ReMindSourceCode);
        var ast = parser.Parse();

        // 2. AST → JSON
        string json = JsonSerializer.Serialize(ast, new JsonSerializerOptions
        {
            WriteIndented = true
        });
        Console.WriteLine("=== AST(JSON) ===");
        Console.WriteLine(json);

        // 3. JSON → AST
        var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json);

        // 4. AST → C#コード
        var generator = new CSharpCodeGenerator();
        string cs = generator.Generate(ast2);

        Console.WriteLine("=== C# Source ===");
        Console.WriteLine(cs);
    }
}
```

## 生成レスポンス
これは System.Text.Json のデシリアライズが null を返す可能性がある ために発生する、C# の正しい警告です。
（JsonSerializer.Deserialize<T>() は、JSON が壊れていたり、型に合わなかったりすると null を返す可能性があるため）
つまり：
```cs:
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json);
```

ここで ast2 は CompilationUnit?（null 許容） と推論されます。
そのため：
```cs:
string cs = generator.Generate(ast2);
```

に対して「null かもしれない」という警告が出ます。

✅ 解決方法は 3 つあります
mylifewithviolinさんのプロジェクトの性質（AST → C# 生成は null では成立しない）を踏まえると、
最も安全で現実的な方法は「null チェックして例外を投げる」 です。

✅ 方法①：null チェックして例外を投げる（推奨）
```cs:
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json);

if (ast2 is null)
{
    throw new InvalidOperationException("AST のデシリアライズに失敗しました。");
}

var generator = new CSharpCodeGenerator();
string cs = generator.Generate(ast2);
```

これが最も安全で、C# の警告も消えます。

✅ 方法②：null 合体演算子で例外を投げる（より簡潔）
```cs:
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json)
          ?? throw new InvalidOperationException("AST のデシリアライズに失敗しました。");

var generator = new CSharpCodeGenerator();
string cs = generator.Generate(ast2);
```

mylifewithviolinさんのコードスタイルにも合うと思います。

✅ 方法③：null 許容を外す（安全性は下がる）
どうしても警告を消したいだけなら：
```cs:
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json)!;
```

! は「null ではないと信じる」という意味です。
ただし、本当に null が返ってきた場合は実行時例外になります。

🎯 結論：mylifewithviolinさんのプロジェクトには方法① or ② が最適
Re:Mind → AST → JSON → AST → C#
というパイプラインでは、AST が null になるのは 異常系 なので、
null チェックして例外を投げるのが最も自然です。

✨ 参考：最終的な Program.cs（安全版）
```cs:
// 3. JSON → AST
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json)
          ?? throw new InvalidOperationException("AST のデシリアライズに失敗しました。");

// 4. AST → C#コード
var generator = new CSharpCodeGenerator();
string cs = generator.Generate(ast2);

Console.WriteLine("=== C# Source ===");
Console.WriteLine(cs);
```


mylifewithviolinさんの Re:Mind プロジェクトは、
AST → C# のパイプラインがどんどん整ってきていて、とても美しい構造になっています。
次は：
- JSON → AST のバリデーション
- パーサーのエラー報告
- C# / Java / VB.NET のコード生成の統一化
なども進められます。
どこを強化していきましょうか。


## 第４ステップの評価
あいかわらず先を急ぐ（ご提案してくる）Microsoft Copilotですが、今回のプロンプトに対する応答はけっこう丁寧だとわたしは感じました。方法③のことは知りませんでした。方法②を採用し、いったん完走することを確認しました。まだ動作結果は不完全ですので、引き続きCopilotとの対話を続けて、生成コードの品質を上げていきます。

# おわりに
第４ステップは以上です。次回の方向性は上記のとおりです。

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
「Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす」の記事リストです。（ステップ降順）
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
