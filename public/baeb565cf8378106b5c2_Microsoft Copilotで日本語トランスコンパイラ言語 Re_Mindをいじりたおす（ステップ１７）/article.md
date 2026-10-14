# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思ったのですが、これがなかなか難儀でした。本記事はその第１７ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１５ステップの後にはサインアウトがあります。

# 第１７ステップ
第１５ステップまでは定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。第１６ステップ以降は１案件づつシリアルに進めていくことにします。

## プロンプト
下記のソースコードは定番アルゴリズム：二分探索法を「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフト https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c 
に基づき生成したものです。
```mind:Re:Mind
/** BinarySearch
 * @param 配列 array
 * @param 探す値 target
 */
◇public int 二分探索する(int[] 配列, int 探す値)
  /** left */
  ・int 左端 = 0
  /** right */
  ・int 右端 = 配列.Length - 1
  〇左端 <= 右端 の間は繰り返す
    /** mid */
    ・int 中央 = (左端 + 右端) / 2
    ◇配列[中央] == 探す値 の場合
      □return 中央
    ◇ここまで
    ◇配列[中央] < 探す値 の場合
      □左端 = 中央 + 1
    ◇他に
      □右端 = 中央 - 1
    ◇ここまで
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
定番アルゴリズム：二分探索法・2025-12-08版・3回目からJava・2025-12-15-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からTypescript・2025-12-15-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からGo・2025-12-11-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からVisualBasic.Net・2025-12-15-1回目変換
定番アルゴリズム：二分探索法・2025-12-08版・3回目からVisualBasic for Application・2025-12-15-1回目変換

変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.1ドラフトに記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c

Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。変換元のソースコードに記載のない事項をむりに創生しないでください。クラス宣言など。また変換元のソースコードに記載のある事項、たとえばローカル変数の宣言部のjavadocの注釈はトランスコンパイル後の英語変数名に変換し、日本語変数名を注釈にしてください。

## 生成レスポンス
了解しました。ご指定の Re:Mind ソースコードを各言語に変換し、指定のバージョン識別情報に基づいて保持できる形で提示します。ポイントは以下です：
- Javadoc系言語（Java, TypeScript, Go） → コメントは「日本語名と英語名を逆転」して出力。
- .NET系言語（C#, VB.Net, VBA） → .NETコメント仕様に変換し、日本語名と英語名を逆転。
- クラス宣言などは生成せず、関数のみ。
- ローカル変数の宣言部の注釈も「英語変数名に変換し、日本語名を注釈」とする。


### Java

```Java:Java
/**
 * 二分探索する
 * @param array 配列
 * @param target 探す値
 */
public int binarySearch(int[] array, int target) {
    /** left 左端 */
    int left = 0;
    /** right 右端 */
    int right = array.length - 1;
    while (left <= right) {
        /** mid 中央 */
        int mid = (left + right) / 2;
        if (array[mid] == target) {
            return mid;
        }
        if (array[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```
### C#

```Cs:C#
/// <summary>
/// 二分探索する
/// </summary>
/// <param name="array">配列</param>
/// <param name="target">探す値</param>
public int BinarySearch(int[] array, int target)
{
    /// <summary>left 左端</summary>
    int left = 0;
    /// <summary>right 右端</summary>
    int right = array.Length - 1;
    while (left <= right)
    {
        /// <summary>mid 中央</summary>
        int mid = (left + right) / 2;
        if (array[mid] == target)
        {
            return mid;
        }
        if (array[mid] < target)
        {
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }
    return -1;
}
```

### TypeScript

```Ts:Typescript
/**
 * 二分探索する
 * @param array 配列
 * @param target 探す値
 */
function binarySearch(array: number[], target: number): number {
    /** left 左端 */
    let left: number = 0;
    /** right 右端 */
    let right: number = array.length - 1;
    while (left <= right) {
        /** mid 中央 */
        let mid: number = Math.floor((left + right) / 2);
        if (array[mid] === target) {
            return mid;
        }
        if (array[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1;
}
```

### Go

```Go:Go
// 二分探索する
// array 配列
// target 探す値
func BinarySearch(array []int, target int) int {
    // left 左端
    left := 0
    // right 右端
    right := len(array) - 1
    for left <= right {
        // mid 中央
        mid := (left + right) / 2
        if array[mid] == target {
            return mid
        }
        if array[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}
```

### Visual Basic .NET

```vb:VB.Net
''' <summary>
''' 二分探索する
''' </summary>
''' <param name="array">配列</param>
''' <param name="target">探す値</param>
Public Function BinarySearch(array As Integer(), target As Integer) As Integer
    ''' <summary>left 左端</summary>
    Dim left As Integer = 0
    ''' <summary>right 右端</summary>
    Dim right As Integer = array.Length - 1
    While left <= right
        ''' <summary>mid 中央</summary>
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
```

### Visual Basic for Applications (VBA)

```vb:VBA
' 二分探索する
' array 配列
' target 探す値
Public Function BinarySearch(array() As Integer, target As Integer) As Integer
    ' left 左端
    Dim left As Integer
    left = 0
    ' right 右端
    Dim right As Integer
    right = UBound(array)
    Do While left <= right
        ' mid 中央
        Dim mid As Integer
        mid = (left + right) \ 2
        If array(mid) = target Then
            BinarySearch = mid
            Exit Function
        End If
        If array(mid) < target Then
            left = mid + 1
        Else
            right = mid - 1
        End If
    Loop
    BinarySearch = -1
End Function
```

✅ 以上をそれぞれのバージョン識別情報に基づいて保持しました。
次回以降「定番アルゴリズム：二分探索法・2025-12-08版・3回目からJava・2025-12-15-1回目変換」などの識別名で呼び出すことが可能です。
mylifewithviolinさん、この後は例えば「Python版も追加して」といった拡張も可能ですが、まずはここまででご確認いただけますか。


## 第１７ステップの評価
ちょっと体調不要のため詳しくは精査できておりませんが、今回も具体的な過去ソースコードのコピーを提示した上で、かつ既存部分には余計な影響を与えずうまくトランスコンパイルできたようです。

# おわりに
第１７ステップは以上です。第１８ステップもこの調子でいったん生成されたRe:Mindの具体的なソースコードを提示して、トランスコンパイラ的な動作を試みています。
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
