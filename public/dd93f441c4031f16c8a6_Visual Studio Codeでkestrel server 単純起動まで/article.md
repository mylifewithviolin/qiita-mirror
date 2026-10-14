# はじめに
ASP.NET Core（空）アプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。kestrel serverは単体でも起動できるようなのですが、ASP.NET Core Webアプリケーションのホストとして以外起動したことがないので、とりあえず空のASP.NET Coreアプリケーションで起動環境を構成してみます。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
C# 12 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# ASP.NET Core（空）環境の構成
最初にASP.NET Core（空） のプロジェクトを作成してVSCodeを起動します。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。（dotnetバージョンチェックは念のための事前動作確認です。）

```
C:\developments\vscode>dotnet --version
8.0.206

C:\developments\vscode>dotnet new web -o kestrel
テンプレート "ASP.NET Core (空)" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\kestrel\kestrel.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\kestrel\kestrel.csproj を復元しました (138 ミリ秒)。
正常に復元されました。

C:\developments\vscode>cd kestrel
C:\developments\vscode\kestrel>code .
```

下記のようなフォルダ構成でプロジェクトが生成され、kestrel serverの起動処理のソースはProgram.csに生成されます。

```cmd:
C:.
│  appsettings.Development.json
│  appsettings.json
│  kestrel.csproj
│  Program.cs
│
├─obj
│      kestrel.csproj.nuget.dgspec.json
│      kestrel.csproj.nuget.g.props
│      kestrel.csproj.nuget.g.targets
│      project.assets.json
│      project.nuget.cache
│
└─Properties
        launchSettings.json
```

最後の「code .」でVSCodeがプロジェクトフォルダをカレントフォルダとして起動します。
VSCodeが起動してからそのまましばらく（１分以上）待つとVSCodeのウィンドウ内右下に下記のメッセージが表示されます。その場合は通常「はい」を選択します。
「ビルドおよびデバッグに必要な資産が'kestrel'にありません。追加しますか？」

下記のようなフォルダ構成となります。（上記のメッセージで「はい」を選択しない場合、.vscodeフォルダは生成されません。）

```cmd:
C:.
│  appsettings.Development.json
│  appsettings.json
│  kestrel.csproj
│  Program.cs
│
├─.vscode
│      launch.json
│      tasks.json
│
├─bin
│  └─Debug
│      └─net8.0
├─obj
│  │  kestrel.csproj.nuget.dgspec.json
│  │  kestrel.csproj.nuget.g.props
│  │  kestrel.csproj.nuget.g.targets
│  │  project.assets.json
│  │  project.nuget.cache
│  │
│  └─Debug
│      └─net8.0
│          ├─ref
│          └─refint
└─Properties
        launchSettings.json
```

## デバッグ実行開始
とりあえずこの状態でもVSCodeの実行とデバッグに「.NET Core Launch (web)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され
```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\kestrel/kestrel.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  kestrel -> C:\developments\vscode\kestrel\bin\Debug\net8.0\kestrel.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

デバッグコンソールに下記のような起動結果が表示されます。

```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7127
Microsoft.Hosting.Lifetime: Information: Now listening on: https://localhost:7127
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5163
Microsoft.Hosting.Lifetime: Information: Now listening on: http://localhost:5163
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
```

※自己発行証明書をインストールしているので、SSL関連の警告は出ていません。

ブラウザが　
https:\//localhost:7127/　で起動して、Hello World! を表示します。

Programs.csには下記のコードが記述されています。
```cs:Programs.cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();

```
launchSettings.jsonの構成上、下記のポートでも着信しますが、
http:\//localhost:5163/

Programs.csにはSwaggerのことはなにも記述していないため、httpsの7127と同じく
Hello World! が応答します。

# おわりに
いかがでしたでしょうか？app.MapGetが記述されているので、最小APIの最小構成みたいな感じでしょうか。
