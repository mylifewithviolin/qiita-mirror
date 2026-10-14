# はじめに
生成AIに日本語トランスコンパイラ言語 Re:Mindの実装言語仕様を読み込ませて、いくつかの抽象度レベルのプロンプトからトランスコンパイラ的な動きをさせてみたところ、Re:Mindっぽい仕様のASTパーサのテンプレと３言語（Java,C#，VB.NET）のコードジェネレータのテンプレを生成してもらえた[^1]ので、ASTパーサが動作するまでの検証[^2]を経て本記事はC#コードジェネレータが動作するまでの改修の第３ステップです。

# Microsoft Copilot
生成AIはWindows11アプリケーションのMicrosoft Copilotとします。モードは「Smart(GPT5.1)」。サインインした状態で使用します。

# 第３ステップ
「Re:MindのASTパーサが動作するまで」の１２ステップでいったんC#のソースコードが生成されるようにはなりましたので、以降はC#コードジェネレータが正常動作することを目指しています。

## プロンプト
今回追加したGenerateInvocationのコンパイルエラーはなくなりましたが、このメソッドの参照元がまだ0のようです。GenerateInvocationはどこから呼び出されますか？

## 生成レスポンス
ここがポイントです。
GenerateInvocation は “まだ一度も呼ばれていません”。
理由はとてもシンプルで、CSharpCodeGenerator の中で GenerateInvocation を呼ぶコードが存在しないからです。

🎯 なぜ呼ばれないのか？
あなたの CSharpCodeGenerator の GenerateExpression はこうなっています：
```cs:
InvocationExpression inv => 
    $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
```
つまり：
- InvocationExpression を見つけても、GenerateInvocation を使っていない
- そのため、Imports の AliasClass を参照する処理が一切走らない
- 結果として GenerateInvocation の参照元は 0 のまま

🎯 ではどうすれば呼ばれるのか？
GenerateExpression の InvocationExpression の分岐を差し替える必要があります。
つまり：
```cs:
InvocationExpression inv => GenerateInvocation(inv, _aliasMap),
```
のように、GenerateInvocation を呼ぶようにします。

✨ 完全な修正手順
① CSharpCodeGenerator に aliasMap を保持するフィールドを追加
```cs:
private Dictionary<string, AliasClass> _aliasMap;
```

② Generate(CompilationUnit cu) の最初で aliasMap を構築
```cs:
public string Generate(CompilationUnit cu)
{
    _aliasMap = BuildAliasMap(cu);
    ...
}
```
③ GenerateExpression の InvocationExpression 分岐を差し替える
元のコード：
```cs:
InvocationExpression inv =>
    $"{GenerateExpression(inv.Target)}({string.Join(", ", inv.Arguments.Select(GenerateExpression))})",
```
これを GenerateInvocation を呼ぶ形に変更：
```cs:
InvocationExpression inv => GenerateInvocation(inv, _aliasMap),
```
🎉 これで何が起きるか？
Re:Mind：
```
□コンソール.一行表示する(引数2)
```

AST：
```
InvocationExpression
  Target = MemberAccessExpression("コンソール", "一行表示する")
  Arguments = [ IdentifierExpression("引数2") ]
```

Imports：
```
コンソール → Console
一行表示する → WriteLine
```

C# 出力：
```
Console.WriteLine(dispStr);
```

ついに consoleOut の中身が生成されるようになります。


ここまで来ると Re:Mind → AST → C# のフルパイプラインが完成 します。
次は Java / VB.NET 版のコードジェネレータも同じ仕組みで作れますね。
必要なら、Java 版の GenerateInvocation も一緒に作りましょう。



## 第３ステップの評価
書き換えたGenerateExpressionは呼ばれるようになっていきますが、まだstatic void consoleOutの定義が出力されないようでした。

# おわりに
第３ステップは以上です。次回の方向性は上記の結果の提示からとなります。



:::note warn
生成レスポンスセクションの内容は生成AIが生成したものです。引用されているソースコードは完全には動作しない状態が含まれます。
:::

[^1]: Microsoft Copilotで日本語トランスコンパイラ言語 Re:Mindをいじりたおす - Qiita
「Re:Mindをいじりたおす」の記事リストです。（ステップ降順）
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
[^2]: Copilotが生成した日本語トランスコンパイラ言語 Re:MindのASTパーサが動作するまで - Qiita
「Re:MindのASTパーサが動作するまで」の記事リストです。（ステップ降順）
[ステップ１２ いったん生成](https://qiita.com/mylifewithviolin/items/f4b81da5d58396243e6d)
[ステップ１１](
https://qiita.com/mylifewithviolin/items/9c891cdcc8d2bd78f36f)
[ステップ１０ 生成済コードの伝達完了](
https://qiita.com/mylifewithviolin/items/a0b5747e40e7b545175a)
[ステップ９](
https://qiita.com/mylifewithviolin/items/f34548d50a974fb4420e)
[ステップ８](
https://qiita.com/mylifewithviolin/items/cb8f54f87329d7e62c9a)
[ステップ７](https://qiita.com/mylifewithviolin/items/1e05c80a0cad0580f073)
[ステップ６ 生成済コードの伝達開始](https://qiita.com/mylifewithviolin/items/31e8413e0789e5433705)
[ステップ５](https://qiita.com/mylifewithviolin/items/2af14676b1c267af22a2)
[ステップ４ Program.csが動作](https://qiita.com/mylifewithviolin/items/b037019608d6b5d068a7)
[ステップ３](https://qiita.com/mylifewithviolin/items/7c9568d238550b997e21)
[ステップ２](https://qiita.com/mylifewithviolin/items/076e1a792b8545fae7a6)
[ステップ１ 検証環境構築](https://qiita.com/mylifewithviolin/items/d1de6cd480055719602e)
