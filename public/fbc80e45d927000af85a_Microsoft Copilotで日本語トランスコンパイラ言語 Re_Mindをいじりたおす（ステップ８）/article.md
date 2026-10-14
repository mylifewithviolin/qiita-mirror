# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第８ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第７ステップの後にはサインアウトがあります。


# 第８ステップ
第５ステップ、第６ステップ、第７ステップで定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindで生成していただきましたが、第６ステップ、第７ステップではトランスコンパイラ言語仕様としては劣化が観測されましたので（ロジック仕様記述言語仕様としては問題ないのですが、トランスコンパイル先の英字言語への関数名、変数名の英語注釈の欠落）このあたりのリカバリーを試みます。しかし、その前段階として生成AIが自身が生成したソースコードを具体的に保持しているのかを確認し、バージョニングが可能かどうかを検討します。

## プロンプト
ありがとうございます。これまで定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindで生成していただきましたが、このソースコードはハードコピーを控えていますが？それとも毎回同じ感じで再生されます？これかな何回か出力内容の改善を試みたいのですが、元の出力バージョンを特定して再現することはできますか？
例えば、定番アルゴリズム：線形探索法・１回目出力　または定番アルゴリズム：線形探索法・生成年月日―ｎ　などの指定（ｎは同じ生成年月日での出力回数目）

## 生成レスポンス
いいご質問ですね。整理してお答えします。

出力の扱いについて
- 私が生成したソースコードは「ハードコピー」として保存されているわけではありません。
- そのため「線形探索法・1回目出力」といったラベルを自動的に付けて記録しているわけではなく、毎回の生成はその場限りです。

再現性について
- 同じアルゴリズムを同じ条件で依頼すれば、基本的には似た構造のコードを再生します。
- ただし、説明の仕方やコメントの付け方などは、その時の文脈や私の表現選択によって微妙に変わることがあります。

バージョン管理の方法
もし「1回目出力」「2回目出力」といった形で改善の履歴を残したい場合は、以下のような方法が有効です。
- ユーザー側でラベルを付ける
例：「定番アルゴリズム：線形探索法・2025-12-07版・1回目」などと記録しておく。
- 私に指定して再現を依頼する
例：「線形探索法・2025-12-07版・1回目の出力を再現してください」と言っていただければ、その時点で生成したスタイルを意識して再現します。
- 改善履歴を明示する
「前回の出力ではコメントが少なかったので、今回はコメントを増やして」といった指示をいただければ、バージョン違いを明確にできます。

提案
mylifewithviolinさんが「改善の試み」を体系的に残したいなら、
- 出力ごとに日付＋通し番号を付けて管理する
- そのラベルを私に伝えて再現依頼する
という流れが一番スムーズです。

mylifewithviolinさん、次に試すとしたら「線形探索法・最適化版（例えば早期終了や汎用比較関数対応）」などを別バージョンとして生成し、ラベルを付けて比較してみるのはいかがでしょう。


## 第８ステップの評価
概ね想定した感じです。画像生成とかお願いすると、構図は前回と同じでここだけ変えてとプロンプトを投げてもよけいなところも変えてくるので、このあたりCopilot的に要注意点と考えておりました。とりあえずこれまでの生成はトライアルということで、バージョニング情報を指定して生成しなおしてもらうところからやり直します。

# おわりに
第８ステップは以上です。第９ステップは引き続き言語仕様の詳細学習のステップの継続となりますが、フィードバックを試みる手前の課題が上記のとおりです。
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
