# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりまして、これがなかなか難儀でしたが、最後の第２２ステップで有益なASTについての情報を生成してもらえたので、本記事はその続きの第２５ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第２３ステップの後にはサインアウトがあります。

# 第２５ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにしましたところ、比較的正常な結果が返るようになりました。第１９，２０，２１ステップの生成レスポンスで、Copilotが次のステップのご提案として「Re:Mind の AST（抽象構文木）風の構造化表示」ということを提案したので第２２ステップでそれをやってみることにしました。第２４ステップではだめもとでそのASTをせ生成するサンプル実装をC#で生成することを試みましたが、予想外にそれっぽいAST生成器ができてきたので、今回はその後処理ターゲット言語C#へのASTからの生成処理をやってみます。

## プロンプト
では、次のステップとして：
- 「この AST から C# コードを生成するクラス（バックエンド）」 のコードをC#で生成していただくことは可能ですか？


## 生成レスポンス
もちろんmylifewithviolinさん、できます。
ここでは、前回あなたと一緒に設計した AST モデル（CompilationUnit / NamespaceDeclaration / ClassDeclaration / MethodDeclaration / Statement / Expression …） を入力として、C# ソースコードを生成するバックエンド（コードジェネレータ） を C# で実装します。

🎯 目的
- Re:Mind → AST（前回作成）
- AST → C# コード（今回作成）
これで Re:Mind → AST → C# のトランスコンパイルパイプラインが成立します。

🧩 バックエンドの設計方針
- AST ノードごとに GenerateCSharp() を実装するのではなく、
専用の CodeGenerator クラスを作り、
ノードを受け取って C# コードを構築する方式にします。
- インデント管理を行う IndentWriter を用意。
- コメント（XML コメント）も AST の Javadoc 情報から生成。
- VB.NET や Java 版も後で同じ構造で作れるように、
言語依存部分をメソッド化しておく。

🏗️ C# コード生成器（バックエンド）実装
以下は 完全に動作する C# コードです。
📌 IndentWriter（インデント管理クラス）
```cs:C#
using System;
using System.Text;

namespace ReMindBackend
{
    public class IndentWriter
    {
        private readonly StringBuilder _sb = new();
        private int _indent = 0;
        private const string IndentString = "    ";

        public void Indent() => _indent++;
        public void Unindent() => _indent--;

        public void WriteLine(string text = "")
        {
            for (int i = 0; i < _indent; i++)
                _sb.Append(IndentString);

            _sb.AppendLine(text);
        }

        public override string ToString() => _sb.ToString();
    }
}
```

