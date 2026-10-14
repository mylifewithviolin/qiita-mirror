# はじめに

[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いています。[Ｃ言語コンパイラ（比較演算子版）](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)を書いた後、諸般の事情でしばらく中断したので、内容忘れてきたため、少し日本語記述というのを試みています。まず、[日本語関数名・変数名を使ったC#で書き直し](https://qiita.com/mylifewithviolin/items/890ed181ee72784a08f5)で、C#で書き直したソースの関数名・変数名を日本語にしてみた上で、これらの記事は差分表記となっているため、このレベルのCコンパイラの全体仕様も見えづらくなっているため、その[ロジック仕様を日本語ロジック仕様記述言語 Re:Mind（リマインド）で記述して](https://qiita.com/mylifewithviolin/items/68577ea36b72ea9da473)みました。
ここまで書いてみますと、実装はまだないのですが、日本語トランスコンパイラ言語 Re:Mind（リマインド）で記述してみるとどうなるのかというのが見たくなりました。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。参考サイトの9ccの「ステップ7: 比較演算子」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため、段階的に対応構文が増えていきます。オリジナルのC言語に関数名・変数名をそろえているC#の記事は[こちら](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)になります。

[日本語ロジック仕様記述言語 Re:Mind](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)はオープンな設計言語仕様で、どなたでもこの記法を使いロジックを記述することができます。こちらはいまのところなにか実装があるわけでなく、記述ルールがあるだけです。[日本語トランスコンパイラ言語 Re:Mind](https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad)は、日本語ロジック仕様記述言語 Re:Mindの記述を下書きとして受け取ることができますが、ターゲット言語のソースコードを出力させるため、ロジックの本質以外のところでいろいろ記述事項が必要となってきます。今回は仕様検討の一環として、このお題で[日本語トランスコンパイラ言語 Re:Mind 2022 Lv1ドラフト](https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad)のソースの記述例を作成し、C#に変換されたらこうなるというイメージを提示してみます。この場合はターゲットにはソースの日本語関数名・変数名のまま出力させるのではなくjavadocで変換後の英字名を指定して英字名で出力している想定としています。

## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code) 1.77.0
C# 10 dotnet-sdk-6.0.404-win-x64

## この記事内容の保証
※この記事には仕様的な情報と実装的な情報が含まれます。Cで書かれた引用ソースに対して、日本語トランスコンパイラ言語 Re:Mind（リマインド）で書かれた内容、C#で書かれた内容の等価性・妥当性は保証されません。C#で書かれた内容は手書きです。トランスコンパイラのソースは仕様イメージです。

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

# C#コンソールアプリケーションとしてコード出力するための記述
ロジックのポイントではないのですが、実装として C#コンソールアプリケーションとしてコード出力するため、若干の実装的な記述の追加が必要となります。これによりターゲット言語の既存ライブラリを使用可能とすることができます。

ロジック仕様記述言語としては実装の定義のない関数名をイメージとして記述して、ロジックの主旨を伝達させればよいとすることも可能なのですが、実装言語としては実装定義に紐づける必要があります。

ここからは上段を日本語トランスコンパイラ言語 Re:Mindのソースコードイメージ、下段をC#の出力ソースコードイメージとします。Re:Mindの実装はまだ存在しませんので、手書きで両者のソースコードの関係を定義・記述しています。

```mind:Re:Mind
/**
* CC9
*/
▽namespace Cコンパイラ9

    /**
    * Program
    */
    ▽class プログラム型

        //列挙体・内部クラスなど記述
        //Mainなど記述
        //Mainから呼ばれる各関数など記述
        //インライン関数記述

    △
 △

■using System 
//使用するC#のクラスライブラリ・メソッドの引用記述
■using System.Text.RegularExpressions
//使用するC#のクラスライブラリ・メソッドの引用記述

```

```cs:Program.cs
using System; 
using System.Text.RegularExpressions;


/// <summary>Cコンパイラ9</summary>
namespace CC9
{
    /// <summary>プログラム型</summary>
    class Program
    {

        //列挙体・内部クラスなど出力
        //Mainなど出力
        //Mainから呼ばれる各関数など出力
        //インライン関数記述

    }
}
```
## 使用するC#のクラスライブラリ・メソッドの引用記述
ある程度はライブラリとして用意しておく想定ですが、未対応の新規のターゲット言語のライブラリを引用する場合は、引用記述を追記することで記述可能となります。

```mind:Re:Mind
  ■using System
  ▼public static class コンソール Console
    ▼public static 改行表示する(string? value)
        WriteLine (string? value)
    ▲
    ▼public static 表示する(string? value)
        Write (string? value)
    ▲
    //他の利用関数・プロパティなど記述
 　▲

  ■using System.Text.RegularExpressions
  ▼public static class 正規表現 Regex

    ▼public static bool 合致するか(string input, string pattern)
        IsMatch (tring input, string pattern)
    ▲
    //他の利用関数・プロパティなど記述
 　▲

```

# Mainから呼ばれる各関数など記述
ここからMain関数までの記述は日本語ロジック仕様記述言語 Re:Mindの記述をベースに記述することが可能です。

javadocによる英字名の指定は省略可能です。省略した場合は[日本語関数名・変数名を使ったC#で書き直した記事](https://qiita.com/mylifewithviolin/items/890ed181ee72784a08f5)のような出力となる想定です。
指定した場合ターゲット言語がC#の場合はC# comment documentation で関数ヘッダに日本語名を出力する想定です。

## expr
exprの対応日本語名は下記のとおりとしています。
式

```mind:Re:Mind
    /**
    * expr
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return equality
    */
    ▽static ノード型 式(List<トークン型> トークンリスト,ref int 現索引) 
        等式(トークンリスト,現索引)を　返す
    △
```
```cs:Program.cs
    /// <summary>式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>等式</returns>
    static Node expr(List<Token> tokenList,ref int curIndex) {
        return equality(tokenList,ref curIndex);
    }
```
## equality
等しい、等しくない。
equalityの対応日本語名は下記のとおりとしています。
等式

```mind:Re:Mind
    /**
    * equality
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽static ノード型 等式(リスト型<トークン型> トークンリスト,ref int 現索引) 
        /** node */
        □ノード型 ノード = 関係式(トークンリスト,ref 現索引)
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        〇繰り返す
            ◇真==使用する(トークン,"-=",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較等号, ノード,  関係式(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇他に 真==使用する(トークン,"!=",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較不等号, ノード, 関係式(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇他に
                □ノード を返す
            ◇ここまで
        〇ここまで
    △
```

```cs:Program.cs
    /// <summary>等式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node equality(List<Token> tokenList,ref int curIndex) {
        Node node = relational(tokenList,ref curIndex);
        Token token = getToken(tokenList,curIndex);//次のトークン
        for (;;) {
            if (consume(token,"-=",ref curIndex)){
                node = new_binary(NodeKind.ND_EQ, node, relational(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
            }
            else if (consume(token,"!=",ref curIndex)){
                node = new_binary(NodeKind.ND_NE, node, relational(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
            }
            else
            return node;
        }
    }

```

## relational
大小関係。
relationalの対応日本語名は下記のとおりとしています。
関係式

```mind:Re:Mind
    /**
    * relational
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽static ノード型 関係式(リスト型<トークン型> トークンリスト,ref int 現索引) 
        /** node */
        □ノード型 ノード = 加減式(トークンリスト,ref 現索引)
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
        〇繰り返す
            ◇真==使用する(トークン,"<",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較小なり, ノード, 優先順位(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
            ◇他に 真==使用する(トークン,"<=",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較小なり等, ノード, 優先順位(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
            ◇他に 真==使用する(トークン,">",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較小なり, 加減式(トークンリスト,ref 現索引), ノード)
                □トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
            ◇他に 真==使用する(トークン,">=",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.比較小なり等, 加減式(トークンリスト,ref 現索引), ノード)
                □トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
            ◇他に
                □ノード を返す
            ◇ここまで
        〇ここまで
  △
```

```cs:Program.cs
    /// <summary>関係式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node relational(List<Token> tokenList,ref int curIndex) {
        Node node = add(tokenList,ref curIndex);
        Token token = getToken(tokenList,curIndex);//次のトークン
        for (;;) {
            if (consume(token,"<",ref curIndex)){
                                node = new_binary(NodeKind.ND_LT, node, primary(tokenList,ref curIndex));
                            token = getToken(tokenList,curIndex);//次のトークン
            }
            else if (consume(token,"<=",ref curIndex)){
                node = new_binary(NodeKind.ND_LE, node, primary(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else if (consume(token,">",ref curIndex)){
                node = new_binary(NodeKind.ND_LT, add(tokenList,ref curIndex), node);
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else if (consume(token,">=",ref curIndex)){
                node = new_binary(NodeKind.ND_LE, add(tokenList,ref curIndex), node);
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else
      return node;
  }
}
```

## add
addの対応日本語名は下記のとおりとしています。
加減式

```mind:Re:Mind
    /**
    * add
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽static ノード型 加減式(リスト型<トークン型> トークンリスト,ref int 現索引 )
        /** node */
        □ノード型 ノード = 乗除式(トークンリスト,ref 現索引)
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        〇繰り返す
            ◇真==使用する(トークン,"+",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.加算記号,ノード, 乗除式(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇他に 真==使用する(token,"-",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.減算記号, ノード, 乗除式(トークンリスト,ref 現索引))
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇他に
                □ノード を返す
            ◇ここまで
        〇ここまで
    △
```

```cs:Program.cs
    /// <summary>加減式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node add(List<Token> tokenList,ref int curIndex) {
        Node node = mul(tokenList,ref curIndex);
        Token token = getToken(tokenList,curIndex);//次のトークン
        for (;;) {
            if (consume(token,"+",ref curIndex)){
                node = new_binary(NodeKind.ND_ADD, node, mul(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else if (consume(token,"-",ref curIndex)){
                node = new_binary(NodeKind.ND_SUB, node, mul(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else
                return node;
        }
    }
```
## mul
mulの対応日本語名は下記のとおりとしています。
乗除式
```mind:Re:Mind
    /**
    * mul
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽static ノード型 乗除式(List<トークン型> トークンリスト,ref int 現索引) 
        /** node */
        □ノード型 ノード = 単項式(トークンリスト,ref 現索引);
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
      〇繰り返す
            ◇真==使用する(トークン,"*",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.乗算記号, ノード, 優先順位(トークンリスト,ref 現索引));
                □トークン = トークンを取得する(トークンリスト,現索引)  //次のトークン
            ◇他に 真==使用する(トークン,"/",ref 現索引) の場合
                □ノード = 新しい二分木(ノード種類.除算記号, ノード, 優先順位(トークンリスト,ref 現索引));
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇他に
                □ノード を返す
            ◇ここまで
        〇ここまで
    △
```
```cs:Program.cs
    /// <summary>乗除式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node mul(List<Token> tokenList,ref int curIndex) {
        //Node node = primary(tokenList,ref curIndex);
        Node node = unary(tokenList,ref curIndex);
        Token token = getToken(tokenList,curIndex);//次のトークン
        for (;;) {
            if (consume(token,"*",ref curIndex)){
                //node = new_node(NodeKind.ND_MUL, node, primary(tokenList,ref curIndex));
                node = new_binary(NodeKind.ND_MUL, node, primary(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
            }
            else if (consume(token,"/",ref curIndex)){
                //node = new_node(NodeKind.ND_DIV, node, primary(tokenList,ref curIndex));
                node = new_binary(NodeKind.ND_DIV, node, primary(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
            }
            else
            return node;
        }
    }
```
## unary
unaryの対応日本語名は下記のとおりとしています。
単項式
```mind:Re:Mind
    /**
    * unary
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽static ノード型  単項式(List<トークン型> トークンリスト,ref int 現索引) 
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        ◇真==使用する(トークン,"+",ref 現索引) の場合
            □単項式(トークンリスト,ref 現索引) を返す
        ◇他に 真==使用する(トークン,"-",ref 現索引) の場合
            □新しい二分木(ノード種類.減算記号,新しい整数(0), 単項式(トークンリスト,ref 現索引)) を返す
        ◇他に
            □優先順位(トークンリスト,ref 現索引) を返す
        ◇ここまで
    △
```
```cs:Program.cs
    /// <summary>単項式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node unary(List<Token> tokenList,ref int curIndex) { 
            Token token = getToken(tokenList,curIndex);//次のトークン
            if (consume(token,"+",ref curIndex)){
                return unary(tokenList,ref curIndex);
            }
            else if (consume(token,"-",ref curIndex)){
                return new_binary(NodeKind.ND_SUB,new_num(0), unary(tokenList,ref curIndex));
            }
            else
            return primary(tokenList,ref curIndex);
    }
```
## primary
primaryの対応日本語名は下記のとおりとしています。
優先順位
```mind:Re:Mind
    /**
    * primary
    * @param トークンリスト tokenList
    * @param 現索引 curIndex
    * @return node
    */
    ▽ノード型 優先順位(List<トークン型> トークンリスト,ref int 現索引) 
        /** token */
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
        // 次のトークンが"("なら、"(" expr ")"のはず
       ◇真==使用する(トークン,"(",ref 現索引) の場合
            □ノード型 ノード = 式(トークンリスト,ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □予想する(トークン,")",ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □ノード を返す
        ◇ここまで

        // そうでなければ数値のはず
        □新しい整数(整数を想定する(トークン,ref 現索引)) を返す
    △
```
```cs:Program.cs
    /// <summary>優先順位</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node primary(List<Token> tokenList,ref int curIndex) {
        Token token = getToken(tokenList,curIndex);//次のトークン
        // 次のトークンが"("なら、"(" expr ")"のはず
        if (consume(token,"(",ref curIndex)) {
            Node node = expr(tokenList,ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            expect(token,")",ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            return node;
        }

        // そうでなければ数値のはず
        //return new_node_num(expect_number(token,ref curIndex));
        return new_num(expect_number(token,ref curIndex));
    }

```
## consume
consumeの対応日本語名は下記のとおりとしています。
使用する

```mind:Re:Mind
    // 次のトークンが期待している記号のときには、トークンを1つ読み進めて
    // 真を返す。それ以外の場合には偽を返す。
    /**
    * consume
    * @param トークン token
    * @param 記号文字 op
    * @param 次索引 next
    * @return bool
    */
    ▽bool 使用する(トークン型トークン,string 記号文字, ref int 次索引) 
        ◇(トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.長さ || 
                    トークン.文字列 != 記号文字) の場合
            □偽 を返す
         ◇ここまで
         □次索引 = トークン.次索引;魏
         □真 を返す
    △
```
```cs:Program.cs
    // 次のトークンが期待している記号のときには、トークンを1つ読み進めて
    // 真を返す。それ以外の場合には偽を返す。
    /// <summary>使用する</summary>
    /// <param name="token">トークン</param>
    /// <param name="op">記号文字</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>
    static bool consume(Token token,string op, ref int next) {
        if (token.kind != TokenKind.TK_RESERVED || op.Length  != token.len || 
                token.str != op)
            return false;
        next = token.next;
        return true;
    }
```
## expect
expectの対応日本語名は下記のとおりとしています。
予想する

```mind:Re:Mind
    /**
    * expect
    * @param トークン token
    * @param 記号文字 op
    * @param 次索引 next
    * @return bool
    */
   ▽予想する(トークン型 トークン,string 記号文字, ref int 次索引) 
     ◇(トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.長さ || 
                    トークン.文字列 != 記号文字) の場合
           □エラー出力($"'{記号文字}'ではありません")
     ◇ここまで
           □次索引 = トークン.次索引
    △
```

```cs:Program.cs
    /// <summary>予想する</summary>
    /// <param name="token">トークン</param>
    /// <param name="op">記号文字</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>
   static  void expect(Token token,string op, ref int next) {
        if (token.kind != TokenKind.TK_RESERVED || op.Length  != token.len || 
                token.str != op)
            error($"'{op}'ではありません");
        next = token.next;
    }
```

## new_nodeとnew_binary
new_nodeがメモリ確保とノード種類のセットの単機能となり、new_binaryが従来のnew_nodeの役割を担っています。
new_nodeとnew_binaryを日本語化した関数名は下記のとおりとしています。
新しいノード
新しい二分木

```mind:Re:Mind
    /**
    * new_node
    * @param 種類 kind
    * @return node
    */
    ▽static ノード型 新しいノード(ノード種類 種類) 
        ・ノード型 ノード = new()
        □ノード.種類 = 種類
        □ノード を返す
   △

    /**
    * new_binary
    * @param 種類 kind
    * @param 左辺 lhs
    * @param 右辺 rhs
    * @return node
    */
    ▽static ノード型 新しい二分木(ノード種類 種類, ノード型 左辺, ノード型 右辺) 
        □ノード型 ノード = 新しいノード(種類)
        □ノード.左辺 = 左辺
        □ノード.右辺 = 右辺
        □ノード を返す
     △
```

```cs:Program.cs
    /// <summary>新しいノード</summary>
    /// <param name="kind">種類</param>
    /// <returns>ノード</returns>
    static Node new_node(NodeKind kind) {
        Node node = new();
        node.kind = kind;
        return node;
    }

    /// <summary>新しい二分木</summary>
    /// <param name="kind">種類</param>
    /// <param name="lhs">左辺</param>
    /// <param name="rhs">右辺</param>
    /// <returns>node</returns>
    static Node new_binary(NodeKind kind, Node lhs, Node rhs) {
        Node node = new_node(kind);
        node.lhs = lhs;
        node.rhs = rhs;
        return node;
    }
```

## tokenize
tokenizeの日本語化した関数名は下記のとおりとしています。
トークナイズする

```mind:Re:Mind
    // 入力文字列をトークナイズしてトークンリストを返す
    /**
    * tokenize
    * @param 入力文字列 p
    * @return tokenList
    */
    ▽リスト型<トークン型> トークナイズする(string 入力文字列) {
        /** next */
        ・int 次索引 = 1;
        /** cur */
        ・トークン型 現トークン = new();
        /** tokenList */
        ・リスト型<トークン型> トークンリスト =new リスト型<トークン型>();
        /** cs */
        ・var 入力文字列配列 = 入力文字列.ToCharArray();
        ・int i= 0;

        〇(i<入力文字列配列.Length) の間は繰り返す
            // 空白文字をスキップ
            ◇真==空白か判定する(入力文字列配列[i]) の場合
                □i++;
                □ループ先頭へ
            ◇ここまで
            // Multi-letter punctuator
            ◇真==比較記号頭文字か判定する(入力文字列配列[i]) の場合
                ◇(i+1<入力文字列配列.Length) の場合
                   ・string comp =入力文字列配列[i]+入力文字列配列[i+1]
                   ◇真==比較記号か判定する(comp)  の場合
                        □現トークン = 新しいトークン(トークン種類.予約語, 次索引, comp,2)
                        □トークンリスト.Add(現トークン)
                        □次索引++
                        □i+=2
                        □ループ先頭へ
                    ◇ここまで
                ◇ここまで
            ◇ここまで

            // Single-letter punctuator
            ◇真==演算子か判定する(入力文字列配列[i]) の場合
                □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 入力文字列配列[i],1)
                □トークンリスト.Add(現トークン)
                □次索引++
                □i++
                □ループ先頭へ
            ◇ここまで

            ◇真==数字か判定する(入力文字列配列[i]) の場合

                ・string 数字文字列 = 入力文字列配列[i]
                □i++
                ◇(i<入力文字列配列.Length) の場合
                    〇(数字か判定する(入力文字列配列[i])) の間は繰り返す
                        □数字文字列+= 入力文字列配列[i]
                        □i++
                        ◇(i>=入力文字列配列.Length) の場合 やめる
                    〇ここまで
                ◇ここまで
                □現トークン = 新しいトークン(トークン種類.整数,次索引, 数字文字列,i)
                □現トークン.値 = strtol(数字文字列)
                □トークンリスト.追加(現トークン)
                □次索引++
                □ループ先頭へ
            ◇ここまで
    
            //ここに進んだら例外
            □エラー出力("トークナイズできません")
            □i++
        〇ここまで

        □現トークン = 新しいトークン(トークン種類.終端,次索引, "",0)
        □トークンリスト.追加(現トークン)
        □トークンリスト を返す
    △
```

```cs:Program.cs
    // 入力文字列をトークナイズしてトークンリストを返す
    /// <summary>トークナイズする</summary>
    /// <param name="p">入力文字列</param>
    /// <returns>トークンリスト</returns>
    static List<Token> tokenize(string p) {
        //次索引
        int next = 1;
        //現トークン
        Token cur = new();
        //トークンリスト
        List<Token> tokenList =new List<Token>();

        //入力文字列配列
        var cs = p.ToCharArray();
        int i= 0;
        while(i<cs.Length) {
            // 空白文字をスキップ
            if (isspace(cs[i].ToString())) {
                i++;
                continue;
            }
            // Multi-letter punctuator
            if (iscomparisonhead(cs[i].ToString())) {
                if(i+1<cs.Length){
                    var comp =cs[i].ToString()+cs[i+1].ToString();
                    if (iscomparison(comp)) {
                        cur = new_token(TokenKind.TK_RESERVED, next, comp,2);
                        tokenList.Add(cur);
                        next++;
                        i+=2;
                        continue;
                    }
                }
            }

            // Single-letter punctuator
            if (isarithmetic(cs[i].ToString())) {
                cur = new_token(TokenKind.TK_RESERVED, next, cs[i].ToString(),1);
                tokenList.Add(cur);
                next++;
                i++;
                continue;
            }

            if (isdigit(cs[i].ToString())) {
    
                string numberStr = cs[i].ToString();
                i++;
                if(i<cs.Length){
                    while(isdigit(cs[i].ToString())) {
                        numberStr+= cs[i].ToString();
                        i++;
                        if(i>=cs.Length)break;
                    }
                }
                cur = new_token(TokenKind.TK_NUM,next, numberStr,i);
                cur.val = strtol(numberStr);
                tokenList.Add(cur);
                next++;
                continue;
            }

            //ここに進んだら例外
            error("トークナイズできません");
            i++;
        }

        cur = new_token(TokenKind.TK_EOF, next, "",0);
        tokenList.Add(cur);
        return tokenList;
    }
```
下記のサポート関数の関数名を
isspace　iscomparison　iscomparisonhead　isdigit isarithmetic　new_token
日本語化した関数名は下記のとおりとしています。
空白か判定する　比較記号か判定する　比較記号頭文字か判定する　数字か判定する 演算子か判定する　新しいトークン
これらの下請け関数はインライン記述例としてMain記述例の次に例示しています。



# 列挙体・内部クラスなど記述
## 列挙体、クラス(変数のみ)の宣言
```mind:Re:Mind
    /**
    * TokenKind
    */
   ▽列挙体 トークン種類
        /** TK_RESERVED */
        予約語,  // 記号
        /** TK_NUM */
        整数,      // 整数トークン
        /** TK_EOF */
        終端      // 入力の終わりを表すトークン
    △
    /**
    * Token
    */
    ▽クラス トークン型 
        /** Token kind */
        ・public トークン種類 種類 // Token kind
        /** next */
        ・public int 次索引    // Next token
        /** val */
        ・public int 値        // kindがTK_NUMの場合、その数値
        /** str */
        ・public string? 文字列     // Token string
        /** len */
        ・public int 長さ        // Token length
    △
```
```cs:Program.cs
    /// <summary>トークン種類</summary>
    enum TokenKind{
        /// <summary>予約語</summary>
        TK_RESERVED, // 記号
        /// <summary>整数/summary>
        TK_NUM,      // 整数トークン
        /// <summary>終端</summary>
        TK_EOF,      // 入力の終わりを表すトークン
    } 

    /// <summary>トークン型</summary>
    class Token {
        /// <summary>種類</summary>
        public TokenKind kind; // トークンの型
        /// <summary>次索引</summary>
        public  int next;    // 次の入力トークン
        /// <summary>値</summary>
        public int val;        // kindがTK_NUMの場合、その数値
        /// <summary>文字列</summary>
        public string? str;      // トークン文字列
        /// <summary>長さ</summary>
        public int len;        // トークンの長さ
        
    }
```
```mind:Re:Mind

    // 抽象構文木のノードの種類
    /**
    * NodeKind
    */
    ▽列挙体 ノード種類{
        /** ND_ADD */
        加算記号, // +
        /** ND_SUB */
        減算記号, // -
        /** ND_MUL */
        乗算記号, // *
        /** ND_DIV */
        除算記号, // /
        /** ND_EQ */
        比較等号,  // ==
        /** ND_NE */
        比較不等号,  // !=
        /** ND_LT */
        比較小なり,  // <
        /** ND_LE */
        比較小なり等,  // <=
        /** ND_NUM */
        整数 // 整数
    △

    // 抽象構文木のノードの型
    /**
    * Node
    */
    ▽クラス ノード型 {
        /** kind */
        ・public ノード種類 種類 // Node kind
        /** lhs */
        ・public ノード型? 左辺    // Left-hand side
        /** rhs */
        ・public ノード型? 右辺    // Right-hand side
        /** val */
        ・public int 値       // kindがND_NUMの場合のみ使う
    △
```

```cs:Program.cs

    // 抽象構文木のノードの種類
    /// <summary>ノード種類</summary>
    enum NodeKind{
        /// <summary>加算記号</summary>
        ND_ADD, // +
        /// <summary>減算記号</summary>
        ND_SUB, // -
        /// <summary>乗算記号</summary>
        ND_MUL, // *
        /// <summary>除算記号</summary>
        ND_DIV, // /
        /// <summary>比較等号</summary>
        ND_EQ,  // ==
        /// <summary>比較不等号</summary>
        ND_NE,  // !=
        /// <summary>比較小なり</summary>
        ND_LT,  // <
        /// <summary>比較小なり等</summary>
        ND_LE,  // <=
        /// <summary>整数</summary>
        ND_NUM, // 整数
    }

    // 抽象構文木のノードの型
    /// <summary>ノード型</summary>
    class  Node {
        /// <summary>種類</summary>
        public NodeKind kind; // ノードの型
        /// <summary>左辺</summary>
        public Node? lhs;     // 左辺
        /// <summary>右辺</summary>
        public Node? rhs;     // 右辺
        /// <summary>値</summary>
        public int val;       // kindがND_NUMの場合のみ使う
    }
```


## gen
genの日本語化した関数名は下記のとおりとしています。
コード生成


```mind:Re:Mind
    /**
    * gen
    * @param ノード node
    */
    ▽コード生成(ノード型 ノード) 
        ◇(ノード.種類 == ノード種類.整数) の場合
            □コンソール.表示する($"  push {ノード.値}\n")
            □返る
        ◇ここまで

        □コード生成(ノード.左辺)
        □コード生成(ノード.右辺)

        □コンソール.表示する("  pop rdi\n")
        □コンソール.表示する("  pop rax\n")

        ◇(ノード.種類)　で分岐する
        ◇ノード種類.加算記号
            □コンソール.表示する("  add rax, rdi\n")
            □脱する
        ◇ノード種類.減算記号
            □コンソール.表示する("  sub rax, rdi\n")
            □脱する
        ◇ノード種類.乗算記号
            □コンソール.表示する("  imul rax, rdi\n")
            □脱する
        ◇ノード種類.除算記号
            □コンソール.表示する("  cqo\n")
            □コンソール.表示する("  idiv rdi\n")
            □脱する
        ◇ノード種類.比較等号
            □コンソール.表示する("  cmp rax, rdi\n")
            □コンソール.表示する("  sete al\n")
            □コンソール.表示する("  movzb rax, al\n")
            □脱する
        ◇ノード種類.比較不等号
            □コンソール.表示する("  cmp rax, rdi\n")
            □コンソール.表示する("  setne al\n")
            □コンソール.表示する("  movzb rax, al\n")
            □脱する
        ◇ノード種類.比較小なり
            □コンソール.表示する("  cmp rax, rdi\n")
            □コンソール.表示する("  setl al\n")
            □コンソール.表示する("  movzb rax, al\n")
            □脱する
        ◇ノード種類.比較小なり等
            □コンソール.表示する("  cmp rax, rdi\n")
            □コンソール.表示する("  setle al\n")
            □コンソール.表示する("  movzb rax, al\n")
            □脱する
        ◇ここまで

        □脱コンソール出力("  push rax\n")
    △
```

```cs:Program.cs
    /// <summary>コード生成</summary>
    /// <param name="node">ノード</param>
   static void gen(Node node) {
        if (node.kind == NodeKind.ND_NUM) {
            Console.Write($"  push {node.val}\n");
            return;
        }

        gen(node.lhs);
        gen(node.rhs);

        Console.Write("  pop rdi\n");
        Console.Write("  pop rax\n");

        switch (node.kind) {
        case NodeKind.ND_ADD:
            Console.Write("  add rax, rdi\n");
            break;
        case NodeKind.ND_SUB:
            Console.Write("  sub rax, rdi\n");
            break;
        case NodeKind.ND_MUL:
            Console.Write("  imul rax, rdi\n");
            break;
        case NodeKind.ND_DIV:
            Console.Write("  cqo\n");
            Console.Write("  idiv rdi\n");
            break;
        case NodeKind.ND_EQ:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  sete al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case NodeKind.ND_NE:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setne al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case NodeKind.ND_LT:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setl al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case NodeKind.ND_LE:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setle al\n");
            Console.Write("  movzb rax, al\n");
            break;
        }

        Console.Write("  push rax\n");
    }

```


# Mainなど記述
## Main

```mind:Re:Mind

    /**
    * Main
    * @param 引数 args
    */
    ▽static int メイン(string[] 引数)

         ◇(引数.Length != 2) の場合
                □コンソール.表示する( "引数の個数が正しくありません\n");
                □1 を返す
         ◇ここまで

        // トークナイズする
        □リスト型<トークン型> トークンリスト = トークナイズする(引数[1]);
        // 現在着目しているトークン
        ・int 現索引=0
        // パースする
        □ノード型 ノード = 式(トークンリスト,ref 現索引)

        // アセンブリの前半部分を出力
        □コンソール.表示する(".intel_syntax noprefix\n")
        □コンソール.表示する(".globl main\n")
        □コンソール.表示する("main:\n")

        // 抽象構文木を下りながらコード生成
        □コード生成(ノード);

        // スタックトップに式全体の値が残っているはずなので
        // それをRAXにロードして関数からの返り値とする
        □コンソール.表示する("  pop rax\n")

        
        □コンソール.表示する("  ret\n")
        □0 を返す
    △
```

```cs:Program.cs
    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static int Main(string[] args)
    {
          if (args.Length != 2) {
                Console.Write( "引数の個数が正しくありません\n");
                return 1;
            }

        // トークナイズする
        List<Token> tokenList = tokenize(args[1]);
        // 現在着目しているトークン
        int curIndex=0;
        // パースする
        Node node = expr(tokenList,ref curIndex);

        // アセンブリの前半部分を出力
        Console.Write(".intel_syntax noprefix\n");
        Console.Write(".globl main\n");
        Console.Write("main:\n");

        // 抽象構文木を下りながらコード生成
        gen(node);

        // スタックトップに式全体の値が残っているはずなので
        // それをRAXにロードして関数からの返り値とする
        Console.Write("  pop rax\n");
      

        Console.Write("  ret\n");
        return 0;
    }
```
# インライン関数記述

開発ユーザーがターゲット言語を理解している場合は、ターゲット言語で直接記述することも可とし、ターゲット言語との相互運用に有利な環境を提供します。

```mind:Re:Mind

        ▼static bool 比較記号頭文字か判定する iscomparisonhead ( string input )
             if(input =="="||input =="!"||input =="<"||input ==">"){
                return true;
             }else{
                return false;
             }       
         ▲

        ▼static bool 比較記号か判定する iscomparison ( string input )
             if(input =="=="||input =="!="||input =="<="||input ==">="){
                return true;
             }else{
                return false;
             }       
        ▲

        ▼static bool 数字か判定する isdigit( string input )
             return( Regex.IsMatch( input, "[0-9]" ) );
        ▲

```

```cs:Program.cs
        static bool iscomparisonhead ( string input )
        {
             if(input =="="||input =="!"||input =="<"||input ==">"){
                return true;
             }else{
                return false;
             }       
         }

        static bool iscomparison ( string input )
        {
             if(input =="=="||input =="!="||input =="<="||input ==">="){
                return true;
             }else{
                return false;
             }       
         }

        static bool isdigit( string input )
        {
             return( Regex.IsMatch( input, "[0-9]" ) );
        }

```

# 入出力コード サンプルイメージ
この記事が対象としているchibicc(9cc)の対象構文は優先順位対応の四則演算に単項演算と比較演算子を加えただけで、変数も導入前のものですから、解釈できるのは下記のような四則演算と比較演算だけです。
```C:C
5 + 6 * 7
5 * ( 9 - 6 )
( 3 + 5 ) / 2
- 10 + 20
2 != 1
1 == 1
1 >= 1
2 <= 1
2 > 1
2 < 1
```
今回は2 != 1を対象にchibicc(9cc)と同じアセンブラを出力します。
## chibicc(9cc)単項演算子版の実行結果
C#との比較用の期待結果として9ccを実行してみます。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
```:2 != 1
$ ./a.out "2 != 1"
.intel_syntax noprefix
.global main
main:
  push 2
  push 1
  pop rdi
  pop rax
  cmp rax, rdi
  setne al
  movzb rax, al
  push rax
  pop rax
  ret
```

# 実行結果
## コンパイラの出力コード
続いてC#をコンパイルします。ビルド（コンパイル）はVSCodeのタスクで実行しました。
（手書きのC#のコードの出力結果です。）
9ccと同じ四則演算文字列を与えて実行すると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。
```:2 != 1
>9cc s "2 !=1 " 
.intel_syntax noprefix
.globl main
main:
  push 2
  push 1
  pop rdi
  pop rax
  cmp rax, rdi
  setne al
  movzb rax, al
  push rax
  pop rax
  ret
```
もう少しテストケースを増やした結果をあとで追記します。
# ソースコード
GitHub [9cc2cs 9cc comparison operator version with c# documentation comments](https://github.com/mylifewithviolin/9cc2cs/commit/0eae1f1df76d56af3754720d3374d095a4db22f1)

# おわりに

[日本語トランスコンパイラ言語 Re:Mind](https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad)は、制御構文の開始シンボルとして、◇、〇、□、・などの全角記号を用い、箇条書きされた日本文としての体裁を[日本語ロジック仕様記述言語 Re:Mind](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)の構文と共有しています。

今回は日本語トランスコンパイラ言語 Re:Mindによる記述ですが、あくまで言語仕様のイメージで、まだ実際にC#などターゲット言語に変換できる実装は存在しません。


# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539

https://qiita.com/mylifewithviolin/items/890ed181ee72784a08f5

https://qiita.com/mylifewithviolin/items/68577ea36b72ea9da473
