# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語Aoi（あおい）の実装言語仕様を読み込ませて設計タスクから実装を展開しています。本記事ではコア構文のトランスコンパイルの最小版を実装します。

日本語プログラミング言語 Aoi （あおい） という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)はこちらをご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub Copilotのフリー版を導入。[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でAmazonのkiro-cliのskillsとかなり近いことができて結果オーライでした。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。


# 本記事のステップ
[こちらの記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」を細分化した[こちらの回の記事](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)の「1. 最小セット（MVP）」の具体的な実装の途中です。今回は「コア構文のトランスコンパイル」の最小版を実装します。

## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。
**Phase 1. Lexer タスク**
前々回記事以前で完了
**Phase 2. Parser タスク**
前々回記事以前で完了
**Phase 3. AST タスク**
前々回記事以前で完了
**Phase 4. 意味解析と名前解決 タスク**
前々回記事以前で完了
**Phase 5. 中間表現（IR） タスク**
前々回記事で完了
**Phase 6. コード生成パイプライン タスク**
前回記事で完了
### Phase 7. コア構文のトランスコンパイル実装
1. まずは以下の「中核構文」を確実に生成できるようにする。
   - □コンソール.一行表示する(引数)
   - □変数名 = 式
   - □(引数)で 関数名
   - ◇条件 の場合 / ◇他に / ◇ここまで
   - 〇繰り返す / 〇(条件) の間は繰り返す / 〇ここまで
2. 生成対象言語ごとに、対応する構文へマッピングする。
3. 仕様上の「日本語の記法」と「ターゲット言語の構文」を両立させるため、変換ルール表を明示的に持つ。

## Microsoft Copilotとの事前準備
### プロンプト１
>Phase 6: コード生成パイプラインが完了しました。
Phase 7: コア構文のトランスコンパイル実装のMVPタスクの最小プロンプトを作成してください。
#### 生成レスポンス１
> Phase 6（コード生成パイプライン）まで完了したので、
いよいよ Phase 7：コア構文のトランスコンパイル実装（MVP） に入れます。
> 
> ここは Re:Mind の「日本語構文 → ターゲット言語構文」への変換ルールを
明示的に持ち、IR → CodeGen の最終段階を固めるフェーズです。
> 以下に、Phase 7 の MVPタスクを正しく進めるための CodeAgent 用最小プロンプトをまとめます。
> 
>🧩 タスク 1：コア構文の変換ルール表（MappingTable）の追加
Re:Mind の Phase 7（コア構文のトランスコンパイル）を開始するため、
MappingTable.cs を新規作成し、以下の「日本語 → ターゲット言語」の変換ルール表を最小構成で追加してください。
>
>必要な構造:
>- Console.WriteLine のマッピング
>- 変数宣言のマッピング
>- 代入のマッピング
>- If / ElseIf / Else のマッピング
>- While のマッピング
>
>中身のロジックは書かず、プロパティと辞書の枠だけ作成してください。
既存コードは保持し、新規ファイルとして最小構造だけ生成してください。
🧩 タスク 2：CSharpCodeGenerator に MappingTable を統合する（枠だけ）
CSharpCodeGenerator.cs に、
MappingTable を参照して IR を C# 構文へ変換するための
「枠（骨格）」だけを差分追加してください。
>
>必要な構造:
>- MappingTable のフィールド
>- コンストラクタで MappingTable を受け取る
>- GenerateStatement / GenerateExpression 内で MappingTable を参照する枠
>
>中身のロジックは書かず、枠だけ追加してください。
既存コードは保持してください。
🧩 タスク 3：□コンソール.一行表示する(引数) の最小変換
CSharpCodeGenerator.cs に、
CallExpressionIR が Console.WriteLine に対応する場合の
最小変換ロジックだけを差分追加してください。
>
>必要な処理:
>- MappingTable から "コンソール.一行表示する" → "Console.WriteLine" を取得
>- 引数をカンマ区切りで出力
>- "Console.WriteLine(引数);" を生成
>
>既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 4：□変数名 = 式 の最小変換
CSharpCodeGenerator.cs に、
AssignmentIR → "変数 = 式;" の最小変換ロジックだけを差分追加してください。
>
>既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 5：◇条件 の場合 / ◇他に / ◇ここまで の最小変換
CSharpCodeGenerator.cs に、
IfIR → "if (条件) { ... }" の最小変換ロジックだけを差分追加してください。
>
>必要な処理:
>- IfIR.Condition を GenerateExpression で変換
>- IfIR.TrueBlock を GenerateStatement で変換
>- ElseIf / Else は後続フェーズで追加するため、今回は最小構成のみ
>
>既存コードは保持し、必要な部分だけ生成してください。
🧩 タスク 6：〇繰り返す / 〇(条件) の間は繰り返す の最小変換
CSharpCodeGenerator.cs に、
WhileIR → "while (条件) { ... }" の最小変換ロジックだけを差分追加してください。
>
>既存コードは保持し、必要な部分だけ生成してください。
>🧩 タスク 7：JavaCodeGenerator / VbNetCodeGenerator に MappingTable を統合（枠だけ）
JavaCodeGenerator.cs と VbNetCodeGenerator.cs に、
MappingTable を参照するための「枠（骨格）」だけを差分追加してください。
>
>必要な構造:
>- MappingTable のフィールド
>- コンストラクタで MappingTable を受け取る
>
>中身のロジックは書かず、枠だけ追加してください。
>
>🧭 Phase 7 の最適な進行順序（MVP）
MappingTable（変換ルール表）を作る
>
>CSharpCodeGenerator に MappingTable を統合
□コンソール.一行表示する(引数)
□変数名 = 式
◇条件 の場合
〇繰り返す
Java / VB.NET の枠追加
>
>この順番が 最小クレジットで最大の進捗を得られます。


## GitHub Copilot
Microsoft Copilotが生成したGitHub CopilotへのPhase 7の各タスクの実行プロンプトを逐次実行した結果、下記のソースコードが生成されました。今回の更新でMappingTableに対応しました。

```cs:MappingTable.cs
using System.Collections.Generic;

namespace ReMindBackend
{
    public class MappingTable
    {
        public Dictionary<string, string> ConsoleWriteLine { get; } = new();
        public Dictionary<string, string> VariableDeclaration { get; } = new();
        public Dictionary<string, string> Assignment { get; } = new();
        public Dictionary<string, string> If { get; } = new();
        public Dictionary<string, string> ElseIf { get; } = new();
        public Dictionary<string, string> Else { get; } = new();
        public Dictionary<string, string> While { get; } = new();
    }
}
```

タスク 4：□変数名 = 式 の最小変換
で下記のレスポンスが返りました。
>CSharpCodeGenerator.cs には、既に以下の AssignmentIR 変換ロジックが存在しています。
変数 = 式;
既存実装が要求を満たしているため、重複する差分追加は行いませんでした。

タスク 5：◇条件 の場合 / ◇他に / ◇ここまで の最小変換
でも下記のレスポンスが返りました。
>CSharpCodeGenerator.cs には既に、指定された IfIR の最小変換ロジックがあります。
なお、現在の IfIR のプロパティ名は TrueBlock ではなく ThenBlock です。重複する差分追加は行いませんでした。

タスク 6：〇繰り返す / 〇(条件) の間は繰り返す の最小変換
でも下記のレスポンスが返りました。
>CSharpCodeGenerator.cs には既に WhileIR の最小変換ロジックがあります。
重複する差分追加は行いませんでした。

このあたりは既に実装されているコードを上書きしないように追加をさけてくれたようです。

CSharpCodeGenerator.cs / JavaCodeGenerator.cs / VbNetCodeGenerator.csがMappingTableに対応しました。JavaとVbNetはとりあえず枠の対応です。

<details><summary>CSharpCodeGenerator.cs</summary>

```cs:CSharpCodeGenerator.cs
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class CSharpCodeGenerator
    {
        private readonly IndentWriter _w = new();
        private readonly MappingTable _mappingTable;
        private Dictionary<string, AliasClass> _aliasMap;

        public CSharpCodeGenerator() : this(new MappingTable())
        {
        }

        public CSharpCodeGenerator(MappingTable mappingTable)
        {
            _mappingTable = mappingTable;
            _mappingTable.ConsoleWriteLine.TryAdd("コンソール.一行表示する", "Console.WriteLine");
        }

        public string Generate(CompilationUnit cu)
        {
            _aliasMap = BuildAliasMap(cu);

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

        public string Generate(ProgramIR program)
        {
            return string.Empty;
        }

        private void GenerateClass(ClassIR classIR)
        {
        }

        private void GenerateMethod(MethodIR methodIR)
        {
        }

        private void GenerateStatement(StatementIR stmt)
        {
            _ = _mappingTable;

            if (stmt is VariableDeclarationIR variable)
            {
                _w.WriteLine($"{variable.Type} {variable.Name} = {GenerateExpression(variable.Initializer)};");
            }

            if (stmt is AssignmentIR assignment)
            {
                _w.WriteLine($"{assignment.Target} = {GenerateExpression(assignment.Value)};");
            }

            if (stmt is IfIR ifStatement)
            {
                _w.WriteLine($"if ({GenerateExpression(ifStatement.Condition)})");
                _w.WriteLine("{");
                _w.Indent();

                foreach (var statement in ifStatement.ThenBlock.Statements)
                {
                    GenerateStatement(statement);
                }

                _w.Unindent();
                _w.WriteLine("}");
            }

            if (stmt is WhileIR whileStatement)
            {
                _w.WriteLine($"while ({GenerateExpression(whileStatement.Condition)})");
                _w.WriteLine("{");
                _w.Indent();

                foreach (var statement in whileStatement.Body.Statements)
                {
                    GenerateStatement(statement);
                }

                _w.Unindent();
                _w.WriteLine("}");
            }
        }

        private string GenerateExpression(ExpressionIR expr)
        {
            _ = _mappingTable;

            return expr switch
            {
                NewExpressionIR arrayCreation => $"new {arrayCreation.TypeName}[{GenerateExpression(arrayCreation.Arguments[0])}]",
                CallExpressionIR call when call.MethodName == "コンソール.一行表示する" => $"{_mappingTable.ConsoleWriteLine["コンソール.一行表示する"]}({string.Join(", ", call.Arguments.Select(GenerateExpression))});",
                CallExpressionIR call => $"{call.MethodName}({string.Join(", ", call.Arguments.Select(GenerateExpression))})",
                MemberAccessIR memberAccess => $"{GenerateExpression(memberAccess.Target)}.{memberAccess.MemberName}",
                _ => string.Empty
            };
        }

        private Dictionary<string, AliasClass> BuildAliasMap(CompilationUnit cu)
        {
            var map = new Dictionary<string, AliasClass>();

            foreach (var import in cu.Imports)
            {
                foreach (var alias in import.AliasClasses)
                {
                    map[alias.OriginalName] = alias;
                }
            }

            return map;
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
                InvocationExpression inv => GenerateInvocation(inv, _aliasMap),
                ArrayLiteralExpression arr => $"new {arr.ElementType}[] {{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "/* 未対応式 */"
            };
        }

        private string GenerateInvocation(InvocationExpression expr, Dictionary<string, AliasClass> aliasMap)
        {
            // ターゲットが MemberAccessExpression の場合（例：コンソール.一行表示する）
            if (expr.Target is MemberAccessExpression ma)
            {
                // 左側（コンソール）
                if (ma.Expression is IdentifierExpression id &&
                    aliasMap.TryGetValue(id.NameJa, out var alias))
                {
                    // メソッド名（例：一行表示する）
                    var originalMember = ma.MemberName;

                    // マッピングを探す
                    var member = alias.Members
                        .FirstOrDefault(m => m.OriginalName == originalMember);

                    var memberName = member?.TranspiledName ?? originalMember;

                    return $"{alias.TranspiledName}.{memberName}({GenerateArgs(expr.Arguments)})";
                }
                }

            // ターゲットが IdentifierExpression の場合（例：バブルソートする）
            if (expr.Target is IdentifierExpression id2)
            {
                if (aliasMap.TryGetValue(id2.NameJa, out var alias))
                {
                    // メソッド名は expr.Target.NameEn ではなく、expr.NameEn を使うべき
                    return $"{alias.TranspiledName}.{id2.NameEn}({GenerateArgs(expr.Arguments)})";
                }
            }

            // fallback
            return $"{GenerateExpression(expr.Target)}({GenerateArgs(expr.Arguments)})";
        }
        private string GenerateArgs(IEnumerable<Expression> args)
        {
            return string.Join(", ", args.Select(GenerateExpression));
        }

        private string GetInvocationMemberName(InvocationExpression expr)
        {
            return expr.Target switch
            {
                MemberAccessExpression ma => ma.MemberName,
                IdentifierExpression id => id.NameEn, // fallback
                _ => ""
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

</details>
<details><summary>JavaCodeGenerator.cs</summary>

```cs:JavaCodeGenerator.cs
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class JavaCodeGenerator
    {
        private readonly IndentWriter _w = new();
        private readonly MappingTable _mappingTable;

        public JavaCodeGenerator() : this(new MappingTable())
        {
        }

        public JavaCodeGenerator(MappingTable mappingTable)
        {
            _mappingTable = mappingTable;
        }

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

        public string Generate(ProgramIR program)
        {
            return string.Empty;
        }

        private void GenerateClass(ClassIR classIR)
        {
        }

        private void GenerateMethod(MethodIR methodIR)
        {
        }

        private void GenerateStatement(StatementIR stmt)
        {
        }

        private string GenerateExpression(ExpressionIR expr)
        {
            return string.Empty;
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

</details>
<details><summary>VbNetCodeGenerator.cs</summary>

```cs:VbNetCodeGenerator.cs
using System;
using System.Linq;
using ReMindAst;

namespace ReMindBackend
{
    public class VbNetCodeGenerator
    {
        private readonly IndentWriter _w = new();
        private readonly MappingTable _mappingTable;

        public VbNetCodeGenerator() : this(new MappingTable())
        {
        }

        public VbNetCodeGenerator(MappingTable mappingTable)
        {
            _mappingTable = mappingTable;
        }

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

        public string Generate(ProgramIR program)
        {
            return string.Empty;
        }

        private void GenerateClass(ClassIR classIR)
        {
        }

        private void GenerateMethod(MethodIR methodIR)
        {
        }

        private void GenerateStatement(StatementIR stmt)
        {
        }

        private string GenerateExpression(ExpressionIR expr)
        {
            return string.Empty;
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
            // ここでは単純に 0 ? array.Length-1 を仮定した実装にしておく（バブルソート用）。

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
</details>

## 本ステップの評価
ついに「最小セット（MVP）」の実装フェーズがほぼ完了に近づいてきました。サンプルソースに対してトランスコンパイルが実行できる状況づくりを目指します。

# おわりに
以上です。次回の方向性はPhase 8: Program.cs からの実行フロー統合の実装からとなります。「最小セット（MVP）」の完成条件の一つ手前になりました。


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
