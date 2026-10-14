# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）開発コード名（Re:Mind）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではParserの最小版を実装します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。実装しなくなったSE向け用途を想定しています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の開始です。Parserの最小版を実装します。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前回記事で完了
### 2. Parser タスク
- 変数宣言文を解析できるようにする
- 定数宣言文を解析できるようにする
- 関数呼び出し文を解析できるようにする
- 関数宣言文を解析できるようにする
- クラス宣言文を解析できるようにする
- クラスのインスタンス生成・参照・メソッド呼び出しを解析できるようにする
- 条件分岐文（if 相当）を解析できるようにする
- 繰り返し文（while / for / do-while 相当）を解析できるようにする
- 例外処理文（try / catch / finally / throw 相当）を解析できるようにする
- `□コンソール.一行表示する` のような中核構文を解析できるようにする


## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 2 の最小タスク化プロンプト（CodeAgent 用）を作成してください。

#### 生成レスポンス１
>Phase 2（Parser）を CodeAgent で安全に・最小クレジットで進めるための「最小タスク化プロンプト」完全版を作成します。
Phase 1（Lexer）が完成しているので、ここからは 構文解析（Parser）を小さく分割して差分生成していくのが最適です。
>
>以下は Re:Mind の構文仕様（□ / ◇ / 〇 / 日本語識別子 / メンバーアクセス / 呼び出し）に完全対応したタスク分割になっています。
>
>以下のプロンプトはすべて 「既存の Parser.cs に差分として追加」する形式になっています。
これにより CodeAgent の推論量が最小になり、クレジット消費を劇的に抑えられます。
>
>① ParseIdentifier（識別子の基本）
以下は Parser の仕様です。
ParseIdentifier() の実装部分だけを既存の Parser.cs に差分として追加してください。
既存コードは保持し、必要な部分だけ生成してください。
② ParsePrimary（最小の式：識別子・数値・文字列）
ParsePrimary() の実装部分だけを既存の Parser.cs に差分として追加してください。
識別子・数値リテラル・文字列リテラルを扱う最小構造を生成してください。
既存コードは保持し、必要な部分だけ生成してください。


AI的にはきっちり反復的にプロンプトを生成していますが、本記事的には以下同様で内容割愛しています。
>③ ParseMemberAccess（コンソール.一行表示する の解析）
④ ParseInvocation（呼び出し：一行表示する(引数)）
⑤ ParseExpression（式の統合：Primary → MemberAccess → Invocation）
⑥ ParseStatement（□構文：代入・呼び出し）
⑦ ParseIf（◇構文：条件分岐）
⑧ ParseLoop（〇構文：繰り返し）
⑨ ParseBlock（{ ... } のブロック構文）
⑩ ParseCompilationUnit（最上位構造：Program.cs から呼ばれる入口）

## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 2の各タスクの実行プロンプトを逐次実行した結果、下記のソースコードが生成されました。

