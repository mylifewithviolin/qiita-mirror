# はじめに

[トランスコンパイラ試作品の内部設計に進行しています](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)が、これがけっこう難航しておりまして、こっちはあまり進捗がないまま記事の未投稿が続くのもなんですので、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみていますの続きです。また、[日本語ロジック記述言語 Re:Mind](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94)によるロジック仕様も引き続き併記しています。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。参考サイトの9ccの「ステップ10：複数文字のローカル変数」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため、段階的に対応構文が増えていきます。

## この記事内容の作業環境
Windows11 Pro 22H2
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　1.78.2
gcc 11　11.3.0
C# 10 dotnet-sdk-6.0.404-win-x64

## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。

## 関連記事

<details><summary>ステップ5から7まで</summary>

参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」までに相当する内容を下記の記事で解説しております。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（四則演算版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)
「ステップ6：単項プラスと単項マイナス」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（単項演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/fb8dc06460855928162f)
「ステップ7：比較演算子」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)

この段階のCコンパイラの仕様を日本語ロジック仕様記述言語 Re:Mindで記述しています。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）のロジック仕様を日本語ロジック仕様記述言語 Re:Mind（リマインド）で記述してみる](https://qiita.com/mylifewithviolin/items/68577ea36b72ea9da473)
</details>

「ステップ8: ファイル分割とMakefileの変更」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（ファイルの分割版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/b4db353163576b5abe87)
「ステップ9: 1文字のローカル変数」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（1文字のローカル変数版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/47b5cda334b5bddbc63c)

# ロジックのポイント
この状態のＣ言語コンパイラ（複数文字のローカル変数版）は下記の拡張BNFで記述された生成規則に対応したコンパイラを実装することにあります。
<pre>
program    = stmt*
stmt       = expr ";"
expr       = assign
assign     = equality ("=" assign)?
equality   = relational ("==" relational | "!=" relational)*
relational = add ("<" add | "<=" add | ">" add | ">=" add)*
add        = mul ("+" mul | "-" mul)*
mul        = unary ("*" unary | "/" unary)*
unary      = ("+" | "-")? primary
primary    = num  | ident | "(" expr ")
</pre>
オリジナルの上記の拡張BNFを日本語表記にしたものが下記です。
<pre>
手続全体   = 構文*
構文       = 式 ";"
式       　= 代入式
代入式     = 等式 ("=" 代入式)?
等式       = 関係式("==" 関係式 | "!=" 関係式)*
関係式     = 加減式 ("<" 加減式 | "<=" 加減式 | ">" 加減式 | ">=" 加減式)*
加減式     = 乗除式 ("+" 乗除式 | "-" 乗除式)*
乗除式     = 単項式 ("*" 単項式 | "/" 単項式)*
単項式     = ("+" | "-")? 優先順位
優先順位   = 数 | 識別子 | "(" 式 ")
</pre>
programは意外と外来語として定着しているので、漢字化がむずかしかったです。手続き型プログラムという意味で「手続き」とするとprocedureっぽい感じになるので、それらの全体としてお茶を濁しました。

前のバージョンとは拡張BNF上の差異はないようです。


# C#のソースファイル分割

オリジナルのCの分割ファイルに対応して、C#ではソースコードファイルは以下のように分割されています。

・main.cs: main関数
・tokenize.cs: トークナイザ
・parse.cs: パーサ
・codegen.cs: コードジェネレータ

<details><summary>各ソースファイルの概要</summary>

main.csにmain関数が記述されています。
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
トークン関連とトークナイザはすべてこのtokenize.csファイルに記述しています。
```cs:tokenize.cs
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
    }
}
```
BNFに対応するパース関連関数はすべてこのparse.csファイルに記述しています。
```cs:parse.cs
namespace CC9
{
    public partial class Program
    {
        /// <summary>手続全体</summary>
        static void program(){
            // パース開始する
        }
    }
}
```
codegen.csにはコード生成とローカル変数のコード生成が記述されています。
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

        /// <summary>ローカル変数のコード生成</summary>
        /// <param name="node">ノード</param>
        static void gen_lval(Node node) {
            //ローカル変数のコード生成
        }
    }
}
```

</details>


# 列挙体・内部クラスなど記述

## 列挙体、クラス(変数のみ)の宣言

### トークナイザ関連（変更無）


```mind:Re:Mind
   ▽列挙体 トークン種類
        予約語,  // 記号
        識別子,  // 識別子
        整数,    // 整数トークン
        終端     // 入力の終わりを表すトークン
    △

    ▽クラス トークン型 
        ・トークン種類 種類 // Token kind
        ・int 次索引    // Next token
        ・int 値        // kindがTK_NUMの場合、その数値
        ・string? 文字列     // Token string
        ・int 長さ        // Token length
    △
