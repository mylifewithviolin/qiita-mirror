# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第１４ステップで、トランスコンパイラ的な動作の続きとなりす。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１３ステップの後にはサインアウトがあります。

# 第１４ステップ
第１１ステップの生成バージョンを下記のバージョン情報で識別します。
定番アルゴリズム：線形探索法・2025-12-08版・3回目
定番アルゴリズム：二分探索法・2025-12-08版・3回目
定番アルゴリズム：バブルソート・2025-12-08版・3回目

上記バージョンのバブルソートの日本語トランスコンパイラ言語 Re:Mindによるソースコードを下記のプログラミング言語のソースコードにトランスコンパイルします。
Java
C#
Typescript
Go
VisualBasic.Net
VisualBasic for Application

第１２ステップで定番アルゴリズム：線形探索法・2025-12-08版・3回目のトランスコンパイルがまがりなりにも実行されたのに対して、第１３ステップで定番アルゴリズム：二分探索法・2025-12-08版・3回目のトランスコンパイルを試みたところ、ソースコードの特定を行う記述に少し装飾を加えてしまったためにCopilotがソースコードを認識しなくなるというアクシデントに見舞われました。今回は定番アルゴリズム：バブルソート・2025-12-08版・3回目を指定している点を除きほぼ第１２ステップと同じプロンプトで実行してみます。

## プロンプト
下記のバージョン情報で識別される
定番アルゴリズム：バブルソート・2025-12-08版・3回目
日本語トランスコンパイラ言語 Re:Mindのソースコードを下記のプログラミング言語のソースコードに変換してください。
・Java
・C#
・Typescript
・Go
・VisualBasic.Net
・VisualBasic for Application
生成された変換後のソースコードを下記のバージョン情報で識別し、次回以降も参照できるように保持してください。
定番アルゴリズム：バブルソート・2025-12-08版・3回目からJava・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からC#・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からTypescript・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からGo・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からC#・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic.Net・2025-12-13-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic for Application・2025-12-13-1回目変換
変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.1ドラフトに記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c
Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。クラス名の宣言は行わないでください。

## 生成レスポンス
元ソースの提示のお願い
「定番アルゴリズム：バブルソート・2025-12-08版・3回目」のRe:Mindコードフラグメント（関数宣言、引数、ローカル変数、日本語Javadoc注釈、コメント）を貼り付けてください。仕様に沿って正確にトランスコンパイルし、注釈の日本語／英語名の逆転やローカル変数の英語名置換を原文どおりに反映します。

- 確認したい点:
- 並び順: 昇順／降順
- 処理方式: 破壊的（インプレース）／非破壊（コピー返却）
- 型: 整数配列か、比較関数の有無
- 返却仕様: ソート済み配列返却か、voidでインプレースのみ
いただいた原文に合わせて、クラス宣言は行わず、6言語（Java／C#／TypeScript／Go／VB.NET／VBA）へ一括変換します。Javadoc採用言語は「@param 英語名 日本語名」に逆転、.NET言語はXMLドキュメントコメントへ変換して逆転します。ローカル変数は英語名へ置換し、元の日本語名対応をコメントで併記します。

生成物のバージョン識別と保持
各ソースの先頭に以下の識別子をヘッダコメントとして明記します。次回以降も同識別子で参照できます。
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からJava・2025-12-13-1回目変換
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からC#・2025-12-13-1回目変換
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からTypescript・2025-12-13-1回目変換
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からGo・2025-12-13-1回目変換
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic.Net・2025-12-13-1回目変換
- 定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic for Application・2025-12-13-1回目変換
Re:Mind 2023 Lv1.1ドラフト仕様に基づく注釈、制御構文、コメントモデルの対応で変換します。


## 第１４ステップの評価
Copilotがソースコードを認識しなくなっている点は第１３ステップと同じでした。この状況からどのように回復するか検討します。

# おわりに
第１４ステップは以上です。第１５ステップはCopilotがソースコードを認識しなくなっている点をどのようにリカバリーできるか検討します。
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
