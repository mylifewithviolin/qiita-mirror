# はじめに
生成AI(Microsoft Copilot)に日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、ASTパーサ[^2]とC#コードジェネレータが一部動作するまで[^3]のところで、ここで主担当AIをGitHub Copilotに変更しました。そしてこれを機会にプログラミング言語名をRe:Mind（リマインド）から Aoi （あおい）に変更します。Re:Mindは開発プロジェクトコード名という位置づけといたします。過去コンテンツは漸次更新して参ります。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語 Aoi（Re:Mind）の原型を作成してもらった生成AI。モードは「無料プラン」。サインインした状態で使用します。貼り付けたソースコードの詳細内容を保持できるスコープに強い制約があるためいったんメインの担当を解除。ただし、GitHub Copilotの使い方アドバイザーとして継続利用。
## GitHub Copilot
Amazonのkiro-cliのskillsのようなことできるとうれしいなと思い、とりあえず使ってみようかということでGitHub Copilotのフリー版を導入。[前回の記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)でかなり近いことができることが判明して結果オーライでした。スーパバイザとしてMicrosoft Copilotを使うことからもそれが一番詳しい推察されるGitHub Copilotでいきます。


# 本記事のステップ
[前回の記事](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)で生成された「Re:Mind コンパイラ全体設計」の具体的な進め方の調整です。

## Microsoft Copilotとの事前準備
### プロンプト１
>CodeAgentでクレジットの消費をおさえながらplan.mdの各フェーズをコード生成することはできませんか？

#### 生成レスポンス１
>結論から言うと、あなたの目的――
>
>plan.md の各フェーズを CodeAgent でコード生成したい
>ただしクレジット消費は最小にしたい
>
>これは 可能です。ただし “正しい使い方” をしないと一瞬でクレジットを消費します。
>
>Copilot Free でも CodeAgent を「賢く」使えば、
>大規模プロジェクトを破綻なく進められます。
>
>以下、mylifewithviolinさんの Re:Mind プロジェクトに最適化した
クレジット最小 CodeAgent 運用戦略をまとめます。
>
>CodeAgent は「小さなタスクに分割して呼び出す」ことでクレジット消費を劇的に抑えられる。
大きなフェーズを丸ごと投げると、内部で大量の推論が走り、クレジット消費が跳ね上がります。しかし、小さな関数単位で依頼すれば消費は最小になります。

### プロンプト２
>とりあえずはPhase 0です。下記のPhase 0の３までは進みたいです。
>## Phase 0: スコープと前提整理
>1. 仕様書の構文を基準に、まず実装対象の最小・中間・拡張セットを分ける。
>2. 第 1 期の MVP では、以下を対象にする。
>   - 変数・定数・配列
>   - 関数宣言・関数呼び出し
>   - クラス宣言・メンバーアクセス
>   - 代入・戻り値
>   - 条件分岐・繰り返し
>   - 例外構文・switch は後続フェーズで扱う
>
>３. 既存の Program.cs の const string ReMindSourceCode を「入力サンプル」から「実行入口」に昇格させ、将来的にファイル入力や CLI 引数にも切り替えられる構造にする。

#### 生成レスポンス２
>了解しました、Phase 0 の 1〜3 を「CodeAgentを使わずに」「Copilot Freeで」「クレジット消費を最小化しながら」進めるための具体的な実行方法を、あなたのプロジェクト構造に合わせて整理します。
>
>ここは「コード生成フェーズ」ではなく 設計フェーズなので、
CodeAgent を使う必要はありません。
むしろ 使わないほうがクレジット消費が圧倒的に少なく、進行も安定します。

>Phase 0 を進める最適な方法（Copilot Free／クレジット最小）
>Phase 0-1
仕様書の構文を基準に、最小・中間・拡張セットを分ける
これは コード生成ではなく分類作業なので、
Copilot Free の Chat に次のように聞くのが最も効率的です。

>Phase 0-2
第1期 MVP の対象構文を確定する
ここもコード生成ではなく 選定作業なので、
Copilot Free の Chat に次のように依頼するのが最適です。

>Phase 0-3
Program.cs の ReMindSourceCode を「実行入口」に昇格させる
ここだけは 小さなコード修正が必要ですが、
CodeAgent を使う必要はありません。
Copilot Free の補完で十分です。