```cs:Parser.cs
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using ReMindAst;

namespace ReMindParser
{
    public class Parser
    {
        private readonly List<string> _tokens;
        private int _index;

        public Parser(List<string> tokens)
        {
            _tokens = tokens ?? new List<string>();
            _index = 0;
        }

        private string ParseIdentifier()
        {
            if (_index >= _tokens.Count)
            {
                throw new InvalidOperationException("Unexpected end of input while parsing identifier.");
            }

            var current = _tokens[_index];

            if (!Regex.IsMatch(current, @"^[\p{L}_][\p{L}\p{Nd}_]*$"))
            {
                throw new InvalidOperationException($"Expected identifier, got '{current}'.");
            }

            _index++;
            return current;
        }

        private string ParsePrimary()
        {
            if (_index >= _tokens.Count)
            {
                throw new InvalidOperationException("Unexpected end of input while parsing primary expression.");
            }

            var current = _tokens[_index];

            if (Regex.IsMatch(current, @"^[\p{L}_][\p{L}\p{Nd}_]*$"))
            {
                return ParseIdentifier();
            }

            if (Regex.IsMatch(current, @"^\d+$"))
            {
                _index++;
                return current;
            }

            if ((current.StartsWith("\"") && current.EndsWith("\"")) || (current.StartsWith("'") && current.EndsWith("'")))
            {
                _index++;
                return current;
            }

            throw new InvalidOperationException($"Expected primary expression, got '{current}'.");
        }

        private Expression ParseMemberAccess()
        {
            var left = ParsePrimary();

            if (_index < _tokens.Count && _tokens[_index] == ".")
            {
                _index++;
                var memberName = ParseIdentifier();

                return new MemberAccessExpression
                {
                    Expression = new IdentifierExpression
                    {
                        NameJa = left,
                        NameEn = MapIdentifierName(left)
                    },
                    MemberName = memberName
                };
            }

            return new IdentifierExpression
            {
                NameJa = left,
                NameEn = MapIdentifierName(left)
            };
        }

        private Expression ParseInvocation()
        {
            var target = ParseMemberAccess();

            if (_index < _tokens.Count && _tokens[_index] == "(")
            {
                _index++;

                var arguments = new List<Expression>();
                while (_index < _tokens.Count && _tokens[_index] != ")")
                {
                    arguments.Add(ParseMemberAccess());
                    if (_index < _tokens.Count && _tokens[_index] == ",")
                    {
                        _index++;
                    }
                }

                if (_index >= _tokens.Count)
                {
                    throw new InvalidOperationException("Unterminated invocation.");
                }

                _index++; // consume )

                return new InvocationExpression
                {
                    Target = target,
                    Arguments = { }
                };
            }

            return target;
        }

        private Expression ParseExpression()
        {
            return ParseInvocation();
        }

        private Statement ParseStatement()
        {
            if (_index >= _tokens.Count)
            {
                throw new InvalidOperationException("Unexpected end of input while parsing statement.");
            }

            if (_tokens[_index] == "□")
            {
                _index++;
                var expr = ParseExpression();

                return new ExpressionStatement
                {
                    Expression = expr
                };
            }

            if (_tokens[_index] == "◇")
            {
                _index++;
                var condition = ParseExpression();

                if (_index >= _tokens.Count || _tokens[_index] != "の場合")
                {
                    throw new InvalidOperationException("Expected 'の場合' after if condition.");
                }

                _index++;

                var thenBody = new List<Statement>();
                while (_index < _tokens.Count && _tokens[_index] != "◇ここまで" && _tokens[_index] != "他に" && _tokens[_index] != "ここまで")
                {
                    thenBody.Add(ParseStatement());
                }

                var elseBody = new List<Statement>();
                if (_index < _tokens.Count && _tokens[_index] == "他に")
                {
                    _index++;
                    while (_index < _tokens.Count && _tokens[_index] != "◇ここまで" && _tokens[_index] != "ここまで")
                    {
                        elseBody.Add(ParseStatement());
                    }
                }

                if (_index < _tokens.Count && (_tokens[_index] == "◇ここまで" || _tokens[_index] == "ここまで"))
                {
                    _index++;
                }

                return new IfStatement
                {
                    Condition = condition,
                    ThenBody = thenBody,
                    ElseBody = elseBody
                };
            }

            if (_tokens[_index] == "〇")
            {
                _index++;
                var condition = ParseExpression();

                var body = new List<Statement>();
                while (_index < _tokens.Count && _tokens[_index] != "〇ここまで" && _tokens[_index] != "ここまで")
                {
                    body.Add(ParseStatement());
                }

                if (_index < _tokens.Count && (_tokens[_index] == "〇ここまで" || _tokens[_index] == "ここまで"))
                {
                    _index++;
                }

                return new WhileStatement
                {
                    Condition = condition,
                    Body = body
                };
            }

            if (_tokens[_index] == "{")
            {
                _index++;
                var statements = new List<Statement>();

                while (_index < _tokens.Count && _tokens[_index] != "}")
                {
                    statements.Add(ParseStatement());
                }

                if (_index >= _tokens.Count)
                {
                    throw new InvalidOperationException("Unterminated block.");
                }

                _index++; // consume }
                return new BlockStatement
                {
                    Statements = statements
                };
            }

            throw new InvalidOperationException($"Unsupported statement start: '{_tokens[_index]}'.");
        }

        public CompilationUnit ParseCompilationUnit()
        {
            var compilationUnit = new CompilationUnit();

            while (_index < _tokens.Count)
            {
                if (string.IsNullOrEmpty(_tokens[_index]))
                {
                    _index++;
                    continue;
                }

                var statement = ParseStatement();
                compilationUnit.Statements.Add(statement);
            }

            return compilationUnit;
        }
    }


    public class ReMindBubbleSortAstGenerator
    {
        private readonly string[] _lines;
        private int _index;

        public ReMindBubbleSortAstGenerator(string source)
        {
            _lines = source.Split(new[] { "\r\n", "\n" }, StringSplitOptions.None);
            _index = 0;
        }

        public CompilationUnit Parse()
        {
            var cu = new CompilationUnit();

            // 名前空間
            NamespaceDeclaration ns = ParseNamespace();
            cu.Namespaces.Add(ns);

            // System import は固定で追加（今回のソース前提）
            cu.Imports.Add(BuildSystemImport());

            return cu;
        }

        private NamespaceDeclaration ParseNamespace()
        {
            // ▽名前空間 BubbleSort
            var ns = new NamespaceDeclaration();

            while (_index < _lines.Length)
            {
                var line = _lines[_index].Trim();

                if (line.StartsWith("▽名前空間"))
                {
                    var name = line.Replace("▽名前空間", "").Trim();
                    ns.Name = name;

                    _index++;
                    break;
                }
                _index++;
            }

            // クラスを一つだけパース（今回の前提）
            ns.Classes.Add(ParseClass());

            return ns;
        }

        private ClassDeclaration ParseClass()
        {
            var cls = new ClassDeclaration();

            JavadocComment? pendingJavadoc = null;

            while (_index < _lines.Length)
            {
                var line = _lines[_index].Trim();

                if (line.StartsWith("/**"))
                {
                    pendingJavadoc = ParseJavadoc();
                    continue;
                }

                if (line.StartsWith("▽public クラス"))
                {
                    // ▽public クラス プログラム型
                    var m = Regex.Match(line, @"▽public\s+クラス\s+(\S+)");
                    if (m.Success)
                    {
                        cls.NameJa = m.Groups[1].Value;
                        cls.NameEn = "ProgramType"; // 今回は固定マッピング
                        cls.Modifiers.Add("public");
                        cls.Javadoc = pendingJavadoc;
                        pendingJavadoc = null;
                    }
                    _index++;
                    break;
                }

                _index++;
            }

            // クラス本体のメソッドたち
            while (_index < _lines.Length)
            {
                var line = _lines[_index].Trim();

                if (line == "△") // クラス終端（今回前提）
                {
                    _index++;
                    break;
                }

                if (line.StartsWith("/**"))
                {
                    var j = ParseJavadoc();
                    // 直後に来るメソッドに付与
                    var method = ParseMethod(j);
                    if (method != null)
                    {
                        cls.Methods.Add(method);
                        continue;
                    }
                }
                else if (line.StartsWith("▽static") || line.StartsWith("▽public"))
                {
                    // Javadoc なしメソッド（例: ほぼ無い想定だが一応）
                    var method = ParseMethod(null);
                    if (method != null)
                    {
                        cls.Methods.Add(method);
                        continue;
                    }
                }
                else
                {
                    _index++;
                }
            }

            return cls;
        }

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

        private MethodDeclaration? ParseMethod(JavadocComment? javadoc)
        {
            var line = _lines[_index].Trim();

            // 例:
            // ▽static void メイン(string[] 引数)
            // ▽public void バブルソートする(int[] 配列)
            // ▽static void コンソール表示する(string 引数2)

            var m = Regex.Match(line, @"▽(?<mod>static|public)\s+void\s+(?<nameJa>\S+)\((?<paramStr>.*)\)");
            if (!m.Success)
            {
                _index++;
                return null;
            }

            var method = new MethodDeclaration
            {
                ReturnType = "void",
                Javadoc = javadoc
            };

            var mod = m.Groups["mod"].Value;
            method.Modifiers.Add(mod);

            var nameJa = m.Groups["nameJa"].Value;
            method.NameJa = nameJa;
            method.NameEn = MapMethodName(nameJa);

            var paramStr = m.Groups["paramStr"].Value.Trim();
            if (!string.IsNullOrEmpty(paramStr))
            {
                var p = ParseParameter(paramStr);
                if (p != null)
                {
                    method.Parameters.Add(p);
                }
            }

            _index++; // メソッドヘッダを進める

            // 本体をパース（今回：かなり前提に依存）
            method.Body.AddRange(ParseMethodBody(nameJa));

            return method;
        }

        private Parameter? ParseParameter(string paramStr)
        {
            // 例: "string[] 引数" / "int[] 配列" / "string 引数2"
            var parts = paramStr.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length != 2) return null;

            var type = parts[0];
            var nameJa = parts[1];

            return new Parameter
            {
                Type = type,
                NameJa = nameJa,
                NameEn = MapIdentifierName(nameJa)
            };
        }

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

        private IfStatement ParseIfSwapBlock()
        {
            // ◇配列[内側] > 配列[内側 + 1] の場合
            var ifStmt = new IfStatement();
            ifStmt.Condition = BuildSwapCondition();
            _index++;

            // /** temp */ ・int 一時 = 配列[内側] 等を順に読む
            // 今回は固定パターン前提
            // 1. Javadoc + ローカル変数宣言
            if (_lines[_index].Trim().StartsWith("/**"))
            {
                var j = ParseJavadoc();
                var decl = ParseLocalVariableDeclaration(j);
                if (decl != null)
                {
                    ifStmt.ThenBody.Add(decl);
                }
            }

            // 2. □配列[内側] = 配列[内側 + 1]
            if (_lines[_index].Trim().StartsWith("□配列[内側] = 配列[内側 + 1]"))
            {
                var assign1 = new AssignmentStatement
                {
                    Left = new ElementAccessExpression
                    {
                        ArrayExpression = new IdentifierExpression
                        {
                            NameJa = "配列",
                            NameEn = "array"
                        },
                        IndexExpression = new IdentifierExpression
                        {
                            NameJa = "内側",
                            NameEn = "inner"
                        }
                    },
                    Right = new ElementAccessExpression
                    {
                        ArrayExpression = new IdentifierExpression
                        {
                            NameJa = "配列",
                            NameEn = "array"
                        },
                        IndexExpression = new BinaryExpression
                        {
                            Operator = "+",
                            Left = new IdentifierExpression
                            {
                                NameJa = "内側",
                                NameEn = "inner"
                            },
                            Right = new LiteralExpression { Value = 1 }
                        }
                    }
                };
                ifStmt.ThenBody.Add(assign1);
                _index++;
            }

            // 3. □配列[内側 + 1] = 一時
            if (_lines[_index].Trim().StartsWith("□配列[内側 + 1] = 一時"))
            {
                var assign2 = new AssignmentStatement
                {
                    Left = new ElementAccessExpression
                    {
                        ArrayExpression = new IdentifierExpression
                        {
                            NameJa = "配列",
                            NameEn = "array"
                        },
                        IndexExpression = new BinaryExpression
                        {
                            Operator = "+",
                            Left = new IdentifierExpression
                            {
                                NameJa = "内側",
                                NameEn = "inner"
                            },
                            Right = new LiteralExpression { Value = 1 }
                        }
                    },
                    Right = new IdentifierExpression
                    {
                        NameJa = "一時",
                        NameEn = "temp"
                    }
                };
                ifStmt.ThenBody.Add(assign2);
                _index++;
            }

            // ◇ここまで
            while (_index < _lines.Length && !_lines[_index].Trim().StartsWith("◇ここまで"))
            {
                _index++;
            }
            if (_index < _lines.Length) _index++;

            return ifStmt;
        }

        private Expression BuildSwapCondition()
        {
            // 配列[内側] > 配列[内側 + 1]
            return new BinaryExpression
            {
                Operator = ">",
                Left = new ElementAccessExpression
                {
                    ArrayExpression = new IdentifierExpression
                    {
                        NameJa = "配列",
                        NameEn = "array"
                    },
                    IndexExpression = new IdentifierExpression
                    {
                        NameJa = "内側",
                        NameEn = "inner"
                    }
                },
                Right = new ElementAccessExpression
                {
                    ArrayExpression = new IdentifierExpression
                    {
                        NameJa = "配列",
                        NameEn = "array"
                    },
                    IndexExpression = new BinaryExpression
                    {
                        Operator = "+",
                        Left = new IdentifierExpression
                        {
                            NameJa = "内側",
                            NameEn = "inner"
                        },
                        Right = new LiteralExpression { Value = 1 }
                    }
                }
            };
        }

        private Expression? ParseConsoleWriteLineElement(string line)
        {
            // □コンソール表示する(配列[i]) / □コンソール表示する(配列[内側]) 等を想定
            var m = Regex.Match(line, @"□コンソール表示する\((?<content>.+)\)");
            if (!m.Success) return null;

            var content = m.Groups["content"].Value.Trim();

            Expression argExpr;

            // 配列[i] 形式
            var mArr = Regex.Match(content, @"配列\[(?<idx>.+)\]");
            if (mArr.Success)
            {
                var idx = mArr.Groups["idx"].Value.Trim();
                argExpr = new ElementAccessExpression
                {
                    ArrayExpression = new IdentifierExpression
                    {
                        NameJa = "配列",
                        NameEn = "array"
                    },
                    IndexExpression = new IdentifierExpression
                    {
                        NameJa = idx,
                        NameEn = MapIdentifierName(idx)
                    }
                };
            }
            else
            {
                // 単純文字列 or 識別子（今回: "該当なし" 等もありえるが、バブルソートでは整数のみ）
                if (content.StartsWith("\"") && content.EndsWith("\""))
                {
                    argExpr = new LiteralExpression
                    {
                        Value = content.Trim('"')
                    };
                }
                else
                {
                    argExpr = new IdentifierExpression
                    {
                        NameJa = content,
                        NameEn = MapIdentifierName(content)
                    };
                }
            }

            var target = new IdentifierExpression
            {
                NameJa = "コンソール表示する",
                NameEn = "consoleOut"
            };

            var inv = new InvocationExpression
            {
                Target = target
            };
            inv.Arguments.Add(argExpr);

            return inv;
        }

        private ImportDeclaration BuildSystemImport()
        {
            var imp = new ImportDeclaration
            {
                Name = "System"
            };

            var alias = new AliasClass
            {
                OriginalName = "コンソール",
                TranspiledName = "Console"
            };

            alias.Members.Add(new AliasMember
            {
                OriginalName = "一行表示する",
                TranspiledName = "WriteLine"
            });

            imp.AliasClasses.Add(alias);
            return imp;
        }

        // --- 日本語名 → 英語名 簡易マップ（今回のバブルソート用） ---

        private string MapMethodName(string nameJa)
        {
            return nameJa switch
            {
                "メイン" => "main",
                "バブルソートする" => "bubbleSort",
                "コンソール表示する" => "consoleOut",
                _ => nameJa
            };
        }

        private string MapIdentifierName(string nameJa)
        {
            return nameJa switch
            {
                "配列" => "array",
                "外側" => "outer",
                "内側" => "inner",
                "一時" => "temp",
                "引数" => "args",
                "引数2" => "dispStr",
                _ => nameJa
            };
        }
    }

}

```
## 本ステップの評価
わるくないと評価しています。コメントが比較的ついている箇所はCopilotが生成していた範囲[^1][^2][^3]で、コメントがついていない範囲はCodeAgentによるコードです。この辺りのコメントはいったん最小版の実装が完了したときに考えます。まだ当初の不具合解消にいたっておりませんが、急がば回れということで次回ASTの実装に進行します。

# おわりに
以上です。次回の方向性はASTの実装の実行からとなります。なるべくサンプルソースに対して実行できる状況づくりを急ぎます。

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
