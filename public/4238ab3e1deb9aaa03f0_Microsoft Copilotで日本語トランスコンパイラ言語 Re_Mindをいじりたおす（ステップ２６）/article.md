# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりまして、これがなかなか難儀でしたが、最後の第２２ステップで有益なASTについての情報を生成してもらえたので、本記事はその続きの第２４ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第２３ステップの後にはサインアウトがあります。

# 第２６ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにしましたところ、比較的正常な結果が返るようになりました。第１９，２０，２１ステップの生成レスポンスで、Copilotが次のステップのご提案として「Re:Mind の AST（抽象構文木）風の構造化表示」ということを提案したので第２２ステップでそれをやってみましたところ驚きの結果で、第２４ステップと第２５ステップではそのASTを生成するサンプル実装と後処理ターゲット言語C#へのASTからの生成処理をやってみましたので、今回はターゲット言語JavaとVB.NETへの展開の試みです。

## プロンプト
次にできること
- Java バックエンドを同じ構造で作る
- VB.NET バックエンドを作る 
では、JavaとVB.NETのバックエンドのC#のソースコードを展開してください。


## 生成レスポンス
Java / VB.NET 向けのバックエンドも、C#版と同じ AST モデルを前提にしたコードジェネレータとして実装してみます。
- すでにある IndentWriter と ReMindAst 名前空間の AST クラスを再利用
- 出力だけ Java 構文 / VB.NET 構文に切り替えます

