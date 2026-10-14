# はじめに
日本語プログラミング言語MindのCGIをC#とkestrelで実行するのステップ６です。今回はMind-CGIのContent-Type出力をkestrelに処理させてみました。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 経緯
[ステップ１](https://qiita.com/mylifewithviolin/items/a2e40c9b0afc1b090f9d)ではMindのCGIアプリが\<DocType\>より手前で出力するプレーンテキストのContent-Typeをkestrelが素通りさせてしまい（ソースのままブラウザに展開）とりあえずC#の起動処理でContentTypeを追加して正常展開させました。

[ステップ２](https://qiita.com/mylifewithviolin/items/a26fe29c3c55211e87f4)ではMind開発者の@killyさんのご提案によりMind側の機能でとりあえずプレーンテキストのContent-Typeの出力を抑止して、見た感じ画面にそれがでないようにしておりました。


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

[前回の記事](https://qiita.com/mylifewithviolin/items/1bda7bb279affba9c3b1)のステップ５で[こちらの記事](https://qiita.com/mylifewithviolin/items/679eb01b608444e8dec4)で検証しましたASP.NET MVCのプロジェクトからwwwrootフォルダをコピーしていますので、あらためて全体を図示いたします。

```cmd:
C:\developments\vscode\kestrelcgi
│  .editorconfig
│  appsettings.Development.json
│  appsettings.json
│  helloMind.cgi
│  helloMind.his
│  helloMind.mco
│  helloMind.src
│  helloMind.sym
│  helloweb.mco
│  kestrelcgi.csproj
│  Program.cs
│  showvars.mco
│  test-cookie-submit.mco
│  test-cookie.mco
│  test-form-submit.mco
│  test-form.mco
│  testupl.mco
│
├─.vscode
│      launch.json
│      tasks.json
│
├─bin
│  └─Debug
│      └─net8.0
├─cgi
│      helloMind.cgi
│      helloweb.cgi
│      mrunt160.exe
│      showvars.cgi
│      test-cookie-submit.cgi
│      test-cookie.cgi
│      test-form-submit.cgi
│      test-form.cgi
│      testupl.cgi
│
├─obj
│  └─Debug
│      └─net8.0
│          ├─ref
│          │      kestrelcgi.dll
├─Properties
│      launchSettings.json
└─wwwroot
    │  favicon.ico
    │  helloweb.html
    │  index.html
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
## Programs.cs
Programs.csの初期状態のコードは[こちらの記事](https://qiita.com/mylifewithviolin/items/dd93f441c4031f16c8a6)を、前回までの状態はよろしければ[前回の記事](https://qiita.com/mylifewithviolin/items/1bda7bb279affba9c3b1)を参照してください。

これをさらに下記のように書き換えます。今回はMindのCGIアプリが\<DocType\>より手前で出力するプレーンテキストのContent-Typeをkestrelで処理するコードを追加しています。（１行目に出力されると想定しています。）

```cs:Programs.cs
using System.Text;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);
//Shift-JISのエンコーディングを処理するプロバイダを登録する
Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

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
        var scriptFilePath = Path.Combine(scriptsDir, scriptName??"");

        // クエリパラメータを取得して文字列に変換、ない場合は空の引数を使用 
        var queryParams = context.Request.Query 
        .Select(q => $"{q.Key}={q.Value}") 
        .DefaultIfEmpty() // クエリパラメータがない場合にデフォルト値を設定 
        .Aggregate((current, next) =>$"{current}&{next}");

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
                    CreateNoWindow = true,
                    StandardOutputEncoding = Encoding.GetEncoding("shift-jis")
                }
            };
            // クエリパラメータを取得して文字列に変換 
            if (context.Request.Method == "POST") {
                using var sreader = new StreamReader(context.Request.Body);
                var formData = await sreader.ReadToEndAsync();
                process.StartInfo.Arguments = formData;
            }
            process.Start();
            //レスポンスヘッダにContent-Typeを追加 
            using var reader = process.StandardOutput; 
            var contentTypeLine = await reader.ReadLineAsync(); 
            var contentType = contentTypeLine?.Split(":")[1].Trim(); 
            context.Response.ContentType= contentType;
            //context.Response.ContentType = "text/html;charset=shift_jis";
            //await process.StandardOutput.BaseStream.CopyToAsync(context.Response.Body);
            string? line;
            while ((line = await reader.ReadLineAsync()) != null) 
            { 
                await context.Response.WriteAsync(line, Encoding.GetEncoding("shift-jis")); }
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
従来は下記のように一発でMindCGIの出力を返していたところを
```cs:Programs.cs
await process.StandardOutput.BaseStream.CopyToAsync(context.Response.Body);
```
今回、下記のように出力を行単位でstringに処理させることとなったため、出力時にエンコードを指定しなければならなくなりました。

