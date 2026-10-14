# はじめに

諸般の流れからVSCodeでMind 7.5 for Windowsがビルドできる環境に加えてC#がビルド、デバッグ実行できる環境をつくっておりました。本記事はついにその目的が明らかになる内容です。タイトルにまんま書かれています。:sweat_smile:

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
C# 10 
dotnet-sdk-6.0.419-win-x64
dotnet-sdk-6.0.419-win-x86
Mind Version 7.5 for Windows

## VSCodeの拡張機能
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

# Mind7環境の構成
## お題のソース
mind7.5付属のDLL実装用サンプルソースmindsdll.srcを下記のように書き加えます。ソースコード中のコメントはあたかもMind開発者の@killyさんが書いたかのようですが、稚拙ながらわたしの方で書かせていただいております。「メインとは」の「※　このＤＬＬではなにもしない　※」など一部を除く。

とはいってもdll.dcomに記述されている内容の引用表現調整なので、実質killyさんが書いているようなものです。ただしわたしが勘違いして書いている場合はわたしのせいです。オリジナルのサンプルは引数２と引数３の例でしたが、引数無と引数１も加えています。

```mind:mindsdll.src
※　引数無のサービス　※
※　__declspec (dllexport) int CALLBACK MindDllService0( void );

ＤＬＬサービス０とは　本定義　（・　→　戻り値）
	コンソールを開き
　　「Hello, World! by mind7 dll」を　表示して　改行し
※	コンソールを閉じ
	100を　返すこと。

※　１引数のサービス　※
※　__declspec (dllexport) int CALLBACK MindDllService1( int data1 );

ＤＬＬサービス１とは　本定義　（引数１(ASCIZ形式文字列)　→　戻り値）
	※文字列でも引数に乗せることは可能。（実型はアドレスポインタのため）
	※呼出し側（アプリケーション）と呼ばれる側（DLL）との約束で型を揃える。
	※戻り値も構造体にしておけば先頭アドレスを返してホスト側で複数の変数を参照可能。

 　	Ｍｉｎｄ文字列に変換し
 	コンソールを開き　表示して　改行し
※	コンソールを閉じ
	200を　返すこと。

※　２引数のサービス　※
※　__declspec (dllexport) int CALLBACK MindDllService2(int data1, int data2);

ＤＬＬサービス２とは　本定義　（引数１、引数２　→　戻り値）
	引くこと。


※　３引数のサービス（さらに分岐する）　※
※　__declspec (dllexport) int CALLBACK MindDllService3(int data1, int data2, int data3);

加えの処理とは　　（引数１、引数２　→　戻り値）
	加えること。

掛けの処理とは　　（引数１、引数２　→　戻り値）
	掛けること。

指示違反の処理とは　（引数１、引数２　→　戻り値）
	二つ捨て
	－１を　返すこと。

ＤＬＬサービス３とは　本定義
　（引数１、引数２、引数３(ASCIZ形式文字列)　→　戻り値）
	※　MindによるDLLは、ホスト言語からみたインポート関数名が（引数の数違いで）9種固定なので
	※　9を超える関数を提供したい場合は本例のように引数３（各インポート関数末尾の引数）で
	※　case分けして引数１、引数２（、・・）で行う処理（処理単語）を分岐させるとよい	
	Ｍｉｎｄ文字列に変換し
	文字列事例をとる
		「加え」なら　加えの処理
		「掛け」なら　掛けの処理
		例外なら　　　指示違反の処理
	事例終り。


※　初期化　※

メインとは
	※　このＤＬＬではなにもしない　※
	※　DLL設計者が独自の初期化処理をおこないたい場合　※
	※　この「メイン」内部に書く。無ければ単に「。」を書く　※
	。

```
DLL側でコンソール出力する際に、dll.dcomの説明（guiprog.dcom）に従って当初、「コンソールを開い」た後すぐに「コンソールを閉じ」ていたのですが、閉じてしまうとC＃側のコンソール出力もされなくなる現象に遭遇したので、閉じるはコメントアウトしています。

