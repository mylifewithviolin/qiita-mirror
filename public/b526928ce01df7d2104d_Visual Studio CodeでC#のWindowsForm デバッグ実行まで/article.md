# はじめに

C#のWindowsFormアプリケーションプロジェクトをVisual Studio Codeでデバッグ実行開始できるようにするまでの備忘録です。

VSCodeや.NETCore、C#とそのVSCodeエクステンションはコンソールアプリケーションがデバッグ実行できる程度には用意されていることを前提とします。

# 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.86.1
C# 12 
dotnet-sdk-8.0.206-win-x64

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# C# Windowsフォームアプリケーションプロジェクトの作成
## 大まかな流れ

最初に.NET コンソールアプリケーションプロジェクトの作成し
>dotnet new console -n WinFormsApp

そのプロジェクトにWindowsフォームアセットを追加し
>dotnet add package System.Windows.Forms
dotnet add package Microsoft.Windows.Compatibility

プロジェクトファイルやVSCodeアセットをハンドで修正
という流れとなります。

## .NET コンソールアプリケーションプロジェクトの作成

まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。
```
C:\developments\vscode>dotnet --version
8.0.204

C:\developments\vscode>dotnet new console -n WinFormsApp
テンプレート "コンソール アプリ" が正常に作成されました。

作成後の操作を処理しています...
C:\developments\vscode\WinFormsApp\WinFormsApp.csproj を復元しています:
  Determining projects to restore...
  C:\developments\vscode\WinFormsApp\WinFormsApp.csproj を復元しました (148 ミリ秒)。
正常に復元されました。
```
## プロジェクトにWindowsフォームアセットを追加
カレントディレクトリをプロジェクトフォルダへ移動します。

```
C:\developments\vscode>cd WinFormsApp
```
```
C:\developments\vscode\WinFormsApp>dotnet add package System.Windows.Forms
  Determining projects to restore...
  Writing C:\Users\mylifewithviolin\AppData\Local\Temp\tmpnievio.tmp
info : X.509 証明書チェーンの検証では、コード署名のために .NET によって選択された既定の信頼ストアが使用されます。
info : X.509 証明書チェーンの検証では、タイムスタンプに .NET によって選択された既定の信頼ストアが使用されます。
info : Adding PackageReference for package 'System.Windows.Forms' into project 'C:\developments\vscode\WinFormsApp\WinFormsApp.csproj'.
info :   GET https://api.nuget.org/v3/registration5-gz-semver2/system.windows.forms/index.json
info :   OK https://api.nuget.org/v3/registration5-gz-semver2/system.windows.forms/index.json 537 ミリ秒
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/system.windows.forms/index.json
error: There are no versions available for the package 'System.Windows.Forms'.


Usage: NuGet.CommandLine.XPlat.dll package add [options]

Options:
  -h|--help               Show help information
  --force-english-output  Forces the application to run using an invariant, English-based culture.
  --package               Id of the package to be added.
  --version               Version of the package to be added.
  -d|--dg-file            Path to the dependency graph file to be used to restore preview and compatibility check.
  -p|--project            Path to the project file.
  -f|--framework          Frameworks for which the package reference should be added.
  -n|--no-restore         Do not perform restore preview and compatibility check. The added package reference will be unconditional.
  -s|--source             Specifies NuGet package sources to use during the restore.
  --package-directory     Directory to restore packages in.
  --interactive           Allow the command to block and require manual action for operations like authentication.
  --prerelease            Allows prerelease packages to be installed.
```
エラーが出ますが、次のコマンドも実行します。