```cs:Programs.cs
    string? line;
    while ((line = await reader.ReadLineAsync()) != null) 
    { await context.Response.WriteAsync(line, Encoding.GetEncoding("shift-jis")); }
```

ですので、今回の状態ではMindCGIのコンテンツタイプの文字コードオプションがSJIS以外を指定しても対応しておりません:sweat_smile:


# Mind CGIアプリケーションの作成

今回もMind9のCGIサンプルをそのまま動かしてみます。
「CGIで出力するhtmlドキュメント」helloweb.cgi

# 実行開始
VSCodeのデバッグ開始で".NET Core Launch (web)"を選択して実行開始します。
ブラウザが下記のURLで立ち上がります。

```
http://localhost:5000/index.html
```
「MindによるCGIの実験」のリンクメニューが立ち上がりますので、「CGIで出力するhtmlドキュメント」リンクをクリックします。

下図の画面が無事に展開しました。

![mindcgi11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5bc8fc8f-8df4-4a18-5101-abe6ed90c1bc.png)

前回の状態ではコンテンツタイプのプレーンテキストが出力されていましたが、今回のはレスポンスヘッダ部分として切り取られ、画面からは消えていますね。

![mindcgi10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/2f026bfe-f57d-bafe-55b3-2bfad29ac56c.png)

参考に、ステップ２でMindCGI側のコンテンツタイプの出力を抑止した下記のhelloMind.cgiを実行しますと

```
http://localhost:5000/cgi/helloMind.cgi
```

今回のコードでは逆にコンテンツタイプの出力行がない場合を想定していないので、下図のように内部エラーとなってしまいます:joy:

![mindcgi12.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9f2b664f-148f-e289-8673-7952451a2561.png)

また、MindCGIの出力を行単位で処理したので、改行コードが欠落したみたいで、プレーンテキスト出力の改行が消失しました:joy::joy:

![mindcgi13.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6f2ab776-6362-2f45-fc54-5f1dcd772e42.png)

これは下記の行出力時に改行を復元しました。

```cs:Programs.cs
    string? line;
    while ((line = await reader.ReadLineAsync()) != null) 
    { await context.Response.WriteAsync(line + "\n", Encoding.GetEncoding("shift-jis")); }
```
先頭行にコンテンツタイプがない場合に内部エラーとなる件は下記のようにいったん逃げます。（途中、どの行でもコンテンツタイプと文字列合致すると応答してしまう問題あり。また大文字小文字不一致もとりあえずパス:sweat_smile:）

```cs:Programs.cs
        process.Start();
        //レスポンスヘッダにContent-Typeを追加 
        using var reader = process.StandardOutput; 
        string? line;
        while ((line = await reader.ReadLineAsync()) != null) 
        { 
            var contentType = (line?.StartsWith("Content-type:")?? false) ? line.Split(":")[1].Trim() :null; 
            if(contentType != null){
                context.Response.ContentType= contentType;
            }else{
                await context.Response.WriteAsync(line + "\n", Encoding.GetEncoding("shift-jis")); 
            }
        }
        await process.WaitForExitAsync();
```


# おわりに
いかがでしたでしょうか？普段コントローラアプリのバックエンドとして何気につかっていたkestrel serverですが、すっぴんの状態から構成するのはけっこうたいへんなんですね。MindCGIのステップとしては足踏み状態ですがステップバイステップでひも解いてまいります。IISでは動かせなかったのでその個人的なリベンジの備忘録です。
