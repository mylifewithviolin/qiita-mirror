 はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ２です。とっかかりとしてステップ１ではVSCode Extensionプロジェクトのテンプレートを生成してみましたので、今回はデバッグ実行の事始めです。コマンドパレットでHello World!してみます。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 20.10.0
npm 10.9.0

# プロジェクトのフォルダ構成

お手数ですが[ステップ１](https://qiita.com/mylifewithviolin/items/36a39d760e06983a694c)をご参照ください。

# extension.ts
プロジェクトのテンプレートで生成されたextension.tsから英文のコメントを削除し、下記のようにコンソールログ出力とコマンドパレットのメッセージを一部日本語にしました。UTF-8で保存します。

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

# VSCodeを起動
evaextensionフォルダをカレントにしてVSCodeを起動します。

```cmd:
C:\developments\vscode\evaextension>code .
```
VSCodeが起動します。既定でできたなりのlaunch.jsonの設定で、デバッグ実行開始してみます。このとき、const disposable = vscode.commands.registerCommandの行がブレークするようにしておきます。

もうひとつのVSCodeが起動して、検索欄に「拡張機能開発ホスト」と表示されています。

![vscodeextension3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/fd52598a-725d-5ff2-1535-1760becfb266.png)

「拡張機能開発ホスト」の方のVSCodeでコマンドパレットを開きます。

筆写の環境では既に実行していますので、下図のように「Hello World」コマンドが候補に現れますが、初回の場合はコマンドパレットのプロンプトに「Hello World」します。候補が出ている場合は選択します。

![vscodeextension4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/cf6e712e-e26c-c7aa-7307-68c1d7072ffb.png)

無事にブレークしました。コンソールログ出力は実行されていますので、デバッグコンソールに日本語メッセージが出力されています。

![vscodeextension5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/378c6b40-11d9-866b-2180-719f62fa71b3.png)

ここでステップオーバーするとコードの最後まで走行し、「拡張機能開発ホスト」の方のVSCodeで下図の（ウィンドウ右下の）メッセージが表示された実行成功です。

![vscodeextension6.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/84db5299-09b1-6907-203c-f106a32e70fd.png)

次回はいよいよextension.tsになにかサンプル実装してデバッグ実行してみます。（前回も言ってなかったか？）

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。とりあえずデバッグできる環境が整ったので、はやく「拡張機能開発ホスト」の方が読み込んだテキストに対してあれこれやってみたいです。

