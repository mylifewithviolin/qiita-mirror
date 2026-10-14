# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思ったのですが、これがなかなか難儀でした。本記事はその第１８ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第１５ステップの後にはサインアウトがあります。

# 第１８ステップ
第１５ステップまでは定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。第１６ステップ以降は１案件づつシリアルに進めていくことにします。

## プロンプト
下記のソースコードは定番アルゴリズム：バブルソートを「オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）」の仕様情報2023 Lv1.1ドラフト https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c 
に基づき生成したものです。
```mind:Re:Mind
/** BubbleSort
 * @param 配列 array
 */
◇public void バブルソートする(int[] 配列)
  /** i */
  ・int 外側 = 0
  〇外側 < 配列.Length の間は繰り返す
    /** j */
    ・int 内側 = 0
    〇内側 < 配列.Length - 外側 - 1 の間は繰り返す
      ◇配列[内側] > 配列[内側 + 1] の場合
        /** temp */
        ・int 一時 = 配列[内側]
        □配列[内側] = 配列[内側 + 1]
        □配列[内側 + 1] = 一時
      ◇ここまで
      □内側++
    〇ここまで
    □外側++
  〇ここまで
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
定番アルゴリズム：バブルソート・2025-12-08版・3回目からJava・2025-12-15-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からTypescript・2025-12-15-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からGo・2025-12-11-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からC#・2025-12-15-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic.Net・2025-12-15-1回目変換
定番アルゴリズム：バブルソート・2025-12-08版・3回目からVisualBasic for Application・2025-12-15-1回目変換

変換すルールは下記のリンク、オープンな実装言語仕様 日本語トランスコンパイラ言語 Re:Mind（リマインド）2023 Lv1.1ドラフトに記載の仕様に従ってください。
https://qiita.com/mylifewithviolin/items/ee1a16a363aaa4fe3f4c

Re:Mind上のJavadocの注釈はJavadocを注釈する仕様とするプログラミング言語の場合は日本語名と英語名を逆転して出力するのを忘れないでください。.NET言語のコメント仕様の言語の場合は.NET言語のコメント仕様に変換して、日本語名と英語名を逆転して出力してください。変換元のソースコードに記載のない事項をむりに創生しないでください。クラス宣言など。また変換元のソースコードに記載のある事項、たとえばローカル変数の宣言部のjavadocの注釈はトランスコンパイル後の英語変数名に変換し、日本語変数名を注釈にしてください。

## 生成レスポンス
承知しました。Re:Mind のバブルソート実装を各言語に変換し、指定のバージョン識別情報に基づいて保持できる形で提示します。ポイントは前回と同様に：
• 	Java, TypeScript, Go → Javadocスタイルで「日本語名と英語名を逆転」して出力。
• 	.NET系（C#, VB.Net, VBA） → .NETコメント仕様に変換し、日本語名と英語名を逆転。
• 	クラス宣言などは生成せず、関数のみ。
• 	ローカル変数の宣言部の注釈も「英語変数名に変換し、日本語名を注釈」とする。


### Java

```Java:Java
/**
 * バブルソートする
 * @param array 配列
 */
public void bubbleSort(int[] array) {
    /** outer 外側 */
    int outer = 0;
    while (outer < array.length) {
        /** inner 内側 */
        int inner = 0;
        while (inner < array.length - outer - 1) {
            if (array[inner] > array[inner + 1]) {
                /** temp 一時 */
                int temp = array[inner];
                array[inner] = array[inner + 1];
                array[inner + 1] = temp;
            }
            inner++;
        }
        outer++;
    }
}
```
### C#

```Cs:C#
/// <summary>
/// バブルソートする
/// </summary>
/// <param name="array">配列</param>
public void BubbleSort(int[] array)
{
    /// <summary>outer 外側</summary>
    int outer = 0;
    while (outer < array.Length)
    {
        /// <summary>inner 内側</summary>
        int inner = 0;
        while (inner < array.Length - outer - 1)
        {
            if (array[inner] > array[inner + 1])
            {
                /// <summary>temp 一時</summary>
                int temp = array[inner];
                array[inner] = array[inner + 1];
                array[inner + 1] = temp;
            }
            inner++;
        }
        outer++;
    }
}
```

### TypeScript

```Ts:Typescript
/**
 * バブルソートする
 * @param array 配列
 */
function bubbleSort(array: number[]): void {
    /** outer 外側 */
    let outer: number = 0;
    while (outer < array.length) {
        /** inner 内側 */
        let inner: number = 0;
        while (inner < array.length - outer - 1) {
            if (array[inner] > array[inner + 1]) {
                /** temp 一時 */
                let temp: number = array[inner];
                array[inner] = array[inner + 1];
                array[inner + 1] = temp;
            }
            inner++;
        }
        outer++;
    }
}
```

### Go

```Go:Go
// バブルソートする
// array 配列
func BubbleSort(array []int) {
    // outer 外側
    outer := 0
    for outer < len(array) {
        // inner 内側
        inner := 0
        for inner < len(array)-outer-1 {
            if array[inner] > array[inner+1] {
                // temp 一時
                temp := array[inner]
                array[inner] = array[inner+1]
                array[inner+1] = temp
            }
            inner++
        }
        outer++
    }
}
```

### Visual Basic .NET

```vb:VB.Net
''' <summary>
''' バブルソートする
''' </summary>
''' <param name="array">配列</param>
Public Sub BubbleSort(array As Integer())
    ''' <summary>outer 外側</summary>
    Dim outer As Integer = 0
    While outer < array.Length
        ''' <summary>inner 内側</summary>
        Dim inner As Integer = 0
        While inner < array.Length - outer - 1
            If array(inner) > array(inner + 1) Then
                ''' <summary>temp 一時</summary>
                Dim temp As Integer = array(inner)
                array(inner) = array(inner + 1)
                array(inner + 1) = temp
            End If
            inner += 1
        End While
        outer += 1
    End While
End Sub
```

### Visual Basic for Applications (VBA)

```vb:VBA
' バブルソートする
' array 配列
Public Sub BubbleSort(array() As Integer)
    ' outer 外側
    Dim outer As Integer
    outer = 0
    Do While outer < UBound(array) + 1
        ' inner 内側
        Dim inner As Integer
        inner = 0
        Do While inner < UBound(array) - outer
            If array(inner) > array(inner + 1) Then
                ' temp 一時
                Dim temp As Integer
                temp = array(inner)
                array(inner) = array(inner + 1)
                array(inner + 1) = temp
            End If
            inner = inner + 1
        Loop
        outer = outer + 1
    Loop
End Sub
```

✅ 以上をそれぞれのバージョン識別情報に基づいて保持しました。
次回以降「定番アルゴリズム：バブルソート・2025-12-08版・3回目からJava・2025-12-15-1回目変換」などの識別名で呼び出すことが可能です。
mylifewithviolinさん、この後は「挿入ソート」や「選択ソート」など他の定番アルゴリズムも同じ形式で追加していくこともできます。続けますか。


## 第１８ステップの評価
ちょっと体調不要のため詳しくは精査できておりませんが、今回も具体的な過去ソースコードのコピーを提示した上でならば、かつ既存部分には余計な影響を与えずうまくトランスコンパイルできたようです。

# おわりに
第１８ステップは以上です。第１９ステップでは変換元のアルゴリズムの表現をもう少し実行可能な状態にした上で、トランスコンパイラ的な動作を試みてみます。
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
