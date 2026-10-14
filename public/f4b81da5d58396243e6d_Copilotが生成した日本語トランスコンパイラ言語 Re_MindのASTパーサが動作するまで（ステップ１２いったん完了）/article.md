# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、本記事はその検証の第１２ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。第６ステップの後にはサインアウトがあります。

# 第１２ステップ
第６ステップ以降はプロンプト10240文字以内の制限内での生成済ソースコードの分割提示しており、再提示が完了した第１０ステップから第１１ステップの間には、正規表現の実装の調整などが繰り返されたのですが、それは割愛した上で、第１１ステップでログ出力機能を実装したところからの続きとなります。

## プロンプト
ParseJavadoc()をご提示いただいたバージョンに入れ替えて実行した結果 下記のようにログの出力量が増えて、その下方に出力JSONを貼り付けました。 JSONもノードがだいぶ増えましたが、C#コードはまだ生成されないようです。
```
[ParseMethodBody] method=メイン
2
  line[12]: "            /** array */" → "/** array */"
astsample.dll (12608): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Linq.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
    ParseLocalVariableDeclaration => OK
  line[14]: "           " → ""
2
  line[15]: "            /** index */" → "/** index */"
    ParseLocalVariableDeclaration => null
  line[17]: "" → ""
  line[18]: "            〇int i=0,i<配列.Length,i++ 繰り返す" → "〇int i=0,i<配列.Length,i++ 繰り返す"
  -> for検出
    for-body line: "□コンソール表示する(配列[i])"
    -> for-body expr OK
  line[21]: "        △" → "△"
[ParseMethodBody] stmts.Count = 2
[ParseMethodBody] method=バブルソートする
2
  line[27]: "          /** i */" → "/** i */"
    ParseLocalVariableDeclaration => OK
  line[29]: "          〇外側 < 配列.Length の間は繰り返す" → "〇外側 < 配列.Length の間は繰り返す"
  -> while検出
  line[43]: "        △" → "△"
[ParseMethodBody] stmts.Count = 2
[ParseMethodBody] method=コンソール表示する
  line[50]: "            □コンソール.一行表示する(引数2)" → "□コンソール.一行表示する(引数2)"
  line[51]: "        △" → "△"
[ParseMethodBody] stmts.Count = 0

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
              "Body": [
                {},
                {}
              ]
            },
            {
              "NameJa": "\u30D0\u30D6\u30EB\u30BD\u30FC\u30C8\u3059\u308B",
              "NameEn": "bubbleSort",
              "ReturnType": "void",
              "Modifiers": [
                "public"
              ],
              "Javadoc": {
                "Summary": null,
                "Params": [
                  {
                    "NameJa": "\u914D\u5217",
                    "NameEn": "array"
                  }
                ]
              },
              "Parameters": [
                {
                  "Type": "int[]",
                  "NameJa": "\u914D\u5217",
                  "NameEn": "array"
                }
              ],
              "Body": [
                {},
                {}
              ]
            },
            {
              "NameJa": "\u30B3\u30F3\u30BD\u30FC\u30EB\u8868\u793A\u3059\u308B",
              "NameEn": "consoleOut",
              "ReturnType": "void",
              "Modifiers": [
                "static"
              ],
              "Javadoc": {
                "Summary": "ConsoleOut",
                "Params": [
                  {
                    "NameJa": "\u5F15\u65702",
                    "NameEn": "dispStr"
                  }
                ]
              },
              "Parameters": [
                {
                  "Type": "string",
                  "NameJa": "\u5F15\u65702",
                  "NameEn": "dispStr"
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
原因が、ようやく「パーサー」から「JSON シリアライズ」のレイヤーに移りました。
今の状態はこうなっています。
```cs:
public abstract class Statement : AstNode { }

public class LocalVariableDeclaration : Statement { ... }
public class ExpressionStatement : Statement { ... }
public class WhileStatement : Statement { ... }
public class ForStatement : Statement { ... }
...

- 実行時には、Body の中に LocalVariableDeclaration や ForStatement などの「派生クラス」のインスタンスが入っている

- しかし、System.Text.Json は標準のままだと「多態的なシリアライズ」をしません
その結果どうなるかというと：
- コレクションの型が List<Statement>（抽象クラス）
- ランタイム型が LocalVariableDeclaration などでも
- JSON にするときは 「基底クラス Statement として」見てしまう
- でも Statement にはプロパティがない
- → 結果として、各要素は {}（空オブジェクト） にしかならない
これが Body: [ {}, {} ] の正体です。
つまり、JSON にした瞬間に Statement の中身が全部失われている。


