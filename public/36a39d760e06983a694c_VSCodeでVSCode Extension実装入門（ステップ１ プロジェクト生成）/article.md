# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ１です。まずはとっかかりとしてプロジェクトのテンプレートを生成してみます。環境は昨年日本語プログラミング言語なでしこv3の検証用に導入した状態ですので最新ではないです。


 # 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 20.10.0
npm 10.2.3 -> 10.9.0

# VSCode Extensionプロジェクトの作成

## YeomanとVSCode Extension Generatorのインストール
最初に YeomanとVSCode Extension Generatorをインストールします。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。
(最初のはどんなnodeとnpmが入っているかの念のための確認です。入っていることに確信のある人は実行不要です。）

```cmd:
C:\developments\vscode>node -v
v20.10.0
C:\developments\vscode>npm -version
10.2.3
C:\developments\vscode>npm install -g yo generator-code
npm WARN deprecated npmlog@2.0.4: This package is no longer supported.
npm WARN deprecated gauge@1.2.7: This package is no longer supported.
npm WARN deprecated are-we-there-yet@1.1.7: This package is no longer supported.
npm WARN deprecated boolean@3.2.0: Package no longer supported. Contact Support at https://www.npmjs.com/support for more info.

added 1053 packages in 2m

156 packages are looking for funding
  run `npm fund` for details
npm notice
npm notice New minor version of npm available! 10.2.3 -> 10.9.0
npm notice Changelog: https://github.com/npm/cli/releases/tag/v10.9.0
npm notice Run npm install -g npm@10.9.0 to update!
npm notice
```
一部警告がでておりますが、npmだけアップデートしてとりあえず先へ進みます。

```cmd:
C:\developments\vscode>npm install -g npm@10.9.0

added 1 package in 12s

25 packages are looking for funding
  run `npm fund` for details
```

## 新しいプロジェクトの生成

yo codeとタイプします。下記のようなプロンプトが出力されますので、「New Extension (TypeScript)」を選択した状態でEnterキーを押します。

```cmd:
C:\developments\vscode>yo code

     _-----_     ╭──────────────────────────╮
    |       |    │   Welcome to the Visual  │
    |--(o)--|    │   Studio Code Extension  │
   `---------´   │        generator!        │
    ( _´U`_ )    ╰──────────────────────────╯
    /___A___\   /
     |  ~  |
   __'.___.'__
 ´   `  |° ´ Y `

? What type of extension do you want to create? (Use arrow keys)
> New Extension (TypeScript)
  New Extension (JavaScript)
  New Color Theme
  New Language Support
  New Code Snippets
  New Keymap
  New Extension Pack
  New Language Pack (Localization)
  New Web Extension (TypeScript)
  New Notebook Renderer (TypeScript)
```
選択肢が消えて下図のプロンプトが表示されます。とりあえず「evaExtension」とします。
```cmd:
? What type of extension do you want to create? New Extension (TypeScript)
? What's the name of your extension? ()
```
プロンプトに答えていくと下図の少し迷うオプションが提示されました。とりあえずなにもバンドルしませんよで既定のままEnterでGO。

```cmd:
? What type of extension do you want to create? New Extension (TypeScript)
? What's the name of your extension? evaExtension
? What's the identifier of your extension? evaextension
? What's the description of your extension? assessment-VsCodeExtension
? Initialize a git repository? Yes
? Which bundler to use? (Use arrow keys)
> unbundled
  webpack
  esbuild
```
下記の状態になりましたので、先ほどアップデートしたのでnpmのままでいきます。
```cmd:
? Which bundler to use? unbundled
? Which package manager to use? (Use arrow keys)
> npm
  yarn
  pnpm
```

下図の状態になって依存関係のインストールが開始します。
```cmd:
? Which package manager to use? npm

Writing in C:\developments\vscode\evaextension...
   create evaextension\.vscode\extensions.json
   create evaextension\.vscode\launch.json
   create evaextension\.vscode\settings.json
   create evaextension\.vscode\tasks.json
   create evaextension\package.json
   create evaextension\tsconfig.json
   create evaextension\.vscodeignore
   create evaextension\vsc-extension-quickstart.md
   create evaextension\.gitignore
   create evaextension\README.md
   create evaextension\CHANGELOG.md
   create evaextension\src\extension.ts
   create evaextension\src\test\extension.test.ts
   create evaextension\.vscode-test.mjs
   create evaextension\eslint.config.mjs

Changes to package.json were detected.

Running npm install for you to install the required dependencies.
```

下図はRunning npm install for you to install the required dependencies.
が
Changes to package.json were detected.
に変わったところからです。警告がでています。内部でgitが呼ばれたらしい。とりあえず無視しておきます。

```cmd:
Changes to package.json were detected.

Running npm install for you to install the required dependencies.
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported

added 266 packages, and audited 267 packages in 56s

70 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
'git' は、内部コマンドまたは外部コマンド、
操作可能なプログラムまたはバッチ ファイルとして認識されていません。
× An error occured while running code:app#end
Error code

Command failed with exit code 1: git init --quiet

```

## プロジェクトのフォルダ構成

下記のようなフォルダ構成でプロジェクトが生成されています。nodeで開発したことがあるひとならなんとなくわかりそうな構成。VSCodeでまだ一度も開いていませんが、.vscodeフォルダも生成してくれている模様。

```cmd:
C:\developments\vscode\evaextension>dir
 C:\developments\vscode\evaextension のディレクトリ

2024/11/17  14:09    <DIR>          .
2024/11/17  14:08    <DIR>          ..
2024/11/17  14:08                43 .gitignore
2024/11/17  14:08    <DIR>          .vscode
2024/11/17  14:08               117 .vscode-test.mjs
2024/11/17  14:08               154 .vscodeignore
2024/11/17  14:08               239 CHANGELOG.md
2024/11/17  14:08               629 eslint.config.mjs
2024/11/17  14:09    <DIR>          node_modules
2024/11/17  14:09           123,613 package-lock.json
2024/11/17  14:08               974 package.json
2024/11/17  14:08             2,180 README.md
2024/11/17  14:08    <DIR>          src
2024/11/17  14:08               535 tsconfig.json
2024/11/17  14:08             3,098 vsc-extension-quickstart.md
              10 個のファイル             131,582 バイト
               5 個のディレクトリ  46,175,457,280 バイトの空き領域
```
プロジェクトルートからツリーをつくるとnode_modulesの下がたいへんなので、とりあずsrcフォルダを展開します。
```cmd:
C:\developments\vscode\evaextension\src>tree /F
C:.
│  extension.ts
│
└─test
        extension.test.ts
```

# VSCodeを起動
evaextensionフォルダをカレントにしてVSCodeを起動します。
```cmd:
C:\developments\vscode\evaextension\src>cd ..
C:\developments\vscode\evaextension>code .
```
VSCodeが起動しますと、拡張機能の推奨事項がウィンドウ右下に表示されました。推奨事項の内容を表示すると必要そうなものでしたのでインストールすることにします。

![vscodeextension1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/e5601fbd-97f3-2c9e-e1ce-7007a0941143.png)

既定でできたなりのlaunch.jsonの設定で、デバッグ実行開始してみますと、もうひとつのVSCodeが起動して、検索欄に「拡張機能開発ホスト」と表示されています。

![vscodeextension2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/91603826-cd36-6327-1eba-3b48237b7d0e.png)

次回はいよいよextension.tsになにかサンプル実装してデバッグ実行してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
