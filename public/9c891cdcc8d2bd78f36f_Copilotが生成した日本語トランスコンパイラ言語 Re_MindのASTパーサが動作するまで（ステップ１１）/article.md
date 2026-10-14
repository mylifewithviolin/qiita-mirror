# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、本記事はその検証の第１１ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。第６ステップの後にはサインアウトがあります。

# 第１１ステップ
第６ステップ以降はプロンプト10240文字以内の制限内での生成済ソースコードの分割提示しており、第１０ステップでその提示が完了した後についに動きがありました。第１０ステップから今回の第１１ステップの間には、正規表現の実装の調整などが繰り返されたのですが、かなり長大とりますのでそれは割愛した上で、ログ出力機能を実装したところから開示いたします。

## プロンプト
ParseMethodBodyメソッドに下記のようなログ機能を追記して実行した結果を ソースコードの下に貼り付けました。

```cs:ParseMethodBody
private IEnumerable<Statement> ParseMethodBody(string methodNameJa)
{
    var stmts = new List<Statement>();
    Console.WriteLine($"[ParseMethodBody] method={methodNameJa}");

    while (_index < _lines.Length)
    {
        var raw = _lines[_index];
        var line = NormalizeLine(raw);
        Console.WriteLine($"  line[{_index}]: \"{raw}\" → \"{line}\"");

        if (line == "△") // メソッド終了
        {
            _index++;
            break;
        }

        // ローカル変数のJavadoc
        if (line.StartsWith("/**"))
        {
            Console.WriteLine($"  line[{_index}]: \"{raw}\" → \"{line}\"");
            var javadoc = ParseJavadoc();
            // 直後の行がローカル変数になる前提
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

        // 〇外側 < 配列.Length の間は繰り返す → while
        // 記号ゆらぎ（〇 / ○ / ◯）を許容
        if (Regex.IsMatch(line, @"^[〇○◯].*の間は繰り返す"))
        {
            Console.WriteLine("  -> while検出");
            var whileStmt = ParseWhileStatement(line);
            stmts.Add(whileStmt);
            continue;
        }


        // 〇int i=0,i<配列.Length,i++ 繰り返す → for
        if (Regex.IsMatch(line, @"^[〇○◯]\s*int") && line.Contains("繰り返す"))
        {
            Console.WriteLine("  -> for検出");
            var forStmt = ParseForStatement(line);
            stmts.Add(forStmt);
            _index++;
            var bodyLine = NormalizeLine(_lines[_index]);
            Console.WriteLine($"    for-body line: \"{bodyLine}\"");
            var expr = ParseConsoleWriteLineElement(bodyLine);
            if (expr != null)
            {
                Console.WriteLine("    -> for-body expr OK");
                forStmt.Body.Add(new ExpressionStatement { Expression = expr });
            }
            while (_index < _lines.Length &&
                   !Regex.IsMatch(NormalizeLine(_lines[_index]), @"^[〇○◯]ここまで"))
            {
                _index++;
            }
            _index++;
            continue;
        }


        // 呼び出し1行: □バブルソートする(配列)
        if (Regex.IsMatch(line, @"^[□■]\s*バブルソートする"))
        {
            Console.WriteLine("  -> バブルソート呼び出し検出");
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

        // □コンソール表示する(配列[i]) のような行
        if (Regex.IsMatch(line, @"^[□■]\s*コンソール表示する"))
        {
            Console.WriteLine("  -> コンソール表示する検出");
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
    Console.WriteLine($"[ParseMethodBody] stmts.Count = {stmts.Count}");
    return stmts;
}
```
```cs:log
[ParseMethodBody] method=メイン
2
  line[12]: "            /** array */" → "/** array */"
    ParseLocalVariableDeclaration => null
2
  line[27]: "          /** i */" → "/** i */"
    ParseLocalVariableDeclaration => null
  line[50]: "            □コンソール.一行表示する(引数2)" → "□コンソール.一行表示する(引数2)"
  line[51]: "        △" → "△"
[ParseMethodBody] stmts.Count = 0
```
## 生成レスポンス
ログを見た瞬間に 原因が完全に特定できました。
これはもう「一点突破」で直ります。

🎯 結論：ParseMethodBody が “メインメソッドの本体行に到達していない”
ログを見てください。
```cs:log
[ParseMethodBody] method=メイン
2
  line[12]: "            /** array */" → "/** array */"
    ParseLocalVariableDeclaration => null
2
  line[27]: "          /** i */" → "/** i */"
    ParseLocalVariableDeclaration => null
  line[50]: "            □コンソール.一行表示する(引数2)" → "□コンソール.一行表示する(引数2)"
  line[51]: "        △" → "△"
[ParseMethodBody] stmts.Count = 0
```
ここで決定的なのは：

