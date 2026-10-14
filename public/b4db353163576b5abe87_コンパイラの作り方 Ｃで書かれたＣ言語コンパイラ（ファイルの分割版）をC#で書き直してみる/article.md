# はじめに

[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみています。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。参考サイトの9ccの「ステップ8: ファイル分割とMakefileの変更」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため、段階的に対応構文が増えていきます。

## この記事内容の作業環境
Windows11 Pro 22H2
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code) 1.78.0
gcc 11　11.3.0
C# 10 dotnet-sdk-6.0.404-win-x64

## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。

## 関連記事
参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」までに相当する内容を下記の記事で解説しております。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（四則演算版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)
「ステップ6：単項プラスと単項マイナス」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（単項演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/fb8dc06460855928162f)
「ステップ7：比較演算子」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)

この段階のCコンパイラの仕様を日本語ロジック仕様記述言語 Re:Mindで記述しています。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）のロジック仕様を日本語ロジック仕様記述言語 Re:Mind（リマインド）で記述してみる](https://qiita.com/mylifewithviolin/items/68577ea36b72ea9da473)

# ロジックのポイント
この状態のＣ言語コンパイラ（比較演算子版）は下記のBNFで記述された生成規則に対応したコンパイラを実装することにあります。
<pre>
expr       = equality
equality   = relational ("==" relational | "!=" relational)*
relational = add ("<" add | "<=" add | ">" add | ">=" add)*
add        = mul ("+" mul | "-" mul)*
mul        = unary ("*" unary | "/" unary)*
unary      = ("+" | "-")? primary
primary    = num | "(" expr ")
</pre>
オリジナルの上記のBNFを日本語表記にしたものが下記です。
<pre>
式         = 等式
等式       = 関係式("==" 関係式 | "!=" 関係式)*
関係式     = 加減式 ("<" 加減式 | "<=" 加減式 | ">" 加減式 | ">=" 加減式)*
加減式     = 乗除式 ("+" 乗除式 | "-" 乗除式)*
乗除式     = 単項式 ("*" 単項式 | "/" 単項式)*
単項式     = ("+" | "-")? 優先順位
優先順位   = 数 | "(" 式 ")
</pre>

# C言語のソースファイル分割をC#で行う方法

## C言語のソースファイル分割
参考サイトの9ccの「ステップ8: ファイル分割とMakefileの変更」では、将来的な保守性の向上のため、これまでのステップでは単一のファイルにソースコードを記述していたのを、以下のように分割するとしています。

・9cc.h: ヘッダファイル
・main.c: main関数
・parse.c: パーサ
・codegen.c: コードジェネレータ

## C#のソースファイル分割

C#ではヘッダファイルはないので、ソースコードファイルを以下のように分割しました。

・main.cs: main関数
・parse.cs: パーサ
・codegen.cs: コードジェネレータ

また、このＣ言語コンパイラのC#プロジェクトは、コンソールアプリケーションとして構成されているため、従来は

・program.cs:すべて

に下記のような名前空間とクラスで実装していました。
```cs:Program.cs
namespace CC9
{
    class Program
    {
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static int Main(string[] args)
        {
            // トークナイズする
            // パースする
            // 抽象構文木を下りながらコード生成
        }

        /// <summary>トークナイズする</summary>
        /// <param name="p">入力文字列</param>
        /// <returns>トークンリスト</returns>
        static List<Token> tokenize(string p) {
            // 入力文字列をトークナイズしてトークンリストを返す
        }

        /// <summary>式</summary>
        /// <param name="tokenList">トークンリスト</param>
        /// <param name="curIndex">現索引</param>
        /// <returns>等式</returns>
        static Node expr(List<Token> tokenList,ref int curIndex) {
            // パース開始する
        }
        
        /// <summary>コード生成</summary>
        /// <param name="node">ノード</param>
        static void gen(Node node) {
            // 抽象構文木を下りながらコード生成
        }
    }
}
```

この点、分割後のクラスの構成方法はいくつか考えられますが、現時点では分割クラスを使用することとしました。

```cs:main.cs
namespace CC9
{
    public partial class Program
    {
        /// <summary>メイン</summary>
        /// <param name="args">引数</param>
        static int Main(string[] args)
        {
            // トークナイズする
            // パースする
            // 抽象構文木を下りながらコード生成
        }
    }
}
```

```cs:parse.cs
namespace CC9
{
    public partial class Program
    {
        /// <summary>トークナイズする</summary>
        /// <param name="p">入力文字列</param>
        /// <returns>トークンリスト</returns>
        static List<Token> tokenize(string p) {
            // 入力文字列をトークナイズしてトークンリストを返す
        }

        /// <summary>式</summary>
        /// <param name="tokenList">トークンリスト</param>
        /// <param name="curIndex">現索引</param>
        /// <returns>等式</returns>
        static Node expr(List<Token> tokenList,ref int curIndex) {
            // パース開始する
        }
    }
}
```
BNFに対応するパース関連関数はすべてこのparse.csファイルに移動しています。
```cs:codegen.cs
namespace CC9
{
    public partial class Program
    {
        /// <summary>コード生成</summary>
        /// <param name="node">ノード</param>
        static void gen(Node node) {
            // 抽象構文木を下りながらコード生成
        }
    }
}
```

# ソースコード
GitHub [9cc2cs 9cc Split version of source files](https://github.com/mylifewithviolin/9cc2cs/commit/19857b7eb8de247361cca6a66c7066a5f9cf0e2c)

# おわりに
いよいよ次のステップは「変数」の対応開始です、ぐっと言語らしくなります。


# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c
