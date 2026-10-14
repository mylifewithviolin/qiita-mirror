# はじめに
VSCode(Visual Studio Code)でVSCode用のExtensionを実装してみる入門のステップ５です。
[ステップ４](https://qiita.com/mylifewithviolin/items/6378f59199186c5fe4de)まではテキストのハイライト処理をextension.tsで実装し、それを呼び出すイベントリスナを追加して、テキストエディタが開いたときと、入力の都度処理するようにしてみました。

今回はそっち方向のアプローチではなくtmLanguageの構成で行ってみます。ターゲット言語は日本語プログラミング言語Mind（８）ですが、今回はとりあえずお試しということで一部のシンタックスのサポートとなります。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 22.12.0
npm 10.9.0

# プロジェクトのフォルダ構成
とりあえずextension.tsは実装せず、tmLanguage.jsonとlanguage-configuration.jsonとpackage.jsonで対応してみます。

```cmd:
C:\developments\vscode\mind-extension>tree /f
C:.
│  language-configuration.json
│  package.json
│
└─syntaxes
        mind.tmLanguage.json
```

# プロジェクトの構成ファイル
## package.json
まずはpackage.jsonです。言語の基本情報が"languages"ノードで定義されて、詳しくはlanguage-configuration.jsonで構成されることがわかります。
また、"grammars"ノードで言語の文法情報が構成され、詳しくはmind.tmLanguage.jsonで構成されることがわかります。

```json:package.json
{
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
      ]
    },
    "engines": {
      "node": ">=10.10.0"
    },
    "dependencies": {
      "vscode": "^1.1.0"
    }
  }
```

## language-configuration.json
続いてlanguage-configuration.jsonです。
ここでは
* コメントに関する設定
* 括弧に関する設定
* 自動で閉じるペアの設定
* 自動インデントの設定
* インデントルールの設定

が主に設定されています。

```js:language-configuration.json
{
    "comments": {// コメントに関する設定
      "lineComment": "※",
      "blockComment": ["/*", "*/"]
    },
    "brackets": [//主に対応する括弧を認識し、ハイライトする
      ["{", "}"],
      ["[", "]"],
      ["(", ")"],
      ["「", "」"],
      ["『", "』"]
    ],
    "autoClosingPairs": [//自動的に閉じる括弧や引用符を補完する
        {"open": "{",  "close": "}"},
        {"open": "[",  "close": "]"},
        {"open": "(",  "close": ")"},
        {"open": "「",  "close": "」"},
        {"open": "『",  "close": "』"},
        {"open": "'", "close": "'"}
    ],
    "autoIndentation": "keep",//自動インデント:現在のインデントレベルを維持する
    "indentationRules": {
        "increaseIndentPattern": "^.*とは[^。\"']*$",//現在の行のインデントパターンに基づいて、次の行のインデントを増やす。
        "decreaseIndentPattern": "^\\s*。", //現在の行のインデントパターンに基づいて、次の行のインデントを減らす。
        "indentNextLinePattern": "^.*とは[^。\"']*$", //現在の行が特定のパターンに一致する場合、新しい次の行が自動的にインデントされる
        "unIndentedLinePattern": "^\\s*※.*$"//インデントされるべきではない行の正規表現パターン
    },
    "syntax": {
      "comments": "lineComment",
      "brackets": "brackets",
      "autoClosingPairs": "autoClosingPairs",
      "autoIndentation": "autoIndentation",
      "indentationRules": "indentationRules"
    }
  }
  
```
## mind.tmLanguage.json
最後にmind.tmLanguage.jsonです。日本語プログラミング言語Mindの場合、基本分ち書きなので、だいぶTextMate想定のルールが適用できそうでした。MindとtmLanguage.jsonの両方を知らないとわかりにくいですが、Mindだけでもご存じの場合なにをやろうとしているのかわかるような気がします。

https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide

```json:mind.tmLanguage.json
  {
    "name": "mind",
    "scopeName": "source.mind",
    "patterns": [
      {
        "include": "#keywords"
      },
      {
        "include": "#comments"
      },
      {
        "include": "#strings"
      }
    ],
    "repository": {
      "keywords": {
        "patterns": [
          {
            "name": "keyword.control.mind",
            "match": "\\b(ならば|つぎへ|つぎに|さもなければ|でなければ|もし|または|かつ|ここから|回数指定|繰り返す|繰り返し|終わり)\\b"
          },
          {
            "name": "keyword.operator.mind",
            "match": "(?<=\\w)(は|とは|を|から|と|に)\\b"
          },
          {
            "name": "keyword.declaration.mind",
            "match": "\\b(変数|文字列|文字列実体変数|数値|定数|文字列定数|文字列定数配列|型紙|等価)\\b"
          }
        ]
      },
      "comments": {
        "patterns": [
          {
            "name": "comment.line.kome-mark.mind",
            "match": "※.*$"
          },
          {
            "name": "comment.line.double-slash.mind",
            "match": "//.*$"
          },
          {
            "name": "comment.block.function.mind",
            "begin": "（(?=.*→)",
            "end": "）"
          }
        ]
      },
      "strings": {
        "patterns": [
          {
            "name": "string.kagi-kakko.mind",
            "begin": "「",
            "end": "」"
          },
          {
            "name": "string.quoted.double.mind",
            "begin": "\"",
            "end": "\""
          }
        ]
      }
    },
    "scope": "source.mind",
    "fileTypes": ["src"]
  }
```

送り仮名は手前になにかの文字があって後ろにない場合の割り切り仕様です。上記定義の場合はまだ不十分で、手前の文字がひらがなだった場合などMindの仕様に適合しない場合があります。

## settings.json
キーワードの着色に少しグラデーションをつけるため、VSCodeのsettings.jsonに下記のノードを追記します。

```json:settings.json
    "editor.tokenColorCustomizations":{
        "keywords": "#0037ff",
        "textMateRules": [
            {
                "scope": "keyword.control.mind",
                "settings": {
                    "foreground": "#4a76e4"
                }
            },
            {
                "scope": "keyword.operator.mind",
                "settings": {
                    "foreground": "#db109e"
                }
            }
        ]
    }

```
# VSCodeでMind８ソースコードを開く
では、VSCodeでMind８ソースコードを開いてみます。しかし、前記のプロジェクトフォルダのままですと拡張機能開発ホストが起動できませんので、少し追加構成します。

## VSCode Extension Generatorによる拡張機能環境の構成
今回はextension.tsを実装していませんが、[ステップ１](https://qiita.com/mylifewithviolin/items/36a39d760e06983a694c)を参考にVSCode Extensionプロジェクトとして再構成します。
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

# extension.ts
今回のextension.tsは下記のように空です。

```ts:extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // この部分に機能を追加します
}

export function deactivate() {}

```

## 拡張機能開発ホストのカレントフォルダ
拡張機能開発ホストのカレントフォルダには下記のMind8のソースコードファイルを格納しました。
```
C:\developments\vscode\evaextensiontest>dir

2025/01/02  20:51             1,618 callfunc.src
2025/01/03  08:30             1,057 count2.src
2023/11/20  23:36               990 hello3.src
2025/01/02  20:48             9,379 mssqlodbc.src
2025/01/02  20:48               157 sample.src
2025/01/03  09:25                92 sample2.src
2025/01/02  20:02                63 あいうえお日本語かきくけこさしすせそ.txt
               7 個のファイル              13,356 バイト
```

# シンタックスハイライトの様子
それではVSCode拡張機能開発プロジェクトのmind-extensionをデバッグ実行開始して、拡張機能開発ホストを起動し、サンプルソースを見てみます。

## hello3.src

![vscode-mind-syntax1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/da9a3a0f-7987-ef25-bf42-860ee0dcb226.png)

## mssqlodbc.src

![vscode-mind-syntax2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d20e1fce-5b1e-3a1e-4a44-636e625eb3e8.png)

![vscode-mind-syntax3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c9592930-6e38-301e-a484-48c2c96abbf7.png)

![vscode-mind-syntax4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/8c0762e4-fecf-121e-fe6d-4068d7e457ba.png)

![vscode-mind-syntax5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d798f472-8042-91b3-ae37-d62fc3500a6c.png)

だいぶ見やすくなりました。関数（処理単語）定義の右側の矢印付きかっこは注釈扱いというのがわたしの中ではポイントです:sweat_smile:空改行をはしょっていますが、この注釈の存在がハイライトされたので、定義の範囲がわかりやすくなった気がします。（もちろん空改行すればなおさらですが。）

tmLanguage内でどれかひとつ正規表現に失敗すると着色は全滅するようでした。着色するパターンを１つづつ増やしていく感じにするとよい気がします。

## callfunc.src

![vscode-mind-syntax6.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4c64582a-f915-59e0-6c9e-21ec592a85a9.png)

上図はコマンドパレットの「開発者：エディタートークンとスコープの検査」（コマンドパレットでDeveloper:Inspect Editor Tokens and Scopesを選択します。）で、ソースコードのトークンにどのようなスコープが適用されたかを表示しているところです。ここで具体的にパターンに適合しているワードがtextmate scopesにsource.mindとか大枠のスコープしか表示されない場合も、当該以外の正規表現が不適切で全体が壊れている場合があることも想定した方がよいです。


# おわりに
いかがでしたでしょうか？お好きな言語のシンタックスハイライトの実装にお役に立てればと思います。日本語プログラミング言語Mindがターゲット例ですが、基本は同じかと存じます。

MindのVSCode上のシンタックスハイライトはおととし以来の悲願でしたが、ようやく影形ができてまいりました。日本語プログラミング言語Re:Mindのシンタックスハイライトを実装いただいた@Syuparnさんの[記事](https://qiita.com/Syuparn/items/20c123a6ad456d7757f7)はおおいに励み（プレッシャー？）になりました。改めて感謝申し上げます。←まだ完成していないのに気がはやい:joy:
