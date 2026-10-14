# はじめに
諸般の流れからVSCodeでMind 7.5 for WindowsのアプリケーションソースがMindコンパイラでビルドできる環境に加えてC#のアプリケーションソースがビルド、デバッグ実行できる環境をつくりましたが、その目的は謎につつまれたまま、あるいはその記事のMind開発者@killyさんのコメントですでにバレているとも言えつつ、今回はせっかくなので？Mindだけの環境を作ってみます。

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

# Mind7環境の構成
Mind7アプリがビルドできる環境を構成します。下記のサンプルソースファイルを作成します。

```mind:hello7.src
メインとは
　　　　「Hello, World! by mind7」を　表示して　改行すること。
```
## tasks.json
tasks.jsonから前回記事でC#が生成した部分を削除して下記の状態とします。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "mind7 build",
            "type": "process",
            "command": "C:/mind7/bin/mind.exe",
            "args": [
                "${workspaceFolder}/hello7.src",
                "C:/mind7/lib/file"
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
            "program": "${workspaceFolder}/hello7.exe",
            "args": [],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}        
```
今回はプレローンチタスクとしてビルドタスクを設定しました。

# Mind8環境の構成
続いてMind8アプリがビルドできる環境を構成します。下記のサンプルソースファイルを作成します。

```mind:hello8.src
メインとは
　　　　「Hello, World! by mind8」を　表示して　改行すること。
```
## tasks.json
tasks.jsonにMind8のタスクを追記して下記の状態とします。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "mind7 build",
            //Mind7用の記述略
        },
        {
            "label": "mind8 build",
            "type": "process",
            "command": "C:/pmind/bin/mind.exe",
            "args": [
                "${workspaceFolder}\\hello8.src",
                "C:\\pmind\\lib\\file"
            ],
            "problemMatcher": []
        }        
    ]
}
    
```
Mind8の場合、args引数のパス区切り文字で/バックスラッシュはNGでした。\を２度打ちしてエスケープしてください。
Mind8コンパイラが読み込むライブラリのパス区切り文字がバックスラッシュの場合は下記のエラーが出力されます。

```
コンパイルエラー：ファイル名の指定が誤りです。
```
## launch.json
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "mind7 Launch (console)",
            //Mind7用の記述略
        },
        {
            "name": "mind8 Launch (console)",
            "type": "cppvsdbg",
            "request": "launch",
            "preLaunchTask": "mind8 build",
            "program": "${workspaceFolder}/hello8.exe",
            "args": [],
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}        
```
これで準備完了です。


# VSCodeの[実行とデバッグ]から実行
VSCodeのメニューからターミナル→タスクの実行を選択します。下図のようにtasks.jsonの内容が展開されているのを確認します。

![vscodec24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/bf0e15aa-a2ef-ce31-a3fb-7117cd93388c.png)


VSCodeの[実行とデバッグ]のプルダウンを展開すると「mind7 Launch (console)」と「mind8 Launch (console)」が表示されているのを確認します

![vscodec25.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5b9381c7-2a19-bec4-668a-74034f3cdd96.png)

## 「mind7 Launch (console)」の結果
ターミナルに下記の実行結果が出力されます。
```
Hello, World! by mind7
PS C:\developments\vscode\pmind\hello> 
```
デバッグコンソールに下記のような出力が表示されました。
```
Loaded 'C:\developments\vscode\pmind\hello\hello7.exe'. Module was built without symbols.
Loaded 'C:\Windows\SysWOW64\ntdll.dll'. 
Loaded 'C:\Windows\SysWOW64\kernel32.dll'. 
Loaded 'C:\Windows\SysWOW64\KernelBase.dll'. 
Loaded 'C:\Windows\SysWOW64\advapi32.dll'. 
Loaded 'C:\Windows\SysWOW64\msvcrt.dll'. 
Loaded 'C:\Windows\SysWOW64\sechost.dll'. 
Loaded 'C:\Windows\SysWOW64\bcrypt.dll'. 
Loaded 'C:\Windows\SysWOW64\rpcrt4.dll'. 
The program '[11144] hello7.exe' has exited with code 0 (0x0).
```
## 「mind8 Launch (console)」の結果
ターミナルに下記の実行結果が出力されます。
```
Hello, World! by mind8
PS C:\developments\vscode\pmind\hello> 
```
デバッグコンソールに下記のような出力が表示されました。
```
Loaded 'C:\developments\vscode\pmind\hello\hello8.exe'. Module was built without symbols.
Loaded 'C:\Windows\SysWOW64\ntdll.dll'. 
Loaded 'C:\Windows\SysWOW64\kernel32.dll'. 
Loaded 'C:\Windows\SysWOW64\KernelBase.dll'. 
Loaded 'C:\Windows\SysWOW64\sechost.dll'. 
Loaded 'C:\Windows\SysWOW64\bcrypt.dll'. 
The program '[10668] hello8.exe' has exited with code 0 (0x0).
```

# おわりに
Mind7とMind8でロードされるライブラリ構成が若干異なるのが興味深いですね。
