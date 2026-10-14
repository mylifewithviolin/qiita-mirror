# はじめに
諸般の流れからVSCodeでMind 8 for WindowsのKernelをデバッグ実行する環境をつくってまいりましたが、どちらかというとそれはCベースな環境でした。今回はその流れに割込みでVSCodeでMind 7.5 for WindowsのアプリケーションソースがMindコンパイラでビルドできる環境に加えてC#のアプリケーションソースがビルド、デバッグ実行できる環境をつくります。その目的はなに？この記事ダレトク？


# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
C# 10 dotnet-sdk-6.0.404-win-x64
Mind Version 7.5 for Windows

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガは直接使わないのですが、Mind7アプリケーションをデバッグ実行で強引にローンチするために流用しています。

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
## tasks.json
適当にデバッグ実行しようとすると下記のようなtasks.jsonとlaunch.jsonを生成してくれます。これに後でMind7の記述を追記していきます。
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

## デバッグ実行開始
VSCodeの実行とデバッグに「.NET Core Launch (console)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され
```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\mind7dll\cs/cs.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild version 17.3.2+561848881 for .NET
  復元対象のプロジェクトを決定しています...
  復元対象のすべてのプロジェクトは最新です。
  cs -> C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0\cs.dll
```

デバッグコンソールにC#サンプルアプリの実行結果が表示されます。
```
Hello, World!
プログラム '[7800] cs.dll' がコード 0 (0x0) で終了しました。
```

# Mind7環境の構成
つづいてMind7アプリがビルドできる環境を構成します。下記のサンプルソースファイルを作成します。

```mind:hello.src
メインとは
　　　　「Hello, World! by mind7」を　表示して　改行すること。
```
## tasks.json
C#のエクステンションが自動生成したtasks.jsonに下記のコードを追記します。

```json:tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "command": "dotnet",          
            //C#が生成した内容略
            "problemMatcher": "$msCompile"
        },
        {
            "label": "mind build",
            "type": "process",
            "command": "C:/mind7/bin/mind.exe",
            "args": [
                "${workspaceFolder}/hello.src",
                "C:/mind7/lib/file"
            ],
            "problemMatcher": []
        },
        {
            "label": "mind launch",
            "type": "process",
            "command": "${workspaceFolder}/hello.exe",
            "args": [
                ],
            "problemMatcher": []
        }
    ]
}
    
```
ここで、VSCodeのメニューからターミナル→タスクの実行を選択します。下図のようにtasks.jsonの内容が展開されますのでmind buildを選択します。

![vscodec22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/263182db-8f30-36c7-9e5e-6f0f15f15adc.png)


ターミナルに下記のような出力が表示されます。
```
 *  実行するタスク: C:/mind7/bin/mind.exe C:\developments\vscode\mind7dll\cs/hello.src C:/mind7/lib/file 

日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:750*****
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe --> C:\developments\vscode\mind7dll\cs\hello.exe
```
同じ手順でmind launchを選択するとMind7サンプルアプリの実行結果がターミナルに出力されます。

```
 *  実行するタスク: C:\developments\vscode\mind7dll\cs/hello.exe  

Hello, World! by mind7
```

## launch.json
しかし、ここではやはりVSCodeの実行とデバッグから実行したい気分です。そこでC#エクステが生成したlaunch.jsonに下記のようなコードを追記してみます。
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            //C#が生成した内容略        
        },
        {
            "name": "mind7",
            "type": "cppvsdbg",
            "request": "launch",
            "program": "${workspaceFolder}/hello.exe",
            "args": [],
            "console": "integratedTerminal"
        }
    ]
}        
```
これはつまりMind7アプリのランタイムはCなので、デバッグは実行できないにしても（シンボルファイルありでビルドしておけばもしかしたらCランタイム部分でブレークできるかもしれませんが）とりあえずローンチしてくれるとうれしいなという思惑です。

## デバッグ実行開始
VSCodeの実行とデバッグのプルダウンを展開すると「mind7」が表示されていますので実行します。
デバッグコンソールに下記のような出力が表示されました。
```
Loaded 'C:\developments\vscode\mind7dll\cs\hello.exe'. Module was built without symbols.
Loaded 'C:\Windows\SysWOW64\ntdll.dll'. 
Loaded 'C:\Windows\SysWOW64\kernel32.dll'. 
Loaded 'C:\Windows\SysWOW64\KernelBase.dll'. 
Loaded 'C:\Windows\SysWOW64\advapi32.dll'. 
Loaded 'C:\Windows\SysWOW64\msvcrt.dll'. 
Loaded 'C:\Windows\SysWOW64\sechost.dll'. 
Loaded 'C:\Windows\SysWOW64\bcrypt.dll'. 
Loaded 'C:\Windows\SysWOW64\rpcrt4.dll'. 
The program '[384] hello.exe' has exited with code 0 (0x0).
```
思惑どおりではあるようです。
ターミナルに下記のような出力が表示されます。:tada:
```
Hello, World! by mind7
PS C:\developments\vscode\mind7dll\cs>
```

![vscodec23.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9a0de911-44b4-28b9-e32f-8512897d73a9.png)


# おわりに
今回は構成していませんが、プレタスクにビルドを設定すれば、ソースコードを改修する都度ビルド実行はできそうですね。
