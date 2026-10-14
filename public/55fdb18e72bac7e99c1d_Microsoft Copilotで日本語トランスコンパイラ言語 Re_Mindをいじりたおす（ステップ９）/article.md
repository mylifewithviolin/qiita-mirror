# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第９ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第８ステップの後にはサインアウトがあります。

# 第９ステップ
第５ステップ、第６ステップ、第７ステップで定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindで生成していただきましたが、バージョニング情報を付与して再生してもらいます。

## プロンプト
下記のリンクは「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフトです。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c
ここには基本的な構文仕様が記述されています。
こちらに記載された内容を把握した上で、定番アルゴリズム：線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindで書いてください。
制御構文の開始シンボルとして、◇、〇、・、□などの全角記号を用い、箇条書きされた日本文としての体裁を保持することを忘れずにお願いします。◇は分岐構文、〇はループ構文の開始と終了を表し、冗長な日本語表記がなくてもフロー図の表現に慣れている方が直感的に認識できることを考慮しています。
また、javadocと同じ/** */で半角英字を囲って、変数宣言文、関数宣言文、クラス宣言の直前に記述することで、ターゲット言語上の英字名を指定できます。ローカル変数のjavadocの記述を忘れないようにしてください。基本的には日本語名を英語名に翻訳していただければだいじょうぶです。
今回生成したソースコードをそれぞれ
定番アルゴリズム：線形探索法・2025-12-08版・1回目
定番アルゴリズム：二分探索法・2025-12-08版・1回目
定番アルゴリズム：バブルソート・2025-12-08版・1回目
というバージョンラベルを紐づけて、同一のソースコードを後から参照できるようにしてください。

## 生成レスポンス
ご要望に沿って、Re:Mind仕様（2023 Lv1.1ドラフト）に基づき、線形探索法・二分探索法・バブルソートのソースコードを日本語トランスコンパイラ形式で記述しました。各アルゴリズムにはバージョンラベルを付与してあります。

定番アルゴリズム：線形探索法・2025-12-08版・1回目
```mind:Re:Mind
/** LinearSearch */
◇public int 線形探索する(int[] 配列, int 探す値)
  /** i */
  ・int インデックス = 0
  〇インデックス < 配列.Length の間は繰り返す
    ◇配列[インデックス] == 探す値 の場合
      □return インデックス
    ◇ここまで
    □インデックス++
  〇ここまで
  □return -1
◇ここまで
```
定番アルゴリズム：二分探索法・2025-12-08版・1回目
```mind:Re:Mind
/** BinarySearch */
◇public int 二分探索する(int[] 配列, int 探す値)
  /** left */
  ・int 左端 = 0
  /** right */
  ・int 右端 = 配列.Length - 1
  〇左端 <= 右端 の間は繰り返す
    /** mid */
    ・int 中央 = (左端 + 右端) / 2
    ◇配列[中央] == 探す値 の場合
      □return 中央
    ◇ここまで
    ◇配列[中央] < 探す値 の場合
      □左端 = 中央 + 1
    ◇他に
      □右端 = 中央 - 1
    ◇ここまで
  〇ここまで
  □return -1
◇ここまで
```
定番アルゴリズム：バブルソート・2025-12-08版・1回目

```mind:Re:Mind
/** BubbleSort */
◇public void バブルソートする(int[] 配列)
  /** i */
  ・int 外側 = 0
  〇外側 < 配列.Length の間は繰り返す
    /** j */
    ・int 内側 = 0
    〇内側 < 配列.Length - 外側 - 1 の間は繰り返す
      ◇配列[内側] > 配列[内側 + 1] の場合
        /** temp */
        ・int 一時 = 配列[内側]
        □配列[内側] = 配列[内側 + 1]
        □配列[内側 + 1] = 一時
      ◇ここまで
      □内側++
    〇ここまで
    □外側++
  〇ここまで
◇ここまで
```
補足
- ◇ は分岐構文（if/else）、〇 はループ構文（for/while）、・ は変数宣言、□ は処理文を表現しています。
- / */ コメントで英字名を指定し、Re:Mind仕様に従って日本語名と英字名を対応付けています。
- 各アルゴリズムにバージョンラベルを明記しましたので、後から参照可能です。

mylifewithviolinさん、この形式はフローチャート的に直感的な読みやすさを意識しました。次は「挿入ソート」や「選択ソート」など他の定番アルゴリズムも同じスタイルで展開してみますか？


## 第９ステップの評価
ローカル変数の内側、外側をi、jとjavadocで注釈してきたのは驚きました。最初の線形探索法のソースを生成したときの、関数引数名にまでちゃんとjavadocしてくれてたのは再現しないようでした。次回試みてみます。

# おわりに
第９ステップは以上です。第１０ステップは引き続き言語仕様の詳細学習のステップの継続となりますが、各定番アルゴリズムのフィードバックを試みます。
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
