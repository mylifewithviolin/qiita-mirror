# はじめに
生成AI(Microsoft Copilot)に日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、ASTパーサが動作するまでの検証を経て[^2]C#コードジェネレータが一部動作するまでCopilotと対話していました[^3]が、ここでソースコードのローカルプロジェクトを読み込むGitHub Copilotに担当AI？を変更しました。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語トランスコンパイラ言語 Re:Mindの原型を作成してもらった生成AI。モードは「無料プラン」。サインインした状態で使用します。貼り付けたソースコードの詳細内容を保持できるスコープに強い制約があるためいったんメインの担当を解除。ただし、GitHub Copilotの使い方アドバイザーとして継続利用。
## GitHub Copilot
Amazonのkiro-cliのskillsのようなことできるとうれしいなと思い、いっそのことkiro-cliからやりなおそうかとも思ったのですが、GitHub Copilotも似たようなことができるのであればとりあえず使ってみようかなということでGitHub Copilotのフリー版を導入。

# 第１ステップ
とりあえずGitHub CopilotのPlanエージェントがどの程度の計画を生成するのかお試しです。６月に導入したとき、Copilotが生成した６つのソースコードへの注釈付けに失敗し（ソースコードの保存文字コードがばらついていて、VSCodeの既定の文字コードをShift-JISにしたままだった。）最終的にソースコード内の既存日本語文字列の扱いに失敗してクレジットを大量消費してしまったので、今回は月内クレジットの消費量を抑えるため、事前にCopilotにGitHub Copilotの使い方を確認していました。現時点でVSCodeの既定の文字コードはUTF-8としてすべてのソースコードの文字コードをUTF-8で再保存しています。


## Microsoft Copilotとの事前準備

### プロンプト１
>仕様が記載されているマークダウンファイルをPlanAgentに読み込ませるにはどうすればよいですか？
#### 生成レスポンス１
結論：PlanAgent に Markdown 仕様ファイルを読み込ませる方法は 3 通りあります。  
これは VSCode / GitHub Copilot の公式仕様（AGENTS.md / custom instructions）に基づいています。
1. Chat でファイルを「添付」する（最も簡単）
2. Markdown をチャットにドラッグ＆ドロップする
3. AGENTS.md / copilot-instructions.md に仕様を組み込む（永続的に読ませる）

mylifewithviolinさんのように 仕様が長く、AST → 生成パイプラインのような複雑な構造化作業をする場合：
最適解：AGENTS.md に仕様をリンクしつつ、作業時は添付で補強する
これが最も安定して PlanAgent が仕様を理解します。

#### レスポンス１の評価
この事前調査をやってよかったのはAGENTS.mdの存在を知ったこと。後述のCopilotが生成したサンプルの内容を見た感じ、Kiro-Cliのskills.mdに近い感じでした。（あくまで筆者の感想です。）また、Copilotは以前のRe:Mindのやりとりを大枠は覚えているので話はスムーズでした。

### プロンプト２
>Re:Mindの仕様のmdはVSCodeプロジェクトフォルダのルートに下記のファイル名で保存してあります。
remind_specification.md
AGENTS.mdはどこに置けばよいですか？

#### 生成レスポンス２

結論から言うと、AGENTS.md は VSCode プロジェクトのルートに置くのが正しい配置です。  mylifewithviolinさんが remind_specification.md を置いたのと 同じフォルダ階層に置けば PlanAgent が自動で読み取ります。

```
your-project-root/
├── AGENTS.md        ← ここに置く（必須）
├── remind_specification.md
├── src/
├── docs/
└── その他のファイル
```
GitHub Copilot の Agent（PlanAgent / CodeAgent）は プロジェクトルートの AGENTS.md を自動で読み込む仕様になっています。
mylifewithviolinさんのプロジェクトに最適化したテンプレートを示します。

