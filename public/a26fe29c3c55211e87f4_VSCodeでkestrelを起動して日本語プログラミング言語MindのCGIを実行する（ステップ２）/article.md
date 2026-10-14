# はじめに
前回のタイトルは長かったので少しつめてみました。日本語プログラミング言語MindのCGIをkestrelで実行するのステップ２です。


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

生成されているフォルダ構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/dd93f441c4031f16c8a6)を参照してください。プロジェクト名がkestrelからkestrelcgiに変わっただけです。

Programs.csには当初下記のコードが記述されています。

```cs:Programs.cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();

```

前回の状態は[前回の記事](https://qiita.com/mylifewithviolin/items/a2e40c9b0afc1b090f9d)を参照してください

これをさらに下記のように書き換えます。前回は実行できるcgiファイル名が固定でしたが、今回はリクエストから切り出したファイルがフォルダに存在したら実行するという形に変更されています。

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
app.Use(static async (context, next) =>
{
    if (context.Request.Path.StartsWithSegments("/cgi", out var remainingPath))
    {
        // 残りのパスからスクリプト名を取得 
        var scriptName = remainingPath.Value?.TrimStart('/'); 
        var scriptsDir = Path.Combine(Directory.GetCurrentDirectory(), "cgi"); 
        var scriptFilePath = Path.Combine(scriptsDir, scriptName??"");
        // スクリプトファイルが存在する場合に実行 
        if (File.Exists(scriptFilePath)) {
            var process = new System.Diagnostics.Process
            {
                StartInfo = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = scriptFilePath, // CGIスクリプトのパス
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
        {   context.Response.StatusCode = 404; 
            await context.Response.WriteAsync("CGI script not found");;
        }
    }
    else
    {
        await next.Invoke();
    }
});

app.Run();
```

# Mind CGIアプリケーションの作成

前回の記事へのMind開発者の@killyさんからのアドバイスによりサンプルコードを下記のように修正します。

```Mind:hellMind.src
メインは
	ヘッダ出力済み・ｍｉｍｅヘッダを　ｈｔｍｌヘッダ出力済みに　入れ
	「ＭｉｎｄによるＣＧＩのテスト」で、HTMLヘッダ出力し
	「こんにちは、Ｍｉｎｄ！」を、大きく表示すること。
```

VSCodeのターミナルでコマンドプロンプトを開いて、Mindでビルドします。
```
C:\developments\vscode\kestrelcgi>mind helloMind c:\pmind\lib\cgilib

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\pmind\bin\mindexcgi.exe --> helloMind.cgi

C:\developments\vscode\kestrelcgi>
```

生成されたhelloMind.cgiをC:\developments\vscode\kestrelcgi\cgiにコピーします。
C:\pmind\binからmrunt160.exeを前回コピー済みです。

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

# 実行開始
VSCodeのデバッグ開始で".NET Core Launch (web)"を選択して実行開始します。ブラウザが立ち上がって下図のようになりました。

![mindcgi3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d3c22350-b89f-3870-fec9-7ebeaa073330.png)

左上に
Content-type: text/html; charset=shift_jis
と出力されていたのは無事に抑止されました。

# おわりに
いかがでしたでしょうか？kestrel serverをC#のコードで構成するのは、本来の目的からはだいぶずれた話となっておりますが、MindCGIが動きはじめたのでだいぶうれしいです。IISでは動かなかったのでその個人的なリベンジの備忘録です。