Java バックエンド（C# 実装）
```cs:C#
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class JavaCodeGenerator
    {
        private readonly IndentWriter _w = new();

        public string Generate(CompilationUnit cu)
        {
            // imports → import System; など
            foreach (var imp in cu.Imports)
            {
                _w.WriteLine($"import {imp.Name};");
            }
            _w.WriteLine();

            // namespace → package
            foreach (var ns in cu.Namespaces)
            {
                _w.WriteLine($"package {ns.Name};");
                _w.WriteLine();

                foreach (var cls in ns.Classes)
                {
                    GenerateClass(cls);
                    _w.WriteLine();
                }
            }

            return _w.ToString();
        }

        private void GenerateClass(ClassDeclaration cls)
        {
            if (cls.Javadoc != null)
                WriteJavadoc(cls.Javadoc);

            var mods = string.Join(" ", cls.Modifiers);
            if (!string.IsNullOrEmpty(mods))
                mods += " ";

            _w.WriteLine($"{mods}class {cls.NameEn} " + "{");
            _w.Indent();

            foreach (var m in cls.Methods)
            {
                GenerateMethod(m);
                _w.WriteLine();
            }

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateMethod(MethodDeclaration m)
        {
            if (m.Javadoc != null)
                WriteJavadoc(m.Javadoc, m.NameJa);

            var mods = string.Join(" ", m.Modifiers);
            if (!string.IsNullOrEmpty(mods))
                mods += " ";

            var paramList = string.Join(", ",
                m.Parameters.Select(p => $"{MapType(p.Type)} {p.NameEn}"));

            _w.WriteLine($"{mods}{MapType(m.ReturnType)} {m.NameEn}({paramList}) " + "{");
            _w.Indent();

            foreach (var stmt in m.Body)
                GenerateStatement(stmt);

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateStatement(Statement stmt)
        {
            switch (stmt)
            {
                case LocalVariableDeclaration v:
                    GenerateLocalVariable(v);
                    break;

                case ExpressionStatement es:
                    _w.WriteLine($"{GenerateExpression(es.Expression)};");
                    break;

                case ForStatement fs:
                    GenerateFor(fs);
                    break;

                case WhileStatement ws:
                    GenerateWhile(ws);
                    break;

                case IfStatement ifs:
                    GenerateIf(ifs);
                    break;

                case AssignmentStatement ass:
                    _w.WriteLine($"{GenerateExpression(ass.Left)} = {GenerateExpression(ass.Right)};");
                    break;

                default:
                    _w.WriteLine("// 未対応ステートメント");
                    break;
            }
        }

        private void GenerateLocalVariable(LocalVariableDeclaration v)
        {
            if (v.Javadoc != null)
                WriteJavadoc(v.Javadoc);

            if (v.Initializer != null)
            {
                _w.WriteLine($"{MapType(v.Type)} {v.NameEn} = {GenerateExpression(v.Initializer)};");
            }
            else
            {
                _w.WriteLine($"{MapType(v.Type)} {v.NameEn};");
            }
        }

        private void GenerateFor(ForStatement fs)
        {
            var init = $"{MapType(fs.Initializer.Type)} {fs.Initializer.NameEn} = {GenerateExpression(fs.Initializer.Initializer)}";
            var cond = GenerateExpression(fs.Condition);
            var iter = GenerateExpression(fs.Iterator);

            _w.WriteLine($"for ({init}; {cond}; {iter}) " + "{");
            _w.Indent();

            foreach (var s in fs.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateWhile(WhileStatement ws)
        {
            _w.WriteLine($"while ({GenerateExpression(ws.Condition)}) " + "{");
            _w.Indent();

            foreach (var s in ws.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateIf(IfStatement ifs)
        {
            _w.WriteLine($"if ({GenerateExpression(ifs.Condition)}) " + "{");
            _w.Indent();

            foreach (var s in ifs.ThenBody)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");

            if (ifs.ElseBody.Any())
            {
                _w.WriteLine("else {");
                _w.Indent();

                foreach (var s in ifs.ElseBody)
                    GenerateStatement(s);

                _w.Unindent();
                _w.WriteLine("}");
            }
        }

        private string GenerateExpression(Expression expr)
        {
            return expr switch
            {
                IdentifierExpression id => id.NameEn,
                LiteralExpression lit => lit.Value is string s ? $"\"{s}\"" : lit.Value!.ToString()!,
                BinaryExpression bin => $"{GenerateExpression(bin.Left)} {bin.Operator} {GenerateExpression(bin.Right)}",
                UnaryExpression un => $"{GenerateExpression(un.Operand)}{un.Operator}",
                MemberAccessExpression ma => GenerateMemberAccess(ma),
                ElementAccessExpression ea => $"{GenerateExpression(ea.ArrayExpression)}[{GenerateExpression(ea.IndexExpression)}]",
                InvocationExpression inv => $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
                ArrayLiteralExpression arr => $"new {MapType(arr.ElementType)}[] {{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "/* 未対応式 */"
            };
        }

        private string GenerateMemberAccess(MemberAccessExpression ma)
        {
            // C# AST → Java では配列 length の扱いに差異あり
            // array.length / list.size() 等だが、今回は配列 Length → length にだけ対応
            if (ma.Expression is IdentifierExpression id &&
                id.NameEn == "array" &&
                ma.MemberName == "Length")
            {
                return $"{id.NameEn}.length";
            }

            return $"{GenerateExpression(ma.Expression)}.{ma.MemberName}";
        }

        private void WriteJavadoc(JavadocComment j, string? methodNameJa = null)
        {
            _w.WriteLine("/**");

            if (!string.IsNullOrEmpty(methodNameJa))
            {
                // 関数名の注釈を日本語関数名にする
                _w.WriteLine($" * {methodNameJa}");
            }
            else if (!string.IsNullOrEmpty(j.Summary))
            {
                _w.WriteLine($" * {j.Summary}");
            }

            foreach (var p in j.Params)
            {
                // @param 英語 日本語
                _w.WriteLine($" * @param {p.NameEn} {p.NameJa}");
            }

            _w.WriteLine(" */");
        }

        private string MapType(string t)
        {
            return t switch
            {
                "string" => "String",
                "string[]" => "String[]",
                "int" => "int",
                "int[]" => "int[]",
                "void" => "void",
                _ => t
            };
        }
    }
}

```
VB.NET バックエンド（C# 実装）
```cs:C#
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class VbNetCodeGenerator
    {
        private readonly IndentWriter _w = new();

        public string Generate(CompilationUnit cu)
        {
            // Imports
            foreach (var imp in cu.Imports)
            {
                _w.WriteLine($"Imports {imp.Name}");
            }
            _w.WriteLine();

            foreach (var ns in cu.Namespaces)
            {
                _w.WriteLine($"Namespace {ns.Name}");
                _w.Indent();

                foreach (var cls in ns.Classes)
                {
                    GenerateClass(cls);
                    _w.WriteLine();
                }

                _w.Unindent();
                _w.WriteLine("End Namespace");
            }

            return _w.ToString();
        }

        private void GenerateClass(ClassDeclaration cls)
        {
            if (cls.Javadoc != null)
                WriteXmlComment(cls.Javadoc);

            var mods = string.Join(" ", cls.Modifiers.Select(MapModifier));
            if (!string.IsNullOrEmpty(mods))
                mods += " ";

            _w.WriteLine($"{mods}Class {cls.NameEn}");
            _w.Indent();

            foreach (var m in cls.Methods)
            {
                GenerateMethod(m);
                _w.WriteLine();
            }

            _w.Unindent();
            _w.WriteLine("End Class");
        }

        private void GenerateMethod(MethodDeclaration m)
        {
            if (m.Javadoc != null)
                WriteXmlComment(m.Javadoc, m.NameJa);

            var mods = string.Join(" ", m.Modifiers.Select(MapMethodModifier));
            if (!string.IsNullOrEmpty(mods))
                mods += " ";

            var paramList = string.Join(", ",
                m.Parameters.Select(p => $"{p.NameEn} As {MapType(p.Type)}"));

            if (m.ReturnType == "void")
            {
                _w.WriteLine($"{mods}Sub {m.NameEn}({paramList})");
            }
            else
            {
                _w.WriteLine($"{mods}Function {m.NameEn}({paramList}) As {MapType(m.ReturnType)}");
            }

            _w.Indent();

            foreach (var stmt in m.Body)
                GenerateStatement(stmt);

            _w.Unindent();

            if (m.ReturnType == "void")
                _w.WriteLine("End Sub");
            else
                _w.WriteLine("End Function");
        }

        private void GenerateStatement(Statement stmt)
        {
            switch (stmt)
            {
                case LocalVariableDeclaration v:
                    GenerateLocalVariable(v);
                    break;

                case ExpressionStatement es:
                    _w.WriteLine(GenerateExpression(es.Expression));
                    break;

                case ForStatement fs:
                    GenerateFor(fs);
                    break;

                case WhileStatement ws:
                    GenerateWhile(ws);
                    break;

                case IfStatement ifs:
                    GenerateIf(ifs);
                    break;

                case AssignmentStatement ass:
                    _w.WriteLine($"{GenerateExpression(ass.Left)} = {GenerateExpression(ass.Right)}");
                    break;

                default:
                    _w.WriteLine("' 未対応ステートメント");
                    break;
            }
        }

        private void GenerateLocalVariable(LocalVariableDeclaration v)
        {
            if (v.Javadoc != null)
                WriteXmlComment(v.Javadoc);

            if (v.Initializer != null)
            {
                _w.WriteLine($"Dim {v.NameEn} As {MapType(v.Type)} = {GenerateExpression(v.Initializer)}");
            }
            else
            {
                _w.WriteLine($"Dim {v.NameEn} As {MapType(v.Type)}");
            }
        }

        private void GenerateFor(ForStatement fs)
        {
            // Re:Mind の for (int i = 0; i < array.Length; i++) を
            // VB.NET の For i As Integer = 0 To array.Length - 1 に変換したい場合もあるが、
            // 今回は「そのまま For ... While 風」にせず、素直に For Next を生成することもできる。
            // ここでは単純に 0 〜 array.Length-1 を仮定した実装にしておく（バブルソート用）。

            if (fs.Initializer == null ||
                fs.Condition is not BinaryExpression bin ||
                fs.Iterator is not UnaryExpression un ||
                un.Operator != "++")
            {
                // 簡易: そのままコメントで逃がす
                _w.WriteLine("' 未対応の For 形式");
                return;
            }

            // int i = 0;
            var varName = fs.Initializer.NameEn;
            var startExpr = GenerateExpression(fs.Initializer.Initializer);

            // i < array.Length
            // → To array.Length - 1 を仮定
            var endExpr = $"{GenerateExpression(bin.Right)} - 1";

            _w.WriteLine($"For {varName} As {MapType(fs.Initializer.Type)} = {startExpr} To {endExpr}");
            _w.Indent();

            foreach (var s in fs.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("Next");
        }

        private void GenerateWhile(WhileStatement ws)
        {
            _w.WriteLine($"While {GenerateExpression(ws.Condition)}");
            _w.Indent();

            foreach (var s in ws.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("End While");
        }

        private void GenerateIf(IfStatement ifs)
        {
            _w.WriteLine($"If {GenerateExpression(ifs.Condition)} Then");
            _w.Indent();

            foreach (var s in ifs.ThenBody)
                GenerateStatement(s);

            _w.Unindent();

            if (ifs.ElseBody.Any())
            {
                _w.WriteLine("Else");
                _w.Indent();

                foreach (var s in ifs.ElseBody)
                    GenerateStatement(s);

                _w.Unindent();
            }

            _w.WriteLine("End If");
        }

        private string GenerateExpression(Expression expr)
        {
            return expr switch
            {
                IdentifierExpression id => id.NameEn,
                LiteralExpression lit => lit.Value is string s ? $"\"{s}\"" : lit.Value!.ToString()!,
                BinaryExpression bin => $"{GenerateExpression(bin.Left)} {bin.Operator} {GenerateExpression(bin.Right)}",
                UnaryExpression un => $"{GenerateExpression(un.Operand)} {MapUnaryOperator(un.Operator)}",
                MemberAccessExpression ma => $"{GenerateExpression(ma.Expression)}.{ma.MemberName}",
                ElementAccessExpression ea => $"{GenerateExpression(ea.ArrayExpression)}({GenerateExpression(ea.IndexExpression)})",
                InvocationExpression inv => $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
                ArrayLiteralExpression arr => $"{{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "' 未対応式"
            };
        }

        private void WriteXmlComment(JavadocComment j, string? methodNameJa = null)
        {
            if (!string.IsNullOrEmpty(methodNameJa))
            {
                _w.WriteLine("''' <summary>");
                _w.WriteLine($"''' {methodNameJa}");
                _w.WriteLine("''' </summary>");
            }
            else if (!string.IsNullOrEmpty(j.Summary))
            {
                _w.WriteLine("''' <summary>");
                _w.WriteLine($"''' {j.Summary}");
                _w.WriteLine("''' </summary>");
            }

            foreach (var p in j.Params)
            {
                _w.WriteLine($"''' <param name=\"{p.NameEn}\">{p.NameJa}</param>");
            }
        }

        private string MapType(string t)
        {
            return t switch
            {
                "string" => "String",
                "string[]" => "String()",
                "int" => "Integer",
                "int[]" => "Integer()",
                "void" => "Void", // Function の場合は使わない想定
                _ => t
            };
        }

        private string MapModifier(string m)
        {
            return m switch
            {
                "public" => "Public",
                "private" => "Private",
                "internal" => "Friend",
                _ => m
            };
        }

        private string MapMethodModifier(string m)
        {
            return m switch
            {
                "static" => "Shared",
                "public" => "Public",
                "private" => "Private",
                "internal" => "Friend",
                _ => m
            };
        }

        private string MapUnaryOperator(string op)
        {
            return op switch
            {
                "++" => "+= 1",
                "--" => "-= 1",
                _ => op
            };
        }
    }
}
```
これで：
- ReMindBubbleSortAstGenerator（フロントエンド）
- CSharpCodeGenerator
- JavaCodeGenerator
- VbNetCodeGenerator
の4点がそろって、Re:Mind → AST → C#/Java/VB.NET の三方向バックエンドが形になりました。
次にやると面白いのは、たとえば：
- 同じ AST から各言語のコードを実際に生成して並べて比較するダンプ用ツール
- バブルソート以外（線形探索 / 二分探索）の AST も流して多言語生成を検証
- AST から Mermaid フローチャートを吐き出すモジュール
どこを広げてみたいか、任意で指定してもらえれば、そこをさらに具体的なコードまで掘り下げます。

## 第２６ステップの評価
第２５ステップでひとつのトランスコンパイラ言語の一部仕様の（かなりRe:Mindの仕様に寄せた）AST生成器の実装が生成したJSONからターゲット言語C#を生成する後処理のC#ソースコードが生成されましたので、今回のJavaとVB.NETのソースコード生成も同程度でできてくると想定しました。この実装の細かい妥当性はまだ検証できませんので、現状有姿の参考情報という扱いでお願いします。現在わたしの方で開発中の実装はASTに明確には対応していません。参考情報として非常に有益のように受け止めております。他の方がASTベースで実装されることをさまたげるものでもありません。

# おわりに
第２６ステップは以上です。Re:Mindのアドベントカレンダーの枠としては第２２ステップで完了しましたが、Mindのアドベントカレンダーのシリーズ２の枠が少し空いていますので、間借りさせていただきました。以降は生成された内容の検証に進行します。

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
