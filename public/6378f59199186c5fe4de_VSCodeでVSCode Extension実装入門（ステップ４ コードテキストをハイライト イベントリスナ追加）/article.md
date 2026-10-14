# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ４です。ステップ３ではVSCodeエディタが読み込んでいるテキストをコマンドで処理しました。ステップ４ではこの処理を呼び出すイベントリスナを追加して、テキストエディタが開いたときと、入力の都度処理するようにしてみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 20.10.0
npm 10.9.0

# プロジェクトのフォルダ構成
お手数ですが[ステップ１](https://qiita.com/mylifewithviolin/items/36a39d760e06983a694c)をご参照ください。

# extension.ts（ステップ３）
[ステップ３](https://qiita.com/mylifewithviolin/items/54ac112c951a438f038e)では下記の状態のコードで無事にコマンドパレットでコードテキストをハイライトしました。

```ts:extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	console.log('エクステンション"evaextension"は現在アクティブです！');
	const disposable1 = vscode.commands.registerCommand('evaextension.helloWorld', () => {
        //～略～
	});

    const disposable2 = vscode.commands.registerCommand('extension.showEditorContent', () => {
        //～略～
    });

	const disposable3 = vscode.commands.registerCommand('extension.highlightEditorContent', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('アクティブなエディタがありません!');
        } else {
            const document = editor.document;
            const text = document.getText();
            // 正規表現パターン（例：'日本語' という単語を検索）
            const regex = new RegExp('日本語', 'g');
            let match;
            const decorations: vscode.DecorationOptions[] = [];           
            // 一致する文字列を検索
            while (match = regex.exec(text)) {
                const startPos = document.positionAt(match.index);
                const endPos = document.positionAt(match.index + match[0].length);
                const range = new vscode.Range(startPos, endPos);
                // ハイライトのための装飾オプション
                const decoration = { range };
                decorations.push(decoration);
            }
            // ハイライトスタイルの定義
            const highlightDecorationType = vscode.window.createTextEditorDecorationType({
                backgroundColor: 'yellow'
            });
            // エディタにハイライトを適用
            editor.setDecorations(highlightDecorationType, decorations);
        }
    });

	context.subscriptions.push(disposable1);
    context.subscriptions.push(disposable2);
	context.subscriptions.push(disposable3);
}

export function deactivate() {}

```

# package.json
package.jsonにもextension.showDocumentContent、extension.highlightEditorContentを追加してます。これを忘れるとコマンドパレットに出現しません。

```json:package.json
{
  "name": "evaextension",
  "displayName": "evaExtension",
  "description": "assessment-VsCodeExtension",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.95.0"
  },
  "categories": [
    "Other"
  ],
  "activationEvents": [],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "evaextension.helloWorld",
        "title": "Hello World"
      },
      {
          "command": "extension.showEditorContent",
          "title": "Show Editor Content"
      },
      {
          "command": "extension.highlightEditorContent",
          "title": "highlight Editor Content"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "pretest": "npm run compile && npm run lint",
    "lint": "eslint src",
    "test": "vscode-test"
  },
  "devDependencies": {
    "@types/vscode": "^1.95.0",
    "@types/mocha": "^10.0.9",
    "@types/node": "20.x",
    "@typescript-eslint/eslint-plugin": "^8.10.0",
    "@typescript-eslint/parser": "^8.7.0",
    "eslint": "^9.13.0",
    "typescript": "^5.6.3",
    "@vscode/test-cli": "^0.0.10",
    "@vscode/test-electron": "^2.4.1"
  }
}
```

# extension.ts（ステップ４）
つづいて今度はコードエディタの中のテキストに対するハイライト強調処理を関数化しておき、それを各イベントリスナーから呼び出すようにしてみたいと思います。

```ts:extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	console.log('エクステンション"evaextension"は現在アクティブです！');
    //～略～
    
    const disposable3 = vscode.commands.registerCommand('extension.highlightEditorContent', highlightEditorContent);
	context.subscriptions.push(disposable3);

    // エディタがアクティブになったときのイベントリスナー
    vscode.window.onDidChangeActiveTextEditor(highlightEditorContent);

    // ドキュメントが変更されたときのイベントリスナー
    vscode.workspace.onDidChangeTextDocument(event => {
        if (vscode.window.activeTextEditor && event.document === vscode.window.activeTextEditor.document) {
            highlightEditorContent();
        }
    });
}

export function deactivate() {}

//コードテキストをハイライト
function highlightEditorContent() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showInformationMessage('アクティブなエディタがありません!');
        return;
    }
    // ハイライトスタイルの定義
    const highlightDecorationType = vscode.window.createTextEditorDecorationType({
        backgroundColor: 'yellow'
    });
    
    const document = editor.document;
    const text = document.getText();
    const regex = new RegExp('日本語', 'g');
    let match;
    const decorations = [];

    while (match = regex.exec(text)) {
        const startPos = document.positionAt(match.index);
        const endPos = document.positionAt(match.index + match[0].length);
        const range = new vscode.Range(startPos, endPos);
        console.log(`range: start line ${range.start.line}, end line ${range.end.line}, start character ${range.start.character}, end character ${range.end.character}`); 
        decorations.push(range);
    }
    console.log(decorations);
    // エディタにハイライトを適用
    editor.setDecorations(highlightDecorationType, decorations);
}

```
# package.json
```json:package.json

  "activationEvents": [
    "onLanguage:plaintext"
  ],

```

## VSCodeでデバッグ実行開始
VSCodeでデバッグ実行開始開発ホストが開いたらエディタになにか適当な文字をタイプして、キーワードの「日本語」もタイプします。
キーワードの「日本語」が１つだけの場合は問題が起きにくいのですが、２つ目が出現（タイプ）すると問題の起きる場合があります。下図は３つ目で問題が起きておりまして、キーワードの「日本語」の後の文字もハイライトされてしまっています。

![vscodeextension11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/efaf325b-6c62-195a-e9b1-5bf84ad13bfc.png)

このときのコンソールログの出力は下図の状態で、ハイライトする範囲の配列は正しくeditor.setDecorationsにわたっているようなのですが、ハイライト範囲が誤動作する原因はこの記事投稿時点でまだわかっておりません。

function highlightEditorContent()の内容はステップ３の状態から若干調整しており、その状態でも実行しており最終状態との実行結果の変化はありませんでした。


```
range: start line 0, end line 0, start character 5, end character 8
range: start line 0, end line 0, start character 18, end character 21
range: start line 0, end line 0, start character 23, end character 26
(3) [ys, ys, ys]
0 =[0:5 -> 0:8)
1 =[0:18 -> 0:21)
2 =[0:23 -> 0:26)
length =3
[[Prototype]] =Array(0)
[[Prototype]] =Object
```

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。今回はちょっと中途半端な状態（問題を残した状態）となってしまっております。次回までに解決を試みたいと考えております。

# 追記
この不可解な挙動はDecorationTypeにrangeBehavior: ClosedClosedオプションを追記することで解消されました。

```ts:extension.ts
    // ハイライトスタイルの定義
    const highlightDecorationType = vscode.window.createTextEditorDecorationType({
        backgroundColor: 'yellow',
        rangeBehavior: vscode.DecorationRangeBehavior.ClosedClosed,
    });
```

下記の記事を参考にさせていただきました。助かりました。
https://qiita.com/yoshi389111/items/8dca20680eb79f01cb2c