## tasks.json
C#側のタスクに追加して、下記のタスクを追記しています。リンクされるライブラリはfileではなくfiledとなります。
```json:tasks.json
        {
            "label": "mind build dll",
            "type": "process",
            "command": "C:/mind7/bin/mind.exe",
            "args": [
                "${workspaceFolder}/mindsdll.src",
                "C:/mind7/lib/filed"
            ],
            "problemMatcher": []
        }
```
## ビルド実行
ここで、VSCodeのメニューからターミナル→タスクの実行を選択します。tasks.jsonの内容が展開されますので"mind build dll"を選択します。

```
 *  実行するタスク: C:/mind7/bin/mind.exe C:\developments\vscode\mind7dll\cs/mindsdll.src C:/mind7/lib/filed 

日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:750****
コンパイル中 -- 終了
Coping.. C:\mind7\bin\mrunt205.dll --> C:\developments\vscode\mind7dll\cs\mindsdll.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
Mind側のビルドは問題なく成功です。ランタイムファイルmrunt205.dllがmindsdll.dllにリネームコピーされたことが読み取れます。

# C#環境の構成
## お題のソース
```cs:Program.cs
using System.Runtime.InteropServices;

//※　引数無のサービス　※
//※　__declspec (dllexport) int CALLBACK MindDllService0( void );
[DllImport("mindsdll.dll", EntryPoint="MindDllService0",CallingConvention = CallingConvention.StdCall)]
    static extern int MindDllService0();

//※　１引数のサービス　※
//※　__declspec (dllexport) int CALLBACK MindDllService1( int data1 );
[DllImport("mindsdll.dll", EntryPoint="MindDllService1",CallingConvention = CallingConvention.StdCall)]
    static extern int MindDllService1(IntPtr data1);

//※　２引数のサービス　※
//※　__declspec (dllexport) int CALLBACK MindDllService2(int data1, int data2);
[DllImport("mindsdll.dll")]
    static extern int MindDllService2(int data1, int data2);

//※　３引数のサービス（さらに分岐する）　※
//※　__declspec (dllexport) int CALLBACK MindDllService3(int data1, int data2, int data3);
[DllImport("mindsdll.dll")]
    static extern int MindDllService3(int data1, int data2, IntPtr data3);


Console.WriteLine("Hello, World! by C#");

int ret;
ret =  MindDllService0();
Console.WriteLine("MindDllService0 return:" + ret);

IntPtr ptr =Marshal.StringToHGlobalAnsi("Hello, World! by C# -> mind7 dll");
ret =  MindDllService1(ptr);
Console.WriteLine("MindDllService1 return:" + ret);

ret =  MindDllService2(500,200);
Console.WriteLine("MindDllService2 return:" + ret);

ptr =Marshal.StringToHGlobalAnsi("掛け");
ret =  MindDllService3(30,40,ptr);
Console.WriteLine("MindDllService3 return:" + ret);
```

## 参考情報
下記のサイトの記事がたいへん参考になりました。C#マネージドの文字列をアンマネージドのC文字列ポインタに変換するところ。
Marshal.StringToHGlobalAutoではMind側で日本語が正常に判定できませんでしたが（サンプルのＤＬＬサービス３）Marshal.StringToHGlobalAnsiとすることで正常に判定できるようになりました。

https://so-zou.jp/software/tech/programming/c-sharp/cpp/marshaling.htm#marshal-copy

## cs.csproj
cs.csprojに
```
<PlatformTarget>x86</PlatformTarget>
```
を追加します。これを忘れるとC#は64bitでビルドされるので32bitのMindのdllのエクスポート関数を実行する時点で、「System.BadImageFormatException: 間違ったフォーマットのプログラムを読み込もうとしました。」 という例外がスローされて停止します。

```
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net6.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <PlatformTarget>x86</PlatformTarget>
  </PropertyGroup>

