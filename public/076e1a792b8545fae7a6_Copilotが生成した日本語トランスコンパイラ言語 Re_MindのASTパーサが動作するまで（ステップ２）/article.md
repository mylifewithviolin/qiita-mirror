# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりましたところ、ほぼ「棚ぼた」でRe:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその続きとも言える検証編の第２ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編第２６ステップの後にはサインアウトがあります。

# 第２ステップ
いじりたおす編第２４ステップ、第２５ステップで生成されたRe:MindのASTパーサとC#コードジェネレータのC#実装が検証できる環境を[本編第１ステップ](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)で構築して、引き続きいじりたおす編第２４ステップの生成コードのメイン部分の問題点を検討します。Copilotは自ら生成したclass CompilationUnitのコードを認識していないので、その提示から開始してみます。

## プロンプト
こちらがコンパイル成功するclass CompilationUnitのコードです。これを踏まえて var unit = new CompilationUnit をちゃんと書くとなるとどうなりますか？

class CompilationUnitのコードは[いじりたおす編ステップ２４ ASTを生成するサンプル実装をC#で生成](https://qiita.com/mylifewithviolin/items/e9589fc28b077ab46fa5)を参照してください。プロンプトにはコードを実際に貼り付けています。

## 生成レスポンス
ありがとうございます。
この AST 構造なら CompilationUnit の正しいインスタンス生成方法は「Namespaces と Imports を埋めたツリーを構築する」ことになります。
つまり、var unit = new CompilationUnit { ... } の中に
- Imports
- Namespaces
- NamespaceDeclaration の中の Classes
- ClassDeclaration の中の Methods
- MethodDeclaration の中の Body
…という階層を作っていく必要があります。

✅ 最小構成の「正しい CompilationUnit インスタンス」例
まずは 最小限の AST を作る例を示します。
（C# のコード生成が動くことを確認するための最小構成）
```cs:
using ReMindAst;
using ReMindBackend;

var unit = new CompilationUnit
{
    // Imports は必要なら追加
    Imports =
    {
        new ImportDeclaration
        {
            Name = "System",
            AliasClasses =
            {
                new AliasClass
                {
                    OriginalName = "Console",
                    TranspiledName = "Console",
                    Members =
                    {
                        new AliasMember
                        {
                            OriginalName = "WriteLine",
                            TranspiledName = "WriteLine",
                            Parameters = { }
                        }
                    }
                }
            }
        }
    },

    // Namespace の追加
    Namespaces =
    {
        new NamespaceDeclaration
        {
            Name = "SampleNamespace",
            Classes =
            {
                new ClassDeclaration
                {
                    NameJa = "メインクラス",
                    NameEn = "MainClass",
                    Modifiers = { "public" },
                    Methods =
                    {
                        new MethodDeclaration
                        {
                            NameJa = "挨拶",
                            NameEn = "Greet",
                            ReturnType = "void",
                            Modifiers = { "public", "static" },
                            Body =
                            {
                                new ExpressionStatement
                                {
                                    Expression = new InvocationExpression
                                    {
                                        Target = new MemberAccessExpression
                                        {
                                            Expression = new IdentifierExpression
                                            {
                                                NameJa = "コンソール",
                                                NameEn = "Console"
                                            },
                                            MemberName = "WriteLine"
                                        },
                                        Arguments =
                                        {
                                            new LiteralExpression { Value = "Hello Re:Mind!" }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
};

var generator = new CSharpCodeGenerator();
string code = generator.Generate(unit);
Console.WriteLine(code);
```


🧩 これが AST として正しい理由
あなたの AST 構造は以下の階層になっています：
```
CompilationUnit
 ├─ Imports : List<ImportDeclaration>
 └─ Namespaces : List<NamespaceDeclaration>
       └─ Classes : List<ClassDeclaration>
             └─ Methods : List<MethodDeclaration>
                   └─ Body : List<Statement>
```

上記のコードはこの構造に完全に従っています。

✨ 生成される C# コードのイメージ（概念）
あなたの CSharpCodeGenerator の実装次第ですが、
おそらく次のようなコードが生成されるはずです：
```cs:
using System;

namespace SampleNamespace
{
    public class MainClass
    {
        public static void Greet()
        {
            Console.WriteLine("Hello Re:Mind!");
        }
    }
}
```


🎯 次にできること
AST はすでに非常に体系的なので、次のステップとして：
- BubbleSort の Re:Mind → AST → C# 生成 の完全パイプライン
- Java / VB.NET のコードジェネレータの整合性チェック
- Javadoc → XML コメント変換ルールの追加
- AliasClass / AliasMember のマッピングテーブルの自動生成
なども一緒に作れます。

必要であれば、
「mylifewithviolinさんの AST 仕様に完全準拠した最小テンプレート」
も作成できます。
次はどの部分を深掘りしましょうか。



## 第２ステップの評価
「Smart(GPT5.1)」モードのMicrosoft Copilotは、同一ログインユーザーとのやりとりをログとしては記録して画面上は履歴を出力してくれるのですが、この内容をすべて生成時に認識するわけではないというのが、「いじりたおす」編でのわたしの学習成果だったのですが、今回の応答でも、またこの後の一連のやりとりでもCopilotが生成したコードをわたしが貼り付けたのでわたしが実装したコードと表現するのにも慣れていく必要があります。（すみません、これはぐちです。）Copilotはけっこう近いサンプルとしてvar unit = new CompilationUnitの内容を生成してきましたが、こちらはAst.csに生成済なので、次回そちらと合わせたコードで調整してみます。

# おわりに
第２ステップは以上です。次回の方向性は上記のとおりです。

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
