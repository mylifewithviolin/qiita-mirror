# はじめに
生成AI(Microsoft CopilotとGitHub Copilot)に日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を読み込ませて仕様駆動開発を展開しており、実装完了した「最小セット（MVP）」[^1]の検証フェーズになります。本記事でそのステップ６になります。MVPのコード生成器はC#、VB.NET、Javaの３言語を想定していますが、いよいよVB.NETの検証に進行します。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態で使用します。GitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro+版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。前回の検証改修ワークフローでフリー版のクレジットを消費しきったのでPro版にアップグレードしましたが、いくつかの別件ワークロードの影響もあって今回の途中でPro版のクレジットを使い切ったのでPro+版にアップグレード。

# 本記事のステップ
## 1. 最小セット（MVP）
まずは「1つの小さなプログラムを通せる」レベルに絞る構成。下記の実装タスクから構成され実行完了しました。
　Phase 1. Lexer タスク
　Phase 2. Parser タスク
　Phase 3. AST タスク
　Phase 4. 意味解析と名前解決 タスク
　Phase 5. 中間表現（IR） タスク
　Phase 6. コード生成パイプライン タスク
　Phase 7. コア構文のトランスコンパイル実装
　Phase 8. Program.cs からの実行フロー統合の実装

### Phase 9: 検証と品質改善
前回のステップで定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つのあおいソースコードのC#ソースコードへのトランスコンパイル検証対応は完了しました。今回はVB.NETの生成ソースコードサンプルの対応に進行します。単純なサンプルで開始します。（要件としてVB.NETコンパイラでのビルド正常要件も入れたので、それがクレジット消費を押し上げたかもしれません。

## 簡単なサンプルと期待コード（答え）でVB.NETコード生成に対応する。
### あおいのソースコードサンプル
**簡単なサンプル1**
**sourceFiles\helloworldcs.aoi**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/41cdd6c2be00cb71792d)を参照してください。

**簡単なサンプル2**
**sourceFiles\variablecs.aoi**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/0c194fad2142bafaef79)を参照してください。
### VB.NETの変換後ソースコードサンプル（期待コード）
**referrenceFiles\helloworld.vb**

```vb:referrenceFiles\helloworld.vb
Imports System
Namespace HelloWorld


    ''' <summary>プログラム型</summary>
    Public Class Program
    

        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())

            Console.WriteLine("Hello World!")
        End Sub

    End Class

End Namespace
```
**referrenceFiles\variable.vb**

```vb:referrenceFiles\variable.vb
Imports System
Namespace HelloWorld

    ''' <summary>
    ''' プログラム型
    ''' </summary>
    Public Class Program

        ''' <summary>挨拶１</summary>
       Private Shared aisatsu1 As String

        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())

           aisatsu1="Hello World one!"
           ConsoleOut(aisatsu1)
        End Sub

        ''' <summary>コンソール表示する</summary>
        ''' <param name=args>引数</param>
       Private Shared Sub ConsoleOut(ByVal args2 As String)

           Console.WriteLine(args2)
       End Sub

    End Class

End Namespace
```
2つ目のサンプルは制御構文としてはループも分岐もない単純な構文なのですが、あおい上static装飾されたMainや変数、関数をVB.NETのSharedに変換するという課題が浮上するサンプルです。

## Microsoft Copilot
このステップの推論もVB.NETコンパイラのビルド検証のところでクレジット消費が上昇して、Proレベルでは終了することができず、Pro+にアップグレードしたのですが、中断時がちょうどVB.NETコンパイラによるコンパイル検証時だったので、そこでのトラブル対処でいろいろやりとりしていました。GitHub Copilotとのやりとりは中断再開後から。
## GitHub Copilot
### プロンプト１
>referrenceFiles\helloworld.vb
referrenceFiles\variable.vb
を少し修正して
Sub Mainを
Shared Sub Mainに訂正しました。
あおいのソースに
▽static void メイン(string[] 引数)
とあった場合
変換ターゲットがVB.NETの場合はSharedに変換するとか無理がありますでしょうか？
この点について
docs\VB.NETのエントリポイントの変換方針について.md
に出力してください。
#### 生成レスポンス１
>方針書を作成しました。
VB.NETのエントリポイントの変換方針について.md
>
>内容には以下を含めています。
static void メイン(...) → Shared Sub Main(...) は実装可能で自然な変換であること
static と Shared の対応表
Main以外のメソッド・フィールドの扱い
現在のMethodIRに修飾子情報がない点
MethodIR.Modifiersを追加する推奨設計
VB.NETコンパイル検証方法
Sharedメソッドからインスタンスフィールドを参照する場合の注意点

VB.NETのエントリポイントの変換方針について.md
はなかなかよく考察されていてわかりやすいものでした。