```

<details><summary>C#ソースコード</summary>

```cs:tokenize.cs
    /// <summary>トークン種類</summary>
    enum TokenKind{
        /// <summary>予約語</summary>
        TK_RESERVED, // 記号
        /// <summary>識別子/summary>
        TK_IDENT,    // 識別子
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
</details>

### パーサ関連（追加有）
抽象構文木のノードの型に変数名を追加しています。

```mind:Re:Mind

    // 抽象構文木のノードの種類
    ▽列挙体 ノード種類
        加算記号, // +
        減算記号, // -
        乗算記号, // *
        除算記号, // /
        代入等号,  // =
        ローカル変数,  // 複数文字ローカル変数
        比較等号,  // ==
        比較不等号,  // !=
        比較小なり,  // <
        比較小なり等,  // <=
        整数 // 整数
    △

    // 抽象構文木のノードの型
    ▽クラス ノード型
        ・ノード種類 種類   // Node kind
        ・ノード型? 左辺    // Left-hand side
        ・ノード型? 右辺    // Right-hand side
        ・int 値            // kindがND_NUMの場合のみ使う
        ・string 変数名     // kindがND_LVARの場合のみ使う
        ・int オフセット値  // kindがND_LVARの場合のみ使う
    △
```

<details><summary>C#ソースコード</summary>

```cs:parse.cs

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
        /// <summary>代入等号</summary>
        ND_ASSIGN, // =
        /// <summary>ローカル変数</summary>
        ND_LVAR,   // 1文字変数
        /// <summary>比較等号</summary>
        ND_EQ,  // ==
        /// <summary>比較不等号</summary>
        ND_NE,  // !=
        /// <summary>比較小なり</summary>
        ND_LT,  // <
        /// <summary>比較小なり等</summary>
        ND_LE,  // <=
        /// <summary>構文</summary>
        ND_EXPR_STMT, // Expression statement
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
        /// <summary>変数名</summary>
        public string name;    // kindがND_LVARの場合のみ使う
        /// <summary>オフセット値</summary>
        public int offset;    // kindがND_LVARの場合のみ使う
    }
```
</details>

上記の従来からの列挙体・構造体（クラス）に加えて、変数を追跡するための構造体（クラス）を追加します。

```mind:Re:Mind

    // ローカル変数の型
    ▽クラス ローカル変数型
        ・ローカル変数型? 次の変数   // 次の変数がnull
        ・文字列 変数名              // 変数の名前
        ・int 変数名長               // 名前の長さ
        ・int オフセット値        // RBPからのオフセット
    △
```
```cs:parse.cs

    /// <summary>ローカル変数型</summary>
    class  LVar {
        /// <summary>次の変数</summary>
        public LVar? next;
        /// <summary>変数名</summary>
        public string name;
        /// <summary>変数名長</summary>
        public int len;
        /// <summary>オフセット値</summary>
        public int offset;
    }
```


# BNFに対応するパース関連関数
BNFに対応するパース関連関数では、primaryに変更が発生します。下記の追加のサポート関数を利用します。

変更関数
・primary
追加サポート関数
・consume_lvar
・new_lvar
・find_lvar
・new_lvar_node


## program （変更無）
programの対応日本語名は下記のとおりとしています。
手続全体

※注意！　Cではノード配列の要素数は100で固定宣言されているのに対して、C#ではノード型のリストにしています。

<details><summary>ロジック仕様とC#ソースコード</summary>

```mind:Re:Mind
    ▽手続全体(List<ノード型> コードリスト,List<トークン型> トークンリスト,参照 int 現索引) 
       □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
       〇(!at_eof(トークン)) の間は繰り返す
          □ノード型 コード = 構文(トークンリスト,ref 現索引)
          □コードリスト.追加(コード)
       〇ここまで
    △
```

Cオリジナルのcode[i] = NULL;はノード配列の終端判定に使用しているようですが、C#ではコードリストの要素数で判定しましたので、このコードは割愛しています。
```cs:parse.cs
    /// <summary>手続全体</summary>
    /// <param name="codeList">コードリスト</param>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    static void program(List<Node> codeList,List<Token> tokenList,ref int curIndex){
        Token token = getToken(tokenList,curIndex);//次のトークン
        while (!at_eof(token)){
            Node code = stmt(tokenList,ref curIndex);
            codeList.Add(code);
            token = getToken(tokenList,curIndex);//次のトークン
        }
    }
```

</details>

## stmt （変更無）
stmtの対応日本語名は下記のとおりとしています。
構文

<details><summary>ロジック仕様とC#ソースコード</summary>

```mind:Re:Mind
    ▽ノード型 構文(List<トークン型> トークンリスト,参照 int 現索引) 
        □ノード型 ノード=式(トークンリスト,ref 現索引)
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        □予想する(トークン,";",ref 現索引) 
        □ノード を返す
    △
```

```cs:parse.cs
    /// <summary>構文</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード型</returns>
    static Node stmt(List<Token> tokenList,ref int curIndex){
      Node node = expr(tokenList,ref curIndex);
      Token token = getToken(tokenList,curIndex);//次のトークン
      expect(token,";",ref curIndex);
      return node;
    }
```
</details>

## expr（変更無）
exprの対応日本語名は下記のとおりとしています。
式

<details><summary>ロジック仕様とC#ソースコード</summary>

```mind:Re:Mind
    ▽ノード型 式(List<トークン型> トークンリスト,参照 int 現索引) 
        □代入式(トークンリスト,ref 現索引)を　返す
    △
```
```c:parse.c
    Node *expr() {
      return assign();
    }
```
```cs:parse.cs
    /// <summary>式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード型</returns>
    static Node expr(List<Token> tokenList,ref int curIndex) {
        return assign(tokenList,ref curIndex);
    }
```
</details>

## assign （変更無）
assignの対応日本語名は下記のとおりとしています。
代入式

<details><summary>ロジック仕様とC#ソースコード</summary>

```mind:Re:Mind
    ▽ノード型 代入式(List<トークン型> トークンリスト,参照 int 現索引) 
        □ノード型 ノード型=等式(トークンリスト,ref 現索引)
        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        ◇真==使用する(トークン,"=",ref 現索引) の場合
             □ノード = 新しい二分木(ノード種類.代入等号, ノード, 代入式(トークンリスト,ref 現索引))
        ◇ここまで
       □ノード を返す
    △
```

```cs:parse.cs
    /// <summary>代入式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード型</returns>
    static Node assign(List<Token> tokenList,ref int curIndex) {
      Node node = equality(tokenList,ref curIndex);
      Token token = getToken(tokenList,curIndex);//次のトークン
      if (consume(token,"=",ref curIndex)){
        node = new_binary(NodeKind.ND_ASSIGN, node, assign(tokenList,ref curIndex));
      }  
      return node;
    }
```
</details>

## equality（変更無）
等しい、等しくない。
equalityの対応日本語名は下記のとおりとしています。
等式

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽ノード型 等式(リスト型<トークン型> トークンリスト,参照 int 現索引) 
        □ノード型 ノード = 関係式(トークンリスト,ref 現索引)
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

```cs:parse.cs
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
</details>

## relational（変更無）
大小関係。
relationalの対応日本語名は下記のとおりとしています。
関係式

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽ノード型 関係式(リスト型<トークン型> トークンリスト,参照 int 現索引) 
        □ノード型 ノード = 加減式(トークンリスト,ref 現索引)
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

```cs:parse.cs
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
</details>

## add（変更無）
addの対応日本語名は下記のとおりとしています。
加減式

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽ノード型 加減式(リスト型<トークン型> トークンリスト,参照 int 現索引 )
        □ノード型 ノード = 乗除式(トークンリスト,ref 現索引)
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

```cs:parse.cs
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
</details>

## mul（変更無）
mulの対応日本語名は下記のとおりとしています。
乗除式

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
        ▽ノード型 乗除式(List<トークン型> トークンリスト,参照 int 現索引) 
            □ノード型 ノード = 単項式(トークンリスト,ref 現索引);
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
```cs:parse.cs
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
</details>

## unary（変更無）
unaryの対応日本語名は下記のとおりとしています。
単項式

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
        ▽ノード型  単項式(List<トークン型> トークンリスト,参照 int 現索引) 
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
```cs:parse.cs
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
</details>

## primary（変更有）
primaryの対応日本語名は下記のとおりとしています。
優先順位

今回追加するローカル変数のサポート関数は、ここで使用されます。

```mind:Re:Mind
        ▽ノード型 優先順位(List<トークン型> トークンリスト,参照 int 現索引) 
            □トークン型 トークン = トークンを取得する(トークンリスト,現索引)//次のトークン
            // 次のトークンが"("なら、"(" expr ")"のはず
           ◇真==使用する(トークン,"(",ref 現索引) の場合
                □ノード型 ノード = 式(トークンリスト,ref 現索引)
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                □予想する(トークン,")",ref 現索引)
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                □ノード を返す
            ◇ここまで

            // そうでなければ識別子
           ◇真==識別子として使用する(トークン,"(",ref 現索引) の場合
                □ローカル変数型? ローカル変数 = ローカル変数を探す(トークン) 
                ◇ローカル変数 ==null の場合
                    ローカル変数 = 新しいローカル変数(トークン.文字列)
                ◇ここまで
                □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                □新しい変数ノード() を返す
            ◇ここまで

            // そうでなければ数値のはず
            □新しい整数(整数を想定する(トークン,ref 現索引)) を返す
        △
```
```cs:parse.cs
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

        // そうでなければ識別子
        if (consume_ident(token, ref curIndex)) {
            LVar? var = find_lvar(token);
            if (var==null){
                var = new_lvar(token.str);
            }
            token = getToken(tokenList,curIndex);//次のトークン
            return new_var_node(var);
        }

        // そうでなければ数値のはず
        //return new_node_num(expect_number(token,ref curIndex));
        return new_num(expect_number(token,ref curIndex));
    }

