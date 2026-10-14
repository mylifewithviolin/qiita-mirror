# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、本記事はその検証の第１０ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。第６ステップの後にはサインアウトがあります。

# 第１０ステップ
第６ステップ以降はプロンプト10240文字以内の制限内での生成済ソースコードの分割提示しており、今回もその続きです。今回で再提示はいったん完了します。

## プロンプト
残りの関数を10240文字の制限内で入るだけ、下記に示します。
```cs:
        private LocalVariableDeclaration? ParseLocalVariableDeclaration(JavadocComment javadoc)
        {
            if (_index >= _lines.Length) return null;

            var line = _lines[_index].Trim();
            // 例: ・int[] 配列 = 15,13,9,6,4,1
            //     ・int 外側 = 0
            var m = Regex.Match(line, @"・(?<type>[a-zA-Z\[\]]+)\s+(?<nameJa>\S+)\s*=\s*(?<rhs>.+)");
            if (!m.Success)
            {
                _index++;
                return null;
            }

            var type = m.Groups["type"].Value;
            var nameJa = m.Groups["nameJa"].Value;
            var rhs = m.Groups["rhs"].Value.Trim();

            Expression initializer;

            if (rhs.Contains(","))
            {
                // 配列のようなリテラル（今回: int[] 配列）
                var arr = new ArrayLiteralExpression
                {
                    ElementType = "int"
                };
                var nums = rhs.Split(',').Select(s => s.Trim());
                foreach (var n in nums)
                {
                    if (int.TryParse(n, out int v))
                    {
                        arr.Elements.Add(new LiteralExpression { Value = v });
                    }
                }
                initializer = arr;
            }
            else if (int.TryParse(rhs, out int v))
            {
                initializer = new LiteralExpression { Value = v };
            }
            else
            {
                // 簡易対応
                initializer = new IdentifierExpression { NameJa = rhs, NameEn = MapIdentifierName(rhs) };
            }

            var decl = new LocalVariableDeclaration
            {
                Javadoc = javadoc,
                Type = type,
                NameJa = nameJa,
                NameEn = MapIdentifierName(nameJa),
                Initializer = initializer
            };

            _index++;
            return decl;
        }

        private WhileStatement ParseWhileStatement(string line)
        {
            // 〇外側 < 配列.Length の間は繰り返す
            var condPart = line.TrimStart('〇').Replace("の間は繰り返す", "").Trim();
            var cond = ParseBinaryCondition(condPart);

            var ws = new WhileStatement
            {
                Condition = cond
            };

            _index++;

            // 本体を読み取る（〇ここまでまで）
            while (_index < _lines.Length)
            {
                var cur = _lines[_index].Trim();
                if (cur.StartsWith("〇ここまで"))
                {
                    _index++;
                    break;
                }

                if (cur.StartsWith("/**"))
                {
                    var j = ParseJavadoc();
                    var decl = ParseLocalVariableDeclaration(j);
                    if (decl != null)
                    {
                        ws.Body.Add(decl);
                        continue;
                    }
                }
                else if (cur.StartsWith("〇") && cur.Contains("の間は繰り返す"))
                {
                    // 内側 while
                    var innerWhile = ParseWhileStatement(cur);
                    ws.Body.Add(innerWhile);
                    continue;
                }
                else if (cur.StartsWith("◇配列[内側] > 配列[内側 + 1] の場合"))
                {
                    var ifStmt = ParseIfSwapBlock();
                    ws.Body.Add(ifStmt);
                    continue;
                }
                else if (cur.StartsWith("□外側++"))
                {
                    var expr = new UnaryExpression
                    {
                        Operator = "++",
                        Operand = new IdentifierExpression
                        {
                            NameJa = "外側",
                            NameEn = "outer"
                        }
                    };
                    ws.Body.Add(new ExpressionStatement { Expression = expr });
                    _index++;
                    continue;
                }
                else if (cur.StartsWith("□内側++"))
                {
                    var expr = new UnaryExpression
                    {
                        Operator = "++",
                        Operand = new IdentifierExpression
                        {
                            NameJa = "内側",
                            NameEn = "inner"
                        }
                    };
                    ws.Body.Add(new ExpressionStatement { Expression = expr });
                    _index++;
                    continue;
                }
                else
                {
                    _index++;
                }
            }

            return ws;
        }

        private ForStatement ParseForStatement(string line)
        {
            // 〇int i=0,i<配列.Length,i++ 繰り返す
            var body = line.TrimStart('〇').Replace("繰り返す", "").Trim();
            // int i=0,i<配列.Length,i++
            var parts = body.Split(',');

            // 初期化: int i=0
            var initPart = parts[0].Trim();
            var mInit = Regex.Match(initPart, @"int\s+(?<name>\w+)\s*=\s*(?<value>\d+)");
            var initializer = new LocalVariableDeclaration
            {
                Type = "int",
                NameJa = mInit.Groups["name"].Value,
                NameEn = mInit.Groups["name"].Value,
                Initializer = new LiteralExpression { Value = int.Parse(mInit.Groups["value"].Value) }
            };

            // 条件: i<配列.Length
            var condPart = parts[1].Trim();
            var condition = ParseBinaryCondition(condPart);

            // 反復: i++
            var iterPart = parts[2].Trim();
            var iterExpr = new UnaryExpression
            {
                Operator = "++",
                Operand = new IdentifierExpression
                {
                    NameJa = "i",
                    NameEn = "i"
                }
            };

            return new ForStatement
            {
                Initializer = initializer,
                Condition = condition,
                Iterator = iterExpr
            };
        }

        private Expression ParseBinaryCondition(string condPart)
        {
            // かなり固定フォーマットに依存: 例 「外側 < 配列.Length」/「内側 < 配列.Length - 外側 - 1」/「i<配列.Length」
            condPart = condPart.Replace(" ", "");

            // 不等号で切る簡易版
            if (condPart.Contains("<="))
            {
                var parts = condPart.Split(new[] { "<=" }, StringSplitOptions.None);
                return new BinaryExpression
                {
                    Operator = "<=",
                    Left = ParseSimpleExpression(parts[0]),
                    Right = ParseSimpleExpression(parts[1])
                };
            }
            if (condPart.Contains("<"))
            {
                var parts = condPart.Split('<');
                return new BinaryExpression
                {
                    Operator = "<",
                    Left = ParseSimpleExpression(parts[0]),
                    Right = ParseSimpleExpression(parts[1])
                };
            }

            throw new NotSupportedException("この条件は簡易パーサでは未対応です: " + condPart);
        }

        private Expression ParseSimpleExpression(string text)
        {
            // 配列.Length - 外側 - 1 のようなものも来るので、ここも簡易。
            if (int.TryParse(text, out var n))
            {
                return new LiteralExpression { Value = n };
            }

            if (text.Contains("配列.Length"))
            {
                // 配列.Length - 外側 - 1 など
                // ここでは BinaryExpression ネストを手書き
                // 今回用途に特化
                if (text == "配列.Length")
                {
                    return new MemberAccessExpression
                    {
                        Expression = new IdentifierExpression
                        {
                            NameJa = "配列",
                            NameEn = "array"
                        },
                        MemberName = "Length"
                    };
                }

                // 配列.Length-外側-1
                var replaced = text.Replace("配列.Length", "L");
                var tokens = replaced.Split('-'); // L,外側,1
                Expression expr = new MemberAccessExpression
                {
                    Expression = new IdentifierExpression
                    {
                        NameJa = "配列",
                        NameEn = "array"
                    },
                    MemberName = "Length"
                };
                for (int i = 1; i < tokens.Length; i++)
                {
                    Expression right;
                    if (int.TryParse(tokens[i], out var vi))
                    {
                        right = new LiteralExpression { Value = vi };
                    }
                    else
                    {
                        right = new IdentifierExpression
                        {
                            NameJa = tokens[i],
                            NameEn = MapIdentifierName(tokens[i])
                        };
                    }
                    expr = new BinaryExpression
                    {
                        Operator = "-",
                        Left = expr,
                        Right = right
                    };
                }

                return expr;
            }

            // 単純識別子
            return new IdentifierExpression
            {
                NameJa = text,
                NameEn = MapIdentifierName(text)
            };
        }
```

