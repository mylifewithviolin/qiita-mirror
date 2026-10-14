# はじめに

[トランスコンパイラ試作品の内部設計に進行しています](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)が、これがけっこう難航しておりまして、こっちはあまり進捗がないまま記事の未投稿が続くのもなんですので、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみていますの続きです。ついに「ステップ12: 制御構文を足す」に到達しました。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。本記事は参考サイトの9ccの「ステップ12: 制御構文を足す」に相当します。どこまでも前半というかは微妙ですが、そろそろ中盤に入ってきた感はあります。作者の方的にはこの項から「執筆中」状態とのことです。このステップではついに「if、if ... else、while、for」といった制御構造がコンパイラ言語に追加されます。記事中ではアセンブラへの出力方法(コードジェネレータ部分）の考え方が詳しく説明されています。よくわかりませんが、return文のトークナイザ追加の延長で書き換えていってみます。

## この記事内容の作業環境
Windows11 Pro 22H2
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　1.78.2
gcc 11　11.3.0
C# 10 dotnet-sdk-6.0.404-win-x64
Compiler Explorer(Execution モード)　x86-64-Clang 16.0.0 -x assembler 

## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。

## 関連記事

<details><summary>ステップ5から9まで</summary>

参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」までに相当する内容を下記の記事で解説しております。

[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（四則演算版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)
「ステップ6：単項プラスと単項マイナス」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（単項演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/fb8dc06460855928162f)
「ステップ7：比較演算子」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)

この段階のCコンパイラの仕様を日本語ロジック仕様記述言語 Re:Mindで記述しています。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（比較演算子版）のロジック仕様を日本語ロジック仕様記述言語 Re:Mind（リマインド）で記述してみる](https://qiita.com/mylifewithviolin/items/68577ea36b72ea9da473)

「ステップ8: ファイル分割とMakefileの変更」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（ファイルの分割版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/b4db353163576b5abe87)
「ステップ9: 1文字のローカル変数」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（1文字のローカル変数版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/47b5cda334b5bddbc63c)
</details>



「ステップ10: 複数文字のローカル変数」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（複数文字のローカル変数版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/c6821d8ef2ba22d6b642)
「ステップ11：return文」に相当する内容は下記の記事です。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（return文対応版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/0d8b1506671ec312f3bf)


# ロジックのポイント
この状態のＣ言語コンパイラ（制御構文対応版）は下記の拡張BNFで記述された生成規則に対応したコンパイラを実装することにあります。
<pre>
program    = stmt*
stmt       = expr ";" 
            | "if" "(" expr ")" stmt ("else" stmt)?
            | "while" "(" expr ")" stmt
            | "for" "(" expr? ";" expr? ";" expr? ")" stmt
            | "return" expr ";"
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
            | "if" "(" 式 ")" 構文 ("else" 構文)?
            | "while" "(" 式 ")" 構文
            | "for" "(" 式? ";" 式? ";" 式? ")" 構文
            | "return" 式 ";"
式       　= 代入式
代入式     = 等式 ("=" 代入式)?
等式       = 関係式("==" 関係式 | "!=" 関係式)*
関係式     = 加減式 ("<" 加減式 | "<=" 加減式 | ">" 加減式 | ">=" 加減式)*
加減式     = 乗除式 ("+" 乗除式 | "-" 乗除式)*
乗除式     = 単項式 ("*" 単項式 | "/" 単項式)*
単項式     = ("+" | "-")? 優先順位
優先順位   = 数 | 識別子 | "(" 式 ")
</pre>

前のバージョンとの拡張BNF上の差異はstmt に
            | "if" "(" expr ")" stmt ("else" stmt)?
            | "while" "(" expr ")" stmt
            | "for" "(" expr? ";" expr? ";" expr? ")" stmt
が追加されたことです。


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
        /// <param name="codelist">コードリスト</param>
        static void codegen(List<Node> codelist) {
            // 抽象構文木を下りながらコード生成
        }

        /// <summary>生成</summary>
        /// <param name="node">ノード</param>
        static void gen(Node node) {
            // コード生成
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

### トークナイザ関連（追加有）
トークン種類の列挙体に前回のステップでリターン文 TK_RETURNを追加しましたが、もう少し後方の実装では TK_RETURNは予約語TK_RESERVEDにマージされているっぽいので、今回追加されるkeywordではトークン種類は増やさないとします。TK_RETURNはとりあえず残しておきます。

```mind:Re:Mind
   ▽列挙体 トークン種類
        予約語,  // 記号
        リターン文,  // return文
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
        /// <summary>return文</summary>
        TK_RETURN, // リターン文
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

今回追加する制御構文「if、if ... else、while、for」のキーワードをリテラルのままソースコードに記述するのもなんので、前回追加したクラス キーワード型に、文字列定数メンバを追加します。現状は"return"以外の従来出現のその他のノード種類の演算子などがソースコード上リテラルで書かれていますが、追って移行します。

```mind:Re:Mind
    ▽クラス キーワード型 
        ・文字列定数 リターン文 = "return" // KW_RETURN
        ・文字列定数 if文 = "if"        // KW_IF
        ・文字列定数 else文 = "else"    // KW_ELSE
        ・文字列定数 while文 = "while"  // KW_WHILE
        ・文字列定数 for文 = "for"      // KW_FOR
    △
```
```cs:tokenize.cs
    /// <summary>キーワード型</summary>
    class Keywords{
        /// <summary>リターン文</summary>
        public const string KW_RETURN = "return";
        /// <summary>if文</summary>
        public const string KW_IF = "if";
        /// <summary>else文</summary>
        public const string KW_ELSE = "else";
        /// <summary>while文</summary>
        public const string KW_WHILE = "while";
        /// <summary>for文</summary>
        public const string KW_FOR = "for";
    }
```
### パーサ関連（追加有）
列挙体のノード種類に今回追加する制御構文のキーワード「if、else、while、for」に対応するノードを追加しています。
クラスノード型に制御構文の条件式、初期化式、増分式、構文ノードを追加しています。

```mind:Re:Mind
    // 抽象構文木のノードの種類
    ▽列挙体 ノード種類
        加算記号, // +
        減算記号, // -
        乗算記号, // *
        除算記号, // /
        代入等号,  // =
        リターン文, // "return"
        if文,    //"if"
        else文,  //"else"
        while文, //"while"
        for文,   //"for"
        ローカル変数,  // 複数文字ローカル変数
        比較等号,  // ==
        比較不等号,  // !=
        比較小なり,  // <
        比較小なり等,  // <=
        構文, // Expression statement
        整数 // 整数
    △

    // 抽象構文木のノードの型
    ▽クラス ノード型
        ・ノード種類 種類   // Node kind
        ・ノード型? 左辺    // Left-hand side
        ・ノード型? 右辺    // Right-hand side
        ・ノード型? 条件式      // condition
        ・ノード型? then側構文  // then-side stmt
        ・ノード型? else側構文  // else-side stmt
        ・ノード型? 初期化式    // initilize
        ・ノード型? 増分式    // incremant
        ・int 値            // kindがND_NUMの場合のみ使う
        ・string 変数名     // kindがND_LVARの場合のみ使う
        ・int オフセット値  // kindがND_LVARの場合のみ使う
    △
```
```mind:Re:Mind
    // ローカル変数の型
    ▽クラス ローカル変数型
        ・ローカル変数型? 次の変数   // 次の変数がnull
        ・文字列 変数名              // 変数の名前
        ・int 変数名長               // 名前の長さ
        ・int オフセット値        // RBPからのオフセット
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
        /// <summary>リターン文</summary>
        ND_RETURN,    // "return"
        /// <summary>if文</summary>
        ND_IF,        // "if"
        /// <summary>else文</summary>
        ND_ELSE,      // "else"
        /// <summary>while文</summary>
        ND_WHILE,     // "while"
        /// <summary>for文</summary>
        ND_FOR,       // "for"
        /// <summary>ローカル変数</summary>
        ND_LVAR,   // ローカル変数
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
        /// <summary>条件式</summary>
        public Node? cond;  //条件式
        /// <summary>then側構文</summary>
        public Node? then;  //then-side stmt
        /// <summary>else側構文</summary>
        public Node? els;   //else-side stmt
        /// <summary>初期化式</summary>
        public Node? init;  //initilize
        /// <summary>増分式</summary>
        public Node? inc;   //incremant
        /// <summary>値</summary>
        public int val;       // kindがND_NUMの場合のみ使う
        /// <summary>変数名</summary>
        public string name;    // kindがND_LVARの場合のみ使う
        /// <summary>オフセット値</summary>
        public int offset;    // kindがND_LVARの場合のみ使う
    }
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
</details>



# BNFに対応するパース関連関数
BNFに対応するパース関連関数では、stmtに変更が発生します。下記の追加のサポート関数を利用します。

変更関数
・stmt
追加サポート関数
・consume_reserved 予約語として使用する
・read_expr_stmt　　構文内式

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

## stmt （変更有）
stmtの対応日本語名は下記のとおりとしています。
構文

TK_RETURNだけ前回ステップでは別トークン種類が与えられていますが、今回追加されたキーワードは予約語というトークン列となっていますので、まず予約語トークンとして認識させ、予約語の内容は実際のトークン文字列とキーワード文字列から判定して、新しい予約語を含むトークン列をパースできるようにします。


```mind:BNF
構文       = 式 ";" 
            | "if" "(" 式 ")" 構文 ("else" 構文)?
            | "while" "(" 式 ")" 構文
            | "for" "(" 式? ";" 式? ";" 式? ")" 構文
            | "return" 式 ";"
```
ここのロジックはよくわからないので上記の拡張BNFの式が下から解釈されていくような感じでまずロジック言語Re:Mindで書いてみます。

```mind:Re:Mind
構文       = 式 ";" 
            | "return" 式 ";"
```
まず前ステップ「ステップ11：return文」での記述では";"の出現を共通部分でまとめてしまっているので、少し冗長になりますが、上記の修正前の拡張BNFとの対応がわかりやすいように書き換えます。

```mind:Re:Mind
    ▽ノード型 構文(List<トークン型> トークンリスト,参照 int 現索引) 
        ・ノード型 ノード

        □トークン型 トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        //"return" 式 ";"
        ◇真==リターンとして使用する(トークン,ref 現索引) の場合
           □ノード = 新しいノード(ノード種類.リターン文)
           □ノード = 式(トークンリスト,ref 現索引)
        　 □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
        　 □予想する(トークン,";",ref 現索引) 
           □ノード を返す

        // 式 ";" 
        ◇他に
           □ノード = 式(トークンリスト,ref 現索引)
           □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
           □予想する(トークン,";",ref 現索引) 
           □ノード を返す
        ◇ここまで

    △
```

そしてまず。上記の分岐構文の間に最もやさしいwhile構文のパースロジックを追記します。
```mind:BNF
構文       = 式 ";" 
            | "while" "(" 式 ")" 構文
            | "return" 式 ";"
```
```mind:Re:Mind
        ・・・・
        //"return" 式 ";"
        ◇真==リターンとして使用する(トークン,ref 現索引) の場合
        ・・・・

        //"while" "(" 式 ")" 構文
        ◇他に 真==予約語として使用する(トークン,キーワード型.while文,ref 現索引) の場合
            □ノード = 新しいノード(ノード種類.while文)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            // 次のトークンは、"(" expr ")"のはず
            □予想する(トークン,"(",ref 現索引)
            □ノード.条件式 = 式(トークンリスト,ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □予想する(トークン,")",ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □ノード.then側構文 = 構文(トークンリスト,ref 現索引)
            □ノード を返す

        // 式 ";" 
        ◇他に
        ・・・・
```
つづいて、つぎに比較的やさしいif構文のパースロジックを追記します。
```mind:BNF
構文       = 式 ";" 
            | "if" "(" 式 ")" 構文 ("else" 構文)?
            | "while" "(" 式 ")" 構文
            | "return" 式 ";"
```
```mind:Re:Mind
        //"return" 式 ";"
        ◇真==リターンとして使用する(トークン,ref 現索引) の場合
        ・・・・
        //"while" "(" 式 ")" 構文
        ◇他に 真==予約語として使用する(トークン,キーワード型.while文,ref 現索引) の場合
        ・・・・

        //"if" "(" 式 ")" 構文 ("else" 構文)?
        ◇他に 真==予約語として使用する(トークン,キーワード型.if文,ref 現索引) の場合
            □ノード = 新しいノード(ノード種類.if文)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            // 次のトークンは、"(" expr ")"のはず
            □予想する(トークン,"(",ref 現索引)
            □ノード.条件式 = 式(トークンリスト,ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □予想する(トークン,")",ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            □ノード.then側構文 = 構文(トークンリスト,ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇真==予約語として使用する(トークン,キーワード型.else文,ref 現索引) の場合
                 □ノード.else側構文 = 構文(トークンリスト,ref 現索引)
            ◇ここまで
           □ノード を返す

        // 式 ";" 
        ◇他に
```
最後にfor構文のパースロジックを追記します。
```mind:BNF
構文       = 式 ";" 
            | "if" "(" 式 ")" 構文 ("else" 構文)?
            | "while" "(" 式 ")" 構文
            | "for" "(" 式? ";" 式? ";" 式? ")" 構文
            | "return" 式 ";"
```
```mind:Re:Mind
        //"return" 式 ";"
        ◇真==リターンとして使用する(トークン,ref 現索引) の場合
        ・・・・
        //"while" "(" 式 ")" 構文
        ◇他に 真==予約語として使用する(トークン,キーワード型.while文,ref 現索引) の場合
        ・・・・
        //"if" "(" 式 ")" 構文 ("else" 構文)?
        ◇他に 真==予約語として使用する(トークン,キーワード型.if文,ref 現索引) の場合
        ・・・・

        //"for" "(" 式? ";" 式? ";" 式? ")" 構文
        ◇他に 真==予約語として使用する(トークン,キーワード型.for文,ref 現索引) の場合
            □ノード = 新しいノード(ノード種類.for文)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            // 次のトークンは、"(" expr ";"のはず
            □予想する(トークン,"(",ref 現索引)
            □ノード型 ノード = 式(トークンリスト,ref 現索引)
            □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
            ◇真==使用する(トークン,";",ref 現索引) の場合
                 □ノード.初期化式 = 構文内式(トークンリスト,現索引)
                 □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                 □予想する(トークン,";",ref 現索引)
            ◇ここまで
            ◇真==使用する(トークン,";",ref 現索引) の場合
                 □ノード.条件式 = 構文内式(トークンリスト,現索引)
                 □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                 □予想する(トークン,";",ref 現索引)
            ◇ここまで
            ◇真==使用する(トークン,")",ref 現索引) の場合
                 □ノード.増分式 = 構文内式(トークンリスト,現索引)
                 □トークン = トークンを取得する(トークンリスト,現索引) //次のトークン
                 □予想する(トークン,")",ref 現索引)
            ◇ここまで
           □ノード を返す

        // 式 ";" 
        ◇他に
```

```cs:parse.cs
    /// <summary>構文</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード型</returns>
    static Node stmt(List<Token> tokenList,ref int curIndex){
        Node node;
        Token token = getToken(tokenList,curIndex);
        //"return" 式 ";"
        if (consume_return(token, ref curIndex)) {//使用していなければcurIndexは変更されない
            node = new_node(NodeKind.ND_RETURN);
            node = expr(tokenList,ref curIndex);
            token = getToken(tokenList,curIndex);
            expect(token,";",ref curIndex);

        //"while" "(" 式 ")" 構文
        }else if (consume_reserved(token, Keywords.KW_WHILE,ref curIndex)) {
            node = new_node(NodeKind.ND_WHILE);
            token = getToken(tokenList,curIndex);//次のトークン
            // 次のトークンは、"(" expr ")"のはず
            expect(token,"(",ref curIndex);
            node.cond = expr(tokenList,ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            expect(token,")",ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            node.then = stmt(tokenList,ref curIndex);

        //"if" "(" 式 ")" 構文 ("else" 構文)?
        }else if (consume_reserved(token, Keywords.KW_IF,ref curIndex)) {
            node = new_node(NodeKind.ND_IF);
            token = getToken(tokenList,curIndex);//次のトークン
            // 次のトークンは、"(" expr ")"のはず
            expect(token,"(",ref curIndex);
            node.cond = expr(tokenList,ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            expect(token,")",ref curIndex);
            token = getToken(tokenList,curIndex);//次のトークン
            node.then = stmt(tokenList,ref curIndex);

            token = getToken(tokenList,curIndex);//次のトークン
            if (consume_reserved(token, Keywords.KW_ELSE,ref curIndex)) {
                node.els = stmt(tokenList,ref curIndex);
            }

        //"for" "(" 式? ";" 式? ";" 式? ")" 構文
        }else if (consume_reserved(token, Keywords.KW_FOR,ref curIndex)) {
            node = new_node(NodeKind.ND_FOR);
            token = getToken(tokenList,curIndex);//次のトークン
            // 次のトークンは、"(" expr ";"のはず
            expect(token,"(",ref curIndex);
            if (consume(token,";",ref curIndex)){
                node.init = read_expr_stmt(tokenList,ref curIndex);
                token = getToken(tokenList,curIndex);//次のトークン
                expect(token,";",ref curIndex);
            }
            if (consume(token,";",ref curIndex)){
                node.cond = expr(tokenList,ref curIndex);
                token = getToken(tokenList,curIndex);//次のトークン
                expect(token,";",ref curIndex);
            }
            if (consume(token,")",ref curIndex)){
                node.inc = read_expr_stmt(tokenList,ref curIndex);
                token = getToken(tokenList,curIndex);//次のトークン
                expect(token,")",ref curIndex);
            }  

        // 式 ";" 
        } else {
            node = expr(tokenList,ref curIndex);
            token = getToken(tokenList,curIndex);
            expect(token,";",ref curIndex);
        }
        return node;
    }
```


## expr（変更無）
exprの対応日本語名は下記のとおりとしています。
式
```mind:BNF
式       　= 代入式
```
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
```mind:BNF
代入式     = 等式 ("=" 代入式)?
```
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
```mind:BNF
等式       = 関係式("==" 関係式 | "!=" 関係式)*
```
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
```mind:BNF
関係式     = 加減式 ("<" 加減式 | "<=" 加減式 | ">" 加減式 | ">=" 加減式)*
```
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
```mind:BNF
加減式     = 乗除式 ("+" 乗除式 | "-" 乗除式)*
```
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
```mind:BNF
乗除式     = 単項式 ("*" 単項式 | "/" 単項式)*
```
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
```mind:BNF
単項式     = ("+" | "-")? 優先順位
```
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

## primary（変更無）
primaryの対応日本語名は下記のとおりとしています。
優先順位

```mind:BNF
優先順位   = 数 
            | 識別子 
            | "(" 式 ")
```

<details><summary>ロジック仕様とC#ソースコード</summary>
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
</details>

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

## consume_lvarとnew_lvar（変更無）
consume_lvarとnew_lvarの対応日本語名は下記のとおりとしています。
識別子として使用する
新しいローカル変数

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽bool 識別子として使用する(トークン型トークン,参照 int 次索引) 
        ◇(トークン.種類 != トークン種類.識別子 ) の場合
            □偽 を返す
        ◇ここまで
        □次索引 = トークン.次索引;
        □真 を返す
    △
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


```mind:Re:Mind
    ▽ローカル変数型 新しいローカル変数(string 変数名)
        □ローカル変数型 ローカル変数 = new()
        □ローカル変数.変数名 = 変数名
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
        var.offset = ( name.Length - 'a' + 1) * 8;
        var.next = locals;
        locals = var;
        return var;
    }
```
</details>

## find_lvarとnew_lvar_node（変更無）
find_lvarとnew_lvar_nodeの対応日本語名は下記のとおりとしています。
ローカル変数名を探す
新しい変数ノード

<details><summary>ロジック仕様とC#ソースコード</summary>
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

```mind:Re:Mind
    ▽ノード型 新しい変数ノード(ローカル変数型 ローカル変数) 
        □ノード型 ノード = 新しいノード(ノード種類.変数)
        □ノード.変数名 = ローカル変数.変数名
        □ノード.オフセット値 = ローカル変数.オフセット値
        □ノード を返す
     △
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
</details>

## consume_return（変更無）
consume_retrunの対応日本語名は下記のとおりとしています。
リターンとして使用する

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽bool リターンとして使用する(トークン型トークン,参照 int 次索引) 
        ◇(トークン.種類 != トークン種類.リターン文 ) の場合
            □偽 を返す
         ◇ここまで
         □次索引 = トークン.次索引;
         □真 を返す
    △
```

```cs:parse.cs
    /// <summary>リターンとして使用する</summary>
    /// <param name="token">トークン</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>  
    static bool consume_return(Token token, ref int next) {
        if (token.kind != TokenKind.TK_RETURN){
            return false;
        }
        next = token.next;
        return true;
    }
```
</details>

## consume_reserved（新規追加）
consume_reservedの対応日本語名は下記のとおりとしています。
予約語として使用する

```mind:Re:Mind
    ▽bool 予約語として使用する(トークン型トークン,string キーワード,参照 int 次索引) 
        ◇(トークン.種類 == トークン種類.予約語 && トークン.文字列 == キーワード) の場合
            □偽 を返す
         ◇ここまで
         □次索引 = トークン.次索引;
         □真 を返す
    △
```

```cs:parse.cs
    /// <param name="token">トークン</param>
    /// <param name="keyword">キーワード</param>
    /// <param name="next">次索引</param>
    /// <returns>bool</returns>  
    static bool consume_reserved(Token token,string keyword, ref int next) {
        if (!(token.kind == TokenKind.TK_RESERVED && token.str == keyword)){
            return false;
        }
        next = token.next;
        return true;
    }
```
## read_expr_stmt（新規追加）
read_expr_stmtの対応日本語名は下記のとおりとしています。
構文内式

```mind:Re:Mind
    ▽bool 構文内式(List<トークン型> トークンリスト,参照 int 現索引) 
        □ノード型 ノード = 新しいノード(ノード種類.構文内式)
        □ノード.左辺 = 式(トークンリスト,ref 現索引)
        □ノード を返す
    △
```

```cs:parse.cs
    /// <summary>構文内式</summary>
    /// <param name="tokenList">トークンリスト</param>
    /// <param name="curIndex">現索引</param>
    /// <returns>ノード</returns>
    static Node read_expr_stmt(List<Token> tokenList,ref int curIndex) {
        Node node = new_node(NodeKind.ND_EXPR_STMT);
        node.lhs = expr(tokenList,ref curIndex);
        return node;
    }
```

下記のサポート関数の関数名を
isspace　iscomparison　iscomparisonhead　isdigit isarithmetic　is_alnum　strncmp
日本語化した関数名は下記のとおりとしています。
空白か判定する　比較記号か判定する　比較記号頭文字か判定する　数字か判定する 演算子か判定する　英数字アンダスコアか判定する　文字列比較

# トークナイザ
## tokenize （変更有）
tokenizeの日本語化した関数名は下記のとおりとしています。
トークナイズする

 トークナイザで「if、else、while、for」いうキーワードに対応したトークンを認識できるようにします。従来のつくりが1文字づつループしているので、それにあわせたつくりとします。前回の複数文字変数を収集するループの中で、まず切り出された識別子の長さが2文字であったら識別子とifを比較して、識別子の長さが3文字であったら識別子とforを比較して、識別子の長さが4文字であったら識別子とelseを比較して、識別子の長さが5文字であったら識別子とwhileを比較して、合致すればキーワード、合致しなければ複数文字変数とします。

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

            // Keywords

            // Multi-letter identfer
            ◇真==識別子か判定する(入力文字列配列[i]) の場合
                ・string 変数文字列 = 入力文字列配列[i]
                ・int トークン長 = 1
                □i++
                ◇(i<入力文字列配列.Length) の場合
                    〇(識別子か判定する(入力文字列配列[i])) の間は繰り返す
                        □変数文字列+= 入力文字列配列[i]
                        □i++
                        □トークン長++
                        ◇(i>=入力文字列配列.Length) の場合 やめる
                    〇ここまで
                ◇ここまで
                // Keywords
                ◇トークン長==キーワード型.リターン文.長さ && 0==文字列比較(変数文字列,キーワード型.リターン文,キーワード型.リターン文.長さ) の場合
                    □現トークン = 新しいトークン(トークン種類.リターン文, 次索引, 変数文字列,トークン長)
                ◇トークン長==キーワード型.if文.長さ && 0==文字列比較(変数文字列,キーワード型.if文,キーワード型.if文.長さ) の場合
                    □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 変数文字列,トークン長)
                ◇トークン長==キーワード型.for文.長さ && 0==文字列比較(変数文字列,キーワード型.for文,キーワード型.for文.長さ) の場合
                    □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 変数文字列,トークン長)
                ◇トークン長==キーワード型.else文.長さ && 0==文字列比較(変数文字列,キーワード型.else文,キーワード型.else文.長さ) の場合
                    □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 変数文字列,トークン長)
                ◇トークン長==キーワード型.while文.長さ && 0==文字列比較(変数文字列,キーワード型.while文,キーワード型.while文.長さ) の場合
                    □現トークン = 新しいトークン(トークン種類.予約語, 次索引, 変数文字列,トークン長)
                ◇他に   // Multi-letter identfer
                    □現トークン = 新しいトークン(トークン種類.識別子, 次索引, 変数文字列,トークン長)
                ◇ここまで

                □トークンリスト.Add(現トークン)
                □次索引++
                □i++
                □ループ先頭へ
            ◇ここまで

            // two-letter punctuator
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

            // Multi-letter number
            ◇真==数字か判定する(入力文字列配列[i]) の場合

                ・string 数字文字列 = 入力文字列配列[i]
                ・int トークン長 = 1
                □i++
                ◇(i<入力文字列配列.Length) の場合
                    〇(数字か判定する(入力文字列配列[i])) の間は繰り返す
                        □数字文字列+= 入力文字列配列[i]
                        □i++
                        □トークン長++
                        ◇(i>=入力文字列配列.Length) の場合 やめる
                    〇ここまで
                ◇ここまで
                □現トークン = 新しいトークン(トークン種類.整数,次索引, 数字文字列,トークン長)
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
                int len = 1;
                i++;
                if(i<cs.Length){
                    while(isidentfer(cs[i].ToString())) {
                        varStr+= cs[i].ToString();
                        i++;
                        len++;
                        if(i>=cs.Length)break;
                    }
                }
  
                // Keywords
                if(len==Keywords.KW_RETURN.Length && 0==strncmp(varStr, Keywords.KW_RETURN, Keywords.KW_RETURN.Length)){
                    //TK_RETERN
                    cur = new_token(TokenKind.TK_RETURN, next, varStr,len);
                }else if(len==Keywords.KW_IF.Length && 0==strncmp(varStr, Keywords.KW_IF, Keywords.KW_IF.Length)){
                    //TK_RESERVED
                    cur = new_token(TokenKind.TK_RESERVED, next, varStr,len);
                }else if(len==Keywords.KW_FOR.Length && 0==strncmp(varStr, Keywords.KW_FOR, Keywords.KW_FOR.Length)){
                    //TK_RESERVED
                    cur = new_token(TokenKind.TK_RESERVED, next, varStr,len);
                }else if(len==Keywords.KW_ELSE.Length && 0==strncmp(varStr, Keywords.KW_ELSE, Keywords.KW_ELSE.Length)){
                    //TK_RESERVED
                    cur = new_token(TokenKind.TK_RESERVED, next, varStr,len);
                }else if(len==Keywords.KW_WHILE.Length && 0==strncmp(varStr, Keywords.KW_WHILE, Keywords.KW_WHILE.Length)){
                    //TK_RESERVED
                    cur = new_token(TokenKind.TK_RESERVED, next, varStr,len);
                }else{
                    // Multi-letter identfer
                    cur = new_token(TokenKind.TK_IDENT, next,varStr,len);
                }
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
                int len = 1;
                i++;
                if(i<cs.Length){
                    while(isdigit(cs[i].ToString())) {
                        numberStr+= cs[i].ToString();
                        i++;
                        len++;
                        if(i>=cs.Length)break;
                    }
                }
                cur = new_token(TokenKind.TK_NUM,next, numberStr,len);
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

# コードジェネレータ
## gen （変更有）
genの日本語化した関数名は下記のとおりとしています。
コード生成


各制御構文ノードに対応したコード出力を追加します。

```mind:Re:Mind
    ・int ラベルシーケンス = 1;

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
        ◇ノード種類.if文
    	    ・シーケンス=ラベルシーケンス++
    	    ◇(ノード.else側構文 != null)の場合
                □コード生成(ノード.条件式)
                □コンソール出力("  pop rax\n")
                □コンソール出力("  cmp rax, 0\n")
                □コンソール出力("  je  .L.else.%d\n", シーケンス)
                □コード生成(ノード.then側構文)
                □コンソール出力("  jmp .L.end.%d\n", シーケンス)
                □コンソール出力(".L.else.%d:\n", シーケンス)
                □コード生成(ノード.else側構文)
                □コンソール出力(".L.end.%d:\n", シーケンス)
    
            ◇他に
                □コード生成(ノード.条件式)
                □コンソール出力("  pop rax\n")
        		□コンソール出力("  cmp rax, 0\n")
        		□コンソール出力("  je  .L.end.%d\n", シーケンス)
        		□コード生成(ノード.then側構文)
        		□コンソール出力(".L.end.%d:\n", シーケンス)
           ◇ここまで
    	　　□返る
        ◇ノード種類.whle文
    	    ・シーケンス=ラベルシーケンス++
    	    □コンソール出力(".L.begin.%d:\n", シーケンス)
                □コード生成(ノード.条件式)
    	    □コンソール出力("  pop rax\n")
    	    □コンソール出力("  cmp rax, 0\n")
    	    □コンソール出力("  je  .L.end.%d\n", シーケンス)
    	    □コード生成(ノード.then側構文)
    	    □コンソール出力("  jmp .L.begin.%d\n", シーケンス)
    	    □コンソール出力(".L.end.%d:\n", seq)
    	　　□返る
        ◇ノード種類.for文
    	    ・シーケンス=ラベルシーケンス++
    	    ◇(ノード.初期化式 != null)の場合
                	□コード生成(ノード.初期化式)
            ◇ここまで
    	    □コンソール出力(".L.begin.%d:\n", シーケンス)
    	　　◇(ノード.条件式 != null)の場合
    	    	□コード生成(ノード.条件式)
    	    	□コンソール出力("  pop rax\n")
    	    	□コンソール出力("  cmp rax, 0\n")
    	    	□コンソール出力("  je  .L.end.%d\n", シーケンス)
            ◇ここまで
    	    □コード生成(ノード.then側構文)
    	　　◇(ノード.増分式 != null)の場合
        		□コード生成(ノード.増分式)
            ◇ここまで
    	    □コンソール出力("  jmp .L.begin.%d\n", シーケンス)
    	    □コンソール出力(".L.end.%d:\n", seq)
    	　　□返る
        ◇ノード種類.リターン文
            □コード生成(ノード.左辺)
            □コンソール出力("  pop rax\n");
            □コンソール出力("  mov rax, [rax]\n");
            □コンソール出力("  push rax\n");
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

<details><summary>C#ソースコード</summary>
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
        case NodeKind.ND_IF: {
            int seq = labelseq++;
            if (node.els!=null) {
                gen(node.cond);
                Console.Write("  pop rax\n");
                Console.Write("  cmp rax, 0\n");
                Console.Write($"  je  .L.else.{seq}\n");
                gen(node.then);
                Console.Write($"  jmp .L.end.{seq}\n");
                Console.Write($".L.else.{seq}:\n");
                gen(node.els);
                Console.Write($".L.end.{seq}:\n");
            } else {
                gen(node.cond);
                Console.Write("  pop rax\n");
                Console.Write("  cmp rax, 0\n");
                Console.Write($"  je  .L.end.{seq}\n");
                gen(node.then);
                Console.Write($".L.end.{seq}:\n");
            }
            return;
        }
        case NodeKind.ND_WHILE: {
            int seq = labelseq++;
            Console.Write($".L.begin.{seq}:\n");
            gen(node.cond);
            Console.Write("  pop rax\n");
            Console.Write("  cmp rax, 0\n");
            Console.Write($"  je  .L.end.{seq}\n");
            gen(node.then);
            Console.Write($"  jmp .L.begin.{seq}\n");
            Console.Write($".L.end.{seq}:\n");
            return;
        }
        case NodeKind.ND_FOR: {
            int seq = labelseq++;
            if (node.init!=null)
                gen(node.init);
            Console.Write($".L.begin.{seq}:\n");
            if (node.cond!=null) {
                gen(node.cond);
                Console.Write("  pop rax\n");
                Console.Write("  cmp rax, 0\n");
                Console.Write($"  je  .L.end.{seq}\n");
            }
            gen(node.then);
            if (node.inc!=null)
                gen(node.inc);
            Console.Write($"  jmp .L.begin.{seq}\n");
            Console.Write($".L.end.{seq}:\n");
            return;
        }
        case NodeKind.ND_RETURN:
            gen(node.lhs);
            Console.Write("  pop rax\n");
            Console.Write("  mov rax, [rax]\n");
            Console.Write("  push rax\n");
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

## codegen （変更無）
codegenの日本語化した関数名は下記のとおりとしています。
コード生成全体

<details><summary>ロジック仕様とC#ソースコード</summary>
```mind:Re:Mind
    ▽コード生成全体(リスト<ノード型> コードリスト)
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
    △
```
```cs:codegen.cs
    /// <summary>コード生成全体</summary>
    /// <param name="codeList">コードリスト</param>
    static void codegen(List<Node> codeList){
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
    }
```
</details>

# Mainなど記述
## Main（変更無）

<details><summary>ロジック仕様とC#ソースコード</summary>
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
        □手続全体( コードリスト,トークンリスト,ref 現索引)

        // コード生成する
        □コード生成全体( コードリスト)

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

        // コード生成する
        codegen(codeList);

        return 0;
    }
```
</details>

# 入出力コード サンプルイメージ
現状はブロック文に対応していないため、追加した制御構文に対応したサンプルコードが書きにくい状況にあります。~~別記事または本記事への追記でサンプルを検証するかもしれませんが、このステップではコンパイラの出力コードの検証を割愛します。~~
2023/6/25 訂正　while文の検証サンプルの確認がとれましたので追記します。


## chibicc(9cc)return文対応版の実行結果
参照しているコミット historical/oldブランチのコミット[8dab60e] Add "for" statement

C#との比較用の期待結果としてchibicc(9cc)を実行してみます。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。

<details><summary>出力コード サンプルイメージ</summary>

```:i=0; while(i<10) i=i+1; return i;
$ ./chibicc 'i=0; while(i<10) i=i+1; return i;'
.intel_syntax noprefix
.global main
main:
  push rbp
  mov rbp, rsp
  sub rsp, 8
  lea rax, [rbp-8]
  push rax
  push 0
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  add rsp, 8
.L.begin.1:
  lea rax, [rbp-8]
  push rax
  pop rax
  mov rax, [rax]
  push rax
  push 10
  pop rdi
  pop rax
  cmp rax, rdi
  setl al
  movzb rax, al
  push rax
  pop rax
  cmp rax, 0
  je  .L.end.1
  lea rax, [rbp-8]
  push rax
  lea rax, [rbp-8]
  push rax
  pop rax
  mov rax, [rax]
  push rax
  push 1
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  add rsp, 8
  jmp .L.begin.1
.L.end.1:
  lea rax, [rbp-8]
  push rax
  pop rax
  mov rax, [rax]
  push rax
  pop rax
  jmp .L.return
.L.return:
  mov rsp, rbp
  pop rbp
  ret
```
</details>

[オンラインコンパイラCompiler Explorerのx86-64-ClangでIntel記法のアセンブラソースをアセンブルする](https://qiita.com/mylifewithviolin/items/bb2705e16347bbbefbb2)の手順でソースエディタにサンプルソースコードイメージを貼り付けます。
```:
Executor x86-64 clang 16.0.0 (C, Editor #1)

x86-64 clang 16.0.0 -x assembler
Could not execute the program
Compiler returned: 1
Compiler stderr
<source>:26:3: error: invalid instruction mnemonic 'movzb'
  movzb rax, al
  ^~~~~
```

今回はx86-64 clang 16.0.0ではmovzbでエラーがでて実行不可でしたので、コンパイラ指定をx86-64 gcc 13.1に変更しています。
エクゼキュータペインが更新されて下記の状態となり、まだ警告が残っていますが期待値が実行されました。

```:
Executor x86-64 gcc 13.1 (C, Editor #1)

x86-64 gcc 13.1 -x assembler
Compiler stderr
<source>: Assembler messages:
<source>: Warning: end of file not at end of a line; newline inserted
/opt/compiler-explorer/gcc-13.1.0/bin/../lib/gcc/x86_64-linux-gnu/13.1.0/../../../../x86_64-linux-gnu/bin/ld: warning: /tmp/ccoprxIg.o: missing .note.GNU-stack section implies executable stack
/opt/compiler-explorer/gcc-13.1.0/bin/../lib/gcc/x86_64-linux-gnu/13.1.0/../../../../x86_64-linux-gnu/bin/ld: NOTE: This behaviour is deprecated and will be removed in a future version of the linker
Program returned: 10
```
# 実行結果
続いてC#をコンパイルします。ビルド（コンパイル）はVSCodeのタスクで実行しました。
9ccと同じソースコード文字列を与えて実行すると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。

<details><summary>出力コード サンプルイメージ</summary>

```:i=0; while(i<10) i=i+1; return i;
>9cc2cs s "i=0; while(i<10) i=i+1; return i;" 
.intel_syntax noprefix
.globl main
main:
  push rbp
  mov rbp, rsp
  sub rsp, 208
  mov rax, rbp
  sub rax, 8
  push rax
  push 0
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  pop rax
.L.begin.1:
  mov rax, rbp
  sub rax, 8
  push rax
  pop rax
  mov rax, [rax]
  push rax
  push 10
  pop rdi
  pop rax
  cmp rax, rdi
  setl al
  movzb rax, al
  push rax
  pop rax
  cmp rax, 0
  je  .L.end.1
  mov rax, rbp
  sub rax, 8
  push rax
  mov rax, rbp
  sub rax, 8
  push rax
  pop rax
  mov rax, [rax]
  push rax
  push 1
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  jmp .L.begin.1
.L.end.1:
  pop rax
  mov rax, rbp
  sub rax, 8
  push rax
  pop rax
  mov rax, [rax]
  push rax
  pop rax
  mov rsp, rbp
  pop rbp
  ret
```
</details>

## 出力コード サンプルイメージの実行結果 sample.asm
オンラインコンパイラCompiler Explorerのコンパイラ指定をchibicc(9cc)と同じくx86-64 gcc 13.1にした結果です。期待値の10が返っています。
```:
Executor x86-64 gcc 13.1 (C, Editor #1)

x86-64 gcc 13.1 -x assembler
Compiler stderr
<source>: Assembler messages:
<source>: Warning: end of file not at end of a line; newline inserted
/opt/compiler-explorer/gcc-13.1.0/bin/../lib/gcc/x86_64-linux-gnu/13.1.0/../../../../x86_64-linux-gnu/bin/ld: warning: /tmp/ccoprxIg.o: missing .note.GNU-stack section implies executable stack
/opt/compiler-explorer/gcc-13.1.0/bin/../lib/gcc/x86_64-linux-gnu/13.1.0/../../../../x86_64-linux-gnu/bin/ld: NOTE: This behaviour is deprecated and will be removed in a future version of the linker
Program returned: 10
```


# ソースコード
GitHub 鋭意準備中

# おわりに
STEP9よりレファレンス実装のソースコードが解説文とかなり乖離してきていますので、引き続き時間がかかってしまいました。追加事項を解説どおりに実装して、あとはデバッグ実行で動くようにしています。
トークナイザでreturnというトークンを認識できるようにした際に、従来のつくりが1文字づつループしているので、前回の複数文字変数を収集するループの中でキーワード判定を実装しているあたりは、オリジナルのCソースとは異なるので、後々ひきずるかもしれません。いまのところ問題がとくにないので新しい複数文字のキーワードも同様のままで進めてみました。続けてステップ13のブロック文に進行します。



# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94