```
C:\developments\vscode\WinFormsApp>dotnet add package Microsoft.Windows.Compatibility
  Determining projects to restore...
  Writing C:\Users\mylifewithviolin\AppData\Local\Temp\tmptedjn4.tmp
info : X.509 証明書チェーンの検証では、コード署名のために .NET によって選択された既定の信頼ストアが使用されます。
info : X.509 証明書チェーンの検証では、タイムスタンプに .NET によって選択された既定の信頼ストアが使用されます。
info : Adding PackageReference for package 'Microsoft.Windows.Compatibility' into project 'C:\developments\vscode\WinFormsApp\WinFormsApp.csproj'.
info :   GET https://api.nuget.org/v3/registration5-gz-semver2/microsoft.windows.compatibility/index.json
info :   OK https://api.nuget.org/v3/registration5-gz-semver2/microsoft.windows.compatibility/index.json 762 ミリ秒
info : C:\developments\vscode\WinFormsApp\WinFormsApp.csproj のパッケージを復元しています...
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.windows.compatibility/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.windows.compatibility/index.json 183 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.windows.compatibility/9.0.1/microsoft.windows.compatibility.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.windows.compatibility/9.0.1/microsoft.windows.compatibility.9.0.1.nupkg 200 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.win32.registry.accesscontrol/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.win32.systemevents/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.codedom/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition.registration/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.configuration.configurationmanager/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.data.odbc/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.data.oledb/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.diagnostics.eventlog/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.diagnostics.performancecounter/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices.accountmanagement/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices.protocols/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.drawing.common/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.io.packaging/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.management/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.reflection.context/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.runtime.caching/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.pkcs/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.protecteddata/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.xml/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.permissions/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/system.configuration.configurationmanager/index.json 235 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.data.oledb/index.json 245 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.servicemodel.syndication/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.configuration.configurationmanager/9.0.1/system.configuration.configurationmanager.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.serviceprocess.servicecontroller/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.data.oledb/9.0.1/system.data.oledb.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.speech/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.text.encoding.codepages/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/system.threading.accesscontrol/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/system.diagnostics.eventlog/index.json 232 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.diagnostics.eventlog/9.0.1/system.diagnostics.eventlog.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.data.oledb/9.0.1/system.data.oledb.9.0.1.nupkg 92 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.configuration.configurationmanager/9.0.1/system.configuration.configurationmanager.9.0.1.nupkg 132 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices.protocols/index.json 383 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices.protocols/9.0.1/system.directoryservices.protocols.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.serviceprocess.servicecontroller/index.json 276 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.win32.systemevents/index.json 629 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.win32.registry.accesscontrol/index.json 635 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.win32.systemevents/9.0.1/microsoft.win32.systemevents.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.serviceprocess.servicecontroller/9.0.1/system.serviceprocess.servicecontroller.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.win32.registry.accesscontrol/9.0.1/microsoft.win32.registry.accesscontrol.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.text.encoding.codepages/index.json 306 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.text.encoding.codepages/9.0.1/system.text.encoding.codepages.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition/index.json 683 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition.registration/index.json 684 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition/9.0.1/system.componentmodel.composition.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.codedom/index.json 696 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition.registration/9.0.1/system.componentmodel.composition.registration.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.codedom/9.0.1/system.codedom.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.diagnostics.eventlog/9.0.1/system.diagnostics.eventlog.9.0.1.nupkg 343 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.win32.systemevents/9.0.1/microsoft.win32.systemevents.9.0.1.nupkg 84 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.text.encoding.codepages/9.0.1/system.text.encoding.codepages.9.0.1.nupkg 80 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices.protocols/9.0.1/system.directoryservices.protocols.9.0.1.nupkg 211 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.io.ports/index.json 616 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.serviceprocess.servicecontroller/9.0.1/system.serviceprocess.servicecontroller.9.0.1.nupkg 137 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.data.odbc/index.json 724 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.io.ports/9.0.1/system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices.accountmanagement/index.json 650 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.data.odbc/9.0.1/system.data.odbc.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.management/index.json 624 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices.accountmanagement/9.0.1/system.directoryservices.accountmanagement.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.management/9.0.1/system.management.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.diagnostics.performancecounter/index.json 698 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.codedom/9.0.1/system.codedom.9.0.1.nupkg 125 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.diagnostics.performancecounter/9.0.1/system.diagnostics.performancecounter.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices/index.json 719 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.drawing.common/index.json 707 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.io.packaging/index.json 711 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.directoryservices/9.0.1/system.directoryservices.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.drawing.common/9.0.1/system.drawing.common.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.io.packaging/9.0.1/system.io.packaging.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.reflection.context/index.json 743 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.data.odbc/9.0.1/system.data.odbc.9.0.1.nupkg 129 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices.accountmanagement/9.0.1/system.directoryservices.accountmanagement.9.0.1.nupkg 138 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.reflection.context/9.0.1/system.reflection.context.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.management/9.0.1/system.management.9.0.1.nupkg 136 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.pkcs/index.json 760 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.io.ports/9.0.1/system.io.ports.9.0.1.nupkg 171 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.servicemodel.syndication/index.json 654 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.runtime.caching/index.json 783 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.xml/index.json 754 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.permissions/index.json 750 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.pkcs/9.0.1/system.security.cryptography.pkcs.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.runtime.caching/9.0.1/system.runtime.caching.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.xml/9.0.1/system.security.cryptography.xml.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.permissions/9.0.1/system.security.permissions.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.servicemodel.syndication/9.0.1/system.servicemodel.syndication.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.threading.accesscontrol/index.json 666 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.threading.accesscontrol/9.0.1/system.threading.accesscontrol.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.drawing.common/9.0.1/system.drawing.common.9.0.1.nupkg 157 ミ リ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.directoryservices/9.0.1/system.directoryservices.9.0.1.nupkg 173 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.io.packaging/9.0.1/system.io.packaging.9.0.1.nupkg 216 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.speech/index.json 784 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.speech/9.0.1/system.speech.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.xml/9.0.1/system.security.cryptography.xml.9.0.1.nupkg 206 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.pkcs/9.0.1/system.security.cryptography.pkcs.9.0.1.nupkg 243 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.runtime.caching/9.0.1/system.runtime.caching.9.0.1.nupkg 265  ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.permissions/9.0.1/system.security.permissions.9.0.1.nupkg 277 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.speech/9.0.1/system.speech.9.0.1.nupkg 305 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition.registration/9.0.1/system.componentmodel.composition.registration.9.0.1.nupkg 774 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.native.system.io.ports/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/system.componentmodel.composition/9.0.1/system.componentmodel.composition.9.0.1.nupkg 932 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.bcl.cryptography/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/system.reflection.context/9.0.1/system.reflection.context.9.0.1.nupkg 824 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.diagnostics.performancecounter/9.0.1/system.diagnostics.performancecounter.9.0.1.nupkg 921 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.servicemodel.syndication/9.0.1/system.servicemodel.syndication.9.0.1.nupkg 820 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.protecteddata/index.json 1642 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.native.system.io.ports/index.json 343 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.security.cryptography.protecteddata/9.0.1/system.security.cryptography.protecteddata.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.native.system.io.ports/9.0.1/runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.threading.accesscontrol/9.0.1/system.threading.accesscontrol.9.0.1.nupkg 877 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.security.cryptography.protecteddata/9.0.1/system.security.cryptography.protecteddata.9.0.1.nupkg 244 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.native.system.io.ports/9.0.1/runtime.native.system.io.ports.9.0.1.nupkg 249 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.windows.extensions/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.bcl.cryptography/index.json 422 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/microsoft.bcl.cryptography/9.0.1/microsoft.bcl.cryptography.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-arm.runtime.native.system.io.ports/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.win32.registry.accesscontrol/9.0.1/microsoft.win32.registry.accesscontrol.9.0.1.nupkg 1550 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-x64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-x86.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-arm.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-x64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-x64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-x64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-x64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.osx-arm64.runtime.native.system.io.ports/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.osx-x64.runtime.native.system.io.ports/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/microsoft.bcl.cryptography/9.0.1/microsoft.bcl.cryptography.9.0.1.nupkg 145 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/system.windows.extensions/index.json 310 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.windows.extensions/9.0.1/system.windows.extensions.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-arm.runtime.native.system.io.ports/index.json 311 ミ リ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-x86.runtime.native.system.io.ports/index.json 305 ミ リ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-x64.runtime.native.system.io.ports/index.json 284 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-arm64.runtime.native.system.io.ports/index.json 313  ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-arm64.runtime.native.system.io.ports/index.json 292 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm64.runtime.native.system.io.ports/index.json 277 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-x64.runtime.native.system.io.ports/index.json 319 ミ リ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-arm.runtime.native.system.io.ports/9.0.1/runtime.android-arm.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/system.formats.asn1/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-bionic-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-bionic-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-x86.runtime.native.system.io.ports/9.0.1/runtime.android-x86.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-x64.runtime.native.system.io.ports/9.0.1/runtime.android-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.android-arm64.runtime.native.system.io.ports/9.0.1/runtime.android-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-x64.runtime.native.system.io.ports/index.json 345 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.osx-x64.runtime.native.system.io.ports/index.json 320 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-arm64.runtime.native.system.io.ports/index.json 346 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-x64.runtime.native.system.io.ports/index.json 355 ミリ 秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.osx-x64.runtime.native.system.io.ports/9.0.1/runtime.osx-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.windows.extensions/9.0.1/system.windows.extensions.9.0.1.nupkg 113 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-arm64.runtime.native.system.io.ports/9.0.1/runtime.maccatalyst-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-arm.runtime.native.system.io.ports/9.0.1/runtime.android-arm.runtime.native.system.io.ports.9.0.1.nupkg 85 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-x64.runtime.native.system.io.ports/9.0.1/runtime.android-x64.runtime.native.system.io.ports.9.0.1.nupkg 96 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-x64.runtime.native.system.io.ports.9.0.1.nupkg 62 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-bionic-x64.runtime.native.system.io.ports.9.0.1.nupkg 112 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-bionic-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-bionic-arm64.runtime.native.system.io.ports.9.0.1.nupkg 116 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-arm64.runtime.native.system.io.ports/9.0.1/runtime.maccatalyst-arm64.runtime.native.system.io.ports.9.0.1.nupkg 99 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-arm64.runtime.native.system.io.ports.9.0.1.nupkg 128 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-arm64.runtime.native.system.io.ports/9.0.1/runtime.android-arm64.runtime.native.system.io.ports.9.0.1.nupkg 139 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.android-x86.runtime.native.system.io.ports/9.0.1/runtime.android-x86.runtime.native.system.io.ports.9.0.1.nupkg 156 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.osx-x64.runtime.native.system.io.ports/9.0.1/runtime.osx-x64.runtime.native.system.io.ports.9.0.1.nupkg 174 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-x64.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-x64.runtime.native.system.io.ports.9.0.1.nupkg 178 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-arm.runtime.native.system.io.ports/index.json 608 ミリ 秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm.runtime.native.system.io.ports/index.json 596 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-arm64.runtime.native.system.io.ports/index.json 617 ミ リ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-arm.runtime.native.system.io.ports/9.0.1/runtime.linux-arm.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-arm.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.osx-arm64.runtime.native.system.io.ports/index.json 585 ミリ 秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.linux-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.osx-arm64.runtime.native.system.io.ports/9.0.1/runtime.osx-arm64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.formats.asn1/index.json 289 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/system.formats.asn1/9.0.1/system.formats.asn1.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-x64.runtime.native.system.io.ports/index.json 622 ミリ秒
info :   GET https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-x64.runtime.native.system.io.ports/9.0.1/runtime.maccatalyst-x64.runtime.native.system.io.ports.9.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/system.formats.asn1/9.0.1/system.formats.asn1.9.0.1.nupkg 36 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-arm.runtime.native.system.io.ports/9.0.1/runtime.linux-arm.runtime.native.system.io.ports.9.0.1.nupkg 102 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.maccatalyst-x64.runtime.native.system.io.ports/9.0.1/runtime.maccatalyst-x64.runtime.native.system.io.ports.9.0.1.nupkg 62 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-arm64.runtime.native.system.io.ports/9.0.1/runtime.linux-arm64.runtime.native.system.io.ports.9.0.1.nupkg 111 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.linux-musl-arm.runtime.native.system.io.ports/9.0.1/runtime.linux-musl-arm.runtime.native.system.io.ports.9.0.1.nupkg 115 ミリ秒
info :   OK https://api.nuget.org/v3-flatcontainer/runtime.osx-arm64.runtime.native.system.io.ports/9.0.1/runtime.osx-arm64.runtime.native.system.io.ports.9.0.1.nupkg 133 ミリ秒
info : コンテンツ ハッシュ DJ0XO49x1LwqH6vhd86UEdnG6kQvKYahmJQ3l/RB1VdgSBEP3CvW4bAI3RJcN2LFr98CiAEc8kJfBC62jNyu7w== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-x64.runtime.native.system.io.ports\9.0.1 に runtime.linux-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ p71oQqnGuDcS613xKljMwON/hKE6reJ5jtASAaVvEZdV4kdP3mrqY/TQfdebgHMWVbMmD2fwoVGOwFs8rgM1XA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.android-arm.runtime.native.system.io.ports\9.0.1 に runtime.android-arm.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ 8WT+kxKsX1K5mJL3Q1Sv01v4ZsU4nKLn2ockdH09Hiq55TT3+DYWM24kP58q/PbFYpeWiiScxdukEBG9wZt4Lw== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.osx-arm64.runtime.native.system.io.ports\9.0.1 に runtime.osx-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ mJLX92tS6qYJWUovBsfmvJusYEBsWzYOtOcbP1Yk6Q6PTDc3ZXj7BtP5lVkaplwXVqJ3+cr5DO7yQMsmcwsusg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-musl-arm64.runtime.native.system.io.ports\9.0.1 に runtime.linux-musl-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ VCeY2fHhTVB0WHWt0BCu4IhzmW3Axr1s3YRdu/U+1bamxH213lZNdFGBuFt6khvfm+uCXESqTvIIk/HWa3D/kA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-musl-arm.runtime.native.system.io.ports\9.0.1 に runtime.linux-musl-arm.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ poj5UQv4K0jEj+pso4+y+ly5FmMC5fv9k5Lvqi2eCjRmRdhvvEdJmn4hsxQR+eR1+vmgUpLbCWeW2lIUPNgZRA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.maccatalyst-arm64.runtime.native.system.io.ports\9.0.1 に runtime.maccatalyst-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ CPjFhGqiTsJcRTFrduIX7D92If6cNkOEgQhRPfnP8kSz3pt6iGL80+MEY1XQpqCz8ZPDLwkV4POrqQy6b0LF6A== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-arm.runtime.native.system.io.ports\9.0.1 に runtime.linux-arm.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ D0Asg6/8dxJgdd1Idsv7IgrwPs/UZZBXJqnloGxovjTlc2xLo9pMZJ5aVPL8YwmNIZZFJYiKMGtQgoiFHX905Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-musl-x64.runtime.native.system.io.ports\9.0.1 に runtime.linux-musl-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ vf//m1N3vYgDpUdHu3REY8wgnJ0F+HqHATsAGZJ/urcYNnY73pdogkWBnCPpbe3WhxzxiOWiyqwxmXQJ5cuqVw== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-bionic-x64.runtime.native.system.io.ports\9.0.1 に runtime.linux-bionic-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ UeqfJsSvnRl3E9QfDOzEDUMSjLnymksQV1e+kmZsrvJjJldFIBcObycky87Dgy7SlwoHbL9h+ID5plH04wh1rA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-bionic-arm64.runtime.native.system.io.ports\9.0.1 に runtime.linux-bionic-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ D9vsyhVrBRP07bS14+DzJh4yw0EZLs200mj/JlQwxjwm4Hn/a9L1Fz60Fvg877e/zL+2ioZ5eRNrN3bNT/mhAw== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.linux-arm64.runtime.native.system.io.ports\9.0.1 に runtime.linux-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ CQNfrttCyPor4ADjQlMAQtasVQqSUrUSL4xjiDVW0apVKY2DQpOC3jIMs2mtVpcEW4fdFW3C0517lTgs9ZLSYA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.maccatalyst-x64.runtime.native.system.io.ports\9.0.1 に runtime.maccatalyst-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ EPsLpR/dKMedSmIBArTMR2Ospje0Ghd7hUw+mRxeu79ayfy5PVSkUwFOdIlQ09yIsy+F2gl0X6KS5KetkxnIfg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.osx-x64.runtime.native.system.io.ports\9.0.1 に runtime.osx-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ S1RMvuVaW1T55hao2hYnncasG2+X4Mb3PEtbkEGlKp6GuxXaekTyo323fJphbJY/yFfytGynjhI+yGA9zT25PA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\microsoft.windows.compatibility\9.0.1 に Microsoft.Windows.Compatibility 9.0.1をインストールしました。
info : コンテンツ ハッシュ OxjcwJqBW/5A1111+vL9d+5KYTvOzeCTJY9zHZ0kpQI4wX075p6L7inHPSYuf0MGakVjUvaShvw9e9pfbInU2Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\microsoft.win32.systemevents\9.0.1  に Microsoft.Win32.SystemEvents 9.0.1をインストールしました。
info : コンテンツ ハッシュ VwoYcHbF+MjnJiEGJ2S4g6F0CRtuq5JYO5oAG9GumiYX7P0wIUb+W2Q/p30l9cEAbLHPDVj3nUK776uWr7b5kg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.componentmodel.composition.registration\9.0.1 に System.ComponentModel.Composition.Registration 9.0.1をインストールしました。
info : コンテンツ ハッシュ OMM+gsL/Lm2cjIyqbdgENBReskG6U741SgnhTE9GpG0hLxmrXlQa6gz7+cyNNVmpnp7ZKtuxB7j0DBoL0SLo/Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.windows.extensions\9.0.1 に System.Windows.Extensions 9.0.1をインストールしました。
info : コンテンツ ハッシュ TW05dNDwphN+sBq8TvF8Txl2bXw83w80aWtEO8Oas+vxxyXQc9o65Jv1HAOaMEL5cN6OL4FwPF+CIZ76TnhuyQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.componentmodel.composition\9.0.1 に System.ComponentModel.Composition 9.0.1をインストールしました。
info : コンテンツ ハッシュ e5XPUkAqgBY/Bv4/ENLBXwbJFgQVioc+AOzarAS4AVI/NT/INejKcTivwGCWOJFKYbMXzF80nPXPlsIuvPZ8pQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\microsoft.win32.registry.accesscontrol\9.0.1 に Microsoft.Win32.Registry.AccessControl 9.0.1をインストールしました。
info : コンテンツ ハッシュ 2J5uq+2smnj+u1jlyVJ6BGGqaK9fHcK/EwN7mbsuPqTI6dZr86br8Cg6o/5B+icQ9ANTvTDpJjnhDNtYYZijHQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.codedom\9.0.1 に System.CodeDom 9.0.1をインストールしました。
info : コンテンツ ハッシュ EyalL36RnOdrJu7pkgrbrhfEHwGmx9Pb9DTpq9GeNkbP6IQPrhvFB74IuhNKZ8fbVS6XuxXDCrAFzleYcMBsoA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.data.oledb\9.0.1 に System.Data.OleDb 9.0.1をインストールしました。
info : コンテンツ ハッシュ ntDQ+3A7vGq6jnv3KI8nv1Tfgmos9TG863xd/5tmms6LqrIxEze1RLuA3JB/AcpXMUSO70DXzXfPnJD2ZHFX0Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.configuration.configurationmanager\9.0.1 に System.Configuration.ConfigurationManager 9.0.1をインストールしました。
info : コンテンツ ハッシュ IEq6oUG77MmC38t76EOMEVt6kLKx67oHhQtOJ21zFB38BPIWzAAZ20vcjebXMyrOqLK8v47e0IslYrkf6XrxLQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.io.ports\9.0.1 に System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ lkALvIfLhDYCu89xlDj2Tybb780BZDgc3lfRWlkMw0A7x6Kqrl52Kf3Q0SwxUDJ/pm1i634jI4D7/JrvtYqnNA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.reflection.context\9.0.1 に System.Reflection.Context 9.0.1をインストールしました。
info : コンテンツ ハッシュ CLEo9O6FuO4GQ3ZQkGssg9CJ2w2TN7GMFf3wHTc7YVWJV4xoyJRPw+XIDQnCcSUJCrHhrAWOO60cAX29EV5LFQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.management\9.0.1 に System.Management 9.0.1をインストールしました。
info : コンテンツ ハッシュ 5E4yKPLeruveoh1EZKHl6f6jWXcd/a4tu+1IedG5ZndPPRAeAzFV4+ZagrcQMwz7xTFYOxC0zKM174nPGuTKoA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.runtime.caching\9.0.1 に System.Runtime.Caching 9.0.1をインストールしました。
info : コンテンツ ハッシュ u+4PH6GyDjEsWgcpKp1S/DiyxtGvazNPdaPFR6p6/qZr3TW+oZWvwfHO2H2CSpS4KGl2z2CBfU6eB38PsmoxtA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.security.cryptography.protecteddata\9.0.1 に System.Security.Cryptography.ProtectedData 9.0.1をインストールしました。
info : コンテンツ ハッシュ 782UEbbkZE5tiYYsUQWn4VuzJCvpJRp3umlC9oEELyWZAB1swMZr/KMlJN/0+BSVolYt9OnbOKqWbcoHbdpIeg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.security.cryptography.pkcs\9.0.1 に System.Security.Cryptography.Pkcs 9.0.1をインストールしました。
info : コンテンツ ハッシュ efRn3TXUx2aWG4yOjD5jxTYlPy4Pz/8fiwYBtIpVb/+ySsNA9PFWFd3M3MdcRx1XjpYtj5QSXGm8XnGCeh7dSA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.formats.asn1\9.0.1 に System.Formats.Asn1 9.0.1をインストールしました。
info : コンテンツ ハッシュ FbghROy1XuLJBVNGFmagA8vWxWOO9vvyIn1/K/Nyy/WCdv8NTr6I+JJ3rbrYSw+3FAXOB/W+hQpMfgr7/8LRTQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.directoryservices\9.0.1 に System.DirectoryServices 9.0.1をインストールしました。
info : コンテンツ ハッシュ J6pspjthfveu+Zg75tfRpsH3PggtpMiuirXtem2n7sJ2FDR+V0pQC6AZVJR5w7etnux2pqbwxGLVQjF/wdZdzQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.data.odbc\9.0.1 に System.Data.Odbc 9.0.1をインストールしました。
info : コンテンツ ハッシュ ZEXoBUZXR2wEA7IDH6LuKW6xpEqysjc9dsiATPM2OIXJz0dS0otQ/Dt+u9SuqjvBkQF6QH+bjRO7HWAsQ9ZdEA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.directoryservices.accountmanagement\9.0.1 に System.DirectoryServices.AccountManagement 9.0.1をインストールしました。
info : コンテンツ ハッシュ eFRm7+6IALzJ5PY44K+IxQ//nvNHjV852UfEJpHSAlyZ8jqI1lU/qtNEcJDkPj7E3tischIpcSlAFtp2UBvL+w== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.security.cryptography.xml\9.0.1 に System.Security.Cryptography.Xml 9.0.1をインストールしました。
info : コンテンツ ハッシュ Cpe2Vz1Htilw8H0Z7D0Ssr5mZKK1Is2k5aSV06UiqkRq9o7Qs9t33K/I3UaepVO29oOEbdzejl/HPVEA9AoRfg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.diagnostics.performancecounter\9.0.1 に System.Diagnostics.PerformanceCounter 9.0.1をインストールしました。
info : コンテンツ ハッシュ Y7eAnpn6jvlIUNHbeR5uKhQYBmldvpAWnthwIpaIKpWvTbO+MfBM55eyyWpcP+4LTAn8N/Pf7ohAKvVEKt9vMQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.directoryservices.protocols\9.0.1 に System.DirectoryServices.Protocols 9.0.1をインストールしました。
info : コンテンツ ハッシュ Ez11nlk7QMERzrFf/EsIG7wfY+KbPW7z75+Mqvrv4lwxqoLCBEJlz0Y0v+KIbMpW7XTZg8ychTJI9Z4p4LroSA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.android-arm64.runtime.native.system.io.ports\9.0.1 に runtime.android-arm64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ iVnDpgYJsRaRFnk77kcLA3+913WfWDtnAKrQl9tQ5ahqKANTaJKmQdsuPWWiAPWE9pk1Kj4Pg9JGXWfFYYyakQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.diagnostics.eventlog\9.0.1 に System.Diagnostics.EventLog 9.0.1をインストールしました。
info : コンテンツ ハッシュ moOMbopAJOxpdX0WTZ/6hxxDM40ePMyMQWrPqwcuELrY5XhpQSLoddknbkdTp70Cy4K5LjMm5IW1zz850O+z9g== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.security.permissions\9.0.1 に System.Security.Permissions 9.0.1をインストールしました。
info : コンテンツ ハッシュ TTPkCqSMyMaG8BXlBKYTTJFtLV0SvjjsvgUN598hYgHaX/5B7tdUc2JhQF9vwrYmlzxId+gwFnKYuxQ2XsSz2g== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.drawing.common\9.0.1 に System.Drawing.Common 9.0.1をインストールしました。
info : コンテンツ ハッシュ +Qg/qX62dGCD8DetCLWX/xlzgYVqBQXKmS6dPeDc4PDGX7S7GfBoMlhU2oMXydd55cYplD+KEbipv8HZW0YSmg== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.servicemodel.syndication\9.0.1 に System.ServiceModel.Syndication 9.0.1をインストールしました。
info : コンテンツ ハッシュ U/tCi1nw6aflfp+H6Hzwgt+CIHx0PoKKOTF7wNaxIg3EgfzqV+DtUantwRNifRu0Hm0W3xnxZ0hOVZVoORLAyQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\microsoft.bcl.cryptography\9.0.1 に Microsoft.Bcl.Cryptography 9.0.1をインストールしました。
info : コンテンツ ハッシュ Ghm4yP29P3cC65Qof8CrgU3WO/q3ERtht6/CrvcUl1FgRs6D7exj75GuG4ciRv0sjygtvyd675924DFsxxnEgA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.serviceprocess.servicecontroller\9.0.1 に System.ServiceProcess.ServiceController 9.0.1をインストールしました。
info : コンテンツ ハッシュ KZA6uD5yFt76EJqMgtKj0sChgXL1kAjwusR/7U3eD5flFOvAuzoof/RrDjcT9yn1A5Dtk816lIYK2GI4dYBy2g== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.threading.accesscontrol\9.0.1 に System.Threading.AccessControl 9.0.1をインストールしました。
info : コンテンツ ハッシュ /iIJryPoMQNiVzNwM94MzUq7YT/Gpjdf5iejKU5odt7NfJIqv4H7e/2FUno7irCJ1iKXjhSDo7dAOq7PDoZgyQ== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.speech\9.0.1 に System.Speech 9.0.1をインストールしました。
info : コンテンツ ハッシュ 7Op2OR5RKJgviMpPsXbcCN5bxew/KmW1AM3bzwFo3kShenYjy9eV5lYYuIxWinhrLMooGu6t2ktMRN9toV7l0Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.text.encoding.codepages\9.0.1 に System.Text.Encoding.CodePages 9.0.1をインストールしました。
info : コンテンツ ハッシュ XvPeKzWWdpYkDKfOx2KnrpLxgobmKHAloEb0AMQZjo9dbHb1FDGR+xX+V5IHtmWSR/bgOrHR3EzHXu082EEt/A== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.android-x86.runtime.native.system.io.ports\9.0.1 に runtime.android-x86.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ VN0wku8wvyIT7u3ieFKt4fJCVdTjOFEtIqa4DGehz+NH7xJM1pnI+NA5/VELtISVDIZPY/zOAySjmhTTwfGMWA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\system.io.packaging\9.0.1 に System.IO.Packaging 9.0.1をインストールしました。
info : コンテンツ ハッシュ Atw3Om7w/1jdVufJViarHAcUpuXujo84123voCM4Ik25JJQ05Ejwf5gCeTE78FJfketBJeBqj31kXLnuYxzm6Q== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.android-x64.runtime.native.system.io.ports\9.0.1 に runtime.android-x64.runtime.native.System.IO.Ports 9.0.1をインストールしました。
info : コンテンツ ハッシュ 7vPfP3+U1WRpPNLUe1aHRwVomtULT5mOnWRq9vgXJtoe7YeepDnVni+BRcIK+9L3PTbNouPpBxRdsnk4XpdfbA== を使用して、 https://api.nuget.org/v3/index.json から C:\Users\mylifewithviolin\.nuget\packages\runtime.native.system.io.ports\9.0.1 に runtime.native.System.IO.Ports 9.0.1をインストールしました。
info :   GET https://api.nuget.org/v3/vulnerabilities/index.json
info :   OK https://api.nuget.org/v3/vulnerabilities/index.json 193 ミリ秒
info :   GET https://api.nuget.org/v3-vulnerabilities/2025.01.15.06.48.40/vulnerability.base.json
info :   GET https://api.nuget.org/v3-vulnerabilities/2025.01.15.06.48.40/2025.01.17.11.29.03/vulnerability.update.json
info :   OK https://api.nuget.org/v3-vulnerabilities/2025.01.15.06.48.40/vulnerability.base.json 174 ミリ秒
info :   OK https://api.nuget.org/v3-vulnerabilities/2025.01.15.06.48.40/2025.01.17.11.29.03/vulnerability.update.json 187 ミリ秒
info : Package 'Microsoft.Windows.Compatibility' is compatible with all the specified frameworks in project 'C:\developments\vscode\WinFormsApp\WinFormsApp.csproj'.
info : PackageReference for package 'Microsoft.Windows.Compatibility' version '9.0.1' added to file 'C:\developments\vscode\WinFormsApp\WinFormsApp.csproj'.
info : アセット ファイルをディスクに書き込んでいます。パス: C:\developments\vscode\WinFormsApp\obj\project.assets.json
log  : C:\developments\vscode\WinFormsApp\WinFormsApp.csproj を復元しました (11.2 秒)。

C:\developments\vscode\WinFormsApp>
```

