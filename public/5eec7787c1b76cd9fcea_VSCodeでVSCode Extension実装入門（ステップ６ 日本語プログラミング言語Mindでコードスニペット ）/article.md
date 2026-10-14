# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ６です。
[ステップ５](https://qiita.com/mylifewithviolin/items/5761f0f29255b121eee9)では日本語プログラミング言語Mind（８）をターゲット言語としてtmLanguageの構成で一部のシンタックスハイライトを実装してみました。今回はスニペット機能の追加にチャレンジします。


# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 22.12.0
npm 10.9.0

# プロジェクトのフォルダ構成
実際にはステップ６のようにVSCode-extensionとして実装するファイルやフォルダが必要ですが、スニペットに関連するファイル・フォルダのみとすると下図のようになります。snippetsフォルダ内のjsonファイル名は推奨やルールがあるわけではないので、シンタックスハイライトのtmlanguage.jsonに雰囲気を揃えてみました。

```cmd:
C:\developments\vscode\mind-extension>tree /f
C:.
│  package.json
│
└─snippets
        mind.snippets.json
```
# プロジェクトの構成ファイル
## package.json
まずはpackage.jsonです。ステップ６の情報は除いてスニペットに関する記述のみを以下に記載します。

```json:package.json
{
    "contributes": {
    "snippets": [
      {
        "language": "mind",
        "path": "./snippets/mind.snippets.json"
      }
    ]
    },
  }
```

## mind.snippets.json
続いて、スニペットの定義の中身、mind.snippets.jsonです。いろいろなスニペットを考えるのは楽しい気がしますが、とりあえず最小限のものを用意してみます。

>コード スニペットは、ループや条件文などの繰り返しコード パターンを簡単に入力できるようにするテンプレートです。

下記の公式解説サイトの言葉を引用しました。

https://code.visualstudio.com/docs/editor/userdefinedsnippets#_creating-your-own-snippets

>スニペットのプレフィックス(トリガー テキスト) を入力してTab キーを押すと、スニペットが挿入されます。

このトリガーテキストprefixとスニペットbodyをjsonファイルに定義していきます。同一のスニペットに対して複数のトリガーが定義できるところがミソで、このあたり工夫次第でなかなか楽しい状況を生み出せます。

```json:mind.snippets.json
{
    "while loop": {
      "prefix":["koko","ここ","〇"],
      "body": [
        "ここから","繰り返し"
      ],
      "description": "ループ構文"
    },
    "for loop": {
        "prefix":["kaisu","回数","〇〇"],
        "body": [
          "${1:count}　回数指定して","繰り返し"
        ],
        "description": "回数指定ループ構文"
    },
    "if else": {
        "prefix":["mosi","もし","◇"],
        "body": [
        "${1:condition}","ならば","つぎへ"
        ],
        "description": "分岐構文"
    },
    "if elseif else": {
        "prefix":["mosisamo","もしさも","◇◇"],
        "body": [
            "${1:condition}","ならば","さもなければ","つぎへ"
        ],
        "description": "分岐構文"
    },
    "case": {
        "prefix":["jirei","じれい","◇◇◇"],
        "body": [
        "${1:condition}で","事例をとる","例外なら","事例終わり"
        ],
        "description": "多分岐構文 事例"
    },
    "case by string ": {
        "prefix":["mojirei","もじれい","◇◇◇も"],
        "body": [
        "${1:condition}で","文字列事例をとる","例外なら","事例終わり"
        ],
        "description": "多分岐構文 文字列事例"
    }
  }

```

\\${1:count} や ${1:condition}はプレースフォルダでスニペットが展開した後、フォーカスがこの文字列に移ります。

# VSCodeでMind８ソースコードを開く
では、VSCodeでMind８ソースコードを開いてみます。しかし、前記のプロジェクトフォルダのままですと拡張機能開発ホストが起動できませんので、少し追加構成します。

## VSCode Extension Generatorによる拡張機能環境の構成
今回もextension.tsを実装していませんが、[ステップ１](https://qiita.com/mylifewithviolin/items/36a39d760e06983a694c)を参考にVSCode Extensionプロジェクトとして構成されたステップ６のプロジェクトに追加しました。
```cmd:
C:\developments\vscode\mind-extension>tree /f
C:.
│  language-configuration.json
│  package-lock.json
│  package.json
│  README.md
│  tsconfig.json
│  vsc-extension-quickstart.md
│
├─.vscode
│      extensions.json
│      launch.json
│      settings.json
│      tasks.json
│
├─node_modules
│  │  .package-lock.json
├─out
│      extension.js
│      extension.js.map
│
├─src
│      extension.ts
│
├─snippets
│       mind.snippets.json
└─syntaxes
        mind.tmLanguage.json
```

## package.json
package.jsonを下記のように構成（マージ）しました。

```json:package.json
{
    "name": "mind-extension",
    "displayName": "mindExtension",
    "description": "mind8-VsCodeExtension",
    "version": "0.0.1",
    "engines": {
      "vscode": "^1.95.0",
      "node": ">=10.10.0"
    },
    "categories": [
        "Other"
      ],
    "main": "./out/extension.js",
    "contributes": {
      "languages": [
        {
          "id": "mind",
          "aliases": ["Mind"],
          "extensions": [".src"],
          "configuration": "./language-configuration.json"
        }
      ],
      "grammars": [
        {
          "language": "mind",
          "scopeName": "source.mind",
          "path": "./syntaxes/mind.tmLanguage.json"
        }
      ],
    "snippets": [
      {
        "language": "mind",
        "path": "./snippets/mind.snippets.json"
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

# コードスニペットの様子
それではVSCode拡張機能開発プロジェクトのmind-extensionをデバッグ実行開始して、拡張機能開発ホストを起動し、コードスニペットの様子を見てみます。

## ループ

デモ動画は自分のだいぶ好みが入っていますが、「〇」をプレフィクスにしたケースを図示しました。「〇」を２つタイプするひとはいないのでは？とソースを見て思われて方がいらっしゃったかもしれません。とりえず下図のように「〇」を１つタイプすると「〇〇」も候補に現れるのがミソでございます。

![vscodeex-mind1.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/27f0edb2-80ba-f5e3-d38b-32c8ebc28643.gif)


## 分岐・多分岐

解像度も低く縦横比もむだありの状態のデモ動画すみません。条件分岐のコードスニペットです。こちらも自分の好みでRe:Mindチックな「◇」をプレフィクスにしたケースです。もちろん「もし」「mosi」でも選択肢でます。またMindの条件分岐の「もし」はオプションで必須ではないので、スニペット側には出力していません。

![vscodeex-mind2.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/29301607-e119-ced4-d0b7-792e409f227d.gif)


設定側のjsonファイルの文字コードはUTF-8で、挿入先のMindのソースファイルはSHIFT-JISですが、問題なく日本語を挿入できました。

# おわりに
いかがでしたでしょうか？お好きな言語のコードスニペットの実装にお役に立てればと思います。日本語プログラミング言語Mindがターゲット例ですが、基本は同じかと存じます。

下記の記事を参考にさせていただきました。@Syuparnさんが書かれた下記の記事の内容をようやく深く理解することができました。

https://qiita.com/Syuparn/items/e8dbbfc29b588ddb45df

https://qiita.com/Syuparn/items/20c123a6ad456d7757f7
