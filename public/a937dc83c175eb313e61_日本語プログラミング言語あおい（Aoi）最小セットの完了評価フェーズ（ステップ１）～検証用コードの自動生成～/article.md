# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の完了評価フェーズのステップ１になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## GitHub Copilot
GitHub CopilotのPro+版。実装と検証の主担当。
## Microsoft Copilot
GitHub Copilotのスーパバイザ[^2]

# 本記事のステップ
## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。Phase 1～8に分けて実装完了しました。[^1]
### Phase 9: 検証と品質改善
[前回の記事](https://qiita.com/mylifewithviolin/items/de68617a710940b0fb23)でPhase 9をいったん完了し完了条件の評価に進みました。

### Phase 10: 完了条件
Phase 9にて検証したバブルソート、線形探索法、二分探索法の定番アルゴリズムのコンソールアプリケーションの３言語対応を踏まえ、最小セット（MVP）の定義とそれぞれのドキュメントの完了条件に照らし合わせてどの程度の状態なのかを評価してみました。

**docs\最小セットMVPの実装済要件.md　一部抜粋**
前回の記事では一部抜粋とはいえ、現状全体仕様に対する実装状態も論じられている部分を含めたためかなり広範囲となったので、今回は最小セットMVPの実装状態に関する範囲のみを抜粋しました。

```md:docs\最小セットMVPの実装済要件.md
# Re:Mind 最小セットMVPの実装済要件

## 5. MVPとして実装済みと判断できる最小要件
次の要件をMVPの実装済みセットとする。

1. UTF-8のRe:Mindソースをファイルから読み込める
2. 日本語識別子とRe:Mindの基本全角記号を字句解析できる
3. ドキュメントコメントからターゲット名を取得できる
4. namespace/class/methodの基本構造をAST化できる
5. ローカル変数、フィールド、代入をAST/IR化できる
6. 配列リテラルと添字アクセスを基本変換できる
7. 関数宣言、基本的な関数呼び出し、returnを変換できる
8. if、while、限定的なforを変換できる
9. Java、C#、VB.NETの基本ソースを出力できる
10. Console出力を各ターゲットの標準出力へ変換できる
11. CLIで入力ファイルと出力ファイルを指定できる
12. Javaについて固定JDKで生成ソースをコンパイル検証できる

この最小セットは、仕様全体ではなく、基本アルゴリズムとコンソール出力を対象
にしたトランスコンパイラMVPである。

```
今後はこの定義をMVPの実装済みセットとします。

```md
# 8. 結論
現在の実装は、Re:Mind仕様の基本構文を使った小規模なアルゴリズムとコンソール
出力を、C#・Java・VB.NETへ変換するMVPとしては成立している。

## 9. 構文分類案のMVP要件との照合
[re_mind_syntax_classification.md](./re_mind_syntax_classification.md) 
の「1. 最小セット（MVP）」に記載された要件を、現在の実装状態と照合した。

### 9.1 判定基準
- **満たす**: 現在のLexer、Parser、AST/IR、CodeGeneratorの経路で基本形を
  処理できる
- **部分的に満たす**: 基本例は処理できるが、仕様に含まれる表記や型・組み合わせ
  に制限がある
- **満たさない**: ASTの型だけが存在する、またはParser以降の処理経路が未接続で
  ある
  
### 9.3 MVP全体の判定
**判定: 部分達成。分類案に定義されたMVP全体を満たしているとは言えない。**

理由は、分類案のMVPに必須の次の要件が未達または不十分だからである。

1. 定数宣言がParserからCodeGeneratorまで接続されていない
2. `&&`、`||`、`!` の論理演算が未実装である
3. `bool`、null、リテラルの処理と型検査が不十分である
4. return、代入、関数呼び出しに対応できる表記と型の範囲が限定されている
5. `ここまで` と `□` の基本形はあるが、仕様上の省略形・複合形まで保証できない

一方、次の**縮小版MVP**は成立している。

//```text
変数・基本代入
数値・文字列リテラル
基本的な算術・比較演算
関数宣言・基本呼び出し・限定的なreturn
基本if・while・限定for
Console出力
C#・Java・VB.NETの基本コード生成
//```

したがって、現在の実装の正確な位置付けは次の通りである。

//```text
分類案のMVP全体: 部分達成
縮小版の基本トランスコンパイルMVP: 達成
分類案の中間セット: 配列・for・コメントなど一部先行実装
分類案の拡張セット: 固定マッピングを除き未達または部分実装
//```

### 9.4 分類案のMVPを正式に満たすための追加作業
優先度の高い順に、次を実装・検証する必要がある。

1. 定数宣言をParser、IR、C#、Java、VB.NET Generatorへ接続する
2. `&&`、`||`、`!` と真偽値リテラルをLexer、Parser、型検査、Generatorへ
  接続する
3. `return` / `返す` の構文を統一し、戻り値型と経路の検査を追加する
4. 代入、関数呼び出し、配列・メンバー操作の左辺と引数型を検証する
5. `ここまで`、省略形、入れ子構文の受入テストを追加する
6. 1つのMVPサンプルに定数、bool論理式、return、if、while、Console出力を
  組み込み、3ターゲットでコンパイル検証する
```

完了評価フェーズでは上記の課題を満たすことをゴールとします。前回記事の最初の完了評価としては不合格。本記事以降では上記の課題の解消に進行します。具体的に本記事では課題を解消するためのあおいの検証用ソースコードの自動生成から開始します。


## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでMicrosoft Copilotとのやりとりはなかったです。
## GitHub Copilot
### プロンプト１
>docs\最小セットMVPの実装済要件.md
の
9.4 分類案のMVPを正式に満たすための追加作業
の
>6. 1つのMVPサンプルに定数、bool論理式、return、if、while、Console出力を組み込み、3ターゲットでコンパイル検証する
>
>を網羅的に検証する
C#/VB.NET用のaoiサンプルソース　.aoi拡張子の直前・主ファイル名の末尾にcsを付加
Java用のサンプルソース　.aoi拡張子の直前・主ファイル名の末尾jvを付加
を作成する実行プランを
docs\最小セットMVPの未実装要件検証用ソースコード作成プラン.md
に出力してください。

#### 生成レスポンス１
>検証用ソースコード作成・実行プランを 最小セットMVPの未実装要件検証用ソースコード作成プラン.md に出力しました。
>
>含まれる内容:
mvpvalidationcs.aoi
mvpvalidationjv.aoi
定数、bool論理式、return、if、while、Console出力の共通仕様
Lexer → Parser → AST → IR → SemanticResolver → CodeGeneratorの検証手順
C#、Java、VB.NETの生成・コンパイル・実行検証
Javaの固定 javac コマンド
期待する実行結果 0 / 1 / 2
失敗時の切り分け順
最終成果物と受入基準
ファイル名は指定どおり、C#/VB.NET用を mvpvalidationcs.aoi、Java用を mvpvalidationjv.aoi とする計画にしています。

### プロンプト２
>docs\最小セットMVPの未実装要件検証用ソースコード作成プラン.md
を実行して
docs\最小セットMVPの未実装要件検証用ソースコード作成プラン完了レポート.md
に出力してください。
#### 生成レスポンス２
>計画を実行し、検証用AOI 2ファイルを作成して、Lexer/Parser/IR/3ターゲット生成・コンパイル・実行まで進めます。まず計画で指定した構文が現行Lexer/Parserでどこまで受け付けられるかを確認し、最小限のソースを作成します。

下記のような検証用のあおいソースコードが生成されました。
```md
C:\developments\cs12\astsample\sourceFiles>dir p*.aoi

2026/09/24  22:59               519 priority01assignmenttypecs.aoi
2026/09/24  22:59               533 priority01assignmenttypejv.aoi
2026/09/24  22:59               705 priority01calltypecs.aoi
2026/09/24  22:59               719 priority01calltypejv.aoi
2026/09/24  22:59               611 priority01conditiontypecs.aoi
2026/09/24  22:59               625 priority01conditiontypejv.aoi
2026/09/24  22:59               591 priority01returntypecs.aoi
2026/09/24  22:59               605 priority01returntypejv.aoi
2026/09/24  22:58             1,111 priority01semanticvalidcs.aoi
2026/09/24  22:58             1,125 priority01semanticvalidjv.aoi
2026/09/24  22:59               491 priority01undefinedcs.aoi
2026/09/24  22:59               505 priority01undefinedjv.aoi
2026/09/24  22:59               568 priority02constantarraycs.aoi
2026/09/24  22:59               582 priority02constantarrayjv.aoi
2026/09/24  22:59               701 priority02constantlocalcs.aoi
2026/09/24  22:59               715 priority02constantlocaljv.aoi
2026/09/24  22:59               529 priority02constantreassigncs.aoi
2026/09/24  22:59               543 priority02constantreassignjv.aoi
2026/09/24  22:59               776 priority03elseifcs.aoi
2026/09/24  22:59               790 priority03elseifjv.aoi
2026/09/24  23:00               718 priority03infiniteloopcs.aoi
2026/09/24  23:00               732 priority03infiniteloopjv.aoi
2026/09/24  23:00               574 priority03omitendcs.aoi
2026/09/24  23:00               588 priority03omitendjv.aoi
2026/09/24  22:59               666 priority03returnkeywordcs.aoi
2026/09/24  22:59               680 priority03returnkeywordjv.aoi
2026/09/24  23:00               474 priority04aliascustomcs.aoi
2026/09/24  23:00               488 priority04aliascustomjv.aoi
2026/09/24  23:00               484 priority04aliasinvalidcs.aoi
2026/09/24  23:00               498 priority04aliasinvalidjv.aoi
2026/09/24  23:00               764 priority04aliasmembercs.aoi
2026/09/24  23:00               785 priority04aliasmemberjv.aoi
2026/09/24  23:00               619 priority05dowhilecs.aoi
2026/09/24  23:00               633 priority05dowhilejv.aoi
2026/09/24  23:00               753 priority05exceptioncs.aoi
2026/09/24  23:00               767 priority05exceptionjv.aoi
2026/09/24  23:00               841 priority05loopcontrolcs.aoi
2026/09/24  23:00               855 priority05loopcontroljv.aoi
2026/09/24  23:00               864 priority05switchcs.aoi
2026/09/24  23:00               878 priority05switchjv.aoi
2026/09/24  23:00               765 priority06inheritancecs.aoi
2026/09/24  23:00               779 priority06inheritancejv.aoi
2026/09/24  23:00               833 priority06instancecs.aoi
2026/09/24  23:00               847 priority06instancejv.aoi
2026/09/24  23:00               627 priority06nulloperatorcs.aoi
2026/09/24  23:00               641 priority06nulloperatorjv.aoi
2026/09/24  23:00             2,377 priority07acceptancecs.aoi
2026/09/24  23:00             2,391 priority07acceptancejv.aoi
              48 個のファイル              36,265 バイト
```

下記は上記のリストの先頭ファイルです。型不一致のエラー検証目的のC#/VB.NET用となります。
```aoi:sourceFiles\priority01assignmenttypecs.aoi
▽名前空間 Priority01AssignmentType
    /** Program */
    ▽public クラス プログラム型
        /** Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            /** count */
            ・int 個数 = 0
            □個数 = "bad"
        △
    △
△
■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲
```
下記は上記のリストの２ファイル目です。１ファイル目と同じ、型不一致のエラー検証目的でJava用となります。インポートするだけ違う形でしっかり作成されています。

```aoi:sourceFiles\priority01assignmenttypejv.aoi
▽名前空間 Priority01AssignmentType
    /** Program */
    ▽public クラス プログラム型
        /** Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            /** count */
            ・int 個数 = 0
            □個数 = "bad"
        △
    △
△
■インポートする java.lang.System
▼public class コンソール PrintStream System.out
    ▼public static 一行表示する(string value)
        ■println (String value)
    ▲
▲
```
## 本ステップの評価
今回は「最小セット（MVP）」の要件を満たすための優先度の高い課題の解消を実行する際の検証用ソースコードを作成してみました。こんだけ大量に作成してくれるとめちゃ助かりますね。次回は課題の解消にむかって検証・修正のワークフローを実行してみます。

# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。


[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[^2]:スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

