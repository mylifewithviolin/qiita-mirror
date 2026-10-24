# はじめに
日本語プログラミング言語Mind８中間コードの走行系CディスパッチャをC#と同じようにJavaに書き換えたい願望があります。Mind開発者の@killyさんはこれに近いことを既にやっていて、Cランタイムもそのまま使ってしまうという凄ワザでご対応されていらっしゃいますが、わたしはC#と同じく中間コードディスパッチャをCからJavaに書き換えたいなと。

と思っていたのですがC#の書き換え自体がスタートアップに処理される中間コードの数の多さにとん挫してしまっていたのですが（ちょうど２年前）

https://qiita.com/mylifewithviolin/items/151517f7a57b5b8b97f5

しかし、昨今GitHub Copilot Pro+の余裕のある推論量に触れて、もしかしてもしかして、こういう機械的なことって得意なのという気がして、やらせてみる（やっていただく）ことにしましたところ、あっさりできてしまったので、Javaについてもやらせてみる（やっていただく）ことにしました。


本記事はその結果報告です。実装・検証自体はとっくの昔には完了していたのですが、人間系の記事化に時間がかかっていたという経過でございます。

# お題のJavaソースコードのクラス構成
お手数ですが[こちらの記事](https://qiita.com/mylifewithviolin/items/70c386cb0aee7b3c016c)をご参照ください。こちらはC#のモので人間系発案ですが、こちらの構造を継承するとしています。

## クラスの説明と対応ソースファイル構成
お手数ですがこちらも[こちらの記事](https://qiita.com/mylifewithviolin/items/70c386cb0aee7b3c016c)をご参照ください。

## お題のMind8の中間コードファイル
```mind:hello.src
メインとは
　　　　「Hello by mind8」を　表示すること。
```

# 使用AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。
## GitHub Copilot
GitHub CopilotのPro+版。あおい実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用していまた。ただし、Pro+版移行でこの点はあまり気にしなくなっています。

# AI仕様駆動開発の実際
## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでその点でのMicrosoft Copilotとのやりとりはなかったです。
## GitHub Copilot
### プロンプト１
>カレントフォルダに
C:\developments\vscode\mind8dispachjava
JavaのコンソールアプリケーションをビルドするVSCode関連フォルダを作成してください。
アプリケーション名は
mind8dispacher
としてください。
>
>このアプリケーションは
C:\developments\vscode\mind8dispatch\docs\Mind8ディスパッチャC実装概要.md
に記載のC言語実装のMindディスパッチャを
C:\developments\vscode\mind8dispatch\docs\Mind8ディスパッチャC＃互換実装の実装状況.md
に記載の
Mind8ディスパッチャC＃実装
と同様にJavaで実装しようとするものです。
C:\developments\vscode\mind8dispatch\docs\Mind8ディスパッチャC＃互換実装の実装状況.md
に記載の
Mind8ディスパッチャC＃実装と同様のクラス構成でJavaクラスファイルのソースコードの枠を実装する
docs\Mind8ディスパッチャJava実装クラス構成.md
を出力してください。

#### 生成レスポンス１
とりあえずクラスの枠をつくってもらいました。
```md
# Mind8ディスパッチャ Java実装クラス枠作成完了レポート
## 作成成果物
```
表はQiitaでレンダリングします。
| 成果物 | 内容 |
| --- | --- |
| `src/mind8dispacher/Main.java` | アプリケーションのエントリーポイント。`Dispatcher` に処理を委譲 |
| `src/mind8dispacher/Dispatcher.java` | MCO準備、関数テーブル初期化、ディスパッチ処理の枠 |
| `src/mind8dispacher/MCodePointer.java` | Mコード領域と位置を保持するポインタークラス |
| `src/mind8dispacher/LocTablePointer.java` | LOCテーブルと位置を保持するポインタークラス |
| `src/mind8dispacher/AccessPointer.java` | データ領域と位置を保持するポインタークラス |
| `src/mind8dispacher/StackPointer.java` | スタック領域と位置を保持するポインタークラス |

### プロンプト２
>このタスクでは推論量をなるべく最大化してください。
ただし中間の推論状況は報告します。
docs\Mind8ディスパッチャJava実装クラス枠作成完了レポート.md
を参照し
C:\developments\vscode\mind8dispatch\
の下の
docs\Mind8ディスパッチャC＃互換実装次の優先項目1の実行プラン.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目2の実行プラン.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目3の実行プラン.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目4の実行プラン.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目1の実行プラン完了レポート.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目2の実行プラン完了レポート.md
docs\Mind8ディスパッチャC＃互換実装次の優先項目3の実行プラン完了レポート.md
を参照して
docs\Mind8ディスパッチャJava互換実装次の優先項目1の実行プラン.md
docs\Mind8ディスパッチャJava互換実装次の優先項目2の実行プラン.md
docs\Mind8ディスパッチャJava互換実装次の優先項目3の実行プラン.md
docs\Mind8ディスパッチャJava互換実装次の優先項目4の実行プラン.md
を作成しこれが最終成果物です。これらを一括出力し
この資料の作成段階ではJavaコンパイラの検証は不要です。
このタスクではJava20の構文を逸脱しない範囲で推論によるソースコード案作成で可です。
最後のプラン4の中にはJavaコンパイラの検証は必要です。
できた順に出力してください。

Javaでの実装はC#実装のリソースを最大限流用するという感じで進めました。

#### 生成レスポンス２
>実装状況完了レポートを作成しました。
C関数テーブル743件を照合し、Java登録85件の名前不一致を解消しました。658件は未実装として明記しています。
両エンディアンのMCOロード、メタデータ異常系、分岐・再開・終了経路の回帰テストを追加し、Java 20で14/14件成功しました。
hello MCOと分岐を含む合成MCOを既存CバイナリとJavaで比較し、標準出力・終了コードが一致することを確認しました。
Java回帰テスト用のGitHub Actions workflowを追加しました。
全体のC互換は未完了です。未実装関数、別名、シグナル処理などの残件と、Cバイナリが既存ビルドである制約は報告書に記載しています。

### docs\Mind8ディスパッチャJava互換実装の実装状況完了レポート.md の一部抜粋

```md
# Mind8ディスパッチャ Java互換実装の実装状況完了レポート

## 結果
**状態: 基本実行経路と優先項目4の検証環境を整備し、Java回帰テスト14件が成功し
ました。通常ユーザーカーネルのhello MCOについて、既存C実行ファイルとJavaの
標準出力・終了コードが一致しました。ディスパッチャ全体のC互換は未完了です。**

次の優先項目4 v2に記載された残課題のうち、C関数テーブルの機械照合、
両エンディアンのMCOロード、メタデータ異常系、主要なディスパッチ制御経路、Windows標準入出力の基本モード処理、継続的なJava回帰テストを実装・検証
しました。未実装C関数の意味的互換性や、hello以外のC/Java実行比較は未完了
であり、全体完了とは扱いません。
```

# 実行結果 
```ps:
PS C:\developments\vscode\mind8dispachjava>  & '.vscode\extensions\redhat.java-1.58.0-win32-x64\jre\25.0.4.1-win32-x86_64\bin\java.exe' '-agentlib:jdwp=transport=dt_socket,server=n,suspend=y,address=localhost:57375' '-XX:+ShowCodeDetailsInExceptionMessages' '-cp' 'redhat.java\jdt_ws\mind8dispachjava_2d291766\bin' 'mind8dispacher.Main' 'tests/fixtures/hello.mco' 
Hello by mind8
PS C:\developments\vscode\mind8dispachjava> 
```
Java版の場合はC#版のようなCディスパッチャに仕込んだ中間コード実行ステップリストの出力はありません。

# おわりに
以上です。いかがでしたでしょうか？本件しばらくつづきがあるかもしれません。やるとしたら次回は検証用Mindのソースコードを増やしたmcoを実行してみます。

Javaの膨大なライブラリをMindで使えるようになるということに意義を見出していました。（実際には走行系の他にコンパイラ系の対応も必要ですが、そのあたりは開発者様のご意向次第という感じ？これはあくまで部外者による前提条件の概念実証という形となります。）

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
