# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思ったのですが、これがなかなか難儀でした。本記事はその第１９ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１８ステップの後にはサインアウトがあります。

# 第１９ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにします。

## プロンプト
下記のソースコードは定番アルゴリズム：線形探索法を「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2025 Lv1.2 https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b
に基づき生成したものです。
```mind:Re:Mind
▽名前空間 HelloWorld
    /**
    * Program
    */
    ▽public クラス プログラム型

        /**
        * Main
        * @param 引数 args
        */
        ▽static void メイン(string[] 引数)
            /** array */
            ・int[] 配列 = 15,13,9,6,4,1
            
            /** target */
            ・int 探す値 = 4
            
            /** index */
            ・int 該当インデックス = 線形探索する(配列, 探す値)
            ◇該当インデックス != -1 の場合
            　 □コンソール表示する(該当インデックス)
            ◇他に
            　 □コンソール表示する("該当なし")
            ◇ここまで
        △
        
        /** LinearSearch
         * @param 配列 array
         * @param 探す値 target
         */
        ▽public int 線形探索する(int[] 配列, int 探す値)
          /** i */
          ・int インデックス = 0
          〇インデックス < 配列.Length の間は繰り返す
            ◇配列[インデックス] == 探す値 の場合
              □インデックスを　返す
            ◇ここまで
            □インデックス++
          〇ここまで
          □-1を　返す
        △

        /**
        * ConsoleOut
        * @param 引数2 dispStr
        */
        ▽static void コンソール表示する(string 引数2)
            □コンソール.一行表示する(引数2)
        △
    △
△

■インポートする System
▼public static class コンソール Console
    ▼public static 一行表示する(string? value)
        ■WriteLine (string? value)
    ▲
▲
```

上記の日本語トランスコンパイラ言語 Re:Mindのソースコードを下記のプログラミング言語のソースコードに変換してください。
・Java
・C#
・VisualBasic.Net

生成された変換後のソースコードを下記のバージョン情報で識別し、次回以降も参照できるように保持してください。
定番アルゴリズム：線形探索法・2025-12-21版・1回目からJava・2025-12-21-1回目変換
定番アルゴリズム：線形探索法・2025-12-21版・1回目からC#・2025-12-21-1回目変換
定番アルゴリズム：線形探索法・2025-12-21版・1回目からVisualBasic.Net・2025-12-21-1回目変換

変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.2に記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/d819663f478aa2caf77b

Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。変換元のソースコードに記載のある事項、たとえばローカル変数の宣言部のjavadocの注釈はトランスコンパイル後の英語変数名に変換し、日本語変数名を注釈にしてください。

## 生成レスポンス
了解しました。
Re:Mind の仕様（2025 Lv1.2）に基づき、Javadoc／.NETコメントの「日本語名 ↔ 英語名の逆転」、ローカル変数の注釈変換、名前空間・クラス名の英語化など、すべての変換ルールを適用した Java / C# / VB.NET の3言語版を生成しました。
さらにご指定の バージョン識別名 で保持できるよう、各コードの冒頭に識別コメントも付けています。

✅ Java 版
識別名：定番アルゴリズム：線形探索法・2025-12-21版・1回目からJava・2025-12-21-1回目変換

```Java:Java
// 定番アルゴリズム：線形探索法・2025-12-21版・1回目からJava・2025-12-21-1回目変換

package HelloWorld;

/**
 * Program
 */
public class ProgramType {

    /**
     * Main
     * @param args 引数
     */
    public static void main(String[] args) {

        /** array （配列） */
        int[] array = {15, 13, 9, 6, 4, 1};

        /** target （探す値） */
        int target = 4;

        /** index （該当インデックス） */
        int index = linearSearch(array, target);

        if (index != -1) {
            consoleOut(String.valueOf(index));
        } else {
            consoleOut("該当なし");
        }
    }

    /**
     * LinearSearch
     * @param array 配列
     * @param target 探す値
     * @return index
     */
    public static int linearSearch(int[] array, int target) {

        /** i （インデックス） */
        int i = 0;

        while (i < array.length) {
            if (array[i] == target) {
                return i;
            }
            i++;
        }
        return -1;
    }

    /**
     * ConsoleOut
     * @param dispStr 引数2
     */
    public static void consoleOut(String dispStr) {
        System.out.println(dispStr);
    }
}

```