```

# サポート関数
## consume（変更無）
consumeの対応日本語名は下記のとおりとしています。
使用する

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    // 次のトークンが期待している記号のときには、トークンを1つ読み進めて
    // 真を返す。それ以外の場合には偽を返す。
    ▽bool 使用する(トークン型トークン,string 記号文字,参照 int 次索引) 
        ◇(トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.長さ || 
                    トークン.文字列 != 記号文字) の場合
            □偽 を返す
         ◇ここまで
         □次索引 = トークン.次索引;
         □真 を返す
    △
```
```cs:parse.cs
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
</details>

## expect（変更無）
expectの対応日本語名は下記のとおりとしています。
予想する

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
      ▽予想する(トークン型 トークン,string 記号文字,参照 int 次索引) 
         ◇(トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.長さ || 
                        トークン.文字列 != 記号文字) の場合
               □エラー出力($"'{記号文字}'ではありません")
         ◇ここまで
               □次索引 = トークン.次索引
    △
```

```cs:parse.cs
    /// <summary>予想する</summary>
    /// <param name="token">トークン</param>
    /// <param name="op">記号文字</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>
   static  void expect(Token token,string op,参照 int next) {
        if (token.kind != TokenKind.TK_RESERVED || op.Length  != token.len || 
                token.str != op)
            error($"'{op}'ではありません");
        next = token.next;
    }
```
</details>