```md:AGENTS.md
# PlanAgent Instructions

このプロジェクトの仕様は `remind_specification.md` に記載されています。
PlanAgent は計画作成時にこの仕様を必ず参照してください。

## 仕様ファイル
- ./remind_specification.md

## PlanAgent に求めること
- 仕様に基づいた正確な計画の作成
- AST → 中間表現 → C# / Java / VB.NET 生成パイプラインの構造化
- 仕様の曖昧な部分があれば質問を返すこと
- 計画は `plan.md` として出力すること
```
#### レスポンス２の評価
置き場所だけではなくAGENTS.mdのテンプレートをCopilotが作成してくれたのは助かりました。内容も理解してくれている感じはします。

### プロンプト３
>とりあえずご提案いただいたAGENTS.mdの状態でPlanAgentを起動するにはどうすればよいですか？Re:MindのサンプルソースコードがProgram.csのconst string ReMindSourceCode変数に定義されているので、それをC#,Java,VB.NETのソースコードをコンソール出力できるようになるのが最初のステップです。既にプロジェクト内にはCopilotによって生成されたRe:MindのサンプルソースコードをASTに変換するAst.csが実装れていて、ASTからC#,Java,VB.NETのソースコードを生成するコードジェネレータCSharpCodeGenerator.cs、JavaCodeGenerator.cs、VbnetCodeGenerator.csが存在しています。□コンソール.一行表示する(引数2) はRe:Mindの中核コンセプトで、下記のようなRe:Mindのインポート文をトランスコンパイルすることで、.NETやJavaの大量のクラスライブラリを簡単に使用できるようにするためのものです。JSONまでは出力されているようなのですが、C#コードジェネレータがここからConsoleクラスのWiteLineにトランスコンパイルできようにするのが最初のステップ完了のための課題です。
#### 生成レスポンス３

状況は完全に把握しました。
あなたが今やりたい「最初のステップ」は Re:Mind のサンプルソースコード（Program.cs の const string ReMindSourceCode）を AST に変換 → C#, Java, VB.NET のコードを生成 → コンソール出力できるようにすることですね。

そしてその中核課題が：

□コンソール.一行表示する(引数2) を
C# の Console.WriteLine に正しくトランスコンパイルさせること

ここを突破すれば、Re:Mind → AST → C# / Java / VB.NET の基本パイプラインが完成します。

#### レスポンス３の評価
このあたりは理解しているといっているのでそのまま受け止めています。驚いたのは上記では割愛していますが、現状のソースコードの改修案も具体的に提示してきました。とりあえずその妥当性は読んだだけでは判定できないので、次に進みます。次のプロンプトはCopilotが提示した選択肢への応答が起点となっています。

### プロンプト４

mylifewithviolinさんへの質問（次のステップを決めるため）
PlanAgent に作らせたい計画はどちらですか？

A. 「最初のステップ」だけの計画（AliasClasses → Console.WriteLine の変換）
B. AST → 生成パイプライン全体の計画（C#, Java, VB.NET すべて）
C. Re:Mind 言語仕様の完全なコンパイラ計画（Lexer → Parser → AST → IR → CodeGen）
どれを PlanAgent に作らせたいか教えてください。

>Cですかね。

#### 生成レスポンス４
了解しました、mylifewithviolinさん。
C（Re:Mind 言語仕様の完全なコンパイラ計画：Lexer → Parser → AST → IR → CodeGen） を PlanAgent に作らせたい、ということですね。

ここまで来ると、あなたの Re:Mind プロジェクトは「言語仕様 → AST → IR → C#/Java/VB.NET 生成」という 本物の言語処理系の全体像を PlanAgent に構築させる段階に入っています。
これはまさに PlanAgent が最も得意とする領域です。

```
/plan remind_specification.md を参照して、
Re:Mind 言語仕様の完全なコンパイラ計画を作成してください。

計画には以下を含めてください：
- 字句解析（Lexer）
- 構文解析（Parser）
- AST モデルの拡張
- 中間表現（IR）の設計
- C#, Java, VB.NET のコード生成パイプライン
- Imports の AliasClasses を使った名前解決（Symbol Table）
- □コンソール.一行表示する のような中核構文のトランスコンパイル
- Program.cs の const string ReMindSourceCode を入力として扱う流れ
- Ast.cs と各 CodeGenerator の既存コードを前提にした改善計画
- 最終的に Re:Mind → C#/Java/VB.NET のコンソール出力が可能になるまでの全工程

計画は段階的に、依存関係が分かるように構造化してください。
```