## GitHub Copilot
Microsoft Copilotが推奨したGitHub CopilotへのPhase 0の各ステップの実行プロンプトを逐次実行した結果、下記のmdが生成されました。

```md:docs\re_mind_syntax_classification.md
# Re:Mind 構文仕様の分類案

仕様書 [remind_specification.md](../remind_specification.md) をもとに、実装順に合わせて Re:Mind の構文を次の3セットに分類する。

## 1. 最小セット（MVP）

まずは「1つの小さなプログラムを通せる」レベルに絞る構成。

- 基本宣言
  - 変数宣言・代入
  - 定数宣言
  - 基本型（int, string, bool）
- 基本文法
  - コメント
  - リテラル
  - 四則演算・論理演算
  - `=` による代入
- 関数
  - 関数呼び出し
  - 値を返す関数
  - `return` / `返す`
- 制御構文
  - `if` 相当の分岐
  - `while` 相当の繰り返し
  - ブロック終了の構文（`ここまで`）
- 実行文
  - `□` で始まる文の実行形式

このセットだけでも、コンソール出力系の簡単なプログラムをトランスコンパイルできる土台となる。

## 2. 中間セット

最小セットを超えて、実用的な構文を追加する段階。

- 配列
  - 配列宣言
  - 配列初期化
- 制御構文の拡張
  - `switch` 相当
  - `for` 相当
  - `do-while` 相当
  - `break` / `continue` 相当の制御
- クラス
  - クラス宣言
  - インスタンス生成
  - フィールド参照
  - メソッド呼び出し
- 例外
  - `try/catch`
  - `finally`
  - `throw`
- コメント・注釈
  - Javadoc 風コメント
  - 引数・戻り値の英字名指定

この段階では、AST とコード生成の構造をかなり本格化させる必要がある。

## 3. 拡張セット

ターゲット言語との親和性を高め、言語仕様としての完成度を上げるための構文。

- 外部ライブラリ連携
  - `using` 相当
  - `import` 相当
  - 既存クラス・メソッドの宣言橋渡し
- 高度な型・オブジェクト機能
  - 継承
  - アクセス修飾子
  - null 条件演算子
  - null 合体演算子
- ターゲット言語依存の柔軟な記述
  - 既存言語構文のそのまま受け入れ
  - 仕様上のパススルー
- 追加の表記ゆれ
  - 省略形
  - 同義表現
  - エイリアス系構文

これは「言語仕様としては豊か」だが、実装コストはかなり高くなる。

## おすすめの実装順

1. 最小セット
2. 中間セット
3. 拡張セット

この順にすると、AST・パーサ・コード生成器の各層を段階的に育てやすい。
```
```md:docs\implementation_tasks.md
# Re:Mind 実装タスク一覧

このドキュメントは、Re:Mind の仕様を Lexer / Parser / AST / IR / CodeGenerator ごとの実装タスクとして整理した一覧である。

## 1. Lexer タスク

- Re:Mind の予約記号を識別できるようにする
  - `・`、`□`、`◇`、`〇`、`▽`、`△`、`▲`、`■`、`▼`
- 文字列・数値・識別子・演算子をトークンとして分解できるようにする
- コメントと Javadoc 風コメントをトークン化できるようにする
- 文字列リテラルや改行・空白の扱いを定義する

## 2. Parser タスク

- 変数宣言文を解析できるようにする
- 定数宣言文を解析できるようにする
- 関数呼び出し文を解析できるようにする
- 関数宣言文を解析できるようにする
- クラス宣言文を解析できるようにする
- クラスのインスタンス生成・参照・メソッド呼び出しを解析できるようにする
- 条件分岐文（if 相当）を解析できるようにする
- 繰り返し文（while / for / do-while 相当）を解析できるようにする
- 例外処理文（try / catch / finally / throw 相当）を解析できるようにする
- `□コンソール.一行表示する` のような中核構文を解析できるようにする

## 3. AST タスク

- AST ノードの基本構造を定義する
- 変数宣言ノードを追加する
- 定数宣言ノードを追加する
- 関数宣言ノードを追加する
- 関数呼び出しノードを追加する
- クラス宣言ノードを追加する
- クラスメンバノードを追加する
- 条件分岐ノードを追加する
- 繰り返しノードを追加する
- 例外処理ノードを追加する
- 既存の Ast.cs を拡張して、Re:Mind 構文に対応させる

## 4. IR タスク

- 中間表現の基本クラスを設計する
- 変数・定数・関数・クラスを IR へ落とし込めるようにする
- 条件分岐・ループ・例外処理を IR へ落とし込めるようにする
- 生成対象言語に依存しない命令体系を定義する
- IR から各ターゲット言語へ変換しやすい構造にする

## 5. CodeGenerator タスク

- C# 用コード生成器を拡張する
- Java 用コード生成器を拡張する
- VB.NET 用コード生成器を拡張する
- 変数宣言・代入・関数呼び出し・条件分岐・繰り返しを生成できるようにする
- `□コンソール.一行表示する` のような例を C#/Java/VB.NET へ変換できるようにする
- 各生成器で共通の出力ルールを揃える

## 6. 名前解決・シンボル管理タスク

- Imports の AliasClasses を使って名前解決できるようにする
- 変数名・関数名・クラス名の参照を解決できるようにする
- 同名シンボルの衝突を扱えるようにする
- 生成前にシンボルテーブルを参照できるようにする

## 7. 入力・実行フロータスク

- Program.cs の `const string ReMindSourceCode` を入力ソースとして扱えるようにする
- 入力文字列を Lexer → Parser → AST → IR → CodeGenerator の流れで処理する
- 実行結果として C#/Java/VB.NET のコンソール出力が得られるようにする
- 変換結果を標準出力またはファイル出力できるようにする

## 8. 実装順序

1. 最小構文の Lexer / Parser / AST / IR / CodeGenerator を実装する
2. 変数・関数・条件分岐・繰り返しの基本パスを通す
3. クラス・例外・配列などを追加する
4. 名前解決と外部ライブラリ連携を強化する
5. C#/Java/VB.NET の出力品質を整える

## 9. 完了条件

- Re:Mind の代表的なサンプルコードを C#/Java/VB.NET に変換できる
- `□コンソール.一行表示する` のような中核構文が正しく出力される
- 既存の Ast.cs と各 CodeGenerator を前提に、段階的に拡張できる構造になっている
```
## 本ステップの評価
わるくないと評価しています。本業の開発業務でもkiroにSKILL.mdを生成させて実行内容を確認してから実行という手順を多く使っています。GitHub Copilotでも同様のことができることが確認できたのは成果です。生成されるmdの内容はインプット情報の内容に依存します。このシリーズの記事ではAoi（Re:Mind）の言語仕様情報mdをしっかり読み込ませています。

