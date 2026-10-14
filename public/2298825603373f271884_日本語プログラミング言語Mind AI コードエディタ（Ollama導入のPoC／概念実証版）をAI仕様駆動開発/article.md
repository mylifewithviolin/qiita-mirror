# はじめに
日本語プログラミング言語Mindのバージョン９でAI仕様駆動開発を行っています。本記事はMind AI コードエディタ（Ollama導入のProof of Concept／概念実証版)の開発という内容です。


# 使用AI
## GitHub Copilot
GitHub CopilotのPro+版。本件実装と検証の主担当。一発でMind言語のAI仕様駆動開発ができたわけではなく、いくつかの場数を踏ませた状態の開発ワークフローとなります。
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。GitHub Copilotの使い方スーパバイザとして利用しています。モードは「無料プラン」のsmart。
## Ollama
日本語プログラミング言語Mind AI コードエディタPoC版に導入するオフラインAI

## 本記事の課題
Phase 1:PoC実装基盤のテキストコードエディタの実装
Phase 2:Ollamaとの実接続を除く
Phase 3:Ollamaとの実接続を含むテキストコードエディタPoCの実装完了　本記事のゴール　モデルトークン数はPoCのため大幅縮小

## Microsoft Copilot
本記事では独自のデスクトップアプリWindows版に導入容易なカスタムモデル対応のAIの基礎情報の取得に利用しました。
## GitHub Copilot
Phase 1:実装プランの作成と実行
Phase 2:実装プランの作成と実行
Phase 3:Ollamaのインストール　Phase 2実装プランをOllama使用を前提して修正、実行。参照情報の範囲をモデルトークン数上限に収まるよう縮小。縮小モデルで完成

# Mind AI コードエディタに組み込むAIサービス比較検討結果
下表はMicrosoft Copilotが出力した比較表を要約したものです。
|番号|比較項目|Ollama|Foundry Local|
|---|---|---|---|
|1|API と SDK|OpenAI互換RESTのみ（SDKなし）|OpenAI互換REST + C# / Python / JS / Rust SDK|
|2|モデル管理|OSSモデルが豊富・`ollama pull`で簡単・Modelfileで軽量カスタム|公式モデル中心・ONNXベースで本格的なカスタム可能・アプリ同梱可能|
|3|性能（GPU/NPU/CPU）|GPU自動利用・NPU非対応・CPU最適化は標準的|GPU/NPU/CPU最適化（ONNX Runtime）・Copilot+ PCで高速|

２のOSSモデルが豊富という点でOllamaを使ってみることにしました。またI/FがOpenAI互換RESTのみもMind言語と相性がよいかもと仮定。

わたしが選定の際に参考にした現状有姿情報の再掲で、この表の事実性を保証するものではありません。

# Mind AI コードエディタ（Ollama導入のPoC／概念実証版）の実装構成
## docs\MindAIテキストエディタ実装案Ollama.md
### 配置
```text
mindaieditor\
  mindaieditor.src           CP932のMind起動口
  mindaieditor_ui.tcl        UTF-8の編集UI・保存・終了処理
  mindaieditor_chat.tcl      UTF-8のチャットUI・資料照合・Host連携・検証・追記
  mindaieditor.exe
  mindaieditor.mco
  native\
    MindAIHost.js            Node.jsのPoC資料検証・非同期Ollama通信
  resources\
    manifest.tsv            模擬モードの既存資料ハッシュ一覧
    generation-rules.md
    manual-md\              全49文書
  resources-poc\
    Mind言語のコード生成ルール（モデル参照用PoC制限版）.md
    02-Program-Hyoki.md      固定根拠範囲の抽出元
    08-Input-and-output.md   固定根拠範囲の抽出元
    approval.json           内容ハッシュ・範囲・通信方式・人の承認記録
  scripts\
    build-mindaieditor.ps1
    run-mindaieditor.ps1
    test-mindaieditor.ps1
    compile-proposal-test.ps1
    diagnose-ollama.ps1
    check-ollama-context.js
    evaluate-ollama-poc.js
  tests\
    ollama-host.test.js
    results\
  build\
```
### Mind言語ソースからOllamaローカルのAPIコールの流れ
現状は下記のようにTclからNode.jsを呼んでそこからAPIを呼ぶ流れです。

```text
Mind（アプリ起動）
  → Tcl/Tk（画面・チャット操作）
    → Node.js（資料検証・リクエスト処理）
      → Ollama（ローカルHTTP API・モデル推論）
```

## 画面と操作
```text
┌────────────────────────────────────────────────────────┐
│ ファイル / 編集 / AI / 資料設定 / 状態                  │
├──────────────┬─────────────────────────────────────────┤
│ フォルダ     │ テキストエディタ                        │
│ ツリー       │ ソースコード本文                         │
│              ├─────────────────────────────────────────┤
│              │ チャット履歴・根拠・不足情報             │
│              │ 候補コードのプレビュー・検証状態         │
│              │ 入力欄 [送信] [取消] [検証] [末尾へ追記] │
└──────────────┴─────────────────────────────────────────┘
```

>チャットは右側下段の分割ペインとし、編集エリアの高さを利用者が調整できる。会話履歴は本文と別の読取専用Textに表示する。

この構成の由来は下記のわたしのプロンプト（Phase 1　一部）です。
>左側にフォルダエクスプローラのようなノードUIを持つウィンドウと
右側にテキストエディタウィンドウを持つ
テキストエディタアプリケーションを実装する
docs\テキストエディタアプリケーション実装プラン.md
を作成してください。

チャットゾーンをどこに設けるかはPhase 2プロンプトで特に指定はしませんでした。実装案からPoCとしては妥当と判定して実行承認しています。

# MindAIテキストエディタ実装Ollama（モデル参照用PoC制限版）完了レポート
```md
# MindAIテキストエディタ実装Ollama（モデル参照用PoC制限版）完了レポート
## O6: PoC引渡し（完了）
結論: 承認されたPoC制限版を使う実Ollamaの限定動作は、実正例取得から明示追記・
保存まで検証できた。汎用AIエディタの完成や網羅評価ではなく、限定テンプレートを
安全に受け入れるPoCの成果として引き渡す。

注意：今回の実機では応答に約15分42秒かかりました。 日本語の実モデル品質や任意
Mindコード生成は未検証・対象外です。
```

## 実行のご様子

粗削りながらAIが自動生成したソースによる実行状態です。

![mindaicode1.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6bf170a6-0b08-4c43-a33e-7b46455aa6c0.jpeg)

まだチャットに日本語を入力すると無効エラーになってますとか、モデルの送受信のつくりのまずさで応答が遅いとかはあるのですが:joy:、人類史上初めて？OllamaでMindのソースコードが自動生成されました。:tada:


# おわりに
いかがでしたでしょうか？同じことをしようとしている方々の参考になれば幸いです。


興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/download/download.html#download-base)にアクセスすると、Mindコンパイラをダウンロードできますよ。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:

https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
