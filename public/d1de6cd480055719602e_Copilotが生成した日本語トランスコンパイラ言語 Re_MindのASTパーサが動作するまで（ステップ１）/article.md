# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりましたところ、ほぼ「棚ぼた」でRe:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその続きとも言える検証編の第１ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編第２６ステップの後にはサインアウトがあります。

# 第１ステップ
いじりたおす編第２４ステップ、第２５ステップで生成されたRe:MindのASTパーサとC#コードジェネレータのC#実装が検証できる環境を構築して、いったん第２４ステップの生成コードの問題点を指摘します。
## C#環境の構成
最初にC#のプロジェクトを作成してVSCodeを起動します。

```
C:\developments\cs12>dotnet --version
8.0.206

C:\developments\cs12>dotnet new console -o astsample
テンプレート "コンソール アプリ" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\cs12\astsample\astsample.csproj を復元しています:
  復元対象のプロジェクトを決定しています...
  C:\developments\cs12\astsample\astsample.csproj を復元しました (132 ms)。
正常に復元されました。

C:\developments\vscode>cd mind8dispatch
C:\developments\vscode\mind8dispatch>code .
```

下記のサンプルソースが生成されています。
```cs:Program.cs
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```

Program.csに併存させて（C#の名前空間は物理フォルダと同期してなくても可なので）第２４ステップで生成されたASTクラスとASTパーサを、Ast.csとParser.csという新規ファイルを作成してコピペします。
第２５ステップで生成されたC#コードジェネレータを、ついでに第２６ステップで生成されたJavaコードジェネレータとVB.NETコードジェネレータを、CSharpCodeGenerator.csとJavaCodeGenerator.csとVbNetCodeGenerator.csとIndenetWriter.csという新規ファイルを作成してそれぞれコピペします。

```
C:\DEVELOPMENTS\CS12\ASTSAMPLE
│  Ast.cs
│  astsample.csproj
│  CSharpCodeGenerator.cs
│  IndenetWriter.cs
│  JavaCodeGenerator.cs
│  Parser.cs
│  Program.cs
│  VbNetCodeGenerator.cs
│
└─.vscode
　     launch.json
　     tasks.json
```
Program.csに生成されたサンプルをコピペします。
```cs:Program.cs
using ReMindAst; using ReMindBackend;

var generator = new CSharpCodeGenerator();
string code = generator.Generate(CompilationUnit);
Console.WriteLine(code);
```
CompilationUnitはクラス名なので、ここでコンパイルエラーとなります。（コンパイルする前にVSCode拡張が警告を出している状態となっています。 「'CompilationUnit' は 種類 です。これは特定のコンテンツでは無効になります」）

## プロンプト
先日ご提案いただいたRe:MindのASTとコードジェネレータクラスをすべてプロジェクトに作成してProgram.csを下記のように記述しましたが、 'CompilationUnit' は 種類 です。これは特定のコンテンツでは無効になります というエラーとなるのはなぜですか？CompilationUnitタイプの変数とインスタンスはどのように実装しますか？
```cs:
using ReMindAst; using ReMindBackend;
var generator = new CSharpCodeGenerator(); 
string code = generator.Generate(CompilationUnit); 
Console.WriteLine(code);
```

## 生成レスポンス
これはとても本質的なポイントに気づかれています。
結論から言うと CompilationUnit は「型（class）」であって「インスタンス」ではないため、そのまま Generate(CompilationUnit) と書くと C# は「型名を値として渡している」と判断し、エラーになります。

🔍 なぜ 'CompilationUnit' は種類です。これは特定のコンテンツでは無効になります というエラーになるのか
C# では、メソッドに渡すのは 値（インスタンス） でなければいけません。
しかし今のコードはこうなっています：
```cs:
string code = generator.Generate(CompilationUnit);
```

ここで CompilationUnit は class の名前であり、インスタンスではありません。
C# は「型を値として渡すのは無効」と判断し、エラーを出します。

🧩 CompilationUnit のインスタンスはどう作る？
あなたが以前作成した Re:Mind AST の構造に基づくと、CompilationUnit は AST の最上位ノードで、
中に Statements や Functions を持つ構造になっているはずです。
典型的なインスタンス生成はこうなります：
```cs:
var unit = new CompilationUnit
{
    Statements = new List<IStatement>
    {
        new VariableDeclarationStatement("i", new IntegerLiteral(0)),
        new WhileStatement(
            new LessThanExpression(new VariableReference("i"), new IntegerLiteral(10)),
            new List<IStatement>
            {
                new ExpressionStatement(
                    new AssignmentExpression(
                        new VariableReference("i"),
                        new AddExpression(new VariableReference("i"), new IntegerLiteral(1))
                    )
                )
            }
        )
    }
};
```
そして Generate に渡すのは このインスタンス です：
```cs:
string code = generator.Generate(unit);
Console.WriteLine(code);
```

🧪 最小構成の例（動作確認用）
まずは AST が正しく動くか確認するために、もっとシンプルな AST を渡す例も示します。
```cs:
var unit = new CompilationUnit
{
    Statements = new List<IStatement>
    {
        new ExpressionStatement(
            new FunctionCallExpression("Print", new List<IExpression>
            {
                new StringLiteral("Hello Re:Mind!")
            })
        )
    }
};

var generator = new CSharpCodeGenerator();
string code = generator.Generate(unit);
Console.WriteLine(code);
```


🎯 まとめ
|問題|原因|解決| 
|:-|:-|:-|
| 'CompilationUnit' は種類です | 型名を値として渡している | new CompilationUnit { ... }でインスタンスを作る| 
| Generate(CompilationUnit) |インスタンスではない  | Generate(unit)のように変数を渡す | 



✨ 次のステップの提案
Re:Mind AST はすでにかなり体系的なので、
AST の最小構成サンプル（Hello World） を一緒に作って、
C#, Java, VB.NET のコード生成がすべて動くことを確認するのが良いと思います。
必要であれば、
- AST の最小構成テンプレート
- Program.cs の完全版
- CSharpCodeGenerator の動作確認用ユニットテスト
なども作成できます。
どこから進めましょうか。




## 第１ステップの評価
「Smart(GPT5.1)」モードのMicrosoft Copilotは、同一ログインユーザーとのやりとりをログとしては記録して画面上は履歴を出力してくれるのですが、この内容をすべて生成時に認識するわけではないというのが、「いじりたおす」編でのわたしの学習成果だったのですが、今回の応答でも、またこの後の一連のやりとりでもCopilotが生成したコードをわたしが貼り付けたのでわたしが実装したコードと表現するのにも慣れていく必要があります。（すみません、これはぐちです。）Copilotはけっこう近いサンプルとしてvar unit = new CompilationUnitの内容を生成してきましたが、こちらはAst.csに生成済なので、次回そちらと合わせたコードで調整してみます。

# おわりに
第１ステップは以上です。次回は上記のとおりです。わたしはシステムエンジニアであってプログラミング言語開発者ではないので、生成AIが自作言語のASTのテンプレを提示してくれたことにはたいへんうれしく思っています。

Re:Mindの設計を開始したころ、下記のような記事でC言語コンパイラをC#で書きなおすことでASTやBNFについて学習していました。

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c

# 参考情報
## 目次　Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす
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
