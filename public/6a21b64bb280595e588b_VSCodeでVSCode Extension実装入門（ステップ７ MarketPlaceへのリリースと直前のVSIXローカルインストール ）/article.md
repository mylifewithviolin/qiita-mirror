# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ７です。
[ステップ５](https://qiita.com/mylifewithviolin/items/5761f0f29255b121eee9)では日本語プログラミング言語Mind８をターゲット言語としてtmLanguageの構成で一部のシンタックスハイライトを実装し、[ステップ６](https://qiita.com/mylifewithviolin/items/5eec7787c1b76cd9fcea)ではスニペット機能の追加を行いましたので、今回はいよいよVisualStudio MarketPlaceのExtensions for Visual Studio Codeへのリリースにチャレンジします。

# 参考情報
下記の記事を参考にさせていただきました。

https://qiita.com/mstakaha1113/items/81ddab698c1d4d01a10b?form=MG0AV3

https://qiita.com/teckback/items/227518fd145b380e0592

https://qiita.com/ss_tom_jp/items/5977e4f16d78b8ca7cc8

VSCode ExtensionをVisualStudio MarketPlaceに登録するためには、Azure DevOpsアカウントを作成し、VisualStudio MarketPlaceにサインインしてパブリッシャIDの取得、そのIDとDevOpsで生成したアクセストークンがリリースに必要なことがわかりました。

# Azure DevOps無料アカウントの作成とサインイン

ユーザー5名まで無料のBasicプランで開始しました。
GitHubアカウントでのサインアップもできたのですが、マイクロソフトアカウントが既にあってそちらとも紐づいていましたので、マイクロソフトアカウントでサインアップしました。

## Azure DevOpsでPersonal Access Tokensを生成しておく

Azure DevOpsのユーザー設定の「Personal Access Tokens」ページを（メニューヘッダの右端のイニシャルアイコンの左側のアイコンをクリックし、ショートカットメニューの「Personal access tokens」をクリックして）開きます。

![access-token.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/7247fee3-cdb4-4410-9723-5119e730af7e.png)


「+ New Token」ボタンをクリックすると「Create a new personal access token」というタイトルのモーダルページが開きます。

トークン名Nameは今回は「mind-extension」として、Scopesをカスタム定義としてMarketplaceのManageにチェックを入れるだけとしています。（ReadとPublishにも無効化されたチェックが入ります。）

長い文字列のトークンが生成されますので、のちのVSCEコマンド実行時に貼り付けられるようにしておきます。

# marketplace.visualstudio.comへのサインインとpublisher登録

https://marketplace.visualstudio.com/

marketplace.visualstudio.comへのサインインします。Azure DevOpsにサインインした状態のブラウザで展開したので、右上のサインインをクリックしただけでサインインできた気がします。

「Visual Studio」「Visual Studio Code」などのメニュータブの並びのリボン右端の「Public extensions」リンクをクリックしてパブリッシャ登録しておきます。

ここで登録したパブリッシャIDが、のちに説明するVSCEのログインに必要となります。

# VSCE（Visual Studio Code Extension Manager）のインストール
VSCEをnpmでインストールします。
>npm install -g vsce

```cmd:
C:\developments\vscode-extention\mind-extension-preview>npm install -g vsce
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated vsce@2.15.0: vsce has been renamed to @vscode/vsce. Install using @vscode/vsce instead.

sing @vscode/vsce instead.

added 123 packages in 36s

37 packages are looking for funding
  run `npm fund` for details

C:\developments\vscode-extention\mind-extension-preview>vsce
Usage: vsce <command>

Options:
  -V, --version                      output the version number
  -h, --help                         display help for command

Commands:
  ls [options]                       Lists all the files that will be
                                     published
  package [options] [version]        Packages an extension
  publish [options] [version]        Publishes an extension
  unpublish [options] [extensionid]  Unpublishes an extension. Example
                                     extension id: microsoft.csharp.
  ls-publishers                      List all known publishers
  delete-publisher <publisher>       Deletes a publisher
  login <publisher>                  Add a publisher to the known publishers     
                                     list
  logout <publisher>                 Remove a publisher from the known
                                     publishers list
  verify-pat [options] [publisher]   Verify if the Personal Access Token has     
                                     publish rights for the publisher.
  show [options] <extensionid>       Show extension metadata
  search [options] <text>            search extension gallery
  help [command]                     display help for command

  ls-publishers                      List all known publishers
  delete-publisher <publisher>       Deletes a publisher
  login <publisher>                  Add a publisher to the known publishers     
                                     list
  logout <publisher>                 Remove a publisher from the known
                                     publishers list
  verify-pat [options] [publisher]   Verify if the Personal Access Token has     
                                     publish rights for the publisher.
  show [options] <extensionid>       Show extension metadata
  search [options] <text>            search extension gallery
  help [command]                     display help for command
```

# VSCEでログイン（パブリッシャIDとアクセストークンがここで必要）
VSCEでログインします。パブリッシャIDとアクセストークンがここで必要となります。
>vsce login \<publisherId>


ここではVSCodeで拡張機能の開発プロジェクトを開いて、そこがカレントディレクトリとなったターミナルで実行しました。
>Personal Access Token for publisher '\<publisherId>': 

で、プロンプトが一度とまりますので、そこにアクセストークンを貼り付けます。

```cmd:
C:\developments\vscode-extention\mind-extension-preview>vsce login mylifewithviolin
(node:6892) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)       
https://marketplace.visualstudio.com/manage/publishers/
Personal Access Token for publisher 'mylifewithviolin': ************************************************************************************

The Personal Access Token verification succeeded for the publisher 'mylifewithviolin'.
```

# VSCEでVSIXパッケージ生成
つづいてVSCEでVSIXパッケージを生成します。
>vsce package

```cmd:
C:\developments\vscode-extention\mind-extension-preview>vsce package
(node:13268) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
Executing prepublish script 'npm run vscode:prepublish'...
Executing prepublish script 'npm run vscode:prepublish'...

> mind-extension-preview@0.0.1 vscode:prepublish
> npm run compile


> mind-extension-preview@0.0.1 compile
> tsc -p ./

 DONE  Packaged: C:\developments\vscode-extention\mind-extension-preview\mind-extension-preview-0.0.1.vsix (18 files, 10.22KB)
```

上記は成功した状態ですが、package.jsonに下記の記述がない場合
```json:package.json
"activationEvents": [ "onLanguage:mind" ],
```
下記のエラーがでました。
```cmd:
ERROR  Manifest needs the 'activationEvents' property, given it has a 'main' property.
```
package.jsonのactivationEventsには下記の推奨事項が表示されていたので、以前削除していたためでした。

>このアクティブ化イベントは、package.json コントリビューション宣言から自動的に生成されるので VS Code として削除できます。

この点解消してコマンド実行成功した後は無事にパッケージファイルvsixが生成されていました。

```cmd:
C:\developments\vscode-extention\mind-extension-preview>dir *.vsix

2025/01/13  16:31            10,464 mind-extension-preview-0.0.1.vsix
               1 個のファイル              10,464 バイト
```

# VSIXパッケージをローカルインストール
念のため動作確認としてVSIXパッケージをローカルインストールします。

![vscodeextension12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/daf46293-3c4d-1a75-f7e2-d27ed74a725d.png)

上記のメニュー選択で、ファイル選択ダイアログが開きますので、生成されたVSIXパッケージファイルを選択します。

![vscodeextension13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/df75ef73-31f9-48da-fe82-f0f94af25546.png)

動作しているっぽいです:tada:

# VSIXパッケージをMarketPlaceへリリース

では、最後にMarketPlaceへリリースします。
>vsce publish

```cmd:
C:\developments\vscode-extention\mind-extension-preview>vsce publish
(node:16180) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
Executing prepublish script 'npm run vscode:prepublish'...

> mind-extension-preview@0.0.1 vscode:prepublish
> npm run compile


> mind-extension-preview@0.0.1 compile
> tsc -p ./

 INFO  Publishing 'mylifewithviolin.mind-extension-preview v0.0.1'...
 INFO  Extension URL (might take a few minutes): https://marketplace.visualstudio.com/items?itemName=mylifewithviolin.mind-extension-preview
 INFO  Hub URL: https://marketplace.visualstudio.com/manage/publishers/mylifewithviolin/extensions/mind-extension-preview/hub
 DONE  Published mylifewithviolin.mind-extension-preview v0.0.1.
```

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/3e0383f5-952d-dacf-2d4d-4ee5cfb12403.png)


# おわりに
いかがでしたでしょうか？ほとんど自分用の備忘録ですが、なにかのお役に立てればと思います。リリースされたエクステンションの様子は導入方法の別記事で触れさせていただきます。