## new_nodeとnew_binary（変更無）
new_nodeとnew_binaryの対応日本語名は下記のとおりとしています。
新しいノード
新しい二分木

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽ノード型 新しいノード(ノード種類 種類) 
        ・ノード型 ノード = new()
        □ノード.種類 = 種類
        □ノード を返す
   △

    ▽ノード型 新しい二分木(ノード種類 種類, ノード型 左辺, ノード型 右辺) 
        □ノード型 ノード = 新しいノード(種類)
        □ノード.左辺 = 左辺
        □ノード.右辺 = 右辺
        □ノード を返す
     △
```

```cs:parse.cs
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
</details>



## new_tokenとnew_num（変更無）
new_tokenとnew_numの対応日本語名は下記のとおりとしています。
新しいトークン
新しい数値

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽トークン型 新しいトークン(ノード種類 種類,int 次索引,string 文字列,int 長さ) 
        □トークン型 トークン = new()
        □トークン.種類 = 種類
        □トークン.文字列 = 文字列
        □トークン.長さ = 長さ
        □トークン.次のトークン= 次索引
        □トークン を返す
    △

    ▽ノード型 新しい数値(int 値) 
        □ノード型 ノード = 新しいノード(ノード種類.整数)
        □ノード.値 = 値
        □ノード を返す
     △
```

```cs:parse.cs
    /// <summary>新しいトークン</summary>
    /// <param name="kind">種類</param>
    /// <param name="next">次索引</param>
    /// <param name="str">文字列</param>
    /// <param name="len">長さ</param>
    /// <returns>トークン</returns>
    static Token new_token(TokenKind kind, int next, string str, int len) {
        Token tok = new();
        tok.kind = kind;
        tok.str = str;
        tok.len = len;
        tok.next = next;
        return tok;
    }

    /// <summary>新しい数値</summary>
    /// <param name="val">値</param>
    /// <returns>ノード</returns>
    static Node new_num(int val) {
        Node node = new_node(NodeKind.ND_NUM);
        node.val = val;
        return node;
    }
```
</details>

## consume_lvar （新規追加）
consume_lvarの対応日本語名は下記のとおりとしています。今回の追加関数となります。
識別子として使用する

```mind:Re:Mind
    ▽bool 識別子として使用する(トークン型トークン,参照 int 次索引) 
        ◇(トークン.種類 != トークン種類.識別子 ) の場合
            □偽 を返す
         ◇ここまで
         □次索引 = トークン.次索引;
         □真 を返す
    △
```
chibccの該当関数とはやや異なる定義としています。（既存のcoshumeに近い定義）
```c:parse.c
    // Consumes the current token if it is an identifier.
    Token *consume_ident(void) {
      if (token->kind != TK_IDENT)
        return NULL;
      Token *t = token;
      token = token->next;
      return t;
    }