# おわりに
以上です。次回の方向性は既存コードの修正の実行からとなります。

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
「Re:Mindをいじりたおす」の記事リストです。（ステップ降順）
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
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
「Re:MindのASTパーサが動作するまで」の記事リストです。（ステップ降順）
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[ステップ１１](
https://qiita.com/mylifewithviolin/items/9c891cdcc8d2bd78f36f)
[ステップ１０ 生成済コードの伝達完了](
https://qiita.com/mylifewithviolin/items/a0b5747e40e7b545175a)
[ステップ９](
https://qiita.com/mylifewithviolin/items/f34548d50a974fb4420e)
[ステップ８](
https://qiita.com/mylifewithviolin/items/cb8f54f87329d7e62c9a)
[ステップ７](https://qiita.com/mylifewithviolin/items/1e05c80a0cad0580f073)
[ステップ６ 生成済コードの伝達開始](https://qiita.com/mylifewithviolin/items/31e8413e0789e5433705)
[ステップ５](https://qiita.com/mylifewithviolin/items/2af14676b1c267af22a2)
[ステップ４ Program.csが動作](https://qiita.com/mylifewithviolin/items/b037019608d6b5d068a7)
[ステップ３](https://qiita.com/mylifewithviolin/items/7c9568d238550b997e21)
[ステップ２](https://qiita.com/mylifewithviolin/items/076e1a792b8545fae7a6)
[ステップ１ 検証環境構築](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)
[^3]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
「Re:MindのC#コード生成が動作するまで」の記事リストです。（ステップ降順）
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
[ステップ３](https://qiita.com/mylifewithviolin/items/9f8082ae6629c9d8e35a)
[ステップ２](https://qiita.com/mylifewithviolin/items/bcb4b56688101463937c)
[ステップ１](https://qiita.com/mylifewithviolin/items/54e3c7cdd2757b694f79)
