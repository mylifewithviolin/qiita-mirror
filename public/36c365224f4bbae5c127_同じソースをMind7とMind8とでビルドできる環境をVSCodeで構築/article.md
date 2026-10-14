# はじめに

諸般の流れからMind7とMind8 どちらでもビルドできる環境をVSCodeで構築してみましたが、前回は極単純なコンソール出力のソースをMind7とMind8用にそれぞれわけておりましたので、今回はもう少し記述量のあるソースをMind7とMind8とで共通してビルドできる環境をVSCodeで構築してみます。Mind7とMind8でどの程度互換性があるのか実はよくわかっていないのでようそろです。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows

Mindはそれぞれのバージョンのパスが構成されていることを前提とします。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガは直接使わないのですが、Mindアプリケーションをデバッグ実行でローンチするために流用しています。

# お題のソースコード
下記の過去記事でMind8でコンパイル実行したソースを使ってみます。
[日本語プログラミング言語 Mind Java C# でHello World実行時間を仲良く競う（Mindミリ秒で再計測）](https://qiita.com/mylifewithviolin/items/09397c9d817fbbc19f36)

[日本語プログラミング言語 Mind Java C# で関数を介した整数カウントアップ実行時間を仲良く競う](
https://qiita.com/mylifewithviolin/items/4ae2e162b90db9f48281)

# Hello World実行時間
## tasks.json
tasks.jsonでは同じソースファイルhello3.srcをMind7とMind8のビルドタスクに設定します。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "mind7 build",
            "type": "process",
            "command": "C:/mind7/bin/mind.exe",
            "args": [
                "${workspaceFolder}/hello3.src",
                "C:/mind7/lib/file"
            ],
            "problemMatcher": []
        },
        {
            "label": "mind8 build",
            "type": "process",
            "command": "C:/pmind/bin/mind.exe",
            "args": [
                "${workspaceFolder}\\hello3.src",
                "C:\\pmind\\lib\\file"
            ],
            "problemMatcher": []
        }        
    ]
}
    
```

## launch.json
launch.jsonでは同じ実行ファイル名hello3.exeを設定します。
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "mind7 Launch (console)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "mind7 build",
            "program": "${workspaceFolder}/hello3.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        },
        {
            "name": "mind8 Launch (console)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "mind8 build",
            "program": "${workspaceFolder}/hello3.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```
## 実行のご様子
下図はMind7でローンチした状態です。:tada:　Mind8でも同様でした。

![vscodec26.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/ae89a5d2-8ba9-3495-5e14-ac1f108516e3.png)



# 関数を介した整数カウントアップ実行時間
## tasks.json
tasks.jsonでは同じソースファイルcount2.srcをMind7とMind8のビルドタスクに設定します。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "mind7 build",
            "type": "process",
            "command": "C:/mind7/bin/mind.exe",
            "args": [
                "${workspaceFolder}/count2.src",
                "C:/mind7/lib/file"
            ],
            "problemMatcher": []
        },
        {
            "label": "mind8 build",
            "type": "process",
            "command": "C:/pmind/bin/mind.exe",
            "args": [
                "${workspaceFolder}\\count2.src",
                "C:\\pmind\\lib\\file"
            ],
            "problemMatcher": []
        }        
    ]
}
```

## launch.json
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "mind7 Launch (console)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "mind7 build",
            "program": "${workspaceFolder}/count2.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        },
        {
            "name": "mind8 Launch (console)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "mind8 build",
            "program": "${workspaceFolder}/count2.exe",
            "args": ["1000"],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}      
```
## 実行のご様子
下図はMind7でローンチした状態です。:tada:　Mind8でも同様でした。

![vscodec27.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/675765cb-c622-e62d-a75d-d281041eeba0.png)

# Mind7でビルドできなかったMind8のソースコード
処理単語を下記のような関数形式にした場合はMind7でビルドできませんでした。
```
カウントアップとは　関数　整数入力　整数出力（c　→　c）
	cは　変数
	cに　入れ
    	cを　一つ増加し
	cを　返す。
```
これは下記のような関数形式で実行するための宣言です。
```
        ※countを　カウントアップし　countに　入れ
	    [count :=  カウントアップ(count)]
```     
```:callfunc.inf
C:\developments\vscode\pmind\odbcsql\callfunc.src 1 行目でエラー。行内容は、
カウントアップとは　関数　整数入力　整数出力（c　→　c）
      要因１："整数入力"は未定義の単語です。
      要因２：かっこ表記に誤りが有ります。
      要因３："整数出力"は未定義の単語です。
```

定数を使用した場合はMind7でビルドできませんでした。
```
openDbは　		定数　1。
closeDbは　		定数　2。
```
```:mssqlodbc.inf
C:\developments\vscode\pmind\odbcsql\mssqlodbc.src 16 行目でエラー。行内容は、
openDbは　		定数　1。
      要因１："定数"は未定義の単語です。
```
このソースは下記の記事のコードの一部です。
[Mindでトランザクション事始めな書き方を探る（C文字列終端とエラーメッセージ）](
https://qiita.com/mylifewithviolin/items/20deeacfa446e71c5bed)
実はこのソースをMind7でビルドしたかったのですが、そう甘くはなかったようです。


![vscodec28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d3de5410-3905-01c6-684e-91ae7301115d.png)


# おわりに
諸般の事情でMind7とMind8を使い分けなければならない場合、同じソースコードに対して各バージョンのコンパイラで手軽にビルド実行が試せるのはよいかなと思いました。わたしはMind5.2をほぼ完全に忘却してMind8で使い始めなおしているひとなのでMind7とMind8の非互換な部分はほぼわかっておりませんので、なにが違うのか試すのにちょうどよいです。動かない場合はソースファイル名をわけて、動くように調整していく感じですね。