</Project>
```
また、x86用の.NET Coreランタイムも別途インストールしておく必要があります。インストールされていない場合は、エラーコード -532462766 (0xe0434352) で終了します。[このあたりは記事にしてあります](https://qiita.com/mylifewithviolin/items/80486f0f7f9e80c5c3ac)。

残念ながらまだデバッグ実行はできておりません。VisualStudioですと、ビルドボタンのすぐとなりのアーキテクチャプルダウンを変更するお手軽さでしたが、VSCodeではまだ成功していません。

そのため、本記事ではビルドタスクの他、起動タスクもtasks.jsonに構成し、launch.jsonでのデバッグ開始は行わないとしています。また解決し次第展開いたします。

## tasks.json
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
                "${workspaceFolder}/cs.csproj",
                "/property:GenerateFullPaths=true",
                "/consoleloggerparameters:NoSummary;ForceNoAlign"
            ],
            "problemMatcher": "$msCompile"
        },
        {
            "label": "exec",
            "command": "${workspaceFolder}/bin/debug/net6.0/cs.exe",
            "type": "process",
            "args": [],
            "problemMatcher": []
        },
        //Mind7のdllのbuildタスク略
    ]
}
```

## ビルド実行
VSCodeのメニューからターミナル→タスクの実行を選択します。tasks.jsonの内容が展開されますので"build"を選択します。

```
 *  実行するタスク: C:\Program Files\dotnet\dotnet.exe build C:\developments\vscode\mind7dll\cs/cs.csproj /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary;ForceNoAlign 

MSBuild version 17.3.2+561848881 for .NET
  復元対象のプロジェクトを決定しています...
  復元対象のすべてのプロジェクトは最新です。
  cs -> C:\developments\vscode\mind7dll\cs\bin\Debug\net6.0\cs.dll
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
ビルド成功です。続いて、"exec"タスクを実行します。
コンソールに下記が出力されます。
```
 *  実行するタスク: C:\developments\vscode\mind7dll\cs/bin/debug/net6.0/cs.exe  

Hello, World! by C#
Hello, World! by mind7 dll
MindDllService0 return:100
Hello, World! by C# -> mind7 dll
MindDllService1 return:200
MindDllService2 return:300
MindDllService3 return:1200
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
無事に完走しました:tada::tada:

↓これはC#側のコンソール出力です。
```
Hello, World! by C#
```
```cs:Program.cs
Console.WriteLine("Hello, World! by C#");
```

↓これはMind7側のリテラル文字列のコンソール出力です。戻り値の100はMindがリテラル整数を返しています。
```
Hello, World! by mind7 dll
MindDllService0 return:100
```
```cs:Program.cs
ret =  MindDllService0();
Console.WriteLine("MindDllService0 return:" + ret);
```
↓これはC#側のリテラル文字列をMind7側でコンソール出力したものです。戻り値の200はMindがリテラル整数を返しています。
```
Hello, World! by C# -> mind7 dll
MindDllService1 return:200
```
```cs:Program.cs
IntPtr ptr =Marshal.StringToHGlobalAnsi("Hello, World! by C# -> mind7 dll");
ret =  MindDllService1(ptr);
Console.WriteLine("MindDllService1 return:" + ret);
```

↓この戻り値の300はMindがC#の引数500から引数200を減算して返しています。
```
MindDllService2 return:300
```
```cs:Program.cs
ret =  MindDllService2(500,200);
Console.WriteLine("MindDllService2 return:" + ret);
```

↓この戻り値の1200はMindがC#の引数30と引数40を、第3引数の「掛け」を判定して乗算して返しています。第3引数の文字列判定に失敗した場合は-1が返っていました。
```
MindDllService3 return:1200
```
```cs:Program.cs
ptr =Marshal.StringToHGlobalAnsi("掛け");
ret =  MindDllService3(30,40,ptr);
Console.WriteLine("MindDllService3 return:" + ret);
```

# おわりに
異なる言語で書かれたプログラムが協調実行（相互運用）される様は私はなんかワクワクします。純然たるC#屋さん的にはこれってダレトク？な感じかもしれません。次回はもう少し非エンジニアよりの言語でお試ししてみます。
