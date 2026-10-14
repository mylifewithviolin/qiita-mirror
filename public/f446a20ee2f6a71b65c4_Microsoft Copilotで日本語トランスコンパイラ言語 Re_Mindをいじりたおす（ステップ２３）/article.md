# はじめに
日本語トランスコンパイラ言語 Re:Mindはたてつけとしてはオープンな実装言語仕様のため、どなたでも処理系を実装することが可能です。逆転の発想で生成AIに実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみようと思っておりまして、これがなかなか難儀でしたが、最後の第２２ステップで有益なASTについての情報を生成してもらえたので、本記事はその続きの第２３ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用しますが、第１ステップのプロンプト実行以前、この１年くらいの間で日本語トランスコンパイラ言語 Re:Mindに関連するセッションはないものとします。第２２ステップの後にはサインアウトがあります。

# 第２３ステップ
定番アルゴリズムの線形探索法、二分探索法、バブルソートのソースコードを日本語トランスコンパイラ言語 Re:Mindでバージョニング情報を付与して再生しようとしてしまいましたが、そのような学習成果のストック的な展開は難しいことが判明。１案件づつシリアルに進めていくことにしましたところ、比較的正常な結果が返るようになりました。第１９，２０，２１ステップの生成レスポンスで、Copilotが次のステップのご提案として「Re:Mind の AST（抽象構文木）風の構造化表示」ということを提案したので第２２ステップでそれをやってみることにしました。今回はその時の生成レスポンスでAIが提案したマッピングルールについても情報を控えておくとします。

## プロンプト
- この AST から
- Java / C# / VB.NET コードを再生成する手順（マッピングルール）を明文化する これを具体的に深堀していただけますか？


## 生成レスポンス
もちろんmylifewithviolinさん、ここは Re:Mind 言語体系の“核”に触れる部分なので、丁寧に体系化していきます。
以下では、先ほど作成した AST（抽象構文木）風構造を前提に、
🎯 「AST → Java / C# / VB.NET」再生成のためのマッピングルール（正式仕様化）
として、言語非依存の AST から各言語のコードを生成するためのルールを、
・構文
・コメント（Javadoc / XML コメント）
・識別子変換
・制御構造
・式
・配列
・メソッド呼び出し
などの観点から体系化します。
これは Re:Mind トランスコンパイラのバックエンド仕様書としてそのまま使えるレベルまで深掘りします。

🧩 1. 全体構造のマッピングルール
=======================================
1-1. Namespace（名前空間）
|ASTノード|Java|C#|VB.NET| 
|:-|:-|:-|:-|
| NamespaceDeclaration | package <name>; | namespace <name> { ... } | Namespace <name> ... End Namespace | 

1-2. Class（クラス）
|AST|Java|C#|VB.NET| 
|:-|:-|:-|:-| 
| ClassDeclaration | public class ProgramType { ... } | public class ProgramType { ... } | Public Class ProgramType ... End Class | 

🧩 2. コメント（Javadoc / XML コメント）マッピング
============================================
Re:Mind のルール：
- Javadoc コメントは
日本語名 ↔ 英語名を逆転して出力する
- .NET 言語は XML コメントに変換する
2-1. Java の場合（Javadoc）
AST の例：
```json:json
"javadoc": {
  "summary": "バブルソートする",
  "params": [
    { "nameJa": "配列", "nameEn": "array" }
  ]
}
```

Java 出力：
```java:Java
/**
 * バブルソートする
 * @param array 配列
 */
```

2-2. C# / VB.NET の場合（XML コメント）
C#：
```cs:C#
/// <summary>
/// バブルソートする
/// </summary>
/// <param name="array">配列</param>
```

VB.NET：
```vb:VB.Net
''' <summary>
''' バブルソートする
''' </summary>
''' <param name="array">配列</param>
```


🧩 3. 識別子（名前）のマッピングルール
============================================
AST には必ず：
- name（日本語名）
- transpiledName（英語名）
が入っている。
ルール：

|種類|Java|C#|VB.NET| 
|:-|:-|:-|:-|
| クラス名 | transpiledName | 同左|同左| 
| メソッド名 | transpiledName |同左|同左| 
| ローカル変数 | transpiledName |同左|同左| 
| コメント内の変数名 | nameJaを使う |同左  |同左| 


例：
Re:Mind

```mind:Re:Mind
/** i */ ・int 外側 = 0
```

AST：
```json:json
"name": "外側",
"transpiledName": "outer"
```

Java：
```java:Java
/** i （外側） */
int outer = 0;
```

🧩 4. 文（Statement）マッピングルール
============================================
4-1. LocalVariableDeclaration
AST：
```json:json
{
  "type": "LocalVariableDeclaration",
  "variableType": "int",
  "name": "外側",
  "transpiledName": "outer",
  "initializer": { "type": "Literal", "value": 0 }
}
```

Java：
```java:Java
/** i （外側） */
int outer = 0;
```

C#：
```cs:C#
/// <summary>i （外側）</summary>
int outer = 0;
```

VB.NET：
```vb:VB.Net
''' <summary>i （外側）</summary>
Dim outer As Integer = 0
```


4-2. WhileStatement

AST：
```json:json
{
  "type": "WhileStatement",
  "condition": { ... },
  "body": [ ... ]
}
```

