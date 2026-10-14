# はじめに
kestrel serverをASP.NET Core 空アプリケーション（最小APIの最小版みたいな）のホストとして起動できるようになりましたので、ここでいよいよ本題です。この環境をCGI用に調整して、日本語プログラミング言語MindによるCGIを動かしてみます。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
C# 12 
dotnet-sdk-8.0.206-win-x64
Mind Version 8.0.08 for Windows

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# ASP.NET Core（空）環境の構成
最初にASP.NET Core（空） のプロジェクトを作成してVSCodeを起動します。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。（dotnetバージョンチェックは念のための事前動作確認です。）

```
C:\developments\vscode>dotnet --version
8.0.206

C:\developments\vscode>dotnet new web -o kestrelcgi
テンプレート "ASP.NET Core (空)" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\kestrelcgi\kestrelcgi.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\kestrelcgi\kestrelcgi.csproj を復元しました (138 ミリ秒)。
正常に復元されました。

C:\developments\vscode>cd kestrelcgi
C:\developments\vscode\kestrelcgi>code .
```

生成されるフォルダ構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/dd93f441c4031f16c8a6)を参照してください。プロジェクト名がkestrelからkestrelcgiに変わっただけです。

Programs.csには下記のコードが記述されています。

```cs:Programs.cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();

```

これを下記のように書き換えます。kestrel ServerをCGIが処理できるようC#で構成する記述例はネットでは発見できなかったので、生成AI（Windows11 Copilot）の提示内容を検証調整した結果です。

```cs:Programs.cs
var builder = WebApplication.CreateBuilder(args);

// Kestrelサーバーの設定
builder.WebHost.UseKestrel(options =>
{
    // localhost（127.0.0.1）からの接続をポート5000で受け入れる 
    options.ListenLocalhost(5000);
});
// ルートディレクトリの設定（CGIスクリプトの配置場所）
builder.WebHost.UseContentRoot(Directory.GetCurrentDirectory());

var app = builder.Build();

// 静的ファイルのサポート
app.UseStaticFiles();

// CGIの設定
app.Use(async (context, next) =>
{
    if (context.Request.Path.StartsWithSegments("/cgi"))
    {
        var process = new System.Diagnostics.Process
        {
            StartInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "helloMind.cgi", // CGIスクリプトのパス
                Arguments = "", // 必要な引数
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };
        process.Start();
        //レスポンスヘッダにContent-Typeを追加 
        context.Response.ContentType = "text/html";
        await process.StandardOutput.BaseStream.CopyToAsync(context.Response.Body);
        await process.WaitForExitAsync();
    }
    else
    {
        await next.Invoke();
    }
});

app.Run();
```

この構成によりVSCodeプロジェクトフォルダのサブフォルダcgiにcgiモジュールを格納すると応答するようになりました。ここではFileNameはワイルドカード指定せず、直接固有名を指定しています。

# Mind CGIアプリケーションの作成

@Mind-Club_2017さんの[こちらの記事](https://qiita.com/Mind-Club_2017/items/0fdad646aff08a87618d)を参考に、MindのCGIのサンプルコードを記述します。

```Mind:hellMind.src
メインは
	「ＭｉｎｄによるＣＧＩのテスト」で、HTMLヘッダ出力し
	「こんにちは、Ｍｉｎｄ！」を、大きく表示すること。
```
VSCodeのターミナルでコマンドプロンプトを開いて、Mindでビルドします。
```
C:\developments\vscode\kestrelcgi>cd \pmind

C:\pmind>usemind
myfolder=pmind\
myfolder=pmind
newpath=[]
Mindの開発環境を設定しました。

C:\pmind>cd C:\developments\vscode\kestrelcgi
C:\developments\vscode\kestrelcgi>mind helloMind c:\pmind\lib\cgilib

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\pmind\bin\mindexcgi.exe --> helloMind.cgi

C:\developments\vscode\kestrelcgi>
```

生成されたhelloMind.cgiをC:\developments\vscode\kestrelcgi\cgiにコピーします。
また、上記のMind8のインストール構成の場合、C:\pmind\binからmrunt160.exeをコピーします。

```
C:.
│  appsettings.Development.json
│  appsettings.json
│  helloMind.cgi
│  helloMind.his
│  helloMind.mco
│  helloMind.src
│  helloMind.sym
│  kestrelcgi.csproj
│  Program.cs
│
├─.vscode
│      launch.json
│      tasks.json
│
├─bin
├─cgi
│      helloMind.cgi
│      mrunt160.exe
```

# launch.json
launch.jsonのserverReadyActionに
```json:launch.json
    "uriFormat": "%s/cgi/helloMind.cgi"
```
uriFormatを追記します。これでブラウザをローンチしたときに既定でhelloMind.cgiが実行されます。

```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            // IntelliSense を使用して、C# デバッグに存在する属性を確認します
            // 既存の属性の説明にホバーを使用する
            // 詳細については、https://github.com/dotnet/vscode-csharp/blob/main/debugger-launchjson.md を参照してください。
            "name": ".NET Core Launch (web)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            // ターゲット フレームワークを変更した場合は、プログラム パスを更新するようにしてください。
            "program": "${workspaceFolder}/bin/Debug/net8.0/kestrelcgi.dll",
            "args": [],
            "cwd": "${workspaceFolder}",
            "stopAtEntry": false,
            // ASP.NET Core の起動時に Web ブラウザーの起動を有効にします。詳細については、次を参照してください: https://aka.ms/VSCode-CS-LaunchJson-WebBrowser
            "serverReadyAction": {
                "action": "openExternally",
                "pattern": "\\bNow listening on:\\s+(https?://\\S+)",
                "uriFormat": "%s/cgi/helloMind.cgi"
            },
            "env": {
                "ASPNETCORE_ENVIRONMENT": "Development"
            }
        },
        {
            "name": ".NET Core Attach",
            "type": "coreclr",
            "request": "attach"
        }
    ]
}
```

# 実行開始
VSCodeのデバッグ開始で".NET Core Launch (web)"を選択して実行開始します。ブラウザが立ち上がって下図のようになりました。

![mindcgi.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4e1e3d5c-b196-f15c-273f-68aa738c4b9d.png)

左上に
Content-type: text/html; charset=shift_jis
と出力されているのはMindのCGIが出力する？応答ヘッダのContent-typeがうまく認識できていない？ようで、当初はHTMLのソースが出力されました。

Programs.csに　context.Response.ContentType = "text/html";　を追記することでとりあえずMindCGIの応答コンテンツをHTMLと認識させました。

# おわりに
いかがでしたでしょうか？kestrel serverをC#のコードで構成するのは、本来の目的からはだいぶずれた話となっておりますが、とりあえずMindCGIが動いたのでめでたしめでたしということで。IISでは動かなかったのでその個人的なリベンジの備忘録です。