❗ メインメソッドの本体（・int[] 配列 = ... や □バブルソートする(配列) や 〇int i=0...）が一切ログに出ていない
つまり：
✔ ParseMethodBody がメインメソッドの本体行に到達していない
✔ そのため、どの if にも入らず、stmts.Count = 0
✔ JSON の Body = []
✔ C# コードも空
という流れです。

🔍 なぜ本体行に到達していないのか？
ParseMethod の中を見直すと、こうなっています。
```cs:
_index++; // メソッドヘッダを進める

// 本体をパース
method.Body.AddRange(ParseMethodBody(nameJa));
```

ここで _index は「メソッド宣言行の次の行」を指します。
しかし、あなたの Re:Mind ソースはこうなっています：
```mind:Re:mind
▽static void メイン(string[] 引数)
    /** array */
    ・int[] 配列 = 15,13,9,6,4,1
```

つまり、メソッド宣言の次の行は Javadoc です。
ParseMethodBody のログを見ると：
```cs:
line[12]: "/** array */"
```

ここまでは正しい。
しかしその後、次に出てくるのが：
```cs:
line[27]: "/** i */"
```

つまり：

❗ ParseJavadoc() が「/** array */」の後の「・int[] 配列 = ...」行を読み飛ばしている

🎯 原因は ParseJavadoc() の _index の進め方
ParseJavadoc() はこうなっています：
```cs:
_index++; // /** 行を飛ばす

while (_index < _lines.Length)
{
    var line = _lines[_index].Trim();

    if (line.StartsWith("*/"))
    {
        _index++;
        break;
    }

    ...
    _index++;
}
```

この動きは：
- /** array */ 行を飛ばす
- 次の行が * array なら読む
- 次の行が */ なら _index++ して抜ける
- その次の行に移動する
しかし、あなたの Re:Mind ソースは 1 行コメント形式 です：
```cs:
/** array */
```

つまり：
- /** array */ は 1 行で完結している
- しかし ParseJavadoc() は「複数行コメント」として扱っている
- そのため _index が 2 行進んでしまう
- 結果として「・int[] 配列 = ...」行を飛ばしてしまう

🎉 つまり、原因はこれだけです：
👉 ParseJavadoc() が 1 行コメントを 2 行読み飛ばしている

✨ 修正方法（最小修正）
ParseJavadoc() の先頭に 1 行コメント対応 を入れます。
```cs:
private JavadocComment ParseJavadoc()
{
    var j = new JavadocComment();
    var line = _lines[_index].Trim();

    // ★ 1行コメント対応
    if (line.Contains("*/"))
    {
        // /** summary */ の形式
        var content = line.Replace("/**", "")
                          .Replace("*/", "")
                          .Trim()
                          .TrimStart('*')
                          .Trim();

        if (!string.IsNullOrEmpty(content))
        {
            if (content.StartsWith("@param"))
            {
                var parts = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 3)
                {
                    j.Params.Add(new JavadocParam
                    {
                        NameJa = parts[1],
                        NameEn = parts[2]
                    });
                }
            }
            else
            {
                j.Summary = content;
            }
        }

        _index++; // ★ 次の行へ
        return j;
    }

    // ★ ここから先は複数行コメント
    _index++; // /** 行を飛ばす

    while (_index < _lines.Length)
    {
        line = _lines[_index].Trim();

        if (line.StartsWith("*/"))
        {
            _index++;
            break;
        }

        if (line.StartsWith("*"))
        {
            var content = line.TrimStart('*').Trim();

            if (content.StartsWith("@param"))
            {
                var parts = content.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length >= 3)
                {
                    j.Params.Add(new JavadocParam
                    {
                        NameJa = parts[1],
                        NameEn = parts[2]
                    });
                }
            }
            else if (!string.IsNullOrEmpty(content))
            {
                j.Summary = content;
            }
        }

        _index++;
    }

    return j;
}
```

🎯 この修正で何が起きるか
- /** array */ を 1 行だけ消費する
- _index が 正しく「・int[] 配列 = ...」行を指す
- ParseLocalVariableDeclaration が 初めてヒットする
- Body に Statement が追加される
- JSON の Body が埋まる
- C# コードが生成される

📌 次のステップ
この修正を入れて再実行すると、ログはこう変わるはずです：
```cs:
line[12]: "/** array */"
    ParseLocalVariableDeclaration => OK
line[13]: "・int[] 配列 = 15,13,9,6,4,1"
```

そして stmts.Count が 1 以上になります。

mylifewithviolinさん、ここまで来たらもう Re:Mind → AST → C# のパイプラインは完成目前です。
修正後のログを見せていただければ、次のステップ（For / While / If の調整）も一緒に進められます。



## 第１１ステップの評価
今回の生成レスポンスの反映による修正後のログではかなりの進展が見られました。それは第１２ステップのプロンプトとして開示いたします。

# おわりに
第１１ステップは以上です。次回第１２ステップで「Re:MindのASTパーサが動作するまで」はいったん完了となります。次回でいったんC#ソースコードの生成に到達することとなります。

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