```
```cs:parse.cs
    /// <summary>識別子として使用する</summary>
    /// <param name="token">トークン</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>  
    static bool consume_ident(Token token, ref int next) {
        if (token.kind != TokenKind.TK_IDENT){
            return false;
        }
        next = token.next;
        return true;
    }
```
## new_lvar （新規追加）
new_lvarの対応日本語名は下記のとおりとしています。今回の追加関数となります。
新しいローカル変数

```mind:Re:Mind
    ▽ローカル変数型 新しいローカル変数(string 変数名)
        □ローカル変数型 ローカル変数 = new()
        □ローカル変数.変数名 = 変数名
        □ローカル変数.変数名長 = 変数名.長さ
        □ローカル変数.オフセット値 = ローカル変数群 + 8
        □ローカル変数.次のローカル変数= ローカル変数群
        □ローカル変数群 = ローカル変数
        □ローカル変数 を返す
    △
```
```cs:parse.cs
    /// <summary>新しいローカル変数</summary>
    /// <param name="name">変数名</param>
    /// <returns>ローカル変数</returns>
    static LVar new_lvar(string name) {
        LVar var =new();
        var.name = name;
        var.len = name.Length;
        var.offset = locals.offset + 8;
        var.next = locals;
        locals = var;
        return var;
    }
```

・2023/05/30 訂正
 □ローカル変数.変数名長 = 変数名.長さ
が漏れていました。このため、次の追加関数「ローカル変数名を探す」が正常動作しておらず、既存変数を返せていませんでした。


## find_lvar （新規追加）
find_lvarの対応日本語名は下記のとおりとしています。今回の追加関数となります。
ローカル変数名を探す

```mind:Re:Mind
    ▽ローカル変数型? ローカル変数名を探す(トークン型 トークン,ローカル変数型? ローカル変数)
       〇ローカル変数型? L変数=ローカル変数,L変数!=null,L変数=L変数.次の変数 繰り返す
        ◇L変数.変数名長==トークン.長さ && 0==文字列比較(トークン.文字列,L変数.変数名,L変数.長さ) の場合
             □L変数 を返す
        ◇ここまで
       〇ここまで
       □null を返す
    △
```
```c:parse.c
    // 変数を名前で検索する。見つからなかった場合はNULLを返す。
    LVar *find_lvar(Token *tok) {
      for (LVar *var = locals; var; var = var->next)
        if (var->len == tok->len && !memcmp(tok->str, var->name, var->len))
          return var;
      return NULL;
    }
```
```cs:parse.cs
    /// <summary>ローカル変数名を探す</summary>
    /// <param name="tok">トークン</param>
    /// <returns>ローカル変数型?</returns>
    static LVar? find_lvar(Token tok) {
        for (LVar? var = locals; (var!=null);  var = var.next){
            if (var.len == tok.len && 0==strncmp(tok.str, var.name, var.len)){
                return var;
            } 
        }  
        return null;
    }
```
## new_lvar_node （新規追加）
new_lvar_nodeの対応日本語名は下記のとおりとしています。今回の追加関数となります。
新しい変数ノード

```mind:Re:Mind
    ▽ノード型 新しい変数ノード(ローカル変数型 ローカル変数) 
        □ノード型 ノード = 新しいノード(ノード種類.変数)
        □ノード.変数名 = ローカル変数.変数名
        □ノード.オフセット値 = ローカル変数.オフセット値
        □ノード を返す
     △
```
このバージョンのchibccではノードにローカル変数を保持している
```c:parse.c
    static Node *new_var_node(Var *var) {
      Node *node = new_node(ND_VAR);
      node->var = var;
      return node;
    }
```
```cs:parse.cs
    /// <summary>新しい変数ノード</summary>
    /// <param name="var">ローカル変数</param>
    /// <returns>ノード</returns>
    static Node new_var_node(LVar var) {
        Node node = new_node(NodeKind.ND_LVAR);
        node.name = var.name;
        node.offset =var.offset;
        return node;
    }
