# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ３です。ステップ２ではコマンドパレットでHello World!してみました。ステップ３ではVSCodeエディタが読み込んでいるテキストを処理してみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 20.10.0
npm 10.9.0

# プロジェクトのフォルダ構成

お手数ですが[ステップ１](https://qiita.com/mylifewithviolin/items/36a39d760e06983a694c)をご参照ください。

# extension.ts（ステップ２）

[ステップ２](https://qiita.com/mylifewithviolin/items/c8e4ebb357a25bd6fcf0)では下記の状態のコードで無事にコマンドパレットでHello World!しました。（実際のステップ２の状態より改行をつめています。）

```ts:extension.ts
import * as vscode from 'vscode';
export function activate(context: vscode.ExtensionContext) {
	console.log('おめでとうございます！,あなたのエクステンション"evaextension"は現在アクティブです！');
	const disposable = vscode.commands.registerCommand('evaextension.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World! evaExtensionです！');
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
```
このとき、重要なのがpackage.jsonです。プロジェクトテンプレートが生成された際に、上記のサンプルコード（生成直後はすべて英語コメントとメッセージ）の生成と同時にpackage.jsonが生成され、"command": "evaextension.helloWorld"が記述されています。

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

extension.tsにコマンドを追加していく際には、このファイルの修正も必要となっていきます。それでは、VSCodeエディタが読み込んでいるテキストを処理するもっともシンプルなサンプルを実装してみます。

# extension.ts（ステップ３の１）
extension.tsにextension.showDocumentContentを追加します。
アクティブなコードエディタの存在を確認して、エディタ内のテキストを読み込みVSCodeのインフォメーションメッセージとして表示します。

```ts:extension.ts
import * as vscode from 'vscode';
export function activate(context: vscode.ExtensionContext) {
	console.log('エクステンション"evaextension"は現在アクティブです！');
	const disposable = vscode.commands.registerCommand('evaextension.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World! evaExtensionです！');
	});

    const disposable2 = vscode.commands.registerCommand('extension.showDocumentContent', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('アクティブなエディタがありません!');
         } else {
            const document = editor.document;
            const documentText = document.getText();
            // 取得したテキストを情報メッセージとして表示
            vscode.window.showInformationMessage('エディタの内容: ' + documentText);
        }
    });
	context.subscriptions.push(disposable);
    context.subscriptions.push(disposable2);
}

export function deactivate() {}
```
## package.json
package.jsonにもextension.showDocumentContentを追加します。これを忘れるとコマンドパレットに出現しません。

```json:package.json
  "contributes": {
    "commands": [
      {
        "command": "evaextension.helloWorld",
        "title": "Hello World"
      },
      {
        "command": "extension.showEditorContent",
        "title": "Show Editor Content"
      }
    ]
  },
```

## VSCodeでデバッグ実行開始

VSCodeでデバッグ実行開始開発ホストが開いたらエディタになにか適当な文字をタイプしてコマンドパレットでコマンドをタイプすると、追加したコマンドがタイプ途中から出現しました。

![vscodeextension7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ac30d106-32c8-4e5d-dcb3-7f692cade92a.png)

タイプしきってコマンドを実行すると、下図のように情報メッセージが表示されました。こんな風にエディタの内容にアクセスするのですね。だいぶイメージがわきました。

![vscodeextension8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/937aa04f-1314-0f64-1cd4-92c0346448ea.png)


# extension.ts（ステップ３）
つづいて今度はコードエディタの中のテキストに対してハイライト強調を行ってみたいと思います。この実装はだいぶ実現したい機能に近いイメージです。

```ts:extension.ts
import * as vscode from 'vscode';
export function activate(context: vscode.ExtensionContext) {
	console.log('エクステンション"evaextension"は現在アクティブです！');
	const disposable = vscode.commands.registerCommand('evaextension.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World! evaExtensionです！');
	});

    const disposable2 = vscode.commands.registerCommand('extension.showDocumentContent', () => {
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

	context.subscriptions.push(disposable);
    context.subscriptions.push(disposable2);
    context.subscriptions.push(disposable3);
}

export function deactivate() {}
```

だいぶコード量が多くなりました。package.jsonにも追加します。
## package.json

```json:package.json
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
        "command": "extension.highlighEditorContent",
        "title": "highlight Matches"
      }
    ]
  },
```

## VSCodeでデバッグ実行開始

VSCodeでデバッグ実行開始開発ホストが開いたらエディタになにか適当な文字をタイプしてコマンドパレットでコマンドをタイプします。

![vscodeextension9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4269ead2-79f8-7007-02ba-c14c9a23cb33.png)

途中まで予測されたところで、追加したコマンドをクリックします。すると下図のようにターゲットの文言が黄色くハイライトされました:tada:

![vscodeextension10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7134ef3b-7ddb-9673-afb1-e79659cfc2b3.png)

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。「拡張機能開発ホスト」のVSCodeが読み込んだテキストに対して初めて操作できました。こんな感じで動くのですね。次回は少しコードを整理して、コマンドパレット以外のイベントから処理させてみます。（あくまで予定）
