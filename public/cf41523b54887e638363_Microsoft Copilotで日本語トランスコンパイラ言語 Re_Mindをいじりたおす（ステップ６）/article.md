# はじめに
日本語トランスコンパイラ言語 Re:Mindは鋭意実装中ですが、たてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第６ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第５ステップの後にはサインアウトがあります。


# 第６ステップ　引き続きCopilotによる日本語トランスコンパイラ言語 Re:Mindの詳しい言語仕様（リンク先のページ記述の情報由来）の学習結果を確認する

第３ステップで確認された下記の方法での学習成果を確認してみます。

>公式仕様文書やドラフト記事の提示
Qiitaなどに公開されている「Lv1.1ドラフト」「Lv1.2ドラフト」のリンクや抜粋を共有いただければ、その記述規則に従ってコード例を生成できます。

第５ステップでは実質さらに下記の補足が安全を見てプロンプトに込められていましたが、今回はこれはなくした状態で再現性を確認してみます。

>構文ルールの具体的な例
例えば「条件分岐は◇で始める」「繰り返しは〇で始める」「関数定義は□で始める」といったルールを教えていただければ、それに従ったRe:Mind風のアルゴリズム展開が可能です。

## プロンプト
下記のリンクは「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフトです。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c
ここには基本的な構文仕様が記述されています。
こちらに記載された内容を把握した上で、定番アルゴリズム：二分探索法のソースコードを日本語トランスコンパイラ言語 Re:Mindで書いてください。


## 生成レスポンス
二分探索法の Re:Mind 実装
Re:Mind 仕様の「関数宣言（▽…△）」「条件分岐（◇…の場合／◇他に／◇ここまで）」「繰り返し（○…の間は繰り返す／○ここまで）」「代入（・）」および「return（□return …）」の記法に従って、昇順に整列済みの整数配列に対する二分探索を実装します。

```mind:Re:Mind
// 昇順に整列された配列から値を探索し、見つかったインデックスを返す。見つからなければ -1。
▽public int 二分探索する(int[] 配列,int 値)
・int 左 = 0
・int 右 = 配列.Length - 1

○(左 <= 右) の間は繰り返す
    ・int 中央 = 左 + ((右 - 左) / 2)

    ◇配列[中央] == 値 の場合
        □return 中央
    ◇他に 配列[中央] < 値 の場合
        ・左 = 中央 + 1
    ◇他に
        ・右 = 中央 - 1
    ◇ここまで
○ここまで

□return -1
△
```


## 第６ステップの評価
英字系プログラミング言語にトランスコンパイルするためのJavaDocが少しゆるくなってしまいました。それに伴い、引数の場合はJavaDocのヘッダに記述できますが、ローカル変数の場合は（宣言箇所に記述する形になるとは思われますが）その記法を定義しておかないといけないことに気づきました。

また、JavaDocで通常英字系プログラミング言語の注釈とは逆のことを書くのはトランスコンパイラ言語の場合です。プログラミングロジック仕様記述言語としては直接トランスコンパイルはしないので、この記述は不要扱いです。



# おわりに
第６ステップは以上です。第７ステップは引き続き言語仕様の詳細学習のステップとなります。どこかのタイミングでターゲット言語にトランスコンパイルさせますが、Copilotさんのご提案どおり、アルゴリズム集を「日本語フロー図」的にまとめてみます。

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