```

下記のサポート関数の関数名を
isspace　iscomparison　iscomparisonhead　isdigit isarithmetic　strncmp
日本語化した関数名は下記のとおりとしています。
空白か判定する　比較記号か判定する　比較記号頭文字か判定する　数字か判定する 演算子か判定する　文字列比較

# トークナイザ・コードジェネレータ
## tokenize （変更有）
tokenizeの日本語化した関数名は下記のとおりとしています。
トークナイズする

 // Multi-letter identfer　のあたりを修正（1文字変数から複数文字列の変数識別子の対応）

```mind:Re:Mind
    // 入力文字列をトークナイズしてトークンリストを返す
    ▽リスト型<トークン型> トークナイズする(string 入力文字列) 
        ・int 次索引 = 1;
        ・トークン型 現トークン = new();
        ・リスト型<トークン型> トークンリスト =new リスト型<トークン型>();

        ・入力文字列配列 = 入力文字列.ToCharArray();
        ・int i= 0;

        〇(i<入力文字列配列.Length) の間は繰り返す
            // 空白文字をスキップ
            ◇真==空白か判定する(入力文字列配列[i]) の場合
                □i++;
                □ループ先頭へ
            ◇ここまで

            // Multi-letter identfer
            ◇真==識別子か判定する(入力文字列配列[i]) の場合
                ・string 変数文字列 = 入力文字列配列[i]
                □i++
                ◇(i<入力文字列配列.Length) の場合
                    〇(識別子か判定する(入力文字列配列[i])) の間は繰り返す
                        □変数文字列+= 入力文字列配列[i]
                        □i++
                        ◇(i>=入力文字列配列.Length) の場合 やめる
                    〇ここまで
                ◇ここまで
                □現トークン = 新しいトークン(トークン種類.識別子, 次索引, 変数文字列,i)
                □トークンリスト.Add(現トークン)
                □次索引++
                □i++
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

            // assign
            ◇真==代入式か判定する(入力文字列配列[i]) の場合
                □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 入力文字列配列[i],1)
                □トークンリスト.Add(現トークン)
                □次索引++
                □i++
                □ループ先頭へ
            ◇ここまで
    
            // statement terminater
            ◇真==構文終端か判定する(入力文字列配列[i]) の場合
                □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 入力文字列配列[i],1)
                □トークンリスト.Add(現トークン)
                □次索引++
                □i++
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

```cs:tokenize.cs
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

            // Multi-letter identfer
            if (isalphapetLower(cs[i].ToString())) {
                string varStr = cs[i].ToString();
                 i++;
                if(i<cs.Length){
                    while(isidentfer(cs[i].ToString())) {
                        varStr+= cs[i].ToString();
                        i++;
                        if(i>=cs.Length)break;
                    }
                }                   
                cur = new_token(TokenKind.TK_IDENT, next,varStr,i);
                tokenList.Add(cur);
                next++;
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

            // assign
            if (isassign(cs[i].ToString())) {
                cur = new_token(TokenKind.TK_RESERVED, next, cs[i].ToString(),1);
                tokenList.Add(cur);
                next++;
                i++;
                continue;
            }

            // statement terminater
            if (isterminater(cs[i].ToString())) {
                cur = new_token(TokenKind.TK_RESERVED, next, cs[i].ToString(),1);
                tokenList.Add(cur);
                next++;
                i++;
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


## gen （変更無）
genの日本語化した関数名は下記のとおりとしています。
コード生成

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽コード生成(ノード型 ノード) 
        ◇(ノード.種類)　で分岐する
        ◇ノード種類.整数
            □コンソール出力($"  push {ノード.値}\n")
            □返る
        ◇ノード種類.ローカル変数
            □ローカル変数のコード生成(ノード)

            □コンソール出力("  pop rax\n")
            □コンソール出力("  mov rax, [rax]\n")
            □コンソール出力("  push rax\n")
            □返る
        ◇ノード種類.代入等号
            □ローカル変数のコード生成(ノード.左辺)
            □コード生成(ノード.右辺)

            □コンソール出力("  pop rdi\n")
            □コンソール出力("  pop rax\n")
            □コンソール出力("  mov [rax], rdi\n")
            □コンソール出力("  push rdi\n")
            □返る
        ◇ここまで

        □コード生成(ノード.左辺)
        □コード生成(ノード.右辺)

        □コンソール出力("  pop rdi\n")
        □コンソール出力("  pop rax\n")

        ◇(ノード.種類)　で分岐する
        ◇ノード種類.加算記号
            □コンソール出力("  add rax, rdi\n")
            □脱出する
        ◇ノード種類.減算記号
            □コンソール出力("  sub rax, rdi\n")
            □脱出する
        ◇ノード種類.乗算記号
            □コンソール出力("  imul rax, rdi\n")
            □脱出する
        ◇ノード種類.除算記号
            □コンソール出力("  cqo\n")
            □コンソール出力("  idiv rdi\n")
            □脱出する
        ◇ノード種類.比較等号
            □コンソール出力("  cmp rax, rdi\n")
            □コンソール出力("  sete al\n")
            □コンソール出力("  movzb rax, al\n")
            □脱出する
        ◇ノード種類.比較不等号:
            □コンソール出力("  cmp rax, rdi\n")
            □コンソール出力("  setne al\n")
            □コンソール出力("  movzb rax, al\n")
            □脱する
        ◇ノード種類.比較小なり
            □コンソール出力("  cmp rax, rdi\n")
            □コンソール出力("  setl al\n")
            □コンソール出力("  movzb rax, al\n")
            □脱出する
        ◇ノード種類.比較小なり等
            □コンソール出力("  cmp rax, rdi\n")
            □コンソール出力("  setle al\n")
            □コンソール出力("  movzb rax, al\n")
            □脱出する
        ◇ここまで

        □コンソール出力("  push rax\n")
    △
```