長いエコーが抜けて無事に完了しました。
VSCodeを起動します。

```
C:\developments\vscode\WinFormsApp>code .
```

VSCodeが起動すると右下に下記のメッセージが表示された場合はかならず「はい」を選択します。
「ビルドおよびデバッグに必要な資産がWinFormAppにありません。追加しますか？」

プロジェクトフォルダに.vscodeフォルダが作成され、デバッグ実行に必要なtasks.jsonとlaunch.jsonを構成作成してくれます。

# プロジェクトフォルダ構成
この時点でのプロジェクトのフォルダ構成です。

```
C:\developments\vscode\WinFormsApp>tree /f
C:.
│  Program.cs
│  WinFormsApp.csproj
│
├─.vscode
│      launch.json
│      tasks.json
│
├─bin
│  └─Debug
│      └─net8.0
└─obj
    │  project.assets.json
    │  project.nuget.cache
    │  WinFormsApp.csproj.nuget.dgspec.json
    │  WinFormsApp.csproj.nuget.g.props
    │  WinFormsApp.csproj.nuget.g.targets
    │
    └─Debug
        └─net8.0
            │  .NETCoreApp,Version=v8.0.AssemblyAttributes.cs
            │  WinFormsApp.AssemblyInfo.cs
            │  WinFormsApp.AssemblyInfoInputs.cache
            │  WinFormsApp.assets.cache
            │  WinFormsApp.GeneratedMSBuildEditorConfig.editorconfig
            │  WinFormsApp.GlobalUsings.g.cs
            │
            ├─ref
            └─refint
```

