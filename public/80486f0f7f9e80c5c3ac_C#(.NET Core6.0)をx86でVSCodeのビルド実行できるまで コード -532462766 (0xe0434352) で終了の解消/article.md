# はじめに
諸般の事情からVSCodeでC#(.NET Core6.0)をx86ターゲットでビルド・デバッグ実行できるようしたいひとのメモです。.NET Core7.0以降は未確認。Windowsです。


# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
C# 10 dotnet-sdk-6.0.404-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft


# C#環境の構成
最初にC#のプロジェクトを作成してVSCodeを起動します。

```
C:\developments\vscode\mind7dll>dotnet new console -o cs
テンプレート "コンソール アプリ" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\mind7dll\cs\cs.csproj で ' dotnet restore ' を実行しています...
  復元対象のプロジェクトを決定しています...
  C:\developments\vscode\mind7dll\cs\cs.csproj を復元しました (150 ms)。
正常に復元されました。

C:\developments\vscode\mind7dll>cd cs
C:\developments\vscode\mind7dll\cs>code .
```
下記のサンプルソースが生成されています。
```cs:Program.cs
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");
```
## cs.csproj
cs.csprojに
```
<PlatformTarget>x86</PlatformTarget>
```
を追加します。

```
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net6.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <PlatformTarget>x86</PlatformTarget>
  </PropertyGroup>

</Project>
```

## tasks.json
適当にデバッグ実行しようとすると下記のようなtasks.jsonとlaunch.jsonを生成してくれます。
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
                "${workspaceFolder}/cs.csproj",
                "/property:GenerateFullPaths=true",
                "/consoleloggerparameters:NoSummary;ForceNoAlign"
            ],
            "problemMatcher": "$msCompile"
        },
        {
            "label": "publish",
            "command": "dotnet",
            "type": "process",
            "args": [
                "publish",
                "${workspaceFolder}/cs.csproj",
                "/property:GenerateFullPaths=true",
                "/consoleloggerparameters:NoSummary;ForceNoAlign"
            ],
            "problemMatcher": "$msCompile"
        },
        {
            "label": "watch",
            "command": "dotnet",
            "type": "process",
            "args": [
                "watch",
                "run",
                "--project",
                "${workspaceFolder}/cs.csproj"
            ],
            "problemMatcher": "$msCompile"
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
            // IntelliSense を使用して、C# デバッグに存在する属性を確認します
            // 既存の属性の説明にホバーを使用する
            // 詳細については、https://github.com/dotnet/vscode-csharp/blob/main/debugger-launchjson.md を参照してください
            "name": ".NET Core Launch (console)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            // ターゲット フレームワークを変更した場合は、プログラム パスを更新するようにしてください。
            "program": "${workspaceFolder}/bin/Debug/net6.0/cs.dll",
            "args": [],
            "cwd": "${workspaceFolder}",
            // 'console' フィールドの詳細については、https://aka.ms/VSCode-CS-LaunchJson-Console を参照してください
            "console": "internalConsole",
            "stopAtEntry": false
        },
        {
            "name": ".NET Core Attach",
            "type": "coreclr",
            "request": "attach"
        }
    ]
}
```
# ビルド実行
VSCodeのメニューからターミナル→タスクの実行を選択します。tasks.jsonの"build"が表示されていますので、それを選択して実行します。

下記のようにターミナルに出力されてビルドは成功します。
```
*  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\mind7dll\cs/cs.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild version 17.3.2+561848881 for .NET
  復元対象のプロジェクトを決定しています...
  復元対象のすべてのプロジェクトは最新です。
  cs -> C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0\cs.dll
```
下記のようなbinフォルダやobjフォルダが生成されて実行ファイルも生成されたようです。
```
C:\developments\vscode\mind7dll\cs>tree
C:.
├─.vscode
├─bin
│  └─Debug
│      └─net6.0
│          └─publish
└─obj
    └─Debug
        └─net6.0
            ├─ref
            └─refint
```

VSCodeの実行とデバッグに「.NET Core Launch (console)」が既定で表示されていますので実行します。VSCodeが一瞬オレンジ色で発火したみたいな感じとなり、コンソール出力は実行されませんでした。

デバッグコンソールには下記が出力されていました。
```
'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\6.0.27\System.Private.CoreLib.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
プログラム '[10684] cs.dll' がコード -532462766 (0xe0434352) で終了しました。
```

# コード -532462766 (0xe0434352) で終了
このエラーコードは、.NET アプリケーションで発生することがあり -532462766 (0xe0434352) は、不明なソフトウェア例外を示しているようです。しかし、デバッグ実行してもブレークはしなかったため？の状態でした。

```
C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0>dir
 C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0 のディレクトリ

2024/03/02  12:52    <DIR>          .
2024/02/28  21:33    <DIR>          ..
2024/03/02  14:12               398 cs.deps.json
2024/03/02  14:49             4,608 cs.dll
2024/03/02  14:49           115,200 cs.exe
2024/03/02  14:49            10,244 cs.pdb
2024/03/02  12:52               147 cs.runtimeconfig.json
2024/03/02  12:52    <DIR>          publish
               5 個のファイル             130,597 バイト

```
binフォルダには上記のように実行ファイルが生成されていますので、とりあえずコマンドプロンプトから実行してみます。

```
C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0>cs
You must install .NET to run this application.