#### レスポンス４の評価
なんとなくAGENTS.mdに含めておいてもよさそうな感じでしたので、プロンプトとしても採用してAGENTS.mdも下記のように編集しました。

```md:AGENTS.md
# PlanAgent Instructions

このプロジェクトの仕様は `remind_specification.md` に記載されています。
PlanAgent は計画作成時にこの仕様を必ず参照してください。

## 仕様ファイル
- ./remind_specification.md

## PlanAgent に求めること
- 仕様に基づいた正確な計画の作成
- AST → 中間表現 → C# / Java / VB.NET 生成パイプラインの構造化
- 仕様の曖昧な部分があれば質問を返すこと
- 計画は `plan.md` として出力すること
- 計画には以下を含めてください：
- 字句解析（Lexer）
- 構文解析（Parser）
- AST モデルの拡張
- 中間表現（IR）の設計
- C#, Java, VB.NET のコード生成パイプライン
- Imports の AliasClasses を使った名前解決（Symbol Table）
- □コンソール.一行表示する のような中核構文のトランスコンパイル
- Program.cs の const string ReMindSourceCode を入力として扱う流れ
- Ast.cs と各 CodeGenerator の既存コードを前提にした改善計画
- 最終的に Re:Mind → C#/Java/VB.NET のコンソール出力が可能になるまでの全工程
- 計画は段階的に、依存関係が分かるように構造化してください。

```

## GitHub Copilotの事前準備
### エージェントの設定
１）チャットセクションの下端のエージェントの設定でPlanを選択
２）同じくモデルではAutoを選択
３）VSCodeのソースコードエディタでremind_specification.mdを開くとチャットセクションの上部にファイル名が＋記号付きで表示されるので＋をクリック。×になります。（念のためファイルをコンテキストに追加）

remind_specification.mdの内容はこちらです。記事のmdのソースをそのままremind_specification.mdとしています。

https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b


## GitHub Copilot PlanAgent

### プロンプト
>/plan remind_specification.md を参照して、
Re:Mind 言語仕様の完全なコンパイラ計画を作成してください。
>
>計画には以下を含めてください：
- 字句解析（Lexer）
- 構文解析（Parser）
- AST モデルの拡張
- 中間表現（IR）の設計
- C#, Java, VB.NET のコード生成パイプライン
- Imports の AliasClasses を使った名前解決（Symbol Table）
- □コンソール.一行表示する のような中核構文のトランスコンパイル
- Program.cs の const string ReMindSourceCode を入力として扱う流れ
- Ast.cs と各 CodeGenerator の既存コードを前提にした改善計画
- 最終的に Re:Mind → C#/Java/VB.NET のコンソール出力が可能になるまでの全工程

>計画は段階的に、依存関係が分かるように構造化してください。

#### 生成レスポンス

仕様書と既存実装の構造を確認し、依存関係の見える形で段階的なコンパイラ計画をまとめます。

Read memory

既存の AST と生成器の構造を確認できたので、仕様に沿って実装フェーズを段階化した計画に落とし込みます。

Read memory

計画内容をセッション記録に保存し、要点をそのまま確認できる形でまとめます。

Created memory file 

###### コンパイラ計画を作成しました

Re:Mind 仕様書を踏まえ、現状の簡易実装を「完全なコンパイラ基盤」へ拡張するための段階的計画を整理しました。計画はセッション記録に保存済みです。

###### 目標
Re:Mind から C#/Java/VB.NET へ、基本構文をトランスコンパイルできるようにすることを最終目標とします。特に、以下の中核構文を最優先で扱います。

- □コンソール.一行表示する のようなメンバー呼び出し
- □変数名 = 式
- □(引数)で 関数名
- ◇条件 の場合 / ◇他に / ◇ここまで
- 〇繰り返す / 〇(条件) の間は繰り返す / 〇ここまで

###### 計画の構成

1. まず対象範囲を整理する
   - MVP では変数・定数・配列、関数・クラス、代入・戻り値、条件分岐・繰り返しを対象にします。
   - switch や例外構文は後続フェーズに回します。

