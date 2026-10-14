# はじめに

ASP.NET Core Web API（コントローラベース）アプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。

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
最初にASP.NET Web API（コントローラベース） のプロジェクトを作成してVSCodeを起動します。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。（dotnetバージョンチェックは念のための事前動作確認です。）
ポイントは　--use-controllers　というオプションで、これがない場合のnew webapiコマンドは最小構成WebAPIとなります。

```
C:\developments\vscode>dotnet --version
8.0.206

C:\developments\vscode>dotnet new webapi --use-controllers -o aspnetapic
テンプレート "ASP.NET Core Web API" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\aspnetapic\aspnetapic.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\aspnetapic\aspnetapic.csproj を復元しました (734 ミリ秒)。
正常に復元されました。

C:\developments\vscode>cd aspnetapic
C:\developments\vscode\aspnetapic>code .
```

最後の「code .」でVSCodeがプロジェクトフォルダをカレントフォルダとして起動します。
VSCodeが起動してからそのまましばらく（１分以上）待つとVSCodeのウィンドウ内右下に下記のメッセージが表示されます。通常「はい」を選択します。

「ビルドおよびデバッグに必要な資産が'aspnetapic'にありません。追加しますか？」

このときVSCodeのウィンドウのどこかをクリックしてしまうなどして、対処する前にこのメッセージが消失したとしても、VSCodeウィンドウ最下のステータスバーのようなところの右端にベルマークがあり、そこをクリックすると再表示されます。

下記のようなフォルダ構成でプロジェクトが生成され、コントローラのサンプルソースはControllers\WeatherForecastController.csに生成されます。（上記のメッセージで「はい」を選択しない場合、.vscodeフォルダは生成されていません。）

```cmd:
C:.
│  appsettings.Development.json
│  appsettings.json
│  aspnetapic.csproj
│  aspnetapic.http
│  Program.cs
│  WeatherForecast.cs
│
├─.vscode
│      launch.json
│      tasks.json
│
├─bin
│  └─Debug
│      └─net8.0
├─Controllers
│      WeatherForecastController.cs
│
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
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\aspnetapic/aspnetapic.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  aspnetapic -> C:\developments\vscode\aspnetapic\bin\Debug\net8.0\aspnetapic.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

デバッグコンソールに下記のような起動結果が表示されます。

```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7089
Microsoft.Hosting.Lifetime: Information: Now listening on: https://localhost:7089
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5228
Microsoft.Hosting.Lifetime: Information: Now listening on: http://localhost:5228
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
Microsoft.Hosting.Lifetime: Information: Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
Microsoft.Hosting.Lifetime: Information: Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: C:\developments\vscode\aspnetapic
Microsoft.Hosting.Lifetime: Information: Content root path: C:\developments\vscode\aspnetapic
aspnetapic.dll (5196): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Security.Principal.Windows.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetapic.dll (5196): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Threading.Channels.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetapic.dll (5196): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Net.WebSockets.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetapic.dll (5196): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Text.RegularExpressions.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetapic.dll (5196): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Net.Http.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。


```

ブラウザが起動して、証明書がないことの警告を通過させると（このあたりはhttpsでローンチされているせいですが、この辺りの構成調整はまた別の機会にゆずります。）ルートで応答するコントローラの実装がなにもないため、とりあえず
```
この localhost ページが見つかりません
Web アドレスに対応する Web ページが見つかりませんでした: https://localhost:7089/
```
というエラーがブラウザに表示されます。

ポート番号5228の方はswaggerが起動していますので
```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5228
```

下記のようにブラウザのURLを変更するとswaggerのインデックスページが展開します。
```
http://localhost:5228/swagger/index.html
```

weatherforecastというGETコマンドのAPIが存在していることがわかります。

※これまでの手順で生成されたswaggerのインデクスですと、リクエスト先が
```
http://localhost:5228/WeatherForecast
```

となってしまっているようで、ブラウザUIのswagger画面上の「try it out」から「Execute」しても
```
Failed to fetch.
```
という応答が返ります。swaggerUIの実行をいったんあきらめて、ブラウザのアドレスを

```
https://localhost:7089/WeatherForecast
```
とすると下記のような応答が返ります。
```
[
    {
        "date": "2024-10-20",
        "temperatureC": 28,
        "temperatureF": 82,
        "summary": "Bracing"
    },
    {
        "date": "2024-10-21",
        "temperatureC": 7,
        "temperatureF": 44,
        "summary": "Mild"
    },
    {
        "date": "2024-10-22",
        "temperatureC": -12,
        "temperatureF": 11,
        "summary": "Bracing"
    },
    {
        "date": "2024-10-23",
        "temperatureC": 48,
        "temperatureF": 118,
        "summary": "Cool"
    },
    {
        "date": "2024-10-24",
        "temperatureC": 50,
        "temperatureF": 121,
        "summary": "Scorching"
    }
]
```

WeatherForecastController.csの    public IEnumerable<WeatherForecast> Get()のreturn Enumerable.Range(1, 5)のあたりにブレークポイントを設定して、ブラウザで前記のURLを打ち込みます。

```cs:WeatherForecastController.cs
using Microsoft.AspNetCore.Mvc;

namespace aspnetapic.Controllers;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<WeatherForecastController> _logger;

    public WeatherForecastController(ILogger<WeatherForecastController> logger)
    {
        _logger = logger;
    }

    [HttpGet(Name = "GetWeatherForecast")]
    public IEnumerable<WeatherForecast> Get()
    {
        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        })
        .ToArray();
    }
}
```

すると設定したブレークポイントにブレークします。それを続行すると５回ブレークを繰り返して前記の応答がブラウザに返ります。

# おわりに
いかがでしたでしょうか？最小構成WebApiに比べると記述量が多いですが、なにをやっているかはこちらのがわかりやすい感じ。処理している内容はいっしょっぽいですが、コードの隠れ具合がこちらの方が隠れなさすぎというあくまでわたしの感想です。
