# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、本記事はその検証の第９ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。第６ステップの後にはサインアウトがあります。

# 第９ステップ
第４ステップでProgram.csが動作可能となりました。ただし、まだターゲット言語C#のソースコード出力にはいたらずASTをシリアライズしたJson出力もまだ不完全のようでしたので、第５ステップでその点を調整しましたところ、過去に生成されたソースの再確認応答がありましたので、第６ステップ以降はプロンプト10240文字以内の制限内での生成済ソースコードの分割提示しており、今回もその続きです。

## プロンプト
以下がParseMethodBodyの全文です。
```cs:
       private IEnumerable<Statement> ParseMethodBody(string methodNameJa)
        {
            var stmts = new List<Statement>();

            while (_index < _lines.Length)
            {
                var line = _lines[_index].Trim();

                if (line == "△") // メソッド終了
                {
                    _index++;
                    break;
                }

                // ローカル変数のJavadoc
                if (line.StartsWith("/**"))
                {
                    var javadoc = ParseJavadoc();
                    // 直後の行がローカル変数になる前提
                    var varStmt = ParseLocalVariableDeclaration(javadoc);
                    if (varStmt != null)
                    {
                        stmts.Add(varStmt);
                        continue;
                    }
                    else
                    {
                        continue;
                    }
                }

                // 〇外側 < 配列.Length の間は繰り返す → while
                if (line.StartsWith("〇") && line.Contains("の間は繰り返す"))
                {
                    var whileStmt = ParseWhileStatement(line);
                    stmts.Add(whileStmt);
                    continue;
                }

                // 〇int i=0,i<配列.Length,i++ 繰り返す → for
                if (line.StartsWith("〇int") && line.Contains("繰り返す"))
                {
                    var forStmt = ParseForStatement(line);
                    stmts.Add(forStmt);
                    _index++;
                    // for の中身1行（コンソール表示する）のみ、今回前提
                    var bodyLine = _lines[_index].Trim();
                    var expr = ParseConsoleWriteLineElement(bodyLine);
                    if (expr != null)
                    {
                        forStmt.Body.Add(new ExpressionStatement { Expression = expr });
                    }
                    // 〇ここまで
                    while (_index < _lines.Length && !_lines[_index].Trim().StartsWith("〇ここまで"))
                    {
                        _index++;
                    }
                    _index++; // 「〇ここまで」超え
                    continue;
                }

                // 呼び出し1行: □バブルソートする(配列)
                if (line.StartsWith("□バブルソートする"))
                {
                    var expr = new InvocationExpression
                    {
                        Target = new IdentifierExpression
                        {
                            NameJa = "バブルソートする",
                            NameEn = "bubbleSort"
                        }
                    };
                    expr.Arguments.Add(new IdentifierExpression
                    {
                        NameJa = "配列",
                        NameEn = "array"
                    });
                    stmts.Add(new ExpressionStatement { Expression = expr });
                    _index++;
                    continue;
                }

                // □コンソール表示する(配列[i]) のような行（他メソッドでもありうる）
                if (line.StartsWith("□コンソール表示する"))
                {
                    var expr = ParseConsoleWriteLineElement(line);
                    if (expr != null)
                    {
                        stmts.Add(new ExpressionStatement { Expression = expr });
                    }
                    _index++;
                    continue;
                }

                _index++;
            }

            return stmts;
        }
```

## 生成レスポンス
原因はかなりはっきりしていて、「デシリアライズ」ではなく「パース側（ParseMethodBody とその中で呼んでいるメソッド）」にあります。

1. まず前提の整理：デシリアライズは悪くない
出力されている JSON を見ると、すでにこの段階で Body が空になっています。
```JSON:
"Methods": [
  {
    "NameJa": "メイン",
    "NameEn": "main",
    "ReturnType": "void",
    "Modifiers": [ "static" ],
    "Javadoc": { ... },
    "Parameters": [ ... ],
    "Body": []  ← ここが最初から空
  }
]
```

つまり、
- JsonSerializer.Serialize(ast) の時点で Body が []
- JsonSerializer.Deserialize<CompilationUnit>(json) をしても、JSON どおり Body.Count == 0
なので、「ノードリストが要素数 0 になる」原因は 100% パーサー側 です。

2. ParseMethod → ParseMethodBody の流れ
ParseMethod は正しくメソッド宣言をパースして、最後にこうしています。
_index++; // メソッドヘッダを進める

// 本体をパース
```cs:
method.Body.AddRange(ParseMethodBody(nameJa));
```

つまり、本体はすべて ParseMethodBody の責任です。

3. ParseMethodBody がやっていること
貼っていただいた ParseMethodBody をざっくり言い換えると：
```cs:
while (_index < _lines.Length)
{
    line = _lines[_index].Trim();

    if (line == "△") メソッド終端として break;

    if (line.StartsWith("/**")) {
        // ローカル変数のJavadoc → ParseLocalVariableDeclaration(javadoc)
    }

    if (line.StartsWith("〇") && line.Contains("の間は繰り返す")) {
        // while 文扱い
    }

    if (line.StartsWith("〇int") && line.Contains("繰り返す")) {
        // for 文扱い（中の1行だけ特別処理）
    }

    if (line.StartsWith("□バブルソートする")) { ... }

    if (line.StartsWith("□コンソール表示する")) { ... }

    _index++;
}
```

