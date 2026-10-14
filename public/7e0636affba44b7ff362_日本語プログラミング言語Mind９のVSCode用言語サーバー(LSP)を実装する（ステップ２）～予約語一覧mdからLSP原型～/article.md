# はじめに
日本語プログラミング言語Mindのバージョン９のVSCode用言語サーバー(LSP)を実装してみます。本記事は第２ステップで、LSPの原型を実装します。

## 採用工法
工法は日本語プログラミング言語あおいコンパイラの開発と同様AIドリブンな感じでいきます。自力では量的に手動実装できないのでAIだのみではありますが、大枠の適切な進め方は理解しているという前提です。(VSCode拡張でシンタックスハイライトやスニペットは自力で実装可能でその自スキルを背景にAIで拡張していきます。）

https://qiita.com/mylifewithviolin/items/66632e23fa7394e669bc

# ステップ２　予約語・変数構造体定義・処理単語の一覧.mdからLSP原型実装
[前回のステップ](https://qiita.com/mylifewithviolin/items/d42b1c9a6e397babc482)でMind９の言語ヘルプHTMLのmarkdown変換が完了しましたので、本ステップではそのmdから予約語・変数構造体定義・処理単語の一覧.mdを抽出し、LSPがカバーする範囲をいったん確認し、その後LSP原型の実装へ進行します。

具体的には下図のようなvscode-extention開発プロジェクトフォルダにMind９の言語ヘルプmdが格納されたmanual-mdフォルダを配置します。

```cmd
C:\developments\vscode-extention\mind-extension>dir
2026/09/20  23:01    <DIR>          .
2025/07/21  20:52    <DIR>          ..
2025/01/13  13:30                20 .gitignore
2025/01/13  13:30    <DIR>          .vscode
2025/07/21  13:54             1,745 language-configuration.json
2025/01/13  14:06             1,094 LICENSE
2026/09/20  23:09    <DIR>          manual-md
2026/09/21  00:14    <DIR>          node_modules
2026/09/20  22:55    <DIR>          out
2026/09/21  00:14           153,395 package-lock.json
2026/09/21  00:14             2,237 package.json
2025/07/21  15:07             1,361 README.md
2025/01/13  13:30    <DIR>          snippets
2026/09/20  22:52    <DIR>          src
2025/01/13  13:30    <DIR>          syntaxes
2026/09/21  00:20               605 tsconfig.json
2024/11/17  14:08             3,098 vsc-extension-quickstart.md
               8 個のファイル             163,555 バイト
```

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい（Re:Mind）の原型を作成してもらった生成AI[^1][^2][^3]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro版を導入。[あおいの検証](https://qiita.com/mylifewithviolin/items/91857ad240e382a9ed54)で検証改修再検証フローを数回廻したところフリー版のクレジット足らなくなったのでPro版へアップグレード。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

## Microsoft Copilotとの事前準備
### プロンプト
>GitHub CopilotのCodeAgentに既存のVSCode拡張に、日本語プログラミング言語Mind用の LanguageServerの追加を指示するプロンプトを作成してください。クレジット消費を最小化するようにしてください。

#### 生成レスポンス
以下のGitHub Copilotに指示しているプロンプトと概ね同じ内容が生成されました。プロンプト１～４を分割して生成。プロンプト３の「manual-md\予約語・変数構造体定義・処理単語の一覧.mdに出力してください。」は確認用にわたしがアレンジしました。

## GitHub Copilot
### プロンプト１
>既存の VSCode 拡張に、日本語プログラミング言語 Mind 用の Language Server クライアントを追加したいです。
>
>vscode-languageclient を使って、拡張子 .src のファイルに対して
LSP サーバを起動し、診断と補完を提供するクライアントコードを
extension.ts に追加してください。
>
>最小構成でよいので、initialize と basic capabilities（textDocumentSync, completion）を設定してください。
既存のシンタックスハイライト、スニペットのコードは維持するようにしてください。

最後の一文はわたしが追加しました。

#### 生成レスポンス１
Microsoft Copilot的にはこのプロンプトでLSPクライアントの枠まで生成というイメージでしたがGitHub Copilot的にはserver.tsの枠まで生成していました。
最終生成物はかなり長くなるので、いったんこの時点の状態を記録しておきます。
const KEYWORDSの内容はどこからひっぱってきかた不明ですが、わたし的にはAIの健気さを感じます。（ハルシネーションっぽいともいう）

```typescript
import {
    createConnection,
    TextDocuments,
    ProposedFeatures,
    InitializeParams,
    InitializeResult,
    TextDocumentSyncKind,
    CompletionItem,
    CompletionItemKind,
    TextDocumentPositionParams
} from 'vscode-languageserver/node';
import { TextDocument } from 'vscode-languageserver-textdocument';

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments(TextDocument);

// Mind 言語の基本キーワード（最小構成の補完候補）
const KEYWORDS = [
    'もし', 'ならば', 'でなければ', 'くりかえし', 'あいだ', 'まで',
    '手続き', '関数', '大域', '局所', '定数'
];

// initialize
connection.onInitialize((_params: InitializeParams): InitializeResult => {
    return {
        capabilities: {
            textDocumentSync: TextDocumentSyncKind.Incremental,
            completionProvider: {
                resolveProvider: false
            }
        }
    };
});

// textDocument/didOpen
documents.onDidOpen((event) => {
    validateTextDocument(event.document);
});

// textDocument/didChange
documents.onDidChangeContent((change) => {
    validateTextDocument(change.document);
});

// textDocument/publishDiagnostics
function validateTextDocument(_document: TextDocument): void {
    // 最小構成のため診断ロジックは未実装（常に空の診断結果を送る）
    connection.sendDiagnostics({ uri: _document.uri, diagnostics: [] });
}

// textDocument/completion
connection.onCompletion((_params: TextDocumentPositionParams): CompletionItem[] => {
    return KEYWORDS.map((keyword) => ({
        label: keyword,
        kind: CompletionItemKind.Keyword
    }));
});

documents.listen(connection);
connection.listen();
```
### プロンプト２
>日本語プログラミング言語 Mind 用の Language Server を TypeScript で実装したいです。
>vscode-languageserver を使って、
>
>initialize
textDocument/didOpen
textDocument/didChange
textDocument/completion
textDocument/publishDiagnostics
を持つ最小限の LSP サーバの骨格を server.ts として生成してください。
>
>診断と補完の中身は仮実装で構いません。
>
>既存コードは保持し、最小構造だけ生成してください。

#### 生成レスポンス２
>既存の initialize・補完実装・依存関係はそのまま維持し、textDocument/didOpen を明示的なハンドラとして追加、各 LSP メソッドに対応するコメントラベルを付けました。ビルド確認済み（エラーなし）。

### プロンプト３
>フォルダ
manual-md
以下の Markdown マニュアルを参照し、
Mind 言語の構造体定義、処理単語、予約語の一覧を抽出して
manual-md\予約語・変数構造体定義・処理単語の一覧.md
に出力してください。
>
>それを元に、LSP サーバの server.ts に以下の機能を追加してください。
>
>テキストドキュメントを行単位で解析し、
>
>未定義の処理単語呼び出し
未定義の構造体参照
を診断として textDocument/publishDiagnostics で返す。
補完要求（textDocument/completion）に対して、
>
>処理単語名
構造体名
予約語
を候補として返す。

#### 生成レスポンス３
>完了内容
>1. マニュアル抽出: 予約語・変数構造体定義・処理単語の一覧.md を新規作成。制御構文/宣言キーワード（予約語）、構造体・変数定義キーワード、算術・文字列・入出力・ファイル・スタック操作の処理単語をカテゴリ別に整理。
>
>2. server.ts の拡張:

ここで予約語・変数構造体定義・処理単語の一覧.mdが生成されました。Mind９のGUIライブラリととりあえず今回は除外とmd内に記録されていました。
```text
本一覧は LSP サーバ（`src/server.ts`）の診断・補完機能が参照する基礎データとしても使用する。
すべてを網羅したものではなく、マニュアル中で明示的に単語として説明されている代表的なものを収録した最小構成である。
```

### プロンプト４
>manual-md\予約語・変数構造体定義・処理単語の一覧.md
と
manual-md 以下のマニュアルから、
処理単語の引数仕様と説明文を抽出し、
LSP サーバの server.ts に以下の機能を追加してください。
>
>textDocument/hover:
>
>処理単語の上にカーソルがある場合、
マニュアルから抜粋した仕様（引数一覧・説明）を表示する。
textDocument/signatureHelp:
>
>処理単語呼び出しの括弧内で補完要求が来た場合、
引数の名前・型・説明を返す。

#### 生成レスポンス４
>実装内容
>server.ts に追加した機能:
>
>WORD_SPECS — 予約語・変数構造体定義・処理単語の一覧.md およびマニュアル本文（構文＝ 欄）から抽出した処理単語の仕様データ。各単語ごとに syntax（引数一覧を含む構文）、description（説明文、出典ファイルへのリンク付き）、params（引数名・型・説明）を保持。算術演算・文字列操作・入出力・ファイル操作・スタック操作の代表的な処理単語を収録（仮実装のため網羅ではなく代表例）。
>
>textDocument/hover — カーソル位置の単語を行内トークンから特定し、送り仮名（する/し/すること等）を除去して WORD_SPECS を照合、構文・引数・説明を Markdown で表示。
>
>textDocument/signatureHelp — カーソル直前の「（」を検出し、その直前の単語（呼び出し対象）を特定して WORD_SPECS から SignatureInformation（引数名・型・説明を含む）を返却。hoverProvider: true と signatureHelpProvider（トリガー文字 （/(）を initialize の capabilities に追加。
>
>ビルド確認済み（エラーなし）。既存の診断・補完ロジックはそのまま維持しています。

## 本ステップの評価
生成レスポンス４の状態ではまだ動作せず、GitHub Copilotでもよかったのですが、ここはMicrosoft Copilotに状況を報告し、いろいろ動かない原因の仮説と状態情報の追加のやりとりをした結果、とりあえず予約語にフォーカスを移すと構文・引数・説明が表示されるところを確認しました。

![vscodeextentionmind2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/e7ce51d2-87e1-4db9-8bee-989eec2de2a7.jpeg)

![vscodeextentionmind2-2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/443efdf6-9862-4238-987a-e05d9b108cb0.jpeg)

生成レスポンス４の完了出力では「送り仮名（する/し/すること等）を除去して」のような気の利いたことが書かれていましたが、このあたりを含めて動作検証をどのように進めるか検討してみます。「加える」は「える」がついて要るっぽいので、この辺りの改修と再検証フローがまわせれるようになるとよさそうです。

# おわりに
コード生成のハルシネーションをおさえるためMindの言語仕様をmarkdown化してAIに学習させてみようと思っていたのですが、markdown化の過程でLSPもできますよとMicrosoft Copilotが提案してきたので、それにのっかってみることにしました。意外といけそうです。次回ステップは未定です。

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[^3]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