## WinFormsApp.csproj
この時点でWinFormsApp.csprojは下記の状態となっていますので、少し書き加えます。
```WinFormsApp.csproj
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Windows.Compatibility" Version="9.0.1" />
  </ItemGroup>

</Project>

```

### 修正後
```WinFormsApp.csproj
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net8.0-windows</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <UseWindowsForms>true</UseWindowsForms>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Windows.Compatibility" Version="9.0.1" />
  </ItemGroup>

</Project>

```

## Program.cs
Program.csはコンソールアプリケーションの状態のままですので、これをWindowsアプリケーションのひな形に書き換えます。

```cs:Program.cs
// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");

```
### 修正後
```cs:Program.cs
using System;
using System.Windows.Forms;

namespace WinFormsApp
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.SetHighDpiMode(HighDpiMode.SystemAware);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new WinForm());
        }
    }
}
```
構成を書き換えてビルドが成功するまでは、互換性警告がでますが無視します。

## WinForm.cs
とりあえず空のフォームを追加します。
```cs:WinForm.cs
using System;
using System.Windows.Forms;
using Microsoft.VisualBasic;

namespace WinFormsApp
{
    public class WinForm : Form
    {
        public WinForm()
        {
        }
    }
}
```

## launch.json
launch.jsonを少し書き換えます。

