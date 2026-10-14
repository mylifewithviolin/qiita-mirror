# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、本記事はその検証の第７ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。第６ステップの後にはサインアウトがあります。

# 第７ステップ
第４ステップでProgram.csが動作可能となりました。ただし、まだターゲット言語C#のソースコード出力にはいたらずASTをシリアライズしたJson出力もまだ不完全のようでしたので、第５ステップでその点を調整しましたところ、過去に生成されたソースの再確認応答がありましたので、第６ステップ以降はプロンプト10240文字以内の制限内での生成済ソースコードの分割提示しており、今回もその続きです。

## プロンプト
こちらがParseClass()の全文です。
```cs:
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
```

## 生成レスポンス
mylifewithviolinさん、ParseClass() の全文を見せていただいたことで、
Body が常に空になる原因が完全に特定できました。
結論から言うと：

🎯 **ParseClass() は「メソッド宣言」しか処理しておらず、
メソッド本体（Body）をパースするコードが一切呼ばれていない**

ParseClass() の構造を見てください。
```cs:
if (line.StartsWith("/**"))
{
    var j = ParseJavadoc();
    var method = ParseMethod(j);
    ...
}
else if (line.StartsWith("▽static") || line.StartsWith("▽public"))
{
    var method = ParseMethod(null);
    ...
}
```

ここで呼ばれているのは ParseMethod() だけ です。
そして ParseMethod() の中で Body を読む処理が存在しない か、
存在しても 呼ばれていない ため、結果として：
```json:
method.Body = []
```

となります。

🔍 ParseClass() の問題点を整理すると
① メソッド宣言は読めている
JSON にも Methods が入っているので、ParseMethod() 自体は動いています。
② しかしメソッド本体の行（・□〇◇）を読む処理がない
ParseClass() の while ループは：
- 「▽static」「▽public」などのメソッド宣言行を見つけたら ParseMethod() を呼ぶ
- それ以外の行は _index++ してスキップ
つまり、メソッド本体の行は 全部スキップされている のです。

🧩 具体的にどの行がスキップされているか
Re:Mind のメソッド本体はこういう行です：
・int[] 配列 = 15,13,9,6,4,1
□バブルソートする(配列)
〇int i=0,i<配列.Length,i++ 繰り返す
　□コンソール表示する(配列[i])
〇ここまで


しかし ParseClass() の else 部分は：
```cs:
else
{
    _index++;
}
```

つまり：
❌ これらの行はすべて無視される
❌ ParseMethod() に渡されない
❌ Body に追加されない
✔ JSON の Body は空になる
✔ C# コード生成も空になる

🎯 原因は ParseMethod() が「メソッド本体の行を読む責任を持っていない」こと
ParseClass() はメソッド宣言を見つけたら ParseMethod() を呼びますが、
その後の行（本体）は ParseClass() が全部スキップしてしまいます。
つまり：
ParseMethod() が Body を読むべきなのに
ParseClass() が Body の行を全部スキップしている
という構造的なバグです。

✨ どう修正すればよいか（最小修正案）
ParseMethod() の中で：
- メソッド宣言行を読み取る
- 次の行から「△」が来るまで Body を読む
- その中で「・」「□」「〇」「◇」を判定して Statement を生成する
という処理を行う必要があります。
つまり ParseMethod() はこうあるべきです：
```cs:
private MethodDeclaration ParseMethod(JavadocComment? javadoc)
{
    var method = new MethodDeclaration();
    method.Javadoc = javadoc;

    // 1. メソッド宣言行を解析（既にできている）

    _index++;

    // 2. メソッド本体を読む
    while (_index < _lines.Length)
    {
        var line = _lines[_index].Trim();

        if (line == "△") // メソッド終端
        {
            _index++;
            break;
        }

        if (line.StartsWith("・"))
        {
            method.Body.Add(ParseLocalVariable(line));
        }
        else if (line.StartsWith("□"))
        {
            method.Body.Add(ParseInvocation(line));
        }
        else if (line.StartsWith("〇"))
        {
            method.Body.Add(ParseLoop(line));
        }
        else if (line.StartsWith("◇"))
        {
            method.Body.Add(ParseIf(line));
        }

        _index++;
    }

    return method;
}
```

🎉 まとめ
| 現象|原因|対策| 
|:-|:-|:-|
| JSON の Body が空 | ParseClass() が本体行を全部スキップしている| ParseMethod() に本体パース処理を移す | 
|デシリアライズ後の AST が空|JSON が空だから|パーサーを修正 | 
|C# コードが空| AST.Body が空 |Body を構築する| 



📌 次に進めること
mylifewithviolinさん、もしよければ：
- ParseMethod() の全文を見せていただければ、Body パース処理を完全に組み込みます。
- または、Re:Mind の構文に完全対応した ParseMethod() / ParseStatements() の完全版 をこちらで作成できます。
どちらで進めましょう。


## 第７ステップの評価
このあたりのやりとりは過去に生成したソースコードを認識してくれていると、かなり生産性があがるというイメージです。過去に自身が生成したソースコードをわたしが実装したものとして、いろいろ分析してくれるのは慣れればそういうものとしてなにも感じなくすることができます:relaxed:

# おわりに
第７ステップは以上です。次回の方向性はParseMethod()などの提示となります。この記事がどんな方に役立つのか想像するに、自作言語のパーサーを構築したい方には参考になるような気がします。わたし自身も完全ではなくても原型を提示してくれることはありがたいと感じています。

:::note warn
生成レスポンスセクションの内容は生成AIが生成したものです。引用されているソースコードは動作しない状態が含まれます。
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
