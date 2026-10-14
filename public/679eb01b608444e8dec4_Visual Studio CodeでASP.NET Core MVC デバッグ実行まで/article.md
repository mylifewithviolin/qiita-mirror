# はじめに

ASP.NET Core MVCアプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.86.1
C# 12 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# ASP.NET MVC環境の構成
最初にASP.NET MVCのプロジェクトを作成してVSCodeを起動します。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。

```
C:\developments\vscode>dotnet --version
8.0.204

C:\developments\vscode>dotnet new mvc -o aspnetmvc
テンプレート "ASP.NET Core Web アプリ (Model-View-Controller)" が正常に作成されました。
このテンプレートには、Microsoft 以外のパーティのテクノロジーが含まれています。詳しくは、https://aka.ms/aspnetcore/8.0-third-party-notices をご覧ください。

作成後の操作を処理しています...
C:\developments\vscode\aspnetmvc\aspnetmvc.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\aspnetmvc\aspnetmvc.csproj を復元しました (138 ミリ秒)。
正常に復元されました。

C:\developments\vscode>cd aspnetmvc
C:\developments\vscode\aspnetmvc>code .
```

最後の「code .」でVSCodeがプロジェクトフォルダをカレントフォルダとして起動します。

下記のようなフォルダ構成でコントローラとモデルとビューのサンプルソースが生成されています。
```cmd:
C:.
│  appsettings.Development.json
│  appsettings.json
│  aspnetmvc.csproj
│  Program.cs
│
├─bin
│  └─Debug
│      └─net8.0
├─Controllers
│      HomeController.cs
├─Models
│      ErrorViewModel.cs
├─obj
│  └─Debug
│      └─net8.0
│          ├─ref
│          └─refint
├─Properties
│      launchSettings.json
│
├─Views
│  │  _ViewImports.cshtml
│  │  _ViewStart.cshtml
│  │
│  ├─Home
│  │      Index.cshtml
│  │      Privacy.cshtml
│  │
│  └─Shared
│          Error.cshtml
│          _Layout.cshtml
│          _Layout.cshtml.css
│          _ValidationScriptsPartial.cshtml
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


## デバッグ実行開始
VSCodeが起動すると右下に下記のメッセージが表示された場合はかならず「はい」を選択します。
「ビルドおよびデバッグに必要な資産がaspnetmvcありません。追加しますか？」

プロジェクトフォルダに.vscodeフォルダが作成され、デバッグ実行に必要なtasks.jsonとlaunch.jsonを構成作成してくれます。
```cmd:
C:.
│   appsettings.Development.json
│   appsettings.json
│   aspnetmvc.csproj
│   Program.cs
│
├───.vscode
│       launch.json
│       tasks.json
```

VSCodeの実行とデバッグに「.NET Core Launch (web)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され
```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\aspnetmvc/aspnetmvc.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  aspnetmvc -> C:\developments\vscode\aspnetmvc\bin\Debug\net8.0\aspnetmvc.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 

```

デバッグコンソールに下記のような起動結果が表示されます。

```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7278
Microsoft.Hosting.Lifetime: Information: Now listening on: https://localhost:7278
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5226
Microsoft.Hosting.Lifetime: Information: Now listening on: http://localhost:5226
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
Microsoft.Hosting.Lifetime: Information: Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
Microsoft.Hosting.Lifetime: Information: Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: C:\developments\vscode\aspnetmvc
Microsoft.Hosting.Lifetime: Information: Content root path: C:\developments\vscode\aspnetmvc

aspnetmvc.dll (17300): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Threading.Channels.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetmvc.dll (17300): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Net.WebSockets.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetmvc.dll (17300): 'Anonymously Hosted DynamicMethods Assembly' が読み込まれました。
aspnetmvc.dll (17300): 'C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App\8.0.6\Microsoft.AspNetCore.WebUtilities.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
aspnetmvc.dll (17300): 'C:\Program Files\dotnet\shared\Microsoft.NETCore.App\8.0.6\System.Net.Http.dll' が読み込まれました。シンボルの読み込みをスキップしました。モジュールは最適化されていて、デバッグ オプションの [マイ コードのみ] 設定が有効になっています。
```

ブラウザが起動して、証明書がないことの警告を通過させればサンプルコントローラのWebページが展開します。（このあたりはhttpsでローンチされているせいですが、この辺りの構成調整はまた別の機会にゆずります。）

下記のHomeControllerのソースのreturn View();の行にブレークポイントを置いて、ブラウザのURLでENTERを押すと無事にブレークすることがわかります。

```cs:HomeController.cs
namespace aspnetmvc.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;

    public HomeController(ILogger<HomeController> logger)
    {
        _logger = logger;
    }

    public IActionResult Index()
    {
        return View();
    }

```

# おわりに
いかがでしたでしょうか？けっこう簡単で助かりました。