App: C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0\cs.exe
Architecture: x86
App host version: 6.0.27
.NET location: Not found

Learn about runtime installation:
https://aka.ms/dotnet/app-launch-failed

Download the .NET runtime:
https://aka.ms/dotnet-core-applaunch?missing_runtime=true&arch=x86&rid=win10-x86&apphost_version=6.0.27
```

上記の結果から、x86の.NET runtimeを別途インストールしないといけないようですね。確かにインストールしてあるのはdotnet-sdk-6.0.404-win-x64ですが、x86で動かすには別途必要なようです。

# 前提条件の訂正
2024/03/02時点では下記のサイトより.NET Core6.0がダウンロードできます。

https://dotnet.microsoft.com/ja-jp/download/dotnet/6.0

6.0.419が最新でしたので、x86の他x64もダウンロードしてバージョンを揃えました。
dotnet-sdk-6.0.419-win-x64
dotnet-sdk-6.0.419-win-x86

# x86ランタイムインストール後のビルド実行
コマンドプロンプトから実行すると、実行できるようになっていました。:tada:
```
C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0>cs
Hello, World!
```

VSCodeは一度再起動しましたが、まだダメのようでした。
デバッグコンソールの出力は以前と同じで、まだ「Microsoft.NETCore.App\6.0.27\System.Private.CoreLib.dll' が読み込まれました。」と出力されています。

project.assets.jsonを確認すると6.0.419にはなっていそう。
```
    "frameworks": {
      "net6.0": {
        "targetAlias": "net6.0",
        "imports": [
          "net461",
          "net462",
          "net47",
          "net471",
          "net472",
          "net48",
          "net481"
        ],
        "assetTargetFallback": true,
        "warn": true,
        "frameworkReferences": {
          "Microsoft.NETCore.App": {
            "privateAssets": "all"
          }
        },
        "runtimeIdentifierGraphPath": "C:\\Program Files\\dotnet\\sdk\\6.0.419\\RuntimeIdentifierGraph.json"
      }
    }
  }
```
binフォルダとobjフォルダを削除してからデバッグ実行してみましたが
デバッグコンソールの出力は以前と同じです。

このフォルダには6.0.27しかないようでした。
```
C:\Program Files\dotnet\shared\Microsoft.NETCore.App>dir
 C:\Program Files\dotnet\shared\Microsoft.NETCore.App のディレクトリ

2024/02/15  20:15    <DIR>          .
2024/03/02  15:20    <DIR>          ..
2024/03/02  15:18    <DIR>          6.0.27
               0 個のファイル                   0 バイト
```

紛らわしいですが、インストーラのバージョンが6.0.419でも、ランタイムバージョンとしては6.0.27のようですね。フォルダもタイムスタンプも本日になっていました。

前記ダウンロードサイトの記述より
>SDK 6.0.419
付加済みランタイム
.NET Runtime 6.0.27
ASP.NET Core ランタイム 6.0.27
.NET デスクトップ ランタイム 6.0.27
言語サポート
C# 10.0
F# 6.0
Visual Basic 16.9

コマンドプロンプトからは正常実行されますが、VSCodeからは正常にデバッグ実行できない。この謎をさぐるため、C#のVSCodeエクステンションが生成したタスクのwatchを実行してみます。
```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe watch run --project C:\developments\vscode\mind7dll\cs/cs.csproj 

dotnet watch 🔥 Hot reload enabled. For a list of supported edits, see https://aka.ms/dotnet/hot-reload.
  💡 Press "Ctrl + R" to restart.
dotnet watch 🔧 Building...
  復元対象のプロジェクトを決定しています...
  復元対象のすべてのプロジェクトは最新です。
  cs -> C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0\cs.dll
dotnet watch 🚀 Started
Failed to load the dll from [C:\Program Files\dotnet\host\fxr\6.0.27\hostfxr.dll], HRESULT: 0x800700C1
The library hostfxr.dll was found, but loading it from C:\Program Files\dotnet\host\fxr\6.0.27\hostfxr.dll failed
  - Installing .NET prerequisites might help resolve this problem.
     https://go.microsoft.com/fwlink/?linkid=798306
dotnet watch ❌ Exited with error code -2147450750
dotnet watch ⏳ Waiting for a file to change before restarting dotnet...
```

デバッグ実行のときだけ、なにかhostfxr.dll（.NET Host Resolver）に問題が生じている模様。
```
C:\developments\vscode\mind7dll\cs>dir "C:\Program Files\dotnet\host\fxr\6.0.27"
 C:\Program Files\dotnet\host\fxr\6.0.27 のディレクトリ

2024/03/02  15:18    <DIR>          .
2024/03/02  15:18    <DIR>          ..
2024/01/21  22:37           378,656 hostfxr.dll
               1 個のファイル             378,656 バイト
```

# おわりに
デバッグ実行開始にはいたりませんがでしたが、ビルド実行はできるようになりましたので、いったん本記事は終了となります。
下記のタスクをtasks.jsonに追加することで、タスクの実行から実行できます。

```json:tasks.json
        {
            "label": "exec",
            "command": "${workspaceFolder}/bin/debug/net6.0/cs.exe",
            "type": "process",
            "args": [],
            "problemMatcher": []
        },
```
