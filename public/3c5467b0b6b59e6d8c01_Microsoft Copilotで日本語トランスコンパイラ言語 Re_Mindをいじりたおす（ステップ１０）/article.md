# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第１０ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第８ステップの後にはサインアウトがあります。

# 第１０ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生してもらい、バージョニング情報付きのソースコードにフィードバック修正を試みます。

## プロンプト
前回生成したソースコードは以下のバージョン情報で識別されています。
定番アルゴリズム：線形探索法・2025-12-08版・1回目
定番アルゴリズム：二分探索法・2025-12-08版・1回目
定番アルゴリズム：バブルソート・2025-12-08版・1回目
それぞれに対して関数ヘッダのjavadocに引数の英語名注釈を追加してください。それ以外は上記のバージョンの状態を維持してください。
今回の生成バージョンを下記のバージョン情報で識別します。
定番アルゴリズム：線形探索法・2025-12-08版・2回目
定番アルゴリズム：二分探索法・2025-12-08版・2回目
定番アルゴリズム：バブルソート・2025-12-08版・2回目

## 生成レスポンス
承知しました。前回生成したソースコードを「1回目」バージョンから引数の英語名注釈を追加した「2回目」バージョンに更新します。関数ヘッダのjavadocに@param相当の英語名を記述し、それ以外は前回の状態を維持しています。

定番アルゴリズム：線形探索法・2025-12-08版・2回目
```mind:Re:Mind
/** LinearSearch
 * @param array
 * @param target
 */
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
定番アルゴリズム：二分探索法・2025-12-08版・2回目
```mind:Re:Mind
/** BinarySearch
 * @param array
 * @param target
 */
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
定番アルゴリズム：バブルソート・2025-12-08版・2回目
```mind:Re:Mind
/** BubbleSort
 * @param array
 */
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

これで「2回目」バージョンは完成です。この形式で「挿入ソート」や「選択ソート」など他のアルゴリズムも同じスタイルで展開していくと、Re:Mind仕様の定番アルゴリズム集が整っていきますね。


## 第１０ステップの評価
第５ステップで最初の線形探索法のソースを生成したときの、関数引数名にまでちゃんとjavadocしてくれてたのは再現しないようでした。再度次回試みてみます。

# おわりに
第１０ステップは以上です。第１１ステップは引き続き言語仕様の詳細学習のステップの継続となりますが、各定番アルゴリズムのフィードバックを試みます。ここからは苦行の連続となっていくのでしょうか？
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