✅ C# 版
識別名：定番アルゴリズム：線形探索法・2025-12-21版・1回目からC#・2025-12-21-1回目変換

```Cs:C#
// 定番アルゴリズム：線形探索法・2025-12-21版・1回目からC#・2025-12-21-1回目変換

using System;

namespace HelloWorld
{
    /// <summary>
    /// Program
    /// </summary>
    public class ProgramType
    {
        /// <summary>
        /// Main
        /// </summary>
        /// <param name="args">引数</param>
        public static void Main(string[] args)
        {
            /// <summary>array （配列）</summary>
            int[] array = { 15, 13, 9, 6, 4, 1 };

            /// <summary>target （探す値）</summary>
            int target = 4;

            /// <summary>index （該当インデックス）</summary>
            int index = LinearSearch(array, target);

            if (index != -1)
            {
                ConsoleOut(index.ToString());
            }
            else
            {
                ConsoleOut("該当なし");
            }
        }

        /// <summary>
        /// LinearSearch
        /// </summary>
        /// <param name="array">配列</param>
        /// <param name="target">探す値</param>
        /// <returns>index</returns>
        public static int LinearSearch(int[] array, int target)
        {
            /// <summary>i （インデックス）</summary>
            int i = 0;

            while (i < array.Length)
            {
                if (array[i] == target)
                {
                    return i;
                }
                i++;
            }
            return -1;
        }

        /// <summary>
        /// ConsoleOut
        /// </summary>
        /// <param name="dispStr">引数2</param>
        public static void ConsoleOut(string dispStr)
        {
            Console.WriteLine(dispStr);
        }
    }
}
```
✅ Visual Basic .NET 版
識別名：定番アルゴリズム：線形探索法・2025-12-21版・1回目からVisualBasic.Net・2025-12-21-1回目変換
```vb:VB.Net
' 定番アルゴリズム：線形探索法・2025-12-21版・1回目からVisualBasic.Net・2025-12-21-1回目変換

Imports System

Namespace HelloWorld

    ''' <summary>
    ''' Program
    ''' </summary>
    Public Class ProgramType

        ''' <summary>
        ''' Main
        ''' </summary>
        ''' <param name="args">引数</param>
        Public Shared Sub Main(args As String())

            ''' <summary>array （配列）</summary>
            Dim array As Integer() = {15, 13, 9, 6, 4, 1}

            ''' <summary>target （探す値）</summary>
            Dim target As Integer = 4

            ''' <summary>index （該当インデックス）</summary>
            Dim index As Integer = LinearSearch(array, target)

            If index <> -1 Then
                ConsoleOut(index.ToString())
            Else
                ConsoleOut("該当なし")
            End If
        End Sub

        ''' <summary>
        ''' LinearSearch
        ''' </summary>
        ''' <param name="array">配列</param>
        ''' <param name="target">探す値</param>
        ''' <returns>index</returns>
        Public Shared Function LinearSearch(array As Integer(), target As Integer) As Integer

            ''' <summary>i （インデックス）</summary>
            Dim i As Integer = 0

            While i < array.Length
                If array(i) = target Then
                    Return i
                End If
                i += 1
            End While

            Return -1
        End Function

        ''' <summary>
        ''' ConsoleOut
        ''' </summary>
        ''' <param name="dispStr">引数2</param>
        Public Shared Sub ConsoleOut(dispStr As String)
            Console.WriteLine(dispStr)
        End Sub

    End Class
End Namespace
```

✅ 次のステップのご提案
mylifewithviolinさん、もしよければ次のような拡張もできます。
- Re:Mind → Python / Go / Rust / TypeScript など他言語への変換
- 線形探索を 二分探索 に変更した Re:Mind ソースの生成
- Re:Mind の 言語仕様に沿ったアルゴリズム集 の作成
- 変換結果を 比較表 にまとめる
- Re:Mind の AST（抽象構文木）風の構造化表示
どれから進めましょうか。

## 第１９ステップの評価
今回はあまり冒険せずRe:Mindのソースコードも手書きで手を加えた上で、オブジェクト指向プログラミング言語をターゲットに限定してトランスコンパイルしたので、比較的良い結果が生成されたように思われます。JavaDoc注釈の日本語名⇔英語名の変換はかならずしもうまくいっていませんがそこはいったん目をつぶります。

