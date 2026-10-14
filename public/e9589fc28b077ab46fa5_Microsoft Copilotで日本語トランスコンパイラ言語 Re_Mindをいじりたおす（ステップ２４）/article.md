# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりまして、これがなかなか難儀でしたが、最後の第２２ステップで有益なASTについての情報を生成してもらえたので、本記事はその続きの第２４ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第２３ステップの後にはサインアウトがあります。

# 第２４ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにしましたところ、比較的正常な結果が返るようになりました。第１９，２０，２１ステップの生成レスポンスで、Copilotが次のステップのご提案として「Re:Mind の AST（抽象構文木）風の構造化表示」ということを提案したので第２２ステップでそれをやってみることにしました。今回はだめもとでそのASTを生成するサンプル実装をC#で生成することを試みます。

## プロンプト
下記のソースコードは定番アルゴリズム：バブルソートを「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2025 Lv1.2 https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b に基づき生成したものです。
```mind:Re:mind
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
このソースからJava / C# / VB.NETのソースへトランスコンパイルしていただいた後、下記のASTを作成していただきました。

Re:Mind バブルソートの AST 風構造（JSON 風）
対象ソース：BubbleSort 名前空間のバブルソート版 Re:Mind。

このASTのJSONは長大であるため再提示できないのですが、前回この AST から
Java / C# / VB.NET コードを再生成する手順（マッピングルール）を明文化していただきました。

今回はこのASTを生成するAST生成器の実装ソースコードをC#で展開することは可能ですか？


## 生成レスポンス
はい、可能です。
ここでは「バブルソート版 Re:Mind ソース」を対象にした AST 生成器のプロトタイプ実装（C#） を示します。
- 対応範囲は今回のバブルソートに出てくる構文に絞った ミニフロントエンド です。
- 実運用レベルの完全パーサではなく、「Re:Mind → AST モデル」の関係が明確になることを優先しています。

1. AST モデル定義（C#クラス群）
まずは、前回の JSON 風 AST をそのままクラス化したモデルです。

```cs:C#
using System;
using System.Collections.Generic;

namespace ReMindAst
{
    // ベースノード
    public abstract class AstNode
    {
    }

    // ルート
    public class CompilationUnit : AstNode
    {
        public List<NamespaceDeclaration> Namespaces { get; } = new();
        public List<ImportDeclaration> Imports { get; } = new();
    }

    public class NamespaceDeclaration : AstNode
    {
        public string Name { get; set; } = "";
        public List<ClassDeclaration> Classes { get; } = new();
    }

    public class ClassDeclaration : AstNode
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = ""; // transpiledName
        public List<string> Modifiers { get; } = new();
        public JavadocComment? Javadoc { get; set; }
        public List<MethodDeclaration> Methods { get; } = new();
    }

    public class JavadocComment
    {
        public string? Summary { get; set; }
        public List<JavadocParam> Params { get; } = new();
    }

    public class JavadocParam
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    public class MethodDeclaration : AstNode
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public string ReturnType { get; set; } = "void";
        public List<string> Modifiers { get; } = new();
        public JavadocComment? Javadoc { get; set; }
        public List<Parameter> Parameters { get; } = new();
        public List<Statement> Body { get; } = new();
    }

    public class Parameter : AstNode
    {
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    // --- ステートメント基底 ---

    public abstract class Statement : AstNode
    {
    }

    public class LocalVariableDeclaration : Statement
    {
        public JavadocComment? Javadoc { get; set; }
        public string Type { get; set; } = "";
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
        public Expression? Initializer { get; set; }
    }

    public class ExpressionStatement : Statement
    {
        public Expression Expression { get; set; } = null!;
    }

    public class ForStatement : Statement
    {
        public LocalVariableDeclaration? Initializer { get; set; }
        public Expression? Condition { get; set; }
        public Expression? Iterator { get; set; }
        public List<Statement> Body { get; } = new();
    }

    public class WhileStatement : Statement
    {
        public Expression Condition { get; set; } = null!;
        public List<Statement> Body { get; } = new();
    }

    public class IfStatement : Statement
    {
        public Expression Condition { get; set; } = null!;
        public List<Statement> ThenBody { get; } = new();
        public List<Statement> ElseBody { get; } = new();
    }

    public class AssignmentStatement : Statement
    {
        public Expression Left { get; set; } = null!;
        public Expression Right { get; set; } = null!;
    }

    // --- 式基底 ---

    public abstract class Expression : AstNode
    {
    }

    public class IdentifierExpression : Expression
    {
        public string NameJa { get; set; } = "";
        public string NameEn { get; set; } = "";
    }

    public class LiteralExpression : Expression
    {
        public object? Value { get; set; }
    }

    public class BinaryExpression : Expression
    {
        public string Operator { get; set; } = "";
        public Expression Left { get; set; } = null!;
        public Expression Right { get; set; } = null!;
    }

    public class UnaryExpression : Expression
    {
        public string Operator { get; set; } = "";
        public Expression Operand { get; set; } = null!;
    }

    public class MemberAccessExpression : Expression
    {
        public Expression Expression { get; set; } = null!;
        public string MemberName { get; set; } = "";
    }

    public class ElementAccessExpression : Expression
    {
        public Expression ArrayExpression { get; set; } = null!;
        public Expression IndexExpression { get; set; } = null!;
    }

    public class InvocationExpression : Expression
    {
        public Expression Target { get; set; } = null!;
        public List<Expression> Arguments { get; } = new();
    }

    public class ArrayLiteralExpression : Expression
    {
        public string ElementType { get; set; } = "";
        public List<Expression> Elements { get; } = new();
    }

    // --- import / System.Console マッピング ---

    public class ImportDeclaration : AstNode
    {
        public string Name { get; set; } = "";
        public List<AliasClass> AliasClasses { get; } = new();
    }

    public class AliasClass
    {
        public string OriginalName { get; set; } = "";
        public string TranspiledName { get; set; } = "";
        public List<AliasMember> Members { get; } = new();
    }

    public class AliasMember
    {
        public string OriginalName { get; set; } = "";
        public string TranspiledName { get; set; } = "";
        public List<Parameter> Parameters { get; } = new();
    }
}
```
2. 超シンプルな Re:Mind バブルソート専用パーサ
ここからは「今回のバブルソートの書式にだけ通用する」ことを前提にした、行ベースの簡易パーサです。
- 正規表現＋前後文脈で最低限の情報を抜き出します。
- 実装対象：
- 名前空間
- クラス
- メインメソッド
- バブルソートする メソッド
- コンソール表示する メソッド
- ローカル変数宣言
- while / for（今回のフォーマット固定）
- if / assignment / 呼び出し

```cs:C#
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using ReMindAst;

namespace ReMindParser
{
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

## 第２４ステップの評価
どんな生成レスポンスがあるかまったく予想していませんでしたが、ひとつのトランスコンパイラ言語の一部仕様の（かなりRe:Mindの仕様に寄せた）AST生成器実装のテンプレとして超大量の出力があって驚きました。この実装の細かい妥当性はまだ検証できませんので、現状有姿の参考情報という扱いでお願いします。現在わたしの方で開発中の実装はASTに明確には対応していません。参考情報として非常に有益のように受け止めております。他の方がASTベースで実装されることをさまたげるものでもありません。

# おわりに
第２４ステップは以上です。Re:Mindのアドベントカレンダーの枠としては第２２ステップで完了しましたが、Mindのアドベントカレンダーのシリーズ２の枠が少し空いていますので、間借りさせていただきました。
## 目次
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
