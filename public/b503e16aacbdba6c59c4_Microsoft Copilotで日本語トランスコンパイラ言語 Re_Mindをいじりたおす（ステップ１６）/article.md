# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思ったのですが、これがなかなか難儀でした。本記事はその第１６ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１５ステップの後にはサインアウトがあります。

# 第１６ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにします。

## プロンプト
下記のソースコードは定番アルゴリズム：線形探索法を「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフト https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c 
に基づき生成したものです。
```mind:Re:Mind
/** LinearSearch
 * @param 配列 array
 * @param 探す値 target
 */
◇public int 線形探索する(int[] 配列, int 探す値)
  /** i */
  ・int インデックス = 0
  〇インデックス < 配列.Length の間は繰り返す
    ◇配列[インデックス] == 探す値 の場合
      □return インデックス
    ◇ここまで
    □インデックス++
  〇ここまで
  □return -1
◇ここまで
```

上記の日本語トランスコンパイラ言語 Re:Mindのソースコードを下記のプログラミング言語のソースコードに変換してください。
・Java
・C#
・Typescript
・Go
・VisualBasic.Net
・VisualBasic for Application

生成された変換後のソースコードを下記のバージョン情報で識別し、次回以降も参照できるように保持してください。
定番アルゴリズム：線形探索法・2025-12-08版・3回目からJava・2025-12-15-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からTypescript・2025-12-15-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からGo・2025-12-11-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic.Net・2025-12-15-1回目変換
定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic for Application・2025-12-15-1回目変換

変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.1ドラフトに記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c

Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。変換元のソースコードに記載のない事項をむりに創生しないでください。クラス宣言など。また変換元のソースコードに記載のある事項、たとえばローカル変数の宣言部のjavadocの注釈はトランスコンパイル後の英語変数名に変換し、日本語変数名を注釈にしてください。

## 生成レスポンス
了解しました。ご指定の Re:Mind ソースコードを各言語に忠実にトランスコンパイルします。仕様に従い、Javadoc系言語では日本語名と英語名を逆転、.NET系言語では XMLコメント仕様に変換しつつ逆転 を行います。また、不要なクラス宣言などは生成せず、関数本体のみを出力します。

### Java
（Javadoc仕様：日本語名と英語名を逆転）
```Java:Java
/**
 * 線形探索する
 * @param array 配列
 * @param target 探す値
 */
public int linearSearch(int[] array, int target) {
    /** インデックス */
    int index = 0;
    while (index < array.length) {
        if (array[index] == target) {
            return index;
        }
        index++;
    }
    return -1;
}
```
### C#
（.NET XMLコメント仕様：日本語名と英語名を逆転）
```Cs:C#
/// <summary>
/// 線形探索する
/// </summary>
/// <param name="array">配列</param>
/// <param name="target">探す値</param>
public int LinearSearch(int[] array, int target)
{
    /// <summary>インデックス</summary>
    int index = 0;
    while (index < array.Length)
    {
        if (array[index] == target)
        {
            return index;
        }
        index++;
    }
    return -1;
}
```

### TypeScript
（JSDoc仕様：日本語名と英語名を逆転）
```Ts:Typescript
/**
 * 線形探索する
 * @param array 配列
 * @param target 探す値
 */
function linearSearch(array: number[], target: number): number {
    /** インデックス */
    let index: number = 0;
    while (index < array.length) {
        if (array[index] === target) {
            return index;
        }
        index++;
    }
    return -1;
}
```

### Go
（Goは Javadoc/.NET コメント仕様を持たないため、通常のコメントで逆転）
```Go:Go
// 線形探索する
// array: 配列
// target: 探す値
func LinearSearch(array []int, target int) int {
    // インデックス
    index := 0
    for index < len(array) {
        if array[index] == target {
            return index
        }
        index++
    }
    return -1
}
```

### Visual Basic .NET
（.NET XMLコメント仕様：日本語名と英語名を逆転）
```vb:VB.Net
''' <summary>
''' 線形探索する
''' </summary>
''' <param name="array">配列</param>
''' <param name="target">探す値</param>
Public Function LinearSearch(array As Integer(), target As Integer) As Integer
    ''' <summary>インデックス</summary>
    Dim index As Integer = 0
    While index < array.Length
        If array(index) = target Then
            Return index
        End If
        index += 1
    End While
    Return -1
End Function
```

### Visual Basic for Applications (VBA)
（VBAは XMLコメント仕様を持たないため、通常コメントで逆転）
```vb:VBA
' 線形探索する
' array: 配列
' target: 探す値
Public Function LinearSearch(array() As Integer, target As Integer) As Integer
    ' インデックス
    Dim index As Integer
    index = 0
    Do While index < UBound(array) + 1
        If array(index) = target Then
            LinearSearch = index
            Exit Function
        End If
        index = index + 1
    Loop
    LinearSearch = -1
End Function
```

バージョン識別保持
以下の識別情報で保持しました。次回以降も参照可能です。
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からJava・2025-12-15-1回目変換
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からC#・2025-12-15-1回目変換
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からTypescript・2025-12-15-1回目変換
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からGo・2025-12-11-1回目変換
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic.Net・2025-12-15-1回目変換
- 定番アルゴリズム：線形探索法・2025-12-08版・3回目からVisualBasic for Application・2025-12-15-1回目変換

mylifewithviolinさん、この変換結果を次回以降も参照できるように保持しました。次は例えば「バイナリ探索法」など別アルゴリズムを Re:Mind から変換して比較してみますか？

## 第１６ステップの評価
ちょっと体調不要のため詳しくは精査できておりませんが、今回は具体的な過去ソースコードのコピーを提示した上で、かつ既存部分には余計な影響を与えずうまくトランスコンパイルできたようです。

# おわりに
第１６ステップは以上です。第１７ステップはこの調子でいったん生成されたRe:Mindの具体的なソースコードを提示して、トランスコンパイラ的な動作を試みています。
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