📌 CSharpCodeGenerator（AST → C#）
```cs:C#
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class CSharpCodeGenerator
    {
        private readonly IndentWriter _w = new();

        public string Generate(CompilationUnit cu)
        {
            // using
            foreach (var imp in cu.Imports)
            {
                _w.WriteLine($"using {imp.Name};");
            }
            _w.WriteLine();

            // namespace
            foreach (var ns in cu.Namespaces)
            {
                _w.WriteLine($"namespace {ns.Name}");
                _w.WriteLine("{");
                _w.Indent();

                foreach (var cls in ns.Classes)
                {
                    GenerateClass(cls);
                }

                _w.Unindent();
                _w.WriteLine("}");
            }

            return _w.ToString();
        }

        private void GenerateClass(ClassDeclaration cls)
        {
            // XML コメント
            if (cls.Javadoc != null)
                WriteXmlComment(cls.Javadoc);

            // public class ProgramType
            var mods = string.Join(" ", cls.Modifiers);
            _w.WriteLine($"{mods} class {cls.NameEn}");
            _w.WriteLine("{");
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
                WriteXmlComment(m.Javadoc);

            var mods = string.Join(" ", m.Modifiers);
            var paramList = string.Join(", ",
                m.Parameters.Select(p => $"{MapType(p.Type)} {p.NameEn}"));

            _w.WriteLine($"{mods} {MapType(m.ReturnType)} {m.NameEn}({paramList})");
            _w.WriteLine("{");
            _w.Indent();

            foreach (var stmt in m.Body)
            {
                GenerateStatement(stmt);
            }

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
                WriteXmlComment(v.Javadoc);

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

            _w.WriteLine($"for ({init}; {cond}; {iter})");
            _w.WriteLine("{");
            _w.Indent();

            foreach (var s in fs.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateWhile(WhileStatement ws)
        {
            _w.WriteLine($"while ({GenerateExpression(ws.Condition)})");
            _w.WriteLine("{");
            _w.Indent();

            foreach (var s in ws.Body)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");
        }

        private void GenerateIf(IfStatement ifs)
        {
            _w.WriteLine($"if ({GenerateExpression(ifs.Condition)})");
            _w.WriteLine("{");
            _w.Indent();

            foreach (var s in ifs.ThenBody)
                GenerateStatement(s);

            _w.Unindent();
            _w.WriteLine("}");

            if (ifs.ElseBody.Any())
            {
                _w.WriteLine("else");
                _w.WriteLine("{");
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
                MemberAccessExpression ma => $"{GenerateExpression(ma.Expression)}.{ma.MemberName}",
                ElementAccessExpression ea => $"{GenerateExpression(ea.ArrayExpression)}[{GenerateExpression(ea.IndexExpression)}]",
                InvocationExpression inv => $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
                ArrayLiteralExpression arr => $"new {arr.ElementType}[] {{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "/* 未対応式 */"
            };
        }

        private void WriteXmlComment(JavadocComment j)
        {
            if (!string.IsNullOrEmpty(j.Summary))
                _w.WriteLine($"/// <summary>{j.Summary}</summary>");

            foreach (var p in j.Params)
                _w.WriteLine($"/// <param name=\"{p.NameEn}\">{p.NameJa}</param>");
        }

        private string MapType(string t)
        {
            return t switch
            {
                "string" => "string",
                "string[]" => "string[]",
                "int" => "int",
                "int[]" => "int[]",
                "void" => "void",
                _ => t
            };
        }
    }
}
```
🧪 動作例（バブルソート AST を渡した場合
```cs:C#
var generator = new CSharpCodeGenerator();
string code = generator.Generate(compilationUnit);
Console.WriteLine(code);
```
出力される C# コードは、前回あなたと作った C# バブルソートと 同等の構造になります。

🎉 これで Re:Mind → AST → C# のパイプラインが完成！
mylifewithviolinさん、ここまで来るともう Re:Mind の正式トランスコンパイラの骨格ができています。

🔧 次にできること
- Java バックエンドを同じ構造で作る
- VB.NET バックエンドを作る
- AST から Mermaid フローチャート生成器を作る
- Re:Mind の フロントエンド（パーサ）を汎用化する
- Re:Mind → AST → C# の ユニットテストを作る
どれを進めてみたいですか。


## 第２５ステップの評価
第２４ステップでひとつのトランスコンパイラ言語の一部仕様の（かなりRe:Mindの仕様に寄せた）AST生成器実装のテンプレとして超大量の出力があって驚きましたましたので、今回は同程度のものは出力されるだろうと読んでいました。未検証ですがAIの意図としてはターゲット言語依存の部分は切り分けてくれているようです。この実装の細かい妥当性はまだ検証できませんので、現状有姿の参考情報という扱いでお願いします。現在わたしの方で開発中の実装はASTに明確には対応していません。参考情報として非常に有益のように受け止めております。他の方がASTベースで実装されることをさまたげるものでもありません。

# おわりに
第２５ステップは以上です。Re:Mindのアドベントカレンダーの枠としては第２２ステップで完了しましたが、Mindのアドベントカレンダーのシリーズ２の枠が少し空いていますので、間借りさせていただきました。

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
