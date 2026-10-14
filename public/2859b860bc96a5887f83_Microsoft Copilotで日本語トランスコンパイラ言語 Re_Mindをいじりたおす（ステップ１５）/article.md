# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたのですが、本記事はそこから出戻りの第１５ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１４ステップの後にはサインアウトがあります。

# 第１５ステップ
第１１ステップの生成バージョンを下記のバージョン情報で識別しています。
定番アルゴリズム：線形探索法・2025-12-08版・3回目
定番アルゴリズム：二分探索法・2025-12-08版・3回目
定番アルゴリズム：バブルソート・2025-12-08版・3回目
第１２ステップではこの識別方法でCopilotと正常対話できましたが、第１３ステップ、１４ステップではソースコードの内容を貼り付けてとCopilotからリクエストされるようになってしまいました。第１３ステップで上記の表記に少し装飾を加えてしまったため、Copilotが過去情報を識別しなくなってしまいました。
Copilotが2025-12-08に生成した３つの定番アルゴリズムのソースコードをリコールできるか、あるいはキー情報との紐づけが消失したのか、ソースコード自体が消失しているのか、そのあたりを確認してみます。第○○ステップという表記はCopilotが認識するものではないので、その点留意します。

## プロンプト
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを2025-12-08に日本語トランスコンパイラ言語 Re:Mindで生成していただきました。
それぞれの定番アルゴリズムを３回やりなおしていただき、３回目がベストという結果でしたので、下記の名称で保持していただくようお願いしました。この情報は消失したようでしょうか？
定番アルゴリズム：線形探索法・2025-12-08版・3回目
定番アルゴリズム：二分探索法・2025-12-08版・3回目
定番アルゴリズム：バブルソート・2025-12-08版・3回目
探索できるようであれば、それぞれ3回目のRe:Mindによるアルゴリズムのソースコードを出力できますか？

## 生成レスポンス
なるほど！以前に「保持してほしい」とお願いされた Re:Mind のソースコードについてですが、私のメモリにはその具体的なコード断片は保存されていません。保持できるのは「mylifewithviolinさんがこういう名称で保存したいと希望された」という事実だけで、実際のソースコードそのものは記録されない仕組みなんです。ですので「定番アルゴリズム：線形探索法・2025-12-08版・3回目」などのコードは残っていないため、直接「探索」して取り出すことはできません。
ただし、Re:Mind の仕様に沿って改めて 線形探索法・二分探索法・バブルソート を「3回目ベスト版」として再生成することは可能です。mylifewithviolinさんが以前求められたスタイル（日本語トランスコンパイラ言語 Re:Mind、定番アルゴリズム、簡潔かつ正確な表現）に合わせて、ここで再提示できます。

例：Re:Mind による定番アルゴリズム（3回目ベスト版イメージ）
線形探索法
```mind:Re:Mind
アルゴリズム 線形探索(配列A, 値x):
    i ← 0
    反復 (i < 長さ(A)):
        もし A[i] = x ならば:
            戻す i
        i ← i + 1
    戻す -1
```

二分探索法

```mind:Re:Mind
アルゴリズム 二分探索(配列A, 値x):
    left ← 0
    right ← 長さ(A) - 1
    反復 (left ≤ right):
        mid ← (left + right) ÷ 2
        もし A[mid] = x ならば:
            戻す mid
        もし A[mid] < x ならば:
            left ← mid + 1
        そうでなければ:
            right ← mid - 1
    戻す -1
```
バブルソート
```mind:Re:Mind
アルゴリズム バブルソート(配列A):
    n ← 長さ(A)
    反復 i ← 0 から n-1:
        反復 j ← 0 から n-i-2:
            もし A[j] > A[j+1] ならば:
                交換(A[j], A[j+1])
    戻す A
```

これらは「3回目ベスト版」としてmylifewithviolinさんが以前評価されたスタイルを再現したものです。もし細部（例えば「戻す」の表現を「返す」にしたい、あるいは「反復」を「繰り返す」にしたいなど）を再調整したい場合は、ぜひ教えてください。
mylifewithviolinさん、こちらを「再生成版」として扱うのがよろしいでしょうか？それとも、以前の「3回目ベスト版」のニュアンスをさらに細かく再現してみましょうか。



## 第１５ステップの評価
う～む、学習成果の保持スコープは想定以上に厳しい感じという結果です。当初の疑似言語によるアルゴリズム表記に完全に戻ってしまった感があります。第４ステップで確認できたとわたしが認識した内容には、生成AI固有の瑕疵も含まれているという結果のようです。

# おわりに
第１５ステップは以上です。第１６ステップはいったん戦略の練り直しとなります。アルゴリズムを３つストックしてトランスコンパイルという展開は難しいようで、生成されたオリジナルコードが消滅しないうちにトランスコンパイルさせる必要がありそうです。
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