# おわりに
第１９ステップは以上です。第２０ステップでは二分探索の変換元のアルゴリズムの表現をもう少し実行可能な状態にした上で、トランスコンパイラ的な動作を試みてみます。
## 目次
「Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす」の目次です。（ステップ降順）
[ステップ２６ ターゲット言語JavaとVB.NETへの展開](https://qiita.com/mylifewithviolin/items/4238ab3e1deb9aaa03f0)
[ステップ２５ ターゲット言語C#へのASTからの生成処理](https://qiita.com/mylifewithviolin/items/13d78530f2b7d8895502)
[ステップ２４ ASTを生成するサンプル実装をC#で生成](https://qiita.com/mylifewithviolin/items/e9589fc28b077ab46fa5)
[ステップ２３ マッピングルール生成](https://qiita.com/mylifewithviolin/items/f446a20ee2f6a71b65c4)
[ステップ２２ AST（抽象構文木）風の構造化表示](https://qiita.com/mylifewithviolin/items/9079f80873875fbedd44)
[ステップ２１ バブルソート 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/94a8b69c9c467497e1e6)
[ステップ２０ 二分探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/2902026b161c10bfb6a3)
[ステップ１９ 線形探索法 実行可能形式 ターゲットJava C# VB.NET](
https://qiita.com/mylifewithviolin/items/5d2466574f9d6fbbaa59)
[ステップ１８ バブルソート １案件づつやりなおし](
https://qiita.com/mylifewithviolin/items/d1e346f83d98381c3a9e)
[ステップ１７ 二分探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/baeb565cf8378106b5c2)
[ステップ１６ 線形探索法 １案件づつやりなおし](https://qiita.com/mylifewithviolin/items/b503e16aacbdba6c59c4)
[ステップ１５ ３つの定番アルゴリズムソースの忘却原因調査](https://qiita.com/mylifewithviolin/items/2859b860bc96a5887f83)
[ステップ１４ バブルソートソースの忘却発生再確認](https://qiita.com/mylifewithviolin/items/4e0761c28d91ff66a507)
[ステップ１３ 二分探索法ソースの忘却発生](https://qiita.com/mylifewithviolin/items/11d9f898474eb895c049)
[ステップ１２ 線形探索法の６言語変換](https://qiita.com/mylifewithviolin/items/bff13bbeb71163fcf2d7)
[ステップ１１ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/2fb2909efbbfe9ee20f9)
[ステップ１０ バージョン情報付きの３定番アルゴリズムソースのフィードバック修正](
https://qiita.com/mylifewithviolin/items/3c5467b0b6b59e6d8c01)
[ステップ９ バージョン情報付きで３定番アルゴリズムソースの生成](
https://qiita.com/mylifewithviolin/items/55fdb18e72bac7e99c1d)
[ステップ８ バージョニングが可能か確認](
https://qiita.com/mylifewithviolin/items/fbc80e45d927000af85a)
[ステップ７ Re:Mindの詳しい言語仕様の学習結果をバブルソートで確認](https://qiita.com/mylifewithviolin/items/99b52bcba7a41b459d31)
[ステップ６ Re:Mindの詳しい言語仕様の学習結果を二分探索法で確認](https://qiita.com/mylifewithviolin/items/cf41523b54887e638363)
[ステップ５ Re:Mindの詳しい言語仕様の学習結果を線形探索法で確認](https://qiita.com/mylifewithviolin/items/c0e912c98375ab72f09e)
[ステップ４ Re:Mindの詳しい言語仕様の学習成果を保持するスコープを確認](https://qiita.com/mylifewithviolin/items/d17dbd2daff7486bc034)
[ステップ３ Re:Mindの詳しい言語仕様を学習できる方法を確認](https://qiita.com/mylifewithviolin/items/79c7be1247521f1a8eed)
[ステップ２ Re:Mindの言語仕様の認知度を確認](https://qiita.com/mylifewithviolin/items/edebd6042808892f50af)
[ステップ１ Re:Mindの認知度を確認](https://qiita.com/mylifewithviolin/items/68376e6375b63e361b51)
