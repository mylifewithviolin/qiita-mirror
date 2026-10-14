# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の検証フェーズのステップ７になります。

日本語プログラミング言語あおい（Aoi）という自作言語の企画趣旨は[こちらの記事](
https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)をご参照ください。開発コード名を「Re:Mind」としており、AIとのやりとりではこの名称が使われています。

# 生成AI
## Microsoft Copilot
Windows11アプリケーションのMicrosoft Copilot。昨年末から日本語プログラミング言語あおい Aoi（Re:Mind）の原型を作成してもらった生成AI[^2][^3][^4]。モードは「無料プラン」。サインインした状態でGitHub Copilotの使い方アドバイザーとして利用。
## GitHub Copilot
GitHub CopilotのPro+版。実装[^1]と検証の主担当。スーパバイザとしてMicrosoft Copilotを使いGitHub CopilotのCodeAgent推論量を最小化するプロンプトをCopilotで生成しGitHub CopilotのCodeAgentで実行という工法？を採用しています。

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
前回はVB.NETの生成ソースコードサンプルの対応が完了しました。本記事ではバブルソートのアルゴリズムを記述したサンプルでのVB.NETコード生成に進行します。

**バブルソートのアルゴリズムを記述したサンプル**
**sourceFiles\bubblesortcs.aoi**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/91857ad240e382a9ed54)を参照してください。

## Microsoft Copilot
このステップの推論はPro+にアップグレード後でしたので、Proへのダウングレードのタイミングなどをやりとりしていましたが、GitHub Copilotへのプロンプトは自分でだしていました。下記は検証用の参照VB.NETコードを少し修正したところからのプロンプトです。（Sharedが一部欠落）
## GitHub Copilot
### プロンプト１
>referrenceFiles\bubblesort.vb
を少し修正しました。
docs\helloworldとvariableをvb.netにトランスコンパイルできるようにするための修正フローv2完了レポート.md
を受けて
docs\bubblesortをVB.NETでトランスコンパイルできるようにするための修正フロー.md
を修正して
docs\bubblesortをVB.NETでトランスコンパイルできるようにするための修正フローv2.md
を出力してください。
#### 生成レスポンス１
>BubbleSort v2の実行を完了し、完了レポートへ出力しました。
>
>bubblesortをVB.NETでトランスコンパイルできるようにするための修正フローv2完了レポート.md
>
>実施結果:
状態を持たないBubbleSortを暫定的にPublic Shared Subへ昇格
bubblesort.vbを生成
VB.NET検証プロジェクトのビルド成功
生成プログラムの実行成功
ソート結果を確認
>
>本体のC#プロジェクトも、0警告・0エラーでビルド成功しています。
参照ファイルとの完全一致は未達ですが、差異はByVal、ToString()、XMLコメント整形、Public有無などとしてレポートに記録しました。

### トランスコンパイル後のVB.NETソースコード
コンパイル検証済コードとなります。
**transcompiledFiles\bubblesort.vb**

```vb:transcompiledFiles\bubblesort.vb
Imports System

Namespace BubbleSort
    ''' <summary>プログラム型</summary>
    Public Class Program
        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())
            ''' <summary>配列</summary>
            Dim array As Integer() = { 15, 13, 9, 6, 4, 1 }
            BubbleSort(array)
            For i As Integer = 0 To array.Length - 1
                ConsoleOut(array(i))
            Next
        End Sub
        
        ''' <summary>バブルソートする</summary>
        ''' <param name=array>配列</param>
        Public Shared Sub BubbleSort(ByVal array As Integer())
            ''' <summary>外側</summary>
            Dim i As Integer = 0
            While i < array.Length
                ''' <summary>内側</summary>
                Dim j As Integer = 0
                While j < array.Length - i - 1
                    If array(j) > array(j + 1) Then
                        ''' <summary>一時</summary>
                        Dim temp As Integer = array(j)
                        array(j) = array(j + 1)
                        array(j + 1) = temp
                    End If
                    j += 1
                End While
                i += 1
            End While
        End Sub
        
        ''' <summary>コンソール表示する</summary>
        ''' <param name=dispStr>引数2</param>
        Shared Sub ConsoleOut(ByVal dispStr As String)
            Console.WriteLine(dispStr)
        End Sub
        
    End Class
    
End Namespace
```
あおいのJavaDoc形式のXMLコメントもVB.NET形式のXMLコメントにしっかり変換されています。わたしの中ではC#とVB.NETが共通のソースから生成されることに感慨深いものがあります。

## 本ステップの評価
バブルソートのアルゴリズムを記述したサンプルでVB.NETコード生成に到達しました。定番アルゴリズムの線形探索法、二分探索法、バブルソートのあおい（Re:MInd）ソースコードとC#、Java、VB.NETのソースコードがありますので、線形探索法、二分探索法のVB.NET言語への展開を進めていきます。VB.NETのがC#と共通的なあおいソースで記述する場合に問題が少ないです。


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
