# はじめに
日本語トランスコンパイラ言語 Re:Mindは鋭意実装中ですが、たてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。仕様策定者本人による実装だけがすべてではないため、逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第１ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。


# 第１ステップ　日本語トランスコンパイラ言語 Re:Mindの認知度を確認する

## プロンプト
 オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）について、どの程度の情報を認識していますか？

## 生成レスポンス

 要点:
Re:Mind（リマインド）は、まだ設計開発中の「日本語トランスコンパイラ言語」であり、Qiita上で仕様ドラフトが公開されている自作言語です。現時点では公式な完成実装はなく、仕様策定と試験的な記述例が中心です。

🔎 Re:Mindの概要
- 性質: 日本語で記述されたプログラムを他言語へトランスコンパイルすることを目的とした言語仕様。
- 公開形態: 「オープンな実装言語仕様」としてQiita記事でドラフトが公開されており、誰でも仕様を参考に実装や記事投稿が可能。
- 開発状況:
- 2023年に「Lv1.1ドラフト」がまとめられ、2024年末に「Lv1.2ドラフト」として改定・追加が検討開始された。
- 言語仕様はまだ流動的で、発案者による完成した実装は存在しない。

🛠 技術的特徴
- 記述スタイル: 日本語ロジック仕様記述を重視し、アルゴリズムやコンパイラ構造を日本語で表現できる。
- 応用例: C言語コンパイラの比較演算子ロジックをRe:Mindで記述する試みが紹介されている。
- ツール連携: VSCode拡張としてシンタックスハイライトやスニペット機能が実装されている。

📚 背景と関連
- Re:Mindは「Mind」など過去の日本語プログラミング言語の流れを意識しつつ、より仕様記述的な側面を強調している。
- 「日本語プログラミング言語」という文脈では、自然言語的な記述を可能にする試みが1980年代から存在しており、Re:Mindはその系譜に新しいアプローチを加えている。

✨ まとめ
現時点でRe:Mindは 「仕様策定段階の日本語トランスコンパイラ言語」 として認識されています。完成した処理系は存在せず、Qiita記事を中心にドラフト仕様や応用例が公開されている段階です。つまり「研究・試作的な言語仕様」としての情報は豊富ですが、実用的なコンパイラやランタイムはまだ整備されていません。

👉 ご希望なら、Re:Mindのドラフト仕様を具体的なコード例（例えば「ビット演算を日本語で書く」）に展開してみましょうか？

## 第１ステップの評価

けっこうまともな認識で驚きました。実勢を正しく認識していると評価できます。マイナーな情報と思っていますので認識されていないという想定もありましたが、Qiitaは検索エンジン露出の面で有利な影響もあってか、ネットワーク接続型の生成AIの場合は十分認識されていて、まずは第１ステップクリアです。

# おわりに
第１ステップは以上です。第２ステップは言語仕様の詳細をどの程度学習させられるか、あるは学習済なのかの評価に進行します。

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
