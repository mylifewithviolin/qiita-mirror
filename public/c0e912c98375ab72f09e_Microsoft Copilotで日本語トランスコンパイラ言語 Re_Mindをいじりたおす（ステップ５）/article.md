# はじめに
日本語トランスコンパイラ言語 Re:Mindは鋭意実装中ですが、たてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第５ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。


# 第５ステップ
Copilotによる日本語トランスコンパイラ言語 Re:Mindの詳しい言語仕様（リンク先のページ記述の情報由来）の学習結果を確認する

第３ステップで確認された下記の方法での学習成果を確認してみます。

>公式仕様文書やドラフト記事の提示
Qiitaなどに公開されている「Lv1.1ドラフト」「Lv1.2ドラフト」のリンクや抜粋を共有いただければ、その記述規則に従ってコード例を生成できます。

## プロンプト
下記のリンクは「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフトです。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c
ここには基本的な構文仕様が記述されています。
こちらに記載された内容を把握した上で、定番アルゴリズム：線形探索法のソースコードを日本語トランスコンパイラ言語 Re:Mindで書いてください。
制御構文の開始シンボルとして、◇、〇、・、□などの全角記号を用い、箇条書きされた日本文としての体裁を保持することを忘れずにお願いします。◇は分岐構文、〇はループ構文の開始と終了を表し、冗長な日本語表記がなくてもフロー図の表現に慣れている方が直感的に認識できることを考慮しています。

## 生成レスポンス
以下に、Re:Mind仕様（2023 Lv1.1ドラフト）に基づいた「線形探索法」のソースコード例を示します。
制御構文は指定の全角記号（◇, 〇, ・, □）を用い、箇条書き形式で直感的に理解できる体裁にしています。

```mind:Re:Mind
/** linearSearch */
/** @param 配列 array */
/** @param 探す値 target */
/** @return 見つかった位置 index、なければ -1 */
▽public int 線形探索する(int[] 配列, int 探す値)
・int 結果 = -1

〇int i=0, i<配列.Length, i++ 繰り返す
    ◇配列[i] == 探す値 の場合
        ・結果 = i
        ・やめる
    ◇ここまで
〇ここまで

□結果 を返す
△
```

解説ポイント
- 関数宣言は ▽ で開始し、△ で終了します。
- ループ構文は 〇 で開始し、〇ここまで で終了。ここでは for 相当の形式を採用。
- 分岐構文は ◇条件 の場合 ～ ◇ここまで で囲みます。
- 変数宣言・代入は ・ を先頭に置き、箇条書き的に記述。
- 戻り値は □変数 を返す で表現。
このように、Re:Mindの仕様に沿って「フロー図的な直感性」を保ちながら、線形探索アルゴリズムを簡潔に表現できます。
mylifewithviolinさんのご要望通り、冗長な日本語表記を省きつつ、記号と箇条書きで直感的に理解できる構造になっています。

【参考仕様】Re:Mind 2023 Lv1.1ドラフト（分岐構文◇、ループ構文〇、箇条書き・、戻り値□の利用）

このスタイルで他の定番アルゴリズム（例えば二分探索やバブルソート）も同じ記号体系で書き起こすと、アルゴリズム集を「日本語フロー図」的にまとめることができます。次は二分探索を同じ形式で書いてみましょうか？




## 第５ステップの評価
正直驚きました。もう少しあさっての感じで返ってくることを想定しておりました。リンクだけでは心配だったので、構文上の基本的な注意事項をプロンプトのテキストで強調したのもよかったかもしれません。英字系プログラミング言語にトランスコンパイルするためのJavaDocもちゃんと書いてきてくれたのはうれしいです。



# おわりに
第５ステップは以上です。第６ステップは引き続き言語仕様の詳細学習のステップとなります。どこかのタイミングでターゲット言語にトランスコンパイルさせますが、Copilotさんのご提案どおり、アルゴリズム集を「日本語フロー図」的にまとめてみます。
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
