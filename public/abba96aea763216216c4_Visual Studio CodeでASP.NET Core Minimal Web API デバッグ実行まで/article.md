# はじめに

ASP.NET Core Web API（非コントローラ最小ベース）アプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.86.1
C# 12 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# ASP.NET Web API環境の構成
最初にASP.NET Web API（最小） のプロジェクトを作成してVSCodeを起動します。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。（dotnetバージョンチェックは念のための事前動作確認です。）

```
C:\developments\vscode>dotnet --version
8.0.206

C:\developments\vscode>dotnet new webapi -o aspnetapi
テンプレート "ASP.NET Core Web API" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\aspnetapi\aspnetapi.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\aspnetapi\aspnetapi.csproj を復元しました (5.43 秒)。
正常に復元されました。


C:\developments\vscode>cd aspnetapi
C:\developments\vscode\aspnetapi>code .
```

最後の「code .」でVSCodeがプロジェクトフォルダをカレントフォルダとして起動します。
VSCodeが起動してからそのまましばらく（１分以上）待つとVSCodeのウィンドウ内右下に下記のメッセージが表示されます。その場合は通常「はい」を選択します。
「ビルドおよびデバッグに必要な資産が'aspnetapi'にありません。追加しますか？」

下記のようなフォルダ構成でプロジェクトが生成され、最小APIのサンプルソースはProgram.csに生成されます。（上記のメッセージで「はい」を選択しない場合、.vscodeフォルダは生成されていません。）

```cmd:
C:.
│  appsettings.Development.json
│  appsettings.json
│  aspnetapi.csproj
│  aspnetapi.http
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
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\aspnetapi/aspnetapi.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  aspnetapi -> C:\developments\vscode\aspnetapi\bin\Debug\net8.0\aspnetapi.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 

```

デバッグコンソールに下記のような起動結果が表示されます。

```
warn: Microsoft.AspNetCore.Server.Kestrel.Core.KestrelServer[8]
      The ASP.NET Core developer certificate is not trusted. For information about trusting the ASP.NET Core developer certificate, see https://aka.ms/aspnet/https-trust-dev-cert.
Microsoft.AspNetCore.Server.Kestrel.Core.KestrelServer: Warning: The ASP.NET Core developer certificate is not trusted. For information about trusting the ASP.NET Core developer certificate, see https://aka.ms/aspnet/https-trust-dev-cert.
aspnetapi.dll (7524): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Net.Security.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7299
Microsoft.Hosting.Lifetime: Information: Now listening on: https://localhost:7299
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5042
Microsoft.Hosting.Lifetime: Information: Now listening on: http://localhost:5042
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
Microsoft.Hosting.Lifetime: Information: Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
Microsoft.Hosting.Lifetime: Information: Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: C:\developments\vscode\aspnetapi
Microsoft.Hosting.Lifetime: Information: Content root path: C:\developments\vscode\aspnetapi
aspnetapi.dll (7524): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Security.Principal.Windows.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetapi.dll (7524): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Security.Claims.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。

```

ブラウザが起動して、証明書がないことの警告を通過させると（このあたりはhttpsでローンチされているせいですが、この辺りの構成調整はまた別の機会にゆずります。）ルートで応答するコントローラの実装がなにもないため、とりあえず
このページは現在機能していません
localhost からデータは送信されませんでした。
というエラーがブラウザに表示されます。

ポート番号5042の方はswaggerが起動していますので
```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5042
```

下記のようにブラウザのURLを変更するとswaggerのインデックスページが展開します。
```
http://localhost:5042/swagger/index.html
```

weatherforecastというGETコマンドのAPIが存在していることがわかります。


```cs:Programs.cs
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast")
.WithOpenApi();

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}

```

Programs.csの public int TemperatureFのラムダ式のあたりにブレークポイントを設定して、ブラウザで下記のURLを打ち込みます。HTTPでは着信しないのでとりあえずHTTPSのままとするのがポイントのようです。

```
https://localhost:7299/weatherforecast
```

証明書の警告を無視して進めますと設定したブレークポイントにブレークします。それを続行すると下記のような応答が返ります。
```
[
    {
        "date": "2024-10-15",
        "temperatureC": 2,
        "summary": "Sweltering",
        "temperatureF": 35
    },
    {
        "date": "2024-10-16",
        "temperatureC": 25,
        "summary": "Hot",
        "temperatureF": 76
    },
    {
        "date": "2024-10-17",
        "temperatureC": 24,
        "summary": "Sweltering",
        "temperatureF": 75
    },
    {
        "date": "2024-10-18",
        "temperatureC": 25,
        "summary": "Bracing",
        "temperatureF": 76
    },
    {
        "date": "2024-10-19",
        "temperatureC": 52,
        "summary": "Balmy",
        "temperatureF": 125
    }
]
```

# おわりに
いかがでしたでしょうか？ラムダ式でAPIが記述できるというのは少し驚きです。デバッグはしづらいような気がしなくもないです。
