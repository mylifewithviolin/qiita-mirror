# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、ASTパーサが動作するまでの検証[^2]を経て本記事はC#コードジェネレータが動作するまでの改修の第４ステップです。


# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。

# 第４ステップ
「Re:MindのASTパーサが動作するまで」の１２ステップでいったんC#のソースコードが生成されるようにはなりましたので、以降はC#コードジェネレータが正常動作することを目指しています。

## プロンプト
下記のように書き換えたGenerateExpressionは何度も呼ばれましたがexpr switch文の中でInvocationExpressionに分岐することはなく、まだstatic void consoleOutの定義が出力されないのはなぜですか？
```cs:
        private string GenerateExpression(Expression expr)
        {
            return expr switch
            {
                IdentifierExpression id => id.NameEn,
                LiteralExpression lit => lit.Value is string s ? $"\"{s}\"" : lit.Value!.ToString()!,
                BinaryExpression bin => $"{GenerateExpression(bin.Left)} {bin.Operator} {GenerateExpression(bin.Right)}",
                UnaryExpression un => $"{GenerateExpression(un.Operand)}{un.Operator}",
                MemberAccessExpression ma => $"{GenerateExpression(ma.Expression)}.{ma.MemberName}",
                ElementAccessExpression ea => $"{GenerateExpression(ea.ArrayExpression)}[{GenerateExpression(ea.IndexExpression)}]",
                InvocationExpression inv => GenerateInvocation(inv, _aliasMap),
                ArrayLiteralExpression arr => $"new {arr.ElementType}[] {{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "/* 未対応式 */"
            };
        }
```
        
## 生成レスポンス
ここは 完全に原因が特定できます。
GenerateExpression が InvocationExpression に一度も分岐しない理由は、
AST の中に「InvocationExpression が存在していない」からです。
つまり：

🎯 consoleOut メソッドの本体が「ExpressionStatement(InvocationExpression)」として AST に入っていない
だから GenerateExpression が何度呼ばれても、
InvocationExpression のケースに入ることはありません。


🔍 ログをもう一度見てください
```cs:
[ParseMethodBody] method=コンソール表示する
  line[50]: "□コンソール.一行表示する(引数2)" → "□コンソール.一行表示する(引数2)"
  line[51]: "△" → "△"
[ParseMethodBody] stmts.Count = 0
```

つまり：
- consoleOut メソッドの本体は 1 行だけ
- その行はパーサーに認識されず
- stmts.Count = 0
- AST の Body は空
- だから C# 出力も空

つまり、原因は「パーサーが consoleOut の呼び出しを拾えていない」こと
CSharpCodeGenerator の問題ではありません。
AST に InvocationExpression が存在しないので、
GenerateExpression が InvocationExpression に分岐しないのは当然です。

🔥 なぜパーサーが拾えていないのか？
あなたの ParseMethodBody の該当部分は：
```cs:
if (Regex.IsMatch(line, @"^[□■]\s*コンソール表示する"))
```

しかし実際の行は：
```
□コンソール.一行表示する(引数2)
```
つまり：
- 「コンソール表示する」ではなく
- 「コンソール.一行表示する」
なので、正規表現が完全に不一致です。

🎯 修正すべきはここ
❌ 今のコード（マッチしない）
```cs:
if (Regex.IsMatch(line, @"^[□■]\s*コンソール表示する"))
```

✔ 修正案（コンソール.一行表示する を拾う）
```cs:
if (Regex.IsMatch(line, @"^[□■]\s*コンソール\.一行表示する"))
{
    var expr = ParseConsoleWriteLineElement(line);
    stmts.Add(new ExpressionStatement { Expression = expr });
    _index++;
    continue;
}
```

✨ さらに汎用的にするなら
Re:Mind の import から「コンソール → Console」「一行表示する → WriteLine」が分かるので、
Imports を使って動的に判定するのが正しい設計です。
```cs:
if (Regex.IsMatch(line, @"^[□■]"))
{
    var expr = ParseInvocationFromImports(line);
    if (expr != null)
    {
        stmts.Add(new ExpressionStatement { Expression = expr });
        _index++;
        continue;
    }
}
```
📌 まとめ
| 現象|原因|対策| 
|:-|:-|:-|
| GenerateExpression が Invocation に入らない |AST に InvocationExpression が存在しない| パーサーで consoleOut の呼び出しを拾う | 
| consoleOut が空 | ParseMethodBody がステートメントを追加していない | 正規表現を「コンソール.一行表示する」に対応させる | 
|GenerateInvocation が呼ばれない|InvocationExpression が生成されていない| パーサー修正で解決 | 


ここを直せば consoleOut の中身が完全に生成されるようになります。
必要なら、ParseConsoleWriteLineElement の強化版も一緒に作れますよ。



## 第４ステップの評価
生成AIが提示してくる内容も即座に理解できるというわけではなく、修正内容を反映して動かしてみて意図がわかるという状況もあります。ASTパーサを介さない試作品と実装の考え方は同じ点もありますが、当然ながらそれよりは少し実装が複雑になっている面はあります。

# おわりに
第４ステップは以上です。少し収束しはじめているような気がしますが、このやりとりだけでは厳しそうな感触もあります。そろそろ人間系でのデバッグ作業を検討する時期かもしれません。

:::note warn
生成レスポンスセクションの内容は生成AIが生成したものです。引用されているソースコードは完全には動作しない状態が含まれます。
:::

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

