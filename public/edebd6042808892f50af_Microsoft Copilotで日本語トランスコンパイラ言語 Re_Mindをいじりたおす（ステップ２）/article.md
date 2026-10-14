# はじめに
日本語トランスコンパイラ言語 Re:Mindは鋭意実装中ですが、たてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。仕様策定者本人による実装だけがすべてではないため、逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第２ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。


# 第２ステップ　日本語トランスコンパイラ言語 Re:Mindの言語仕様の認知度を確認する

## プロンプト
オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）について、その言語仕様の詳細についてはどの程度の情報を認識していますか？定番のアルゴリズムをRe:Mindのソースコードで展開できるレベルですか？

## 生成レスポンス

ご質問のポイントを整理すると「Re:Mind言語仕様をどの程度把握しているか」「定番アルゴリズムをRe:Mindで記述できるレベルか」という確認ですね。

📖 私が認識しているRe:Mind仕様の範囲
- 仕様の公開状況
Qiita上で「Lv1.1ドラフト」「Lv1.2ドラフト」が公開されており、基本的な文法・記述ルールが提示されています。
- 制御構造（条件分岐、繰り返し）
- 演算子（算術、比較、論理）
- 関数定義と呼び出し
- 配列や文字列の扱い（ドラフト段階で簡易的に定義）
- 目的
日本語でアルゴリズムや仕様を記述し、それを他言語（Cなど）へトランスコンパイルすることを想定。
「日本語ロジック仕様記述」を重視しており、自然言語的な可読性を持たせています。
- 実装状況
完成した処理系はまだ存在せず、ドラフト仕様とサンプル記述が中心。VSCode拡張でシンタックスハイライトは提供されています。

✍️ 記述可能なレベル
- 定番アルゴリズム（例: フィボナッチ数列、ソート、探索）
→ ドラフト仕様に基づけば、擬似コード的にRe:Mindで展開可能です。
ただし「実際に動作するコンパイラ」が存在しないため、実行可能コードというより「仕様に沿った日本語ソース例」として記述する形になります。
例: フィボナッチ数列（Re:Mind風）

```
関数 フィボナッチ(整数 n) を定義する
    もし n が 0 以下ならば
        戻り値は 0
    もし n が 1 ならば
        戻り値は 1
    それ以外ならば
        戻り値は フィボナッチ(n - 1) + フィボナッチ(n - 2)
関数定義終了

整数 i を 0 から 10 まで繰り返す
    出力 フィボナッチ(i)
繰り返し終了
```

このように「日本語仕様記述」としては十分展開可能です。

✅ 結論
- 私はRe:Mindのドラフト仕様を把握しており、定番アルゴリズムをRe:Mind風ソースコードで展開できるレベルに認識しています。
- ただし「実際に動作する処理系」は未完成なので、実行可能コードではなく仕様準拠の記述例として提示することになります。


## 第２ステップの評価

自信ありの認識を示してくることと、ソースコード例は基本的に適合しないのは想定内でした。ネット上の情報から抽象化された概要は実勢を正しく認識していると評価できますが、個々の詳細は学習として残っていないと評価できます。マイナーな情報と思っていますのでこのあたりからは想定内です。

# おわりに
第２ステップは以上です。第３ステップは言語仕様の詳細をどの程度学習させられるかに進行します。
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