このどれにもヒットしなければ、単に _index++ してスキップして終わり、
stmts は最後まで空のまま返されます。

4. どこでヒットが落ちているのか（メインメソッドを例に）
メインメソッドの本体はこの部分です：
```
        /** array */
        ・int[] 配列 = 15,13,9,6,4,1
       
        /** index */
        □バブルソートする(配列)

        〇int i=0,i<配列.Length,i++ 繰り返す
        　□コンソール表示する(配列[i])
        〇ここまで
```

これに対して ParseMethodBody は本来こう動くはずです。
- /** array */
→ StartsWith("/**") にヒット
→ ParseJavadoc() → その直後の行を ParseLocalVariableDeclaration
→ stmts.Add(LocalVariableDeclaration) されるはず
- □バブルソートする(配列)
→ StartsWith("□バブルソートする") にヒット
→ InvocationExpression を生成して stmts.Add(...)
- 〇int i=0,i<配列.Length,i++ 繰り返す
→ StartsWith("〇int") && Contains("繰り返す") にヒット
→ ParseForStatement → forStmt.Body に ExpressionStatement(Console.WriteLine(...))
→ stmts.Add(forStmt)
つまり、本来なら Body は 3 つ以上の Statement で埋まるはず です。
それが空になっているということは、
- ParseLocalVariableDeclaration(javadoc) が null を返している
- ParseWhileStatement(line) / ParseForStatement(line) / ParseConsoleWriteLineElement(...) もパターンマッチに失敗している
- その結果、どの if でも stmts.Add(...) が呼ばれない
のどれか（あるいくつか）です。

5. 特に怪しいポイント
今の情報だけで「確実にここがバグ」と言えるところを挙げると：
- ParseLocalVariableDeclaration(javadoc) が null を返している可能性が高い
- そうだとするとローカル変数宣言が一切 AST に入らない
- その結果、/** array */ / /** index */ が丸ごと捨てられている
- 行パターンの判定が Re:Mind 実際の文字列と微妙にズレている
- 全角・半角、カンマやスペースの数、< と ＜ など
- 正規表現や StartsWith の文字列が厳しすぎると一気に全部すり抜けます
- ParseForStatement の中で _index を進めすぎたり、戻さなかったりしている
- ただし、これだけではメインメソッドの Body が完全に空になる説明にはならないので、
「ローカル変数とバブルソート呼び出しが AST に出ていない」ことから、
やはり 1・2 が本丸だと思います。

6. どう切り分けるといいか（デバッグ方針）
ParseMethodBody に 3 行ほどログを入れると一気に原因が見えます。
```cs:
private IEnumerable<Statement> ParseMethodBody(string methodNameJa)
{
    var stmts = new List<Statement>();

    Console.WriteLine($"[ParseMethodBody] method={methodNameJa}");

    while (_index < _lines.Length)
    {
        var raw = _lines[_index];
        var line = raw.Trim();

        Console.WriteLine($"  line[{_index}]: \"{raw}\" → Trim: \"{line}\"");

        if (line == "△")
        {
            Console.WriteLine("  -> メソッド終端");
            _index++;
            break;
        }

        if (line.StartsWith("/**"))
        {
            Console.WriteLine("  -> ローカルJavadoc検出");
            var javadoc = ParseJavadoc();
            var varStmt = ParseLocalVariableDeclaration(javadoc);
            Console.WriteLine($"    ParseLocalVariableDeclaration => {(varStmt == null ? "null" : "OK")}");
            if (varStmt != null)
            {
                stmts.Add(varStmt);
                continue;
            }
            else
            {
                continue;
            }
        }

        // 以下の if でも同様にログを入れていく
        ...
    }

    Console.WriteLine($"[ParseMethodBody] stmts.Count = {stmts.Count}");
    return stmts;
}
```

これで、
- そもそもどの行が ParseMethodBody に見えているか
- どの if に入っているか／入っていないか
- ParseLocalVariableDeclaration などの戻り値が null かどうか
が一目で分かります。

7. 直感的なまとめ
- デシリアライズは正しい。空なのは JSON 側の Body がそもそも空だから。
- JSON の Body が空なのは、ParseMethodBody がどの行も Statement として認識できていないから。
- 特に、
- ローカル変数（ParseLocalVariableDeclaration）
- □バブルソートする(配列) のマッチ
- 〇int i=0,...繰り返す のマッチ
あたりが実際にヒットしていないのが原因と考えられる。

もしよければ、次は
- ParseLocalVariableDeclaration
- ParseConsoleWriteLineElement
- ParseForStatement
あたりの実装を部分的に見せてもらえれば、
「この正規表現（または StartsWith の文字列）がズレているので、こう直すと Body が埋まる」というところまで具体的に詰められます。


## 第９ステップの評価
途中のログ出力を追記してくださいはのちに対応することとなるのですが、要求された生成済のコードの再確認に引き続き進行します。

# おわりに
第９ステップは以上です。次回の方向性は上記記載のとおりです。

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
