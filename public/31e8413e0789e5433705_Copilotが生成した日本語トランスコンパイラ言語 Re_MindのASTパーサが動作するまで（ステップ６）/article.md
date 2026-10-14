# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえたので、本記事はその検証の第６ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。いじりたおす編[^1]第２６ステップの後にはサインアウトがあります。

# 第６ステップ
第４ステップでProgram.csが動作可能となりました。ただし、まだターゲット言語C#のソースコード出力にはいたらずASTをシリアライズしたJson出力もまだ不完全のようでしたので、第５ステップでその点を調整しましたところ。その応答でReMindBubbleSortAstGeneratorを見せてくれとのことでした。しかし、いじりたおす編でCopilotが生成したこのクラスのコードはCopilotのプロンプト文字数上限を超えてしまうようでした。そこで、人間系のオペレーションとしては問題のある個所をデバッグ実行である程度特定して提示するとしています。

## プロンプト
パーサーのソースコードは10240文字を超えてしまうためすべてはお伝え出来ないのですが、デバッグ実行してみた感じ、下記の範囲のコードが走行されていました。
```cs:
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
```
        
## 生成レスポンス
mylifewithviolinさん、ここまでの情報で **原因がほぼ確定** しました。  
そして、あなたが貼ってくださったパーサーのコード断片は、まさに問題の本質を示しています。

---

# 🎯 結論  
**パーサーが「クラス宣言まで」しか処理しておらず、  
メソッド本体（Body）を一切パースしていないため、  
AST の Body が常に空になる。**

つまり：

- JSON は正しい  
- デシリアライズも正しい  
- C# コードジェネレータも正しい  
- **パーサーが Body を構築していないため、結果として空の AST が生成されている**

ということです。

---

# 🔍 なぜそう言えるのか（根拠）

あなたが貼ってくれたコードは：

```csharp
ns.Classes.Add(ParseClass());
```

しかし **ParseClass() の中身が貼られていない**。

そして、ParseNamespace() の中では：

- 名前空間名を読む  
- クラスを 1 つだけパースする  

ここまでしかしていません。

つまり：

### ✔ メソッド宣言を読むコードがあるかどうか不明  
### ✔ メソッドの Body を読むコードがあるかどうか不明  
### ✔ ステートメント（・□〇◇）を読むコードがあるかどうか不明  

そして JSON では：

```json
"Body": []
```

これは **パーサーが Body に何も追加していない** ことを意味します。

---

# 🧩 さらに重要な点  
あなたの JSON には **メソッド宣言は存在している** ので、  
ParseClass() の中で **メソッド宣言まではパースできている** ことが分かります。

しかし Body が空なので：

### ❌ ParseMethod() の中で Body を構築していない  
または  
### ❌ ParseStatements() が呼ばれていない  
または  
### ❌ ParseStatements() が空実装  
または  
### ❌ _index の進め方が間違っていて Body の行に到達していない  

のいずれかです。

---

# 🔍 さらに深掘り：あなたのパーサー構造から推測できること

あなたのパーサーは：

- `_lines` に全文を split  
- `_index` を進めながら行単位でパース  
- `Trim()` してキーワードを判定  

という構造です。

この方式だと、次のような問題が起きやすいです：

---

## ❗ 問題1：ParseClass() が「△」を見つけた時点で return してしまう  
Re:Mind の構造は：

```
▽クラス
    ▽メソッド
        本体
    △
△
```

もし ParseClass() が「△」を見つけたら return する実装だと、  
**メソッド本体の行に到達する前に return してしまう** ことがあります。

---

## ❗ 問題2：ParseMethod() が Body を読む前に return している  
メソッド宣言は読めているので、ParseMethod() は存在します。

しかし Body が空なので：

- `〇`（for/while）  
- `・`（変数宣言）  
- `□`（メソッド呼び出し）  
- `◇`（if）  

などの行を **ParseMethod() が無視している** 可能性が高いです。

---

## ❗ 問題3：インデントや記号（・□〇◇）の判定が正しく動いていない  
あなたの Re:Mind ソースは：

```
    ・int[] 配列 = 15,13,9,6,4,1
```

しかし Trim() すると：

```
・int[] 配列 = 15,13,9,6,4,1
```

この行をパーサーが拾っていない可能性があります。

---

# 🎯 どうすれば原因を特定できるか（最短の方法）

### ✔ 1. ParseClass() の return 直前でログを出す

```csharp
Console.WriteLine("Class parsed. Methods count = " + cls.Methods.Count);
```

### ✔ 2. ParseMethod() の return 直前でログを出す

```csharp
Console.WriteLine("Method parsed. Body count = " + method.Body.Count);
```

これで：

- ParseMethod() が Body を構築していないのか  
- ParseClass() がメソッド本体に到達していないのか  

が一瞬で分かります。

---

# 🎯 さらに一歩：あなたが貼ったコードから確実に言えること

あなたの ParseNamespace() は **クラス宣言の開始位置までしか進んでいない**。

つまり：

### ✔ ParseClass() が「クラス本体の行」を読む責任を持っている  
### ✔ ParseClass() の中でメソッド本体を読む必要がある  
### ❌ しかし実際には Body が空なので、ParseClass() が不完全  

ということです。

---

# ✨ 次のステップ（あなたが選べます）

1. **ParseClass() のコードを見せていただければ、Body が空になる原因を完全に特定できます。**  
   （全文でなくても、メソッドを読む部分だけで十分です）

2. または、  
   **ReMindBubbleSortAstGenerator の構造を推測して、正しい ParseClass() / ParseMethod() / ParseStatements() のテンプレートを作成する**  
   こともできます。
   
mylifewithviolinさん、どちらで進めましょう。


## 第６ステップの評価
今回のプロンプトに対する応答は、だいぶ詳細に立ち入った内容となりました。次ステップの提示も以前のような盛った言い回しはなく、具体的な選択肢となっております。どの段階で生成AIとの対話を離脱して人間系のデバッグで仕上げていくか悩ましいところですが、生成AIを使った実装支援はわたしも興味深いので、もう少し対応してみます。

# おわりに
第６ステップは以上です。次回の方向性はParseClass() 関連のコードを提示していく流れとなります。ログにはReMindBubbleSortAstGeneratorの出力結果が記録されているので、このログのテキストを遡って確認してくれると人間系の手間はだいぶ省力化される気はします。


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
