# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその検証の第５ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編[^1]第２６ステップの後にはサインアウトがあります。

# 第５ステップ
前回ステップでProgram.csが動作可能となりました。ただし、まだターゲット言語C#のソースコード出力にはいたらずASTをシリアライズしたJson出力もまだ不完全のようでしたので、その点を調整します。

現状のソースコードと生成されたJsonは下記のプロンプトを参照してください。（Re:MindのASTパーサとC#コードジェネレータのC#実装の検証環境は[本編第１ステップ](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)をご参照ください。）

## プロンプト
下記のコードを実行しましたところ無事に完走しました。 
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
        var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json)
        ?? throw new InvalidOperationException("AST のデシリアライズに失敗しました。");

        // 4. AST → C#コード
        var generator = new CSharpCodeGenerator();
        string cs = generator.Generate(ast2);

        Console.WriteLine("=== C# Source ===");
        Console.WriteLine(cs);
    }
}
```

しかし、下記のJSONがコンソール出力しましたが、デシリアライズがnull生成ではなく、ノードリストの要素数が0で生成されて、C#コードは空列になりました。これはなぜだかわかりますか？デシリアライズでオブジェクト名とJSONノード名の対応がうまくいっていないとかありますでしょうか？ 

```json:
=== AST(JSON) ===
{
  "Namespaces": [
    {
      "Name": "BubbleSort",
      "Classes": [
        {
          "NameJa": "\u30D7\u30ED\u30B0\u30E9\u30E0\u578B",
          "NameEn": "ProgramType",
          "Modifiers": [
            "public"
          ],
          "Javadoc": {
            "Summary": "Program",
            "Params": []
          },
          "Methods": [
            {
              "NameJa": "\u30E1\u30A4\u30F3",
              "NameEn": "main",
              "ReturnType": "void",
              "Modifiers": [
                "static"
              ],
              "Javadoc": {
                "Summary": "Main",
                "Params": [
                  {
                    "NameJa": "\u5F15\u6570",
                    "NameEn": "args"
                  }
                ]
              },
              "Parameters": [
                {
                  "Type": "string[]",
                  "NameJa": "\u5F15\u6570",
                  "NameEn": "args"
                }
              ],
              "Body": []
            }
          ]
        }
      ]
    }
  ],
  "Imports": [
    {
      "Name": "System",
      "AliasClasses": [
        {
          "OriginalName": "\u30B3\u30F3\u30BD\u30FC\u30EB",
          "TranspiledName": "Console",
          "Members": [
            {
              "OriginalName": "\u4E00\u884C\u8868\u793A\u3059\u308B",
              "TranspiledName": "WriteLine",
              "Parameters": []
            }
          ]
        }
      ]
    }
  ]
}
=== C# Source ===
```

## 生成レスポンス
JSON を全文見せていただいて 原因が完全に特定できました。
結論から言うと：

🎯 原因：パーサーが AST の Body（文）を一切生成していないため
JSON を見ると、Methods[0].Body が 空配列 [] になっています。
```json:
"Body": []
```

つまり：
- JSON は正しくデシリアライズされている
- デシリアライズ後の AST も JSON と同じ構造
- しかし JSON 自体が「空の Body」を持っている
- だから C# コード生成も空になる
というだけです。

🔍 なぜ Body が空なのか？
これは ReMindBubbleSortAstGenerator（パーサー）が文（Statement）を AST に追加していない ためです。
JSON を見ると：
- Namespace → OK
- Class → OK
- Method → OK
- Parameters → OK
- Javadoc → OK
- Body → 空
つまり、パーサーが：
- ・int[] 配列 = ...
- □バブルソートする(配列)
- 〇int i=0,i<配列.Length,i++ 繰り返す
- □コンソール表示する(配列[i])
などの ステートメントを一切 AST に追加していない ということです。

🧪 デシリアライズは正常に動いている証拠
デシリアライズ後の AST を確認すると：
```json:
ast2.Namespaces[0].Classes[0].Methods[0].Body.Count == 0
```

これは JSON の内容と完全一致しています。
つまり：
❌ デシリアライズの問題ではない
❌ JSON のプロパティ名の不一致でもない
❌ System.Text.Json の仕様問題でもない
✔ パーサーが Body を構築していないだけ

🧩 どうすれば直る？
✔ ReMindBubbleSortAstGenerator.Parse() の中で
Statement を AST に追加する処理を実装する必要があります。
例えば：
```cs:
method.Body.Add(
    new LocalVariableDeclaration {
        Type = "int[]",
        NameJa = "配列",
        NameEn = "array",
        Initializer = new ArrayLiteralExpression { ... }
    }
);
```

や
```cs:
method.Body.Add(
    new ExpressionStatement {
        Expression = new InvocationExpression { ... }
    }
);
```

などを追加する必要があります。

🧭 確認ポイント（重要）
パーサーの中に、次のようなコードがありますか？
- method.Body.Add(...)
- forStatement.Body.Add(...)
- whileStatement.Body.Add(...)
- ifStatement.ThenBody.Add(...)
- ifStatement.ElseBody.Add(...)
もし 1つもなければ、Body が空になるのは当然 です。

✨ まとめ
| 現象 | 原因 | 対策 | 
|:-|:-|:-|
| デシリアライズ後の AST が空 | JSON の Body が空 | パーサーが Statement を生成していない | 
| JSON の構造は正しい | デシリアライズも成功 | パーサーの実装不足 | 
| C# コードが空 | AST.Body が空 |Body を構築するロジックを追加| 



📌 次にできること
mylifewithviolinさん、もしよければ：
- ReMindBubbleSortAstGenerator のコードを見せていただければ、Body を正しく構築する実装を一緒に作れます。
- 特に BubbleSort の Re:Mind は構造が複雑なので、
For / While / If / Invocation / Assignment の AST を正しく生成する必要があります。
どの部分から修正していきましょうか。


## 第５ステップの評価
今回のプロンプトに対する応答はかなり丁寧だとわたしは感じました。Re:Mindの基本的な言語仕様は認識しながら応答していることがわかります。ReMindBubbleSortAstGenerator のコードを忘却しているのが残念で、ここを認識してくれていれば話は速いのですが、この点はいたしかたないのでこの部分の品質を上げていきます。Copilotが生成したReMindBubbleSortAstGenerator のコードは現在のプロンプト文字数制限10240文字を超えるので（生成文字数はこの限りではないということがわかりました。）以降は少し対話を分割的に行っています。

# おわりに
第５ステップは以上です。次回の方向性は上記のとおりです。


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