2. 字句解析を追加する
   - 予約語、識別子、文字列・数値リテラル、演算子、コメントを整理したトークン体系を定義します。
   - エラー位置を正確に出せるようにします。

3. 構文解析を全面再設計する
   - 現状の Parser.cs の BubbleSort 前提実装を置き換え、宣言・文・式を段階的に解析できるようにします。

4. AST を仕様準拠に拡張する
   - Ast.cs に定数・フィールド・戻り値・制御構文・new 式などのノードを追加します。
   - 日本語名とターゲット言語名を両方保持する構造にします。

5. 名前解決とシンボルテーブルを導入する
   - Imports の AliasClasses を使って、Re:Mind の日本語メンバー呼び出しをターゲット言語名へ解決します。
   - 変数・メソッド・クラス・引数のスコープ解決もここで行います。

6. IR を設ける
   - AST から言語非依存の中間表現へ変換する層を追加し、後続の生成器が共通で扱えるようにします。

7. 各ターゲット言語のコード生成を再構成する
   - CSharpCodeGenerator.cs
   - JavaCodeGenerator.cs
   - VbNetCodeGenerator.cs
   - まず C# を安定化し、その後 Java、VB.NET の順で整えます。

8. 実行フローを統合する
   - Program.cs で、ReMindSourceCode を入力として受け取り、Lexer → Parser → 名前解決 → IR → CodeGenerator の流れに統合します。

9. 検証を行う
   - サンプルコードで生成結果を確認し、未対応構文は明示的に扱えるようにします。

###### 主要対象ファイル
- Ast.cs
- Parser.cs
- Program.cs
- CSharpCodeGenerator.cs
- JavaCodeGenerator.cs
- VbNetCodeGenerator.cs
- IndenetWriter.cs

###### 依存関係
- Lexer 実装 → Parser 変更
- Parser 安定化 → AST 拡張
- AST 安定化 → 名前解決 / IR
- IR 安定化 → 各コード生成器
- AliasClasses の解決 → コンソールやクラスメンバー呼び出しの生成

この計画で実装に着手できます。

#### レスポンスの評価
生成されたplan.mdがユーザーアカウントフォルダのAppData\Roaming\Code\User\workspaceStorage\UUID\GitHub.copilot-chat\memory-tool\memories
の奥深いところでした。もしかしたら設定によってはプロジェクトフォルダに保存できるのかもしれません。生成されたmdの内容はチャットのレスポンスとほぼほぼ同じでした。内容的にはkiro-cliの生成内容をほうふつとさせるもでした。