## 生成レスポンス
結論から言うと：
- デシリアライズがノードを「消している」のではなく
- そもそもシリアライズ前の AST の時点で Body が空 ([])
- つまり原因は パーサー側（ParseMethodBody 周辺）にあり、JSON のプロパティ名対応やデシリアライズの問題ではない
です。

もしよければ、次の一歩として、
- ParseJavadoc の実装
- 1 回だけログ入り ParseMethodBody を走らせた結果
あたりを一緒に見て、「どの行でマッチがすり抜けているか」をピンポイントで特定していきませんか。
そこが分かれば、Body に Statement が入り始めて、一気に Re:Mind → C# が「フル AST モード」で動き出します。


## プロンプト２
ParseJavadoc()の全文です。

```cs:
       private JavadocComment ParseJavadoc()
        {
            var j = new JavadocComment();
            _index++; // /** 行を飛ばす

            while (_index < _lines.Length)
            {
                var line = _lines[_index].Trim();

                if (line.StartsWith("*/"))
                {
                    _index++;
                    break;
                }

                // * Program
                if (line.StartsWith("*"))
                {
                    var content = line.TrimStart('*').Trim();

                    if (content.StartsWith("@param"))
                    {
                        // @param 引数 args
                        var parts = content.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
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

## 生成レスポンス２
ParseJavadoc() を見せていただきありがとうございます。
この関数自体は 正常に動いています。
そして、ここまでの全コードを総合すると、Body が空になる原因は ParseJavadoc() ではなく、ParseMethodBody() の行判定ロジックにあります。
ただし、ParseJavadoc() にも 副作用として Body が空になる原因を引き起こす可能性があるポイント が 1 つだけあります。

🎯 結論
**ParseJavadoc() 自体は正しく動いているが、
ParseJavadoc() が _index を 1 行多く進めてしまうと、
直後のローカル変数行（・）をスキップしてしまう可能性がある。**
つまり：
```cs:
/** array */
・int[] 配列 = 15,13,9,6,4,1
```

この 2 行をパースするときに、
- ParseJavadoc() が */ の次の行まで進む
- その後 ParseLocalVariableDeclaration() が呼ばれる
- しかし _index がすでに「・」行を通り過ぎていると、ローカル変数がパースされない
- 結果として Body に Statement が追加されない
という現象が起きます。

## 第１０ステップの評価
この生成レスポンスの後も、詳しいソースコードの評価から正規表現の実装の調整などが繰り返されたのですが、かなり長大とりますのでそれは割愛します。

# おわりに
第１０ステップは以上です。次回はログ出力機能を実装したところから開示いたします。

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