```json:launch.json
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
            "program": "${workspaceFolder}/bin/Debug/net8.0/WinFormsApp.dll",
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

### 修正後
```json:launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": ".NET Core Launch (WinForms)",
            "type": "coreclr",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/bin/Debug/net8.0-windows/WinFormsApp.exe",
            "args": [],
            "cwd": "${workspaceFolder}",
            "console": "externalTerminal",
            "stopAtEntry": false,
            "internalConsoleOptions": "neverOpen"
        },
        {
            "name": ".NET Core Attach",
            "type": "coreclr",
            "request": "attach"
        }
    ]
}
```

## tasks.json
tasks.jsonはそのまま使います。
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
                "${workspaceFolder}/WinFormsApp.csproj",
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
                "${workspaceFolder}/WinFormsApp.csproj",
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
                "${workspaceFolder}/WinFormsApp.csproj"
            ],
            "problemMatcher": "$msCompile"
        }
    ]
}
```
# ビルド・デバッグ実行開始
VSCodeの実行とデバッグに「.NET Core Launch (WinForm)」が既定で表示されていますので実行します。
ターミナルに下記のような出力が表示され

```

 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\WinFormsApp/WinFormsApp.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild のバージョン 17.9.8+610b4d3b5 (.NET)
  Determining projects to restore...
  復元対象のすべてのプロジェクトは最新です。
  WinFormsApp -> C:\developments\vscode\WinFormsApp\bin\Debug\net8.0-windows\WinFormsApp.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```

下図のような空のウィンドウが展開します。

![CsWinForm1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/75d55693-6383-52c5-84c6-fec371558228.png)

下記のフォルダに実行ファイルが生成されています。

```cmd:
C:\developments\vscode\WinFormsApp\bin\Debug\net8.0-windows>dir
2025/01/17  23:45            59,140 WinFormsApp.deps.json
2025/01/17  23:45             5,120 WinFormsApp.dll
2025/01/17  23:45           142,848 WinFormsApp.exe
2025/01/17  23:45            13,512 WinFormsApp.pdb
2025/01/17  23:45               386 WinFormsApp.runtimeconfig.json
```

今回は白紙のウィンドウフォームなので、デバッグのしようがありませんが、コンストラクタの宣言部にブレークさせることはできます。

# おわりに
いかがでしたでしょうか？けっこう手書き修正が必要でした。なにかの役にたてば幸いです。次回はなにかウィンドウアプリを書いてみます。
