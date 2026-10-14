# はじめに
日本語プログラミング言語MindのCGIをkestrelで実行するのステップ３です。

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

前回の状態は[前回の記事](https://qiita.com/mylifewithviolin/items/a26fe29c3c55211e87f4)を参照してください

これをさらに下記のように書き換えます。今回はリクエストからクエリーパラメータを切り出してCGIコマンドの引数に渡すという形に変更されています。

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
        // クエリパラメータを取得して文字列に変換、ない場合は空の引数を使用 
        var queryParams = context.Request.Query 
        .Select(q => $"{q.Key}={q.Value}") 
        .DefaultIfEmpty() // クエリパラメータがない場合にデフォルト値を設定 
        .Aggregate((current, next) =>$"{current}&{next}");
        var scriptFilePath = Path.Combine(scriptsDir, scriptName??"");
        // スクリプトファイルが存在する場合に実行 
        if (File.Exists(scriptFilePath)) {
            var process = new System.Diagnostics.Process
            {
                StartInfo = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = scriptFilePath, // CGIスクリプトのパス
                    Arguments = queryParams??"", // 必要な引数
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
今回はMind9のCGIサンプルをそのまま動かしてみます。
Mind9のインストールフォルダのC:\pmind\cgilib\sampleフォルダから
showvars.cgiをC:\developments\vscode\kestrelcgi\cgiにコピーします。
showvars.mcoをC:\developments\vscode\kestrelcgiにコピーします。
C:\pmind\binからmrunt160.exeをコピー済みです。

# 実行開始
VSCodeのデバッグ開始で".NET Core Launch (web)"を選択して実行開始します。
ブラウザが下記のURLで立ち上がります。

```
http://localhost:5000/cgi/helloMind.cgi
```

これを下記のように打ち直します。
```
http://localhost:5000/cgi/showvars.cgi?name1=value1&name2=value2
```

![mindcgi4.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/0b09af2d-fc53-7733-495f-04cbea0256df.png)

上図のように展開しましたが、パラメータはうまく拾えていないようです。本来は「名前と値のリスト」の下に出力されるはず？

![mindcgi5.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/18108a90-7ba7-2f26-f080-5ce938e82773.png)

パラメータは下記のように引き渡しているようでした。
```
name1=value1&name2=value2
```
MindのCGIがクエリパラメータをどのような形で認識しているかはよくわかっていません。最初は＆の代わりに空白で連結していましたが、それでも認識しなかったので＆にしてみています。


# おわりに
いかがでしたでしょうか？kestrel serverをC#のコードで構成するのは、本来の目的からはだいぶずれた話となっておりますが、MindCGIが動きはじめたのでだいぶうれしいです。IISでは動かせなかったのでその個人的なリベンジの備忘録です。