```cs:codegen.cs
    /// <summary>コード生成</summary>
    /// <param name="node">ノード</param>
   static void gen(Node node) {
        switch (node.kind) {
        case NodeKind.ND_NUM:
            Console.Write($"  push {node.val}\n");
            return;
        case NodeKind.ND_LVAR:
            gen_lval(node);
            Console.Write("  pop rax\n");
            Console.Write("  mov rax, [rax]\n");
            Console.Write("  push rax\n");
            return;
        case NodeKind.ND_ASSIGN:
            gen_lval(node.lhs);
            gen(node.rhs);

            Console.Write("  pop rdi\n");
            Console.Write("  pop rax\n");
            Console.Write("  mov [rax], rdi\n");
            Console.Write("  push rdi\n");
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
</details>

## gen_lval （変更無）
gen_lvalの日本語化した関数名は下記のとおりとしています。
ローカル変数のコード生成

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽ローカル変数のコード生成(ノード型 ノード) 
        ◇(ノード.種類 != ノード種類.ローカル変数) の場合
            □コンソール出力( "代入の左辺値が変数ではありません\n");
        ◇ここまで

        □コンソール出力("  mov rax, rbp\n");
        □コンソール出力($"  sub rax, {node.offset}\n");
        □コンソール出力("  push rax\n");
    △
```
```cs:codegen.cs
    /// <summary>ローカル変数のコード生成</summary>
    /// <param name="node">ノード</param>
    static void gen_lval(Node node) {
      if (node.kind != NodeKind.ND_LVAR){
        Console.Write("代入の左辺値が変数ではありません\n");
      }
      Console.Write("  mov rax, rbp\n");
      Console.Write($"  sub rax, {node.offset}\n");
      Console.Write("  push rax\n");
    }
```
</details>

# Mainなど記述
## Main（変更有）
プログラム型クラスのスコープでローカル変数型? ローカル変数群を宣言しました。

```mind:Re:Mind
    ・ローカル変数型 ローカル変数群=new()

    ▽int メイン(string[] 引数)

         ◇(引数.Length != 2) の場合
                □コンソール出力( "引数の個数が正しくありません\n")
                □1 を返す
         ◇ここまで

        □リスト型<ノード型> コードリスト =リスト型<ノード型>で初期化
        // トークナイズする
        □リスト型<トークン型> トークンリスト = トークナイズする(引数[1])
        // 現在着目しているトークン
        ・int 現索引=0
        // パースする
        □手続全体(トークンリスト,ref 現索引)

        // アセンブリの前半部分を出力
        □コンソール出力(".intel_syntax noprefix\n")
        □コンソール出力(".globl main\n")
        □コンソール出力("main:\n")

        // プロローグ
        // 変数26個分の領域を確保する
        □コンソール出力("  push rbp\n")
        □コンソール出力("  mov rbp, rsp\n")
        □コンソール出力("  sub rsp, 208\n")

        // 先頭の式から順にコード生成
        〇i=0,i< コードリスト.Length,i++ 繰り返す
            □コード生成(コードリスト.ElementAt(i))

            // 式の評価結果としてスタックに一つの値が残っている
            // はずなので、スタックが溢れないようにポップしておく
            □コンソール出力("  pop rax\n")
        〇ここまで

        // エピローグ
        // 最後の式の結果がRAXに残っているのでそれが返り値になる
        □コンソール出力("  mov rsp, rbp\n")
        □コンソール出力("  pop rbp\n")
        □コンソール出力("  ret\n")
        □0 を返す
    △
```

```cs:main.cs

    /// <summary>ローカル変数群</summary>
    LVar locals = new();

    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static int Main(string[] args)
    {
          if (args.Length != 2) {
                Console.Write( "引数の個数が正しくありません\n");
                return 1;
            }

        //Nodeリストを初期化する
        List<Node> codeList = new List<Node>();
        // トークナイズする
        List<Token> tokenList = tokenize(args[1]);
        // 現在着目しているトークン
        int curIndex=0;
        // パースする
        program(codeList,tokenList,ref curIndex);

        // アセンブリの前半部分を出力
        Console.Write(".intel_syntax noprefix\n");
        Console.Write(".globl main\n");
        Console.Write("main:\n");

        // プロローグ
        // 変数26個分の領域を確保する
        Console.Write("  push rbp\n");
        Console.Write("  mov rbp, rsp\n");
        Console.Write("  sub rsp, 208\n");

        // 先頭の式から順にコード生成
        for (int i = 0; i< codeList.Count; i++) {
            gen(codeList.ElementAt(i));//コード;

            // 式の評価結果としてスタックに一つの値が残っている
            // はずなので、スタックが溢れないようにポップしておく
            Console.Write("  pop rax\n");
        }

        // エピローグ
        // 最後の式の結果がRAXに残っているのでそれが返り値になる
        Console.Write("  mov rsp, rbp\n");
        Console.Write("  pop rbp\n");
        Console.Write("  ret\n");
        return 0;
    }
```