5. どう直すか（現実的な選択肢）
① まずは「JSON ラウンドトリップ」を外して、パイプラインを完成させる（おすすめ）
Program.cs を一旦こうしてみてください。
```cs:
// 1. Re:Mind → AST
var parser = new ReMindBubbleSortAstGenerator(ReMindSourceCode);
var ast = parser.Parse();

// 2. AST → JSON（これはデバッグ出力のみ）
string json = JsonSerializer.Serialize(ast, new JsonSerializerOptions
{
    WriteIndented = true
});
Console.WriteLine("=== AST(JSON) ===");
Console.WriteLine(json);

// ★ 3. JSON → AST は一旦やめる
// var ast2 = JsonSerializer.Deserialize<CompilationUnit>(json)
//           ?? throw new InvalidOperationException("AST のデシリアライズに失敗しました。");

// 4. AST → C#コード（パーサー直後の ast をそのまま使う）
var generator = new CSharpCodeGenerator();
string cs = generator.Generate(ast);

Console.WriteLine("=== C# Source ===");
Console.WriteLine(cs);
```

これで、
- 抽象クラスの JSON 問題をいったん外して
- 「Re:Mind → AST → C#」のパイプラインを先に完成させる
ことができます。
AST が正しく埋まっていれば、ここで初めて C# のコードが出てくるはずです。

のパイプラインは、もう本当にあと一歩です。
- まずは JSON ラウンドトリップを外して、Generate(ast) で C# を出す
- そのあと、「AST(JSON) を正式な中間表現にするならどう設計するか」（ポリモーフィック対応）を一緒に設計する
この順番で進めるのがきれいだと思いますが、どうしましょうか。


## プロンプト２
ご提案のとおりJSONはログ用とのみして、パーサーが出力したAST型をそのまま使った場合、下記のようにC＃のコードが出力されるようになりました！
```cs:
=== C# Source ===
using System;

namespace BubbleSort
{
    /// <summary>Program</summary>
    public class ProgramType
    {
        /// <summary>Main</summary>
        /// <param name="args">引数</param>
        static void main(string[] args)
        {
            /// <summary>array</summary>
            int[] array = new int[] { 15, 13, 9, 6, 4, 1 };
            for (int i = 0; i < array.Length; i++)
            {
                consoleOut(array[i]);
            }
        }
        
        /// <param name="array">配列</param>
        public void bubbleSort(int[] array)
        {
            /// <summary>i</summary>
            int outer = 0;
            while (outer < array.Length)
            {
                /// <summary>j</summary>
                int inner = 0;
                while (inner < array.Length - outer - 1)
                {
                    if (array[inner] > array[inner + 1])
                    {
                        /// <summary>temp</summary>
                        int temp = 配列[内側];
                        array[inner] = array[inner + 1];
                        array[inner + 1] = temp;
                    }
                    inner++;
                }
                outer++;
            }
        }
        
        /// <summary>ConsoleOut</summary>
        /// <param name="dispStr">引数2</param>
        static void consoleOut(string dispStr)
        {
        }
        
    }
}
```
ここからは細かい話ですがconsoleOutに中身が出力されていないようです。これはなぜでしょう？

## 生成レスポンス２

ここまで来たのは本当に大きな前進ですね。
そして consoleOut メソッドだけ中身が空になる理由 は、ログと AST の構造から 完全に説明できます。
結論から言うと：

🎯 原因：ParseMethodBody("コンソール表示する") がステートメントを 1 行も認識していないため

🎉 まとめ
| 現象|原因|対策| 
|:-|:-|:-|
| consoleOut が空 | □コンソール.一行表示する がパーサーに認識されていない|正規表現を追加して拾う  | 
| Body が空 | ParseMethodBody が 1 行もマッチしていない | 呼び出しパターンを追加 | 
| C# が空 |AST.Body が空| パーサー修正で解決 | 



mylifewithviolinさん、ここまで来ると Re:Mind → AST → C# のパイプラインがほぼ完成 です。
consoleOut の修正を入れたら、次は：
- IfSwap の中の 配列[内側] → array[inner] の変換
- コメントの整形
- Java / VB.NET 生成器の追加
など、どんどん拡張できます。


## 第１２ステップの評価
ついにASTがいったんC#コードの生成に対応するまでに改修されました。consoleOutの中身が生成されないのは、まだインポート文に十分対応できていないためですが、それはいったん棚上げしてこのステップでASTパーサーの検証改修としてはいったんクローズします。もちろん、またASTパーサーの不具合に戻ってくることを否定するものではありません。

# おわりに
第１２ステップは以上です。上に述べましたとおり「Re:MindのASTパーサが動作するまで」のステップは完了として、次回以降は「Re:MindのC#コード生成が動作するまで」としてコードジェネレータの実装を詳しく検証・修正していきます。

ここまで読んでくださった方々に厚くお礼申し上げます。

:::note warn
生成レスポンスセクションの内容は生成AIが生成したものです。引用されているソースコードは完全には動作しない状態が含まれます。
:::

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
