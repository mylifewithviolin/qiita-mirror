# はじめに
日本語プログラミング言語あおい（Aoi）の実装[言語仕様](https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b)を生成AIに読み込ませて仕様駆動開発を展開しており、本記事は実装完了した「最小セット（MVP）」[^1]の検証フェーズのステップ８になります。

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
前回のステップでバブルソートのアルゴリズムを記述したサンプルでVB.NETのコード生成を行いました。本記事では線形探索法、二分探索法のVB.NETコード生成に進行します。

## 線形探索法、二分探索法のアルゴリズムを記述したサンプルに対応
**線形探索法のアルゴリズムを記述したサンプル**
**sourceFiles\linearsearchcs.aoi**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/5acf86b12bd538caca30)を参照してください。

**二分探索法のアルゴリズムを記述したサンプル**
**sourceFiles\binarysearchcs.aoi**
[こちらの記事](
https://qiita.com/mylifewithviolin/items/5acf86b12bd538caca30)を参照してください。


## Microsoft Copilot
GitHub Copilotへのプロンプトは自分でだしていましたのでMicrosoft Copilotとのやりとりはなかったです。
## GitHub Copilot
### プロンプト１
>sourceFiles\linearsearchcs.aoiは線形探索法のソース
sourceFiles\binarysearchcs.aoiは二分探索法のソースです。
VB.NETソースコードにトランスコンパイルして
transcompiledFiles\linearsearch.vb
transcompiledFiles\binarysearch.vb
に出力し（変換元ソース格納フォルダと変換後ソース格納フォルダは起動パラメータ扱い）
VB.NETコンパイラでコンパイル可能かを検証し
referrenceFiles\linearsearch.vb
referrenceFiles\binarysearch.vb
と比較検証する実行プランを作成して
docs\linearsearchとbinarysearchをvb.netにトランスコンパイルできるようにするための修正フロー.md
に出力してください。

#### 生成レスポンス１
>計画を実行し、完了レポートを作成しました。
>
>linearsearchとbinarysearchをvb.netにトランスコンパイルできるようにするための修正フロー完了レポート.md
>
>実施内容:
ReturnIRからVB.NETのReturnを生成
== -> =、!= -> <>
BinarySearchの/ -> \整数除算
配列添字、Length、While、If/Elseを変換
非static探索関数を暫定的にShared Functionへ昇格
linearsearch.vb、binarysearch.vbを生成
両方のVB.NETコンパイル成功
LinearSearch実行結果: 4
BinarySearch実行結果: 該当なし
BinarySearchの入力配列が降順のため、通常の昇順前提の二分探索では該当なしになります。この点は変換エラーではなく、入力データとアルゴリズム前提の不一致としてレポートに記録しました。

### トランスコンパイル後のVB.NETソースコード
コンパイル検証済コードとなります。
**transcompiledFiles\linearsearch.vb**

```vb:transcompiledFiles\linearsearch.vb
Imports System

Namespace LinearSearch
    ''' <summary>プログラム型</summary>
    Public Class Program
        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())
            ''' <summary>配列</summary>
            Dim array As Integer() = { 15, 13, 9, 6, 4, 1 }
            ''' <summary>探す値</summary>
            Dim target As Integer = 4
            ''' <summary>該当インデックス</summary>
            Dim index As Integer = LinearSearch(array, target)
            If index <> -1 Then
                ConsoleOut(index)
            Else
                ConsoleOut("該当なし")
            End If
        End Sub
        
        ''' <summary>線形探索する</summary>
        ''' <param name=array>配列</param>
        ''' <param name=target>探す値</param>
        Public Shared Function LinearSearch(ByVal array As Integer(), ByVal target As Integer) As Integer
            ''' <summary>インデックス</summary>
            Dim i As Integer = 0
            While i < array.Length
                If array(i) = target Then
                    Return i
                End If
                i += 1
            End While
            Return -1
        End Function
        
        ''' <summary>コンソール表示する</summary>
        ''' <param name=dispStr>引数2</param>
        Shared Sub ConsoleOut(ByVal dispStr As String)
            Console.WriteLine(dispStr)
        End Sub
        
    End Class
    
End Namespace
```
**transcompiledFiles\binarysearch.vb**

```vb:transcompiledFiles\binarysearch.vb
Imports System

Namespace BinarySearch
    ''' <summary>プログラム型</summary>
    Public Class Program
        ''' <summary>メイン</summary>
        ''' <param name=args>引数</param>
        Shared Sub Main(ByVal args As String())
            ''' <summary>配列</summary>
            Dim array As Integer() = { 15, 13, 9, 6, 4, 1 }
            ''' <summary>探す値</summary>
            Dim target As Integer = 4
            ''' <summary>該当インデックス</summary>
            Dim index As Integer = BinarySearch(array, target)
            If index <> -1 Then
                ConsoleOut(index)
            Else
                ConsoleOut("該当なし")
            End If
        End Sub
        
        ''' <summary>二分探索する</summary>
        ''' <param name=array>配列</param>
        ''' <param name=target>探す値</param>
        Public Shared Function BinarySearch(ByVal array As Integer(), ByVal target As Integer) As Integer
            ''' <summary>左端</summary>
            Dim left As Integer = 0
            ''' <summary>右端</summary>
            Dim right As Integer = array.Length - 1
            While left <= right
                ''' <summary>中央</summary>
                Dim mid As Integer = (left + right) \ 2
                If array(mid) = target Then
                    Return mid
                End If
                If array(mid) < target Then
                    left = mid + 1
                Else
                    right = mid - 1
                End If
            End While
            Return -1
        End Function
        
        ''' <summary>コンソール表示する</summary>
        ''' <param name=dispStr>引数2</param>
        Shared Sub ConsoleOut(ByVal dispStr As String)
            Console.WriteLine(dispStr)
        End Sub
        
    End Class
    
End Namespace
```
あおいのJavaDoc形式のXMLコメントもVB.NET形式のXMLコメントにしっかり変換されています。構文的にはC#とVB.NETは異なる要件があるので、後の検証フェーズで細かく対応していきます。

## 本ステップの評価
定番アルゴリズムの線形探索法、二分探索法のアルゴリズムを記述したサンプルでVB.NETコード生成対応が完了しました。定番アルゴリズムの線形探索法、二分探索法、バブルソートのあおい（Re:MInd）ソースコードとC#、Java、VB.NETのソースコードがありますので、次回はJava対応となりますが、定番アルゴリズムのソースはそこそこ複雑なので、まずはHelloworldなどのサンプルから着手します。Javaの場合はC#と共通的なあおいソースで記述する場合に若干問題があります。

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
