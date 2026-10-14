# はじめに
日本語プログラミング言語MindのCGIをkestrelで実行するのステップ５です。C#でkestrelの着信、応答処理を実装する話にもなってきたみたい。今回はスタティックファイルを応答させます。（いままでできてなかったのでした。）

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

生成されているフォルダ構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/dd93f441c4031f16c8a6)を参照してください。Programs.csの初期状態のコードもこちらに記載していましたので割愛しております。

前回までの状態はよろしければ[前回の記事](https://qiita.com/mylifewithviolin/items/dfd3c78846fedad57291)を参照してください

これをさらに下記のように書き換えます。今回は静的ファイルのサポートにオプションでルートフォルダを設定する処理を追加しています。

```cs:Programs.
using Microsoft.Extensions.FileProviders;

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
app.UseStaticFiles(new StaticFileOptions { 
    FileProvider = new PhysicalFileProvider( 
        Path.Combine(Directory.GetCurrentDirectory(), "wwwroot")), 
    RequestPath = ""
});
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

            // クエリパラメータを取得して文字列に変換 
            if (context.Request.Method == "POST") { 
                using (var reader = new StreamReader(context.Request.Body))
                 { var formData = await reader.ReadToEndAsync(); 
                 process.StartInfo.Arguments = formData;
                }
            }
            
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
# wwwrootフォルダをASP.NET MVCプロジェクトからコピー

[こちらの記事](https://qiita.com/mylifewithviolin/items/679eb01b608444e8dec4)で検証しましたASP.NET MVCのプロジェクトからwwwrootフォルダをコピーします。wwwrootフォルダを単純に作成してもよいのですが、jqueryのライブラリとかもあとで使えるかなと。

```cmd:
C:.
│
└─wwwroot
    │  favicon.ico
    ├─css
    │      site.css
    ├─js
    │      site.js
    └─lib
        ├─bootstrap
        │  └─dist
        │      ├─css
        │      └─js
        ├─jquery
        ├─jquery-validation
        └─jquery-validation-unobtrusive

```

# Mind CGIアプリケーションの作成

今回もMind9のCGIサンプルをそのまま動かしてみます。
Mind9のインストールフォルダのC:\pmind\cgilib\sampleフォルダからindex.htmlとhelloweb.htmlをC:\developments\vscode\kestrelcgi\wwwrootフォルダにコピーします。

launch.jsonも修正してindex.htmlを展開するようにします。

```json:launch.json
    "serverReadyAction": {
        "action": "openExternally",
        "pattern": "\\bNow listening on:\\s+(https?://\\S+)",
        "uriFormat": "%s/index.html"
    },
```

# 実行開始
VSCodeのデバッグ開始で".NET Core Launch (web)"を選択して実行開始します。
ブラウザが下記のURLで立ち上がります。

```
http://localhost:5000/index.html
```

下図のような画面が展開します。

![mindcgi9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/315d8343-5a12-c828-4576-8223953e6368.png)

CGIのパスは/cgiとなっていて/index.htmlとは異なる構成となっておりますので、index.htmlを少し修正します。

```html:index.html
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<link rel="stylesheet" href="css/site.css" type="text/css">
<title>MindによるCGIの実験</title>
</head>
<body>
<br>
<h2 align="center">MindによるCGIの実験です</h2>
<br>
<br>
<ul>
<li><a href="helloweb.html"><font color="blue">普通のhtmlドキュメント</font></a></li>
<li><a href="cgi/helloweb.cgi"><font color="blue">CGIで出力するhtmlドキュメント</font></a></li>
<li><a href="cgi/showvars.cgi?name1=value1&name2=value2"><font color="blue">標準CGI変数の確認</font></a></li>
<li><a href="cgi/test-form.cgi"><font color="blue">フォームのテスト</font></a></li>
<li><a href="cgi/test-cookie.cgi"><font color="blue">クッキーのテスト</font></a></li>
<li><a href="testupl.html"><font color="blue">ブラウザ側ファイルをサーバにアップロード</font></a></li>
</ul>
</body>
</html>
```

無事に「CGIで出力するhtmlドキュメント」のリンクからCGIが動作しました。

![mindcgi10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2f026bfe-f57d-bafe-55b3-2bfad29ac56c.png)

# おわりに
いかがでしたでしょうか？kestrel serverをC#のコードで構成するのは、もしかしたらこれもひとつの目的のような気がしてきました。kestrelの挙動とMindCGIの中身をステップバイステップでひも解いてまいります。IISでは動かせなかったのでその個人的なリベンジの備忘録です。
