# はじめに
VSCodeで「プロデル」アプリケーションをビルドして実行開始できるようにtasks.jsonとlaunch.jsonを構成してみます。


# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.95.1
Produire Version 2.0.1197 for Windows


## VSCodeの拡張機能
日本語プログラミング言語「プロデル」拡張機能 0.1.0
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガは直接使わないのですが、「プロデル」アプリケーションをデバッグ実行でローンチするために流用しています。

## tasks.json

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Produire build",
            "type": "process",
            "command": "C:\\Program Files (x86)\\Produire\\Produire.exe",
            "args": [
                "${workspaceFolder}\\callfunc2.rdr"
            ],
            "problemMatcher": []
        }        
    ]
}
    
```
このタスクの実行結果は下記のようにいい感じのようでした。

```cmd:
 *  実行するタスク: C:\Program Files (x86)\Produire\rdrc.exe C:\produire\vscode\callfunc2.rdr 

■☆Ｐ　プロデル コンパイラ Ver.2.0.1197　Ｐ☆■
 Copyright(C) 2007-2023 utopiat.net. All rights reserved.

次のソースファイルをコンパイルします。
　callfunc2.rdr

次のフォルダにあるプラグインを参照します。
　C:\Program Files (x86)\Produire\plugins\

プログラムを解析中...
コンパイル済み実行可能ファイルを生成中...

次のファイルが生成されました！
　C:\produire\vscode\callfunc2.exe
```

## launch.json
launch.jsonではプロデルコンパイラが出力した実行ファイル名callfunc2.exeを設定します。
ダミーのデバッガは.NETコアランタイムで作成してみましたが、x86アプリケーションは起動不可にひっかかって実行できませんでしたので、Mindと同じくC/C++用で設定しました。いちおう起動にはこぎつけましたが、実行ファイル自体がまだ正常に動いていないようでした。

```json:launch.json
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Produire Launch (console cpp)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "Produire build",
            "program": "${workspaceFolder}/callfunc2.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "internalConsole",
        },
        {
            "name": "Produire Launch (console cs)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "Produire build",
            "program": "${workspaceFolder}/callfunc2.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "internalConsole",
        }
    ]
}
```
## 実行のご様子（cppvsdbgでの起動）

コンソールが展開してプロンプトのタイトルからすると実行されている感じですが、結果が出力されずハングアップしている雰囲気でした。
※正常な使い方ではないのは百も承知ですので不具合とは認識しておりませんので念のため。

![produire1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/eb9e99ab-1fc3-3abb-a661-ba3f8be3b018.png)


コンパイラが出力した実行ファイルをコマンドプロンプトから起動しても同様でした。内部でループしている感じでControlキー+Cの打鍵でブレークすると変数出力は実行されました。

```cmd:
C:\produire\vscode>callfunc2
^X
処理回数：0回
処理時間：0ミリ秒

C:\produire\vscode>callfunc2 1000
^X
処理回数：0回
処理時間：0ミリ秒

C:\produire\vscode>
```

# おわりに
いかがでしたでしょうか？あまり役に立った話ではなく申し訳ないです。プロデルデザイナから出力した実行ファイルとrdrcコンパイラが出力した実行ファイルになにか差異があるのかとか、よくわかっておりませんのでご容赦お願いいたします。