# 入出力コード サンプルイメージ
今回は　aloha = 3;bravo = 5 * 6 - 8;aloha + bravo / 2;　を対象にchibicc(9cc)と同じアセンブラを出力します。
しかし、参考サイトの推奨実装はリファクタリングが進行していて完全に同等のバージョンの特定が困難となっているように感じられたので、historical/oldブランチのコミット[2dd952c]のSupport multi-letter local variablesをビルドして実行してみました。
C#の出力結果は若干これと異なっています。現状の比較は参考程度となります。（この出力はintel_syntax noprefixがつかないのでインテル用ではない感じ）

## chibicc(9cc)複数文字のローカル変数版の実行結果
C#との比較用の期待結果として9ccを実行してみます。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。

<details><summary>出力コード サンプルイメージ</summary>

```:aloha = 3;bravo = 5 * 6 - 8;aloha + bravo / 2;
$ ./chibicc 'aloha = 3;bravo = 5 * 6 - 8;aloha + bravo / 2;'
  .globl main
main:
  push %rbp
  mov %rsp, %rbp
  sub $16, %rsp
  lea -16(%rbp), %rax
  push %rax
  mov $3, %rax
  pop %rdi
  mov %rax, (%rdi)
  lea -8(%rbp), %rax
  push %rax
  mov $8, %rax
  push %rax
  mov $6, %rax
  push %rax
  mov $5, %rax
  pop %rdi
  imul %rdi, %rax
  pop %rdi
  sub %rdi, %rax
  pop %rdi
  mov %rax, (%rdi)
  mov $2, %rax
  push %rax
  lea -8(%rbp), %rax
  mov (%rax), %rax
  pop %rdi
  cqo
  idiv %rdi
  push %rax
  lea -16(%rbp), %rax
  mov (%rax), %rax
  pop %rdi
  add %rdi, %rax
  mov %rbp, %rsp
  pop %rbp
  ret
```
</details>

# 実行結果
## コンパイラの出力コード
続いてC#をコンパイルします。ビルド（コンパイル）はVSCodeのタスクで実行しました。
9ccと同じソースコード文字列を与えて実行すると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。

<details><summary>出力コード サンプルイメージ</summary>

```:aloha = 3;bravo = 5 * 6 - 8;aloha + bravo / 2;
>9cc2cs s "aloha = 3;bravo = 5 * 6 - 8;aloha + bravo / 2;" 
.intel_syntax noprefix
.globl main
main:
  push rbp
  mov rbp, rsp
  sub rsp, 208
  mov rax, rbp
  sub rax, 8
  push rax
  push 3
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  pop rax
  mov rax, rbp
  sub rax, 16
  push rax
  push 5
  push 6
  pop rdi
  pop rax
  imul rax, rdi
  push rax
  push 8
  pop rdi
  pop rax
  sub rax, rdi
  push rax
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  pop rax
  mov rax, rbp
  sub rax, 8
  push rax
  pop rax
  mov rax, [rax]
  push rax
  mov rax, rbp
  sub rax, 16
  push rax
  pop rax
  mov rax, [rax]
  push rax
  push 2
  pop rdi
  pop rax
  cqo
  idiv rdi
  push rax
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rax
  mov rsp, rbp
  pop rbp
  ret
```
</details>

・2023/05/30 訂正
追加関数「新しいローカル変数」で
 □ローカル変数.変数名長 = 変数名.長さ
の記述が漏れていました。このため、次の追加関数「ローカル変数名を探す」が正常動作しておらず、既存変数を返せていないため、変数が再度出現したときのスタックオフセット値が不正でした。更新した出力イメージに差し替えました。

# ソースコード
GitHub 鋭意準備中

# おわりに
前STEPよりレファレンス実装のソースコードが解説文とかなり乖離してきていますので、引き続き苦戦しました。追加事項を解説どおりに実装して、あとはデバッグ実行で動くようにしています。
historical/oldブランチのコミット[2dd952c]のSupport multi-letter local variablesと結果が一部異なっておりますが、とりあえず先に進めば見えてくることもあるかと思いますので、次回「ステップ11：return文」に進行します。

# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94