### プロンプト２
>referrenceFiles\variable.vb
を少し修正して
変数と引用関数にSharedを追記しました。
docs\VB.NETのエントリポイントの変換方針について.md
の恒久策の方を
docs\helloworldとvariableをvb.netにトランスコンパイルできるようにするための修正フロー.md
に反映して
docs\helloworldとvariableをvb.netにトランスコンパイルできるようにするための修正フローv2.md
として出力して適切な再開位置から再開して
docs\helloworldとvariableをvb.netにトランスコンパイルできるようにするための修正フローv2完了レポート.md
に出力してください。

#### 生成レスポンス２
>v2の修正フローを作成し、中断時点から実行して完了レポートを出力しました。
>
>修正フロー v2
v2完了レポート
実施内容:
>
>MethodIR.Modifiersを追加
ASTのメソッド修飾子をIRへ引き継ぎ
VB.NETでstatic -> Sharedへ変換
フィールドもstatic -> Sharedへ変換
HelloWorld / Variableを再生成
両方のVB.NET検証プロジェクトをビルド成功
本体astsample.csprojもビルド成功
参照ファイルとの完全一致は、空白・インデントとConsoleOutのPrivate有無に差異が残っていますが、生成されたVB.NETコードのコンパイル検証は完了しています。


### トランスコンパイル後のVB.NETソースコード
コンパイル検証済コードとなります。
**transcompiledFiles\helloworld.vb**

```vb:transcompiledFiles\helloworld.vb
Imports System

Namespace HelloWorld
    ''' <summary>プログラム型</summary>
    Public Class Program
        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())
            Console.WriteLine("Hello World!")
        End Sub
        
    End Class
    
End Namespace
```
**transcompiledFiles\variable.vb**

```vb:transcompiledFiles\variable.vb
Imports System

Namespace HelloWorld
    ''' <summary>プログラム型</summary>
    Public Class Program
        ''' <summary>挨拶１</summary>
        Private Shared aisatsu1 As String
        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())
            aisatsu1 = "Hello World one!"
            ConsoleOut(aisatsu1)
        End Sub
        
        ''' <summary>コンソール表示する</summary>
        ''' <param name=dispStr>引数2</param>
        Shared Sub ConsoleOut(ByVal dispStr As String)
            Console.WriteLine(dispStr)
        End Sub
        
    End Class
    
End Namespace
```

## 本ステップの評価
VB.NETの生成ソースコードサンプルの対応が完了しました。より複雑なソースコードとして定番アルゴリズムの線形探索法、二分探索法、バブルソートの３つがありますが、次回はバブルソートを変換します。


# おわりに
以上です。いかがでしたでしょうか？なにか似たようなことをされようとしている方々の参考になれば幸いです。

[^1]: AIとつくる日本語プログラミング言語Aoi （あおい） - Qiita
記事リストです。（ステップ降順）
[ステップ１２ 実行フロー統合の最小実装](https://qiita.com/mylifewithviolin/items/3d2ceebf28db01ad04a2)
[ステップ１１ コア構文のトランスコンパイルの最小実装](
https://qiita.com/mylifewithviolin/items/d66a707c8ae7419f001c)
[ステップ１０ コード生成パイプラインの最小実装](
https://qiita.com/mylifewithviolin/items/c02b35b762aa11b42540)
[ステップ９ 中間表現（IR）の最小実装](
https://qiita.com/mylifewithviolin/items/a787e4a85866fe52074f)
[ステップ８ 中間表現（IR）の最小実装 ひな形](
https://qiita.com/mylifewithviolin/items/b8b142c4046c6df2654b)
[ステップ７ 「意味解析と名前解決」の最小実装](https://qiita.com/mylifewithviolin/items/4c2a0811b824402ea177)
[ステップ６ 「意味解析と名前解決」か「中間表現（IR）」か](https://qiita.com/mylifewithviolin/items/13a90dec5eefaf9bd1b5)
[ステップ５ AST最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/1ce67bdee49bcdf052e6)
[ステップ４ Parser最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/c35fed8a80254eb7c1a6)
[ステップ３ Lexer最小版の実装 CodeAgent推論量最小化](https://qiita.com/mylifewithviolin/items/34a4872e17869824a3f3)
[ステップ２ PlanAgent計画細分化](https://qiita.com/mylifewithviolin/items/5f14b5f98f052103729c)
[ステップ１ Copilotが生成した日本語トランスコンパイラ言語 Re:Mindの原型をGitHub CopilotのPlanエージェントで再計画](https://qiita.com/mylifewithviolin/items/647c8d8ad9b9785ce942)
[^2]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[^3]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[^4]:Copilotが生成した日本語トランスコンパイラ言語 Re:MindのC#コード生成が動作するまで - Qiita
[ステップ４](https://qiita.com/mylifewithviolin/items/ccf382e785cc2489c822)
