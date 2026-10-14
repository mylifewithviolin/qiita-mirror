# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思います。本記事はその第１２ステップで、最初のトランスコンパイラ的な動作となりす。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１１ステップの後にはサインアウトがあります。

# 第１２ステップ
第１１ステップでは、定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しました。

第１１ステップの生成バージョンを下記のバージョン情報で識別します。
定番アルゴリズム：線形探索法・2025-12-08版・3回目
定番アルゴリズム：二分探索法・2025-12-08版・3回目
定番アルゴリズム：バブルソート・2025-12-08版・3回目

上記バージョンの線形探索法の日本語トランスコンパイラ言語 Re:Mindによるソースコードを下記のプログラミング言語のソースコードにトランスコンパイルします。
Java
C#
Typescript
Go
VisualBasic.Net
VisualBasic for Application


## プロンプト
下記のバージョン情報で識別される
定番アルゴリズム：線形探索法・2025-12-08版・3回目
日本語トランスコンパイラ言語 Re:Mindのソースコードを下記のプログラミング言語のソースコードに変換してください。
・Java
・C#
・Typescript
・Go
・VisualBasic.Net
・VisualBasic for Application
生成された変換後のソースコードを下記のバージョン情報で識別し、次回以降も参照できるように保持してください。
定番アルゴリズム：線形探索法・2025-12-08版・3回目からJava・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からTypescript・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からGo・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic.Net・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic for Application・2025-12-11-1回目変換
変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.1ドラフトに記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c
Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。

## 生成レスポンス
承知しました。指定された「定番アルゴリズム：線形探索法・2025-12-08版・3回目」を各言語に変換し、バージョン情報を付与して保持できるように提示します。ポイントは以下です：
- Java / TypeScript → Javadocスタイルのコメントを使用し、日本語名と英語名を逆転して出力。
- C# / VisualBasic.Net / VBA → .NET系コメント仕様（XMLドキュメントコメントや ' コメント）に変換し、日本語名と英語名を逆転して出力。
- Go → Goのコメント仕様に合わせ、関数直前に // コメントで注釈。

定番アルゴリズム：線形探索法・2025-12-08版・3回目からJava・2025-12-11-1回目変換
```Java:Java
/**
 * LinearSearch
 * @param array 配列
 * @param target 探す値
 */
public class LinearSearch {
    public int 線形探索する(int[] array, int target) {
        int インデックス = 0;
        while (インデックス < array.length) {
            if (array[インデックス] == target) {
                return インデックス;
            }
            インデックス++;
        }
        return -1;
    }
}
```

定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-11-1回目変換
```Cs:C#
/// <summary>
/// LinearSearch
/// </summary>
/// <param name="array">配列</param>
/// <param name="target">探す値</param>
public class LinearSearch {
    public int 線形探索する(int[] array, int target) {
        int インデックス = 0;
        while (インデックス < array.Length) {
            if (array[インデックス] == target) {
                return インデックス;
            }
            インデックス++;
        }
        return -1;
    }
}
```
定番アルゴリズム：線形探索法・2025-12-08版・3回目からTypescript・2025-12-11-1回目変換
```Ts:Typescript
/**
 * LinearSearch
 * @param array 配列
 * @param target 探す値
 */
class LinearSearch {
    線形探索する(array: number[], target: number): number {
        let インデックス: number = 0;
        while (インデックス < array.length) {
            if (array[インデックス] === target) {
                return インデックス;
            }
            インデックス++;
        }
        return -1;
    }
}
```
定番アルゴリズム：線形探索法・2025-12-08版・3回目からGo・2025-12-11-1回目変換

```Go:Go
// LinearSearch
// @param array 配列
// @param target 探す値
package main

import "fmt"

func 線形探索する(array []int, target int) int {
    インデックス := 0
    for インデックス < len(array) {
        if array[インデックス] == target {
            return インデックス
        }
        インデックス++
    }
    return -1
}

func main() {
    fmt.Println(線形探索する([]int{1,2,3,4}, 3))
}

```
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic.Net・2025-12-11-1回目変換
```vb:VB.Net
''' <summary>
''' LinearSearch
''' </summary>
''' <param name="array">配列</param>
''' <param name="target">探す値</param>
Public Class LinearSearch
    Public Function 線形探索する(array As Integer(), target As Integer) As Integer
        Dim インデックス As Integer = 0
        While インデックス < array.Length
            If array(インデックス) = target Then
                Return インデックス
            End If
            インデックス += 1
        End While
        Return -1
    End Function
End Class
```
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic for Application・2025-12-11-1回目変換
```vb:VBA
' LinearSearch
' @param array 配列
' @param target 探す値
Function 線形探索する(array As Variant, target As Integer) As Integer
    Dim インデックス As Integer
    インデックス = 0
    Do While インデックス < UBound(array) + 1
        If array(インデックス) = target Then
            線形探索する = インデックス
            Exit Function
        End If
        インデックス = インデックス + 1
    Loop
    線形探索する = -1
End Function
```
これで各言語への変換が完了しました。この形式で「二分探索法」や「バブルソート」も同じルールで展開していけば、Re:Mind仕様から各言語への体系的な変換集が構築できますね。


## 第１２ステップの評価
今回はトランスコンパイルのファーストトライでした。概ね想定どおりといえば想定どおりで、最初かから完全は期待しておりませんでした。そもそもレファレンス実装もしていないので、最初から実装されているかのようなことを期待するのはぜいたくすぎると言えるでしょう。
Re:Mind側でターゲット言語がオプジェクト指向言語の場合はクラス情報を指定できるのですが、今回はあくまでフラグメント状態で定番アルゴリズム：線形探索法のロジックを記述しているため、トランスコンパイル後はどのように生成AIがさばいてくるのかは要確認事項でした。
クラス名が英語になった形の場合、関数名が日本語のままのようでした。変数も引数は変換されましたが、ローカル変数は日本語のままのようで、JavaDoc相当の備考も出力されませんでした。

# おわりに
第１２ステップは以上です。第１３ステップはRe:Mind側ソースコードは現状を維持してトランスコンパイル結果の改善を試みてみます。
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
