# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、ASTパーサが動作するまでの検証[^2]を経て本記事はC#コードジェネレータが動作するまでの改修の第２ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。

# 第２ステップ
「Re:MindのASTパーサが動作するまで」の１２ステップ[^2]は非常に長きにわたるもので、筆者も生成ＡＩと実装コードがらみで根気よく向き合ったのはこれが初めてでした。こちらの１２ステップでいったんC#のソースコードが生成されるようにはなりましたので、以降はC#コードジェネレータが正常動作することを目指しています。

## プロンプト
下記のようにCSharpCodeGeneratorクラスにBuildAliasMapとGenerateInvocationを追記しましたが GenerateInvocation内でGenerateArgs、expr.MemberName、expr.Target.NameEnが未定義エラーと なるようです。
```cs:
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
                InvocationExpression inv => $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
                ArrayLiteralExpression arr => $"new {arr.ElementType}[] {{ {string.Join(", ", arr.Elements.Select(GenerateExpression))} }}",
                _ => "/* 未対応式 */"
            };
        }

		private string GenerateInvocation(InvocationExpression expr, Dictionary<string, AliasClass> aliasMap)
		{
		    // expr.Target は IdentifierExpression または MemberAccessExpression
		    if (expr.Target is IdentifierExpression id)
		    {
		        if (aliasMap.TryGetValue(id.NameJa, out var alias))
		        {
		            // メンバー名の変換
		            var member = alias.Members
		                .FirstOrDefault(m => m.OriginalName == expr.MemberName);

		            var memberName = member?.TranspiledName ?? expr.MemberName;

		            return $"{alias.TranspiledName}.{memberName}({GenerateArgs(expr.Arguments)})";
		        }
		    }

		    // fallback
		    return $"{expr.Target.NameEn}({GenerateArgs(expr.Arguments)})";
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

## 生成レスポンス
ここは 完全に原因が特定できていて、しかも綺麗に直せるポイント です。
あなたが遭遇している未定義エラーは、次の 3 つが理由です。

🎯 未定義エラーの原因（3つ）
① GenerateArgs が存在しない
→ これはまだ実装していない補助関数なので当然エラーになります。
② expr.MemberName が存在しない
→ あなたの InvocationExpression 型には MemberName プロパティが存在しない ためです。
実際の AST では：
- InvocationExpression.Target-  が
- IdentifierExpression（関数呼び出し）
- または MemberAccessExpression（オブジェクト.メソッド呼び出し）
になっており、
メソッド名は Target の中に入っています。
つまり：

□コンソール.一行表示する(引数2)
は AST では：
```cs:
InvocationExpression
  Target = MemberAccessExpression
      Expression = IdentifierExpression("コンソール")
      MemberName = "一行表示する"
  Arguments = [...]
```
 なので、expr.MemberName ではなく：
 ```cs:
((MemberAccessExpression)expr.Target).MemberName
```
と読む必要があります。
③ expr.Target.NameEn が存在しない
→ expr.Target は Expression 型なので、
IdentifierExpression なら NameEn があるが、
MemberAccessExpression には NameEn がありません。
つまり、ここも Target の型を見て分岐する必要があります。



🎉 では、どう直すか（完全版を提示します）
以下の 3 点を修正します。

✅ 修正1：GenerateArgs を追加する
```cs:
private string GenerateArgs(IEnumerable<Expression> args)
{
    return string.Join(", ", args.Select(GenerateExpression));
}
```


✅ 修正2：InvocationExpression のメソッド名を正しく取得する
```cs:
private string GetInvocationMemberName(InvocationExpression expr)
{
    return expr.Target switch
    {
        MemberAccessExpression ma => ma.MemberName,
        IdentifierExpression id => id.NameEn, // fallback
        _ => ""
    };
}
```
✅ 修正3：GenerateInvocation を正しく書き直す
```cs:
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
            var member = alia
```


✨ まとめ
| エラー|原因|対策| 
|:-|:-|:-|
| GenerateArgs 未定義 | 補助関数未実装 | GenerateArgs を追加 | 
|expr.MemberName 未定義  | InvocationExpression に MemberName がない | MemberAccessExpression から取得 | 
| expr.Target.NameEn 未定義 | Target が Identifier とは限らない | 型分岐して処理 | 



mylifewithviolinさん、ここまで来ると Re:Mind → AST → C# のフルパイプラインが完成目前 です。
次は：
- IfSwap の中の 配列[内側] → array[inner] の変換
- Java / VB.NET 生成器の追加
- Imports の構文拡張
など、どんどん広げられます。
次はどこを進めましょう。



## 第２ステップの評価
解決が確認される前に次のステップをご提案するのはどうなんだろうと思いつつ改修結果を確認しました。書き換えたGenerateExpressionは何度も呼ばれるようになりましたが、まだstatic void consoleOutの定義が出力されないようでした。

# おわりに
第２ステップは以上です。次回の方向性は上記の結果の提示からとなります。



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

 
