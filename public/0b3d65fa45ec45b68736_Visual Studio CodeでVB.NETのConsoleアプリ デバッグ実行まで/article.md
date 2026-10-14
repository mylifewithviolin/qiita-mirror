# はじめに
VisualBasic.NET(VB.NET)のConsoleアプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。

VSCodeや.NETCore、VB.NET、C#のVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.98.2
VB.NET 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# VB.NET Consoleアプリケーションプロジェクトの作成
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。
>dotnet new console -lang vb -o HelloWorld

dotnet --versionは念のための確認です。既定のC#とは異なり-langオプションで言語を指定します。
```
C:\developments\vscode>dotnet --version
8.0.204

C:\developments\vb>dotnet new console -lang vb -o HelloWorld
テンプレート "コンソール アプリ" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vb\HelloWorld\HelloWorld.vbproj を復元しています:
  Determining projects to restore...
  C:\developments\vb\HelloWorld\HelloWorld.vbproj を復元しました (126 ミリ秒)。
正常に復元されました。
```

カレントフォルダをプロジェクトフォルダHelloWorldに移動して、VSCodeを起動します。

```
C:\developments\vb>dir
 C:\developments\vb のディレクトリ

2025/03/30  16:53    <DIR>          .
2025/03/30  16:52    <DIR>          ..
2025/03/30  16:53    <DIR>          HelloWorld
               0 個のファイル                   0 バイト
               3 個のディレクトリ   ***,535,971,328 バイトの空き領域

C:\developments\vb>cd HelloWorld

C:\developments\vb\HelloWorld>code .```
```

VSCodeが起動したあと、いきなりデバッグ実行で「実行とデバッグ」をクリックすると下図のダイアログが表示されますので、キャンセルをクリックします。

![vb1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/f19ea6c5-3f65-452f-ba22-6f682f335ca8.png)

とりあえず、「launch.jsonファイルを作成する」をクリックして、.NET関連の機能を選択します。すると.vscodeフォルダとlaunch.jsonファイルは作成してくれます。
## launch.json
下図の状態のlaunch.jsonは自動生成例です。これを少し書き換えます。

```json:launch.json
{
    // IntelliSense を使用して利用可能な属性を学べます。
    // 既存の属性の説明をホバーして表示します。
    // 詳細情報は次を確認してください: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
    {
        "name": ".NET Core Launch (console)",
        "type": "coreclr",
        "request": "launch",
        "preLaunchTask": "build",
        "program": "${workspaceFolder}/bin/Debug/<target-framework>/<project-name.dll>",
        "args": [],
        "cwd": "${workspaceFolder}",
        "stopAtEntry": false,
        "console": "internalConsole"
    }
    ]
}
```

### 修正後
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": ".NET Core Launch (console)",
        "type": "coreclr",
        "request": "launch",
        "preLaunchTask": "build",
        "program": "${workspaceFolder}/bin/Debug/net8.0/HelloWorld.dll",
        "args": [],
        "cwd": "${workspaceFolder}",
        "stopAtEntry": true,
        "console": "internalConsole"
      },
        {
            "name": ".NET Core Attach",
            "type": "coreclr",
            "request": "attach"
        }
    ]
  }

```

## tasks.json
tasks.jsonは下記のようなのを手動で作成します。
```json:tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "command": "dotnet",
      "type": "process",
      "args": [
        "build",
        "${workspaceFolder}"
      ],
      "problemMatcher": "$msCompile"
    }
  ]
}

```
# ビルド・デバッグ実行開始
VSCodeの実行とデバッグに「.NET Core Launch (Console)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され

```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vb\HelloWorld 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  HelloWorld -> C:\developments\vb\HelloWorld\bin\Debug\net8.0\HelloWorld.dll

ビルドに成功しました。
    0 個の警告
    0 エラー

経過時間 00:00:02.74
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

下図のようにエントリポイントでいったんブレークします。本記事の構成の場合はまだ任意の位置にブレークポイント設定できません。また別の機会で触れてまいります。

![vb2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/94d204d9-4acd-421e-8dfe-8263ea4f0790.png)

ブレークを抜けるとデバッグコンソールに「Hello World!」が出力されます。
```
Hello World!
プログラム '[11480] HelloWorld.dll' がコード 0 (0x0) で終了しました。
```

# おわりに
いかがでしたでしょうか？launch.jsonやtasks.jsonはけっこう手書き修正が必要でした。なにかの役にたてば幸いです。
