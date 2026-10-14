# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりましたところ、ほぼ「棚ぼた」でRe:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその続きとも言える検証編の第３ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編第２６ステップの後にはサインアウトがあります。

# 第３ステップ
いじりたおす編第２４ステップ、第２５ステップで生成されたRe:MindのASTパーサとC#コードジェネレータのC#実装が検証できる環境を[本編第１ステップ](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)で構築して、引き続きいじりたおす編第２４ステップの生成コードのメイン部分の問題点を検討します。Copilotに自ら生成したコードを少しづつ思い出してもらっています。

## プロンプト
以前、下記のRe:Mindのソースコードから
```mind:Re:Mind
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

ASTのJsonを生成していただきましたが、このRe:Mindのソースコードを文字列定数変数として定義して、それを入力として、AST文字列を生成し、そのAST文字列をC#コードジェネレータが読み込んでC#ソースコード文字列を生成してコンソール出力するように実装できますか？

## 生成レスポンス
できます。
しかも miylifewithviolinさんがすでに構築している AST クラス体系と C# コードジェネレータをそのまま活かした “Re:Mind → AST(JSON) → C#コード” の完全パイプライン を実装できます。
ただし、実現するには 3つのコンポーネント が必要です：

🧩 必要な3コンポーネント
① Re:Mind ソースコード → AST オブジェクト
（Re:Mind パーサー）
② AST オブジェクト → JSON
（AST シリアライザ）
③ JSON → AST オブジェクト → C# コード
（AST デシリアライズ＋C#コードジェネレータ）

mylifewithviolinさんがすでに持っているのは：
- AST クラス群（CompilationUnit など）
- CSharpCodeGenerator（AST → C#）
足りないのは：
- Re:Mind パーサー（文字列 → AST）
- AST JSON シリアライズ／デシリアライズ
これを補えば、Program.cs で次のように書けます：
```cs:
string rem = ReMindSourceCode; // ← Re:Mind のソースコード文字列

// 1. Re:Mind → AST
var parser = new ReMindParser();
CompilationUnit ast = parser.Parse(rem);

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
```


🎯 では、実際にどう実装するか？
以下に 実装可能な最小構成 を示します。

① Re:Mind パーサー（最小構成）
まずは BubbleSort の構文だけを扱う簡易パーサー を作るところから始めるのが現実的です。
```cs:
public class ReMindParser
{
    public CompilationUnit Parse(string source)
    {
        var unit = new CompilationUnit();

        // ここでは最小限のデモとして、
        // 名前空間 BubbleSort とクラス プログラム型 を固定で生成する
        var ns = new NamespaceDeclaration { Name = "BubbleSort" };
        unit.Namespaces.Add(ns);

        var cls = new ClassDeclaration
        {
            NameJa = "プログラム型",
            NameEn = "Program",
            Modifiers = { "public" }
        };
        ns.Classes.Add(cls);

        // メインメソッド（デモ）
        var main = new MethodDeclaration
        {
            NameJa = "メイン",
            NameEn = "Main",
            ReturnType = "void",
            Modifiers = { "public", "static" }
        };
        cls.Methods.Add(main);

        // 配列初期化（デモ）
        main.Body.Add(new LocalVariableDeclaration
        {
            Type = "int[]",
            NameJa = "配列",
            NameEn = "array",
            Initializer = new ArrayLiteralExpression
            {
                ElementType = "int",
                Elements =
                {
                    new LiteralExpression { Value = 15 },
                    new LiteralExpression { Value = 13 },
                    new LiteralExpression { Value = 9 },
                    new LiteralExpression { Value = 6 },
                    new LiteralExpression { Value = 4 },
                    new LiteralExpression { Value = 1 }
                }
            }
        });

        return unit;
    }
}
```


② AST → JSON（標準の System.Text.Json でOK）
```cs:
string json = JsonSerializer.Serialize(ast, new JsonSerializerOptions
{
    WriteIndented = true
});
```


③ JSON → AST
```cs:
var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json);
```


④ AST → C#コード（既存の CSharpCodeGenerator を使用）
```cs:
var generator = new CSharpCodeGenerator();
string cs = generator.Generate(ast2);
Console.WriteLine(cs);
```


🧪 Program.cs の完成形（動作デモ）
```cs:
using System;
using System.Text.Json;
using ReMindAst;
using ReMindBackend;

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
        var parser = new ReMindParser();
        var ast = parser.Parse(ReMindSourceCode);

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


🌟 ここからどう拡張できるか
miylifewithviolinさんの Re:Mind プロジェクトはすでに AST → C# の部分が完成しているので、
次のステップは Re:Mind → AST のパーサーを本格的に作ることです。
例えば：
- ▽名前空間 → NamespaceDeclaration
- ▽public クラス → ClassDeclaration
- ▽static void メイン → MethodDeclaration
- ・int[] 配列 = ... → LocalVariableDeclaration
- □バブルソートする(配列) → InvocationExpression
- 〇...繰り返す → ForStatement / WhileStatement
- ◇...の場合 → IfStatement
これらをすべて AST に落とし込めば、
Re:Mind 言語 → AST → C# / Java / VB.NET
という完全なトランスパイラが完成します。

✨ 次に進める提案
miylifewithviolinさんのスタイルに合わせて、次のどれを作りましょうか。
- Re:Mind パーサーの正式仕様（BNF）を作る
- BubbleSort の Re:Mind を完全にパースする実装を作る
- AST → C# のコードジェネレータを強化する
- AST → Java / VB.NET のコードジェネレータを追加する
どれから進めたいですか。


## 第３ステップの評価
あいかわらず先を急ぐ（ご提案してくる）Microsoft Copilotですが、今回の応答はかなりヒットでクォリティがぐんとあがった印象です。Copilotもけっこうよいしょしてきますが、われわれもCopilotをいかにおだてて？以前の内容を思い出させるかがポイントのようです。引き続きCopilotとの対話を続けて、このメイン部分の品質を上げていきます。

# おわりに
第３ステップは以上です。次回の方向性は上記のとおりです。

# 参考情報
## 目次　Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす
「Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす」の目次です。（ステップ降順）
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