```md:plan.md
# Plan: Re:Mind コンパイラ全体設計

TL;DR
Re:Mind の現状実装は BubbleSort サンプル向けの簡易パーサーと 1 つの C# 生成器に寄っているため、仕様に沿った完全なパイプラインへ再設計する。最初に字句解析と構文解析を固め、その後 AST を拡張し、意味解析・IR 変換・各ターゲット言語生成へ段階的に進める。最終的に Program.cs の ReMindSourceCode を入力として扱い、Re:Mind から C#/Java/VB.NET へのコンソール出力ができる状態を目指す。

## Phase 0: スコープと前提整理
1. 仕様書の構文を基準に、まず実装対象の最小・中間・拡張セットを分ける。
2. 第 1 期の MVP では、以下を対象にする。
   - 変数・定数・配列
   - 関数宣言・関数呼び出し
   - クラス宣言・メンバーアクセス
   - 代入・戻り値
   - 条件分岐・繰り返し
   - 例外構文・switch は後続フェーズで扱う
3. 既存の Program.cs の const string ReMindSourceCode を「入力サンプル」から「実行入口」に昇格させ、将来的にファイル入力や CLI 引数にも切り替えられる構造にする。

## Phase 1: 字句解析（Lexer）
1. Re:Mind のトークン体系を定義する。
   - 予約語: ・, □, ▽, △, ◇, 〇, ■, ▼, ▲, ここまで, の場合, で分岐する, 既定, 繰り返す, ここから, の間は, 返す, 試す, 捉まえる, 必ず最後に, 脱出する, ループ先頭へ, 反復処理, やめる
   - 識別子・日本語識別子・英字識別子
   - リテラル: 文字列、数値、真偽値
   - 演算子: =, +, -, *, /, %, ==, !=, >, <, >=, <=
   - 区切り: (), [], {}, カンマ, ドット, セミコロン
2. コメント・空白・マルチラインコメントをトークン化対象から除外する。
3. 行番号・列番号を保持し、エラー位置を正確に報告できるようにする。
4. 既存の Parser.cs から文字列ベースの前処理を分離し、Lexer を通した入力へ移行する。

## Phase 2: 構文解析（Parser）
1. 現状の Parser.cs の「BubbleSort 用の前提実装」を全面的に置き換える。
2. 構文を以下の層に分けて実装する。
   - ルート: CompilationUnit
   - 宣言: namespace / import / class / method / variable / constant
   - 文: assignment / expression-statement / if / while / for / return / break / continue
   - 式: identifier / literal / binary / unary / member access / invocation / array literal / new expression
3. 仕様にある中核構文を優先実装する。
   - □コンソール.一行表示する(引数)
   - □年齢 = ...
   - □(名前, 特待区分)で メソッド名
   - ◇条件 の場合 / ◇他に / ◇ここまで
   - 〇繰り返す / 〇(条件) の間は繰り返す / 〇ここまで
4. 構文エラー時には、トークン列と行番号を含むエラー情報を返すようにする。

## Phase 3: AST モデルの拡張
1. 既存の Ast.cs を拡張し、仕様に必要なノードを追加する。
2. 追加する主なノードを整理する。
   - 宣言系: ConstantDeclaration, FieldDeclaration, NamespaceDeclaration, ImportDeclaration, AliasClass, AliasMember
   - 文系: ReturnStatement, BreakStatement, ContinueStatement, TryCatchStatement, SwitchStatement, EmptyStatement
   - 式系: NewExpression, NullLiteralExpression, ConditionalExpression, AssignmentExpression, ArrayCreationExpression
   - メタ情報: JavadocComment, Parameter, TypeReference
3. 既存の NameJa / NameEn の扱いを維持しつつ、ターゲット言語名と元の日本語名を両方保持する。
4. AST には「構文上の形」を残し、意味解析前の情報として保持する。

## Phase 4: 意味解析と名前解決
1. Symbol Table を導入し、以下を解決する。
   - ローカル変数・引数・フィールド・メソッド名
   - クラス名・名前空間名
   - import された AliasClasses とそのメンバー
2. Imports の AliasClasses を活用して、Re:Mind の日本語メンバー呼び出しをターゲット言語側の英字名へ変換する。
3. 例として、以下のような解決を実現する。
   - コンソール.一行表示する → Console.WriteLine
   - メンバー取り扱い方法.年齢 → object.age
   - 変数・メソッドの型とスコープを解決する
4. 変数宣言前の使用や未定義名の検出を行う。
5. これは後続の IR 変換とコード生成の正確性を保証する基盤になる。

## Phase 5: 中間表現（IR）の設計
1. AST から後続ターゲットへ落とし込むための IR を追加する。
2. IR の設計例は以下の通り。
   - ProgramIR: namespace/import/class/method の集合
   - ClassIR: field と method の集合
   - MethodIR: parameter / local variable / body block
   - BlockIR: 文の列
   - StatementIR: assignment / call / if / while / for / return / break / continue
   - ExpressionIR: identifier / literal / binary / call / member access / array access / new
3. AST → IR の変換は「構文情報を保持したまま、バックエンド非依存の形に近づける」設計にする。
4. 生成器は IR を受け取って言語別に出力する構造に切り替える。

## Phase 6: コード生成パイプラインの再設計
1. 既存の CSharpCodeGenerator.cs / JavaCodeGenerator.cs / VbNetCodeGenerator.cs を、AST 直生成から IR ベース生成へ切り替える。
2. 各バックエンドで共通に使える出力ユーティリティを整える。
3. 実装対象は以下の順で進める。
   - まず C# を安定化する
   - 次に Java を追加する
   - 最後に VB.NET を追加する
4. 各生成器で実装する主な変換規則を整理する。
   - 変数宣言: 型と初期化式の変換
   - 配列: C# int[] / Java int[] / VB.NET Integer()
   - 代入・演算: 中置演算子の変換
   - 条件・ループ: if / while / for の変換
   - 呼び出し: メソッド呼び出し・メンバー呼び出し・AliasClass の解決
   - 例外・switch: 後続フェーズで追加

## Phase 7: コア構文のトランスコンパイル実装
1. まずは以下の「中核構文」を確実に生成できるようにする。
   - □コンソール.一行表示する(引数)
   - □変数名 = 式
   - □(引数)で 関数名
   - ◇条件 の場合 / ◇他に / ◇ここまで
   - 〇繰り返す / 〇(条件) の間は繰り返す / 〇ここまで
2. 生成対象言語ごとに、対応する構文へマッピングする。
3. 仕様上の「日本語の記法」と「ターゲット言語の構文」を両立させるため、変換ルール表を明示的に持つ。

## Phase 8: Program.cs からの実行フロー統合
1. Program.cs をオーケストレータとして再構成する。
2. 実行フローは次の順にする。
   - ReMindSourceCode を読み込む
   - Lexer でトークン化する
   - Parser で AST を生成する
   - SemanticResolver で名前解決・型解決を行う
   - IR へ変換する
   - 指定ターゲット言語の CodeGenerator でコードを生成する
   - 生成コードを標準出力またはファイルに書き出す
3. 既存の JSON 直列化・デシリアライズはデバッグ用途として残しつつ、本番フローでは不要なら段階的に外す。

## Phase 9: 検証と品質改善
1. 既存のビルド・実行を継続的に確認する。
2. 各フェーズごとにサンプル入力を用意し、期待コードが出力されることを確認する。
3. 追加する検証サンプルを用意する。
   - 変数宣言 + 代入 + console 出力
   - if / while / for のハンドリング
   - import / alias class の解決
   - class / method / member access
4. 未対応構文は明示的にエラーまたはプレースホルダーとして出力する。

## 依存関係
1. Lexer 実装 → Parser 変更
2. Parser が安定 → AST 拡張
3. AST が安定 → SemanticResolver / IR 変換
4. IR が安定 → 各 CodeGenerator の実装
5. Imports / AliasClasses の解決 → Console などのメンバー呼び出し生成
6. 上記が揃って初めて Program.cs のエンドツーエンド実行が成立する

## 主要対象ファイル
- Ast.cs
- Parser.cs
- Program.cs
- CSharpCodeGenerator.cs
- JavaCodeGenerator.cs
- VbNetCodeGenerator.cs
- IndenetWriter.cs

## 完了条件
1. Re:Mind の代表的なサンプルコードが Lexer と Parser を通過する
2. AST に必要な構文ノードが保持される
3. Imports の AliasClasses を利用した名前解決ができる
4. C#/Java/VB.NET のそれぞれに対して、コア構文の生成ができる
5. Program.cs から const string ReMindSourceCode を入力として受け取り、標準出力に生成コードを出せる

```

## 第１ステップの評価
Copilotが生成したソースコードのローカルプロジェクトと仕様情報のmdを同時に読み込ませての診断のため、期待値は高いです。

Copilotの場合はネットから仕様情報を読み込ませれたのはよかったのですが、ローカルのプロジェクトへの反映は手動で、入力文字数に制限がありましたのでCopilotが生成したソースを再認識させるのがたいへんでした。

Github Copilotのようにローカルの情報をすべて必要な範囲で読み込ませれるのは助かりました。あとは生成される実装がどのようなものになるかですが、kiro-cliの実力に近いものを感じます。（あくまで筆者の感想です。）

ただし、今回のGithub Copilot planAgentへのインプットは事前にCopilotが認識している知見（Github Copilot一般の他、Re:Mindのローカル事案も含めて）を使ったことによる結果で、その点は大きかったです。

# おわりに
第１ステップは以上です。次回の方向性は上記のplan.mdの実行からとなります。

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