Java：
```java:Java
while (condition) {
    ...
}
```

C#：
```cs:C#
while (condition)
{
    ...
}
```

VB.NET：
```vb:VB.Net
While condition
    ...
End While
```


4-3. ForStatement
Java：
```java:Java
for (int i = 0; i < array.length; i++) { ... }
```

C#：
```cs:C#
for (int i = 0; i < array.Length; i++) { ... }
```

VB.NET：
```vb:VB.Net
For i As Integer = 0 To array.Length - 1
    ...
Next
```

※ VB.NET は To を使うため、AST の < 条件を Length - 1 に変換する必要がある。

🧩 5. 式（Expression）マッピングルール
============================================
5-1. BinaryExpression
AST：
```json:json
{
  "type": "BinaryExpression",
  "operator": "<",
  "left": { "type": "Identifier", "name": "i" },
  "right": { "type": "MemberAccess", ... }
}
```

Java/C#：
```java:Java/C#
i < array.length
```

VB.NET：
```vb:VB.Net
i < array.Length
```


5-2. MemberAccess
AST：
```json:json
{
  "type": "MemberAccess",
  "expression": { "type": "Identifier", "name": "配列", "transpiledName": "array" },
  "memberName": "Length"
}
```

Java：
```java:Java
array.length
```

C#：
```cs:C#
array.Length
```

VB.NET：
```vb:VB.Net
array.Length
```


5-3. ElementAccess（配列アクセス）
AST：
```json:json
{
  "type": "ElementAccess",
  "array": { "name": "配列", "transpiledName": "array" },
  "index": { "name": "内側", "transpiledName": "inner" }
}
```

Java/C#：
```java:Java/C#
array[inner]
```

VB.NET：
```vb:VB.Net
array(inner)
```


5-4. InvocationExpression（メソッド呼び出し）
AST：
```json:json
{
  "type": "InvocationExpression",
  "target": { "transpiledName": "bubbleSort" },
  "arguments": [...]
}
```

Java：
```java:Java
bubbleSort(array);
```

C#：
```cs:C#
BubbleSort(array);
```

VB.NET：
```vb:VB.Net
BubbleSort(array)
```


🧩 6. 配列リテラルのマッピング
============================================
AST：
```json:json
{
  "type": "ArrayLiteral",
  "values": [15, 13, 9, 6, 4, 1]
}
```

Java：
```java:Java
int[] array = {15, 13, 9, 6, 4, 1};
```

C#：
```cs:C#
int[] array = { 15, 13, 9, 6, 4, 1 };
```

VB.NET：
```vb:VB.Net
Dim array As Integer() = {15, 13, 9, 6, 4, 1}
```


🧩 7. メソッド宣言のマッピング
============================================
AST：
```json:json
{
  "type": "MethodDeclaration",
  "modifiers": ["public"],
  "returnType": "void",
  "name": "バブルソートする",
  "transpiledName": "bubbleSort",
  "parameters": [...]
}
```

Java：
```java:Java
public static void bubbleSort(int[] array) { ... }
```

C#：
```cs:C#
public static void BubbleSort(int[] array) { ... }
```

VB.NET：
```vb:VB.Net
Public Shared Sub BubbleSort(array As Integer())
    ...
End Sub
```
🧩 8. まとめ：AST → 各言語コード生成の全体フロー
============================================
AST
 ↓
識別子変換（日本語 → 英語）
 ↓
コメント変換（Javadoc / XML コメント）
 ↓
構文ノードごとのテンプレート適用
 ↓
言語固有の構文差分を適用
   - Java: package, length, for文
   - C#: namespace, Length, PascalCase
   - VB.NET: Namespace, End Class, array(), For To
 ↓
コード整形（インデント、改行）
 ↓
完成



🎉 mylifewithviolinさんへ：次のステップのご提案
このマッピングルールを使えば、Re:Mind → AST → 任意言語 の 正式なトランスコンパイラ仕様書が作れます。
次にできることとして：
✔ 1. このルールを「正式仕様書 PDF 風」にまとめる
✔ 2. AST → Java/C#/VB.NET の **コード生成テンプレート（雛形）**を作る
✔ 3. Re:Mind → AST の フロントエンド仕様も作る
✔ 4. AST から Mermaid フローチャート生成も可能
どれを進めてみたいですか。


## 第２３ステップの評価
どんな生成レスポンスがあるかまったく予想していませんでしたが、ひとつのトランスコンパイラ言語の一部仕様の（かなりRe:Mindの仕様に寄せた）AST仕様のテンプレとして超大量の出力があって驚きました。Jsonや言語別のコードブロックの枠の記述は手書きで追記しています。この仕様の細かい妥当性はまだ検証できませんので、現状有姿の参考情報という扱いでお願いします。現在わたしの方で開発中の実装はASTに明確には対応していません。参考情報として非常に有益のように受け止めております。他の方がASTベースで実装されることをさまたげるものでもありません。

# おわりに
第２３ステップは以上です。Re:Mindのアドベントカレンダーの枠としては第２２ステップで完了しましたが、Mindのアドベントカレンダーのシリーズ２の枠が少し空いていますので、間借りさせていただきました。
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
