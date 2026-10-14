# はじめに

[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いています。「ステップ7：比較演算子」を書いた時点で諸般の事情で間が空いたので、少し内容を忘れてきました。そこで、関数名・変数名を日本語を導入することでソースコードの可読性を向上させて、なにを書いているロジックなのかをわかりやすくしてみることにしました。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。参考サイトの9ccの「ステップ7: 比較演算子」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため、段階的に対応構文が増えていきます。オリジナルのC言語に関数名・変数名をそろえている記事は[こちら](https://qiita.com/mylifewithviolin/items/030a0e3a38d3461d2539)になります。記事内容はほとんどこちらと同じで、ソースコードの関数名・変数名・構造体名などが日本語になっています。

## この記事内容の作業環境
Windows 11 22H2
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
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

# 実装のポイント
## トークン長さの追加とconsume関数の引数型変更
参考サイトの9ccの「ステップ6：単項プラスと単項マイナス」につづく「ステップ7: 比較演算子」では、ソースコード上の差分としては、下記の関数２つが説明されており、レファレンスとして9cc後継のchibiccソースコードのgithub上の最も近い状態のコミットへのリンクが記載されています。

```c:chibicc.c
    // トークンの種類
    typedef enum {
        TK_RESERVED, // 記号
        TK_NUM,      // 整数トークン
        TK_EOF,      // 入力の終わりを表すトークン
    } TokenKind;

    struct Token {
      TokenKind kind; // Token kind
      Token *next;    // Next token
      int val;        // If kind is TK_NUM, its value
      char *str;      // Token string
      int len;        // Token length
    };

    // Consumes the current token if it matches `op`.
    bool consume(char *op) {
      if (token->kind != TK_RESERVED || strlen(op) != token->len ||
          memcmp(token->str, op, token->len))
        return false;
      token = token->next;
      return true;
    }
```
今回の差分では、chibiccとの差異はなく、前回のステップでchibiccソースコードベースめの移行は完了していますので、C側ではconsume関数の引数が文字列ポインタになった点に注意すればだいじょうぶです。


github上のchibiccソースコード同士の直前コミットとの差分も手掛かりにはなります。
C側の対応ソースはchibicc状態とします。

consumeの日本語化した関数名は下記のとおりとしています。
使用する

```cs:Program.cs
   enum トークン種類{
        予約語,  // 記号
        整数,      // 整数トークン
        終端,      // 入力の終わりを表すトークン
    }

    class トークン型 {
        public トークン種類 種類; // Token kind
        public int 次索引;    // Next token
        public int 値;        // kindがTK_NUMの場合、その数値
        public string? 文字列;     // Token string
        public int 長さ;        // Token length
        
    }

    // 次のトークンが期待している記号のときには、トークンを1つ読み進めて
    // 真を返す。それ以外の場合には偽を返す。
    static bool 使用する(トークン型トークン,string 記号文字, ref int 次索引) {
        if (トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.長さ || 
                    トークン.文字列 != 記号文字)
            return false;
        次索引 = トークン.次索引;
        return true;
    }
```
C#でconsume関数を書いたとき、文字の引数型は文字列にしていたので、C側の変更の影響は受けません。

## 比較演算子の追加
<、<=、==、!=を追加します。>、>=　を追加しないのは、左辺と右辺を交代させることで、対処するようです。

```c:chibicc.c
    typedef enum {
      ND_ADD, // +
      ND_SUB, // -
      ND_MUL, // *
      ND_DIV, // /
      ND_EQ,  // ==
      ND_NE,  // !=
      ND_LT,  // <
      ND_LE,  // <=
      ND_NUM, // Integer
    } NodeKind;

    struct Node {
      NodeKind kind; // Node kind
      Node *lhs;     // Left-hand side
      Node *rhs;     // Right-hand side
      int val;       // Used if kind == ND_NUM
    };
```

```cs:Program.cs

    // 抽象構文木のノードの種類
    enum ノード種類{
        加算記号, // +
        減算記号, // -
        乗算記号, // *
        除算記号, // /
        比較等号,  // ==
        比較不等号,  // !=
        比較小なり,  // <
        比較小なり等,  // <=
        整数, // 整数
    }

    // 抽象構文木のノードの型
    class  ノード型 {
        public ノード種類 種類; // Node kind
        public ノード型? 左辺;    // Left-hand side
        public ノード型? 右辺;    // Right-hand side
        public int 値;       // kindがND_NUMの場合のみ使う
    }
```
この変更(追加)に伴い、直感的にわかりやすい変更は、コード生成関数genです。

## genの変更
genの日本語化した関数名は下記のとおりとしています。
コード生成

```c:chibicc.c
 // 抽象構文木を下りながらコード生成
void gen(Node *node) {
  if (node->kind == ND_NUM) {
    printf("  push %d\n", node->val);
    return;
  }

  gen(node->lhs);
  gen(node->rhs);

  printf("  pop rdi\n");
  printf("  pop rax\n");

  switch (node->kind) {
  case ND_ADD:
    printf("  add rax, rdi\n");
    break;
  case ND_SUB:
    printf("  sub rax, rdi\n");
    break;
  case ND_MUL:
    printf("  imul rax, rdi\n");
    break;
  case ND_DIV:
    printf("  cqo\n");
    printf("  idiv rdi\n");
    break;
    case ND_EQ:
      printf("  cmp rax, rdi\n");
      printf("  sete al\n");
      printf("  movzb rax, al\n");
      break;
    case ND_NE:
      printf("  cmp rax, rdi\n");
      printf("  setne al\n");
      printf("  movzb rax, al\n");
      break;
    case ND_LT:
      printf("  cmp rax, rdi\n");
      printf("  setl al\n");
      printf("  movzb rax, al\n");
      break;
    case ND_LE:
      printf("  cmp rax, rdi\n");
      printf("  setle al\n");
      printf("  movzb rax, al\n");
      break;
  }

  printf("  push rax\n");
}
```

```cs:Program.cs
    static void コード生成(ノード型 ノード) {
        if (ノード.種類 == ノード種類.整数) {
            Console.Write($"  push {ノード.値}\n");
            return;
        }

        コード生成(ノード.左辺);
        コード生成(ノード.右辺);

        Console.Write("  pop rdi\n");
        Console.Write("  pop rax\n");

        switch (ノード.種類) {
        case ノード種類.加算記号:
            Console.Write("  add rax, rdi\n");
            break;
        case ノード種類.減算記号:
            Console.Write("  sub rax, rdi\n");
            break;
        case ノード種類.乗算記号:
            Console.Write("  imul rax, rdi\n");
            break;
        case ノード種類.除算記号:
            Console.Write("  cqo\n");
            Console.Write("  idiv rdi\n");
            break;
        case ノード種類.比較等号:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  sete al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case ノード種類.比較不等号:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setne al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case ノード種類.比較小なり:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setl al\n");
            Console.Write("  movzb rax, al\n");
            break;
        case ノード種類.比較小なり等:
            Console.Write("  cmp rax, rdi\n");
            Console.Write("  setle al\n");
            Console.Write("  movzb rax, al\n");
            break;
        }

        Console.Write("  push rax\n");
    }
```
case文にもノード種類が追加されました。

## expectの変更
expectの日本語化した関数名は下記のとおりとしています。
予想する

```c:chibicc.c
    void expect(char *op) {
      if (token->kind != TK_RESERVED || strlen(op) != token->len ||
          memcmp(token->str, op, token->len))
        error_at(token->str, "expected \"%s\"", op);
      token = token->next;
    }
```
```cs:Program.cs
   static  void 予想する(トークン型 トークン,string 記号文字, ref int 次索引) {
        if (トークン.種類 != トークン種類.予約語 || 記号文字.Length  != トークン.len || 
                トークン.文字列 != 記号文字)
            error($"'{記号文字}'ではありません");
        次索引 = トークン.次索引;
    }
```
基本的にトークン長チェックの追加です。
## exprの変更
exprの日本語化した関数名は下記のとおりとしています。
式

```c:chibicc.c
    // expr = equality
    Node *expr() {
      return equality();
    }
```
```cs:Program.cs
    static ノード型 式(List<トークン型> トークンリスト,ref int 現索引) {
        return 等式(トークンリスト,現索引);
    }
```
exprは演算子の優先順位の変更に伴い、equalityを返すだけに変更されます。従来のexprの中身はこの後に追加されるaddに継承されます。


# 比較演算子対応関数の追加

比較演算子対応関数の追加です。

## equality
等しい、等しくない。
equalityの日本語化した関数名は下記のとおりとしています。
等式

```c:chibicc.c
    // equality = relational ("==" relational | "!=" relational)*
    Node *equality() {
      Node *node = relational();
    
      for (;;) {
        if (consume("=="))
          node = new_binary(ND_EQ, node, relational());
        else if (consume("!="))
          node = new_binary(ND_NE, node, relational());
        else
          return node;
      }
    }
```

```cs:Program.cs
    static ノード型 等式(List<トークン型> トークンリスト,ref int 現索引) {
        ノード型 ノード = 関係式(トークンリスト,ref 現索引);
        トークン型 トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
        for (;;) {
            if (使用する(トークン,"-=",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較等号, ノード,  関係式(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
            }
            else if (使用する(トークン,"!=",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較不等号, ノード, 関係式(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
            }
            else
            return ノード;
        }
    }
```
## relational
大小関係。
relationalの日本語化した関数名は下記のとおりとしています。
関係式

```c:chibicc.c
    // relational = add ("<" add | "<=" add | ">" add | ">=" add)*
    Node *relational() {
      Node *node = add();
    
      for (;;) {
        if (consume("<"))
          node = new_binary(ND_LT, node, add());
        else if (consume("<="))
          node = new_binary(ND_LE, node, add());
        else if (consume(">"))
          node = new_binary(ND_LT, add(), node);
        else if (consume(">="))
          node = new_binary(ND_LE, add(), node);
        else
          return node;
      }
    }
```

```cs:Program.cs
    static ノード型 関係式(List<トークン型> トークンリスト,ref int 現索引) {
        ノード型 ノード = 加減式(トークンリスト,ref 現索引);
        トークン型 トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
        for (;;) {
            if (使用する(トークン,"<",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較小なり, ノード, 優先順位(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
            }
            else if (使用する(トークン,"<=",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較小なり等, ノード, 優先順位(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
                }
            else if (使用する(トークン,">",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較小なり, 加減式(トークンリスト,ref 現索引), ノード);
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
                }
            else if (使用する(トークン,">=",ref 現索引)){
                ノード = 新しい二分木(ノード種類.比較小なり等, 加減式(トークンリスト,ref 現索引), ノード);
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
                }
            else
              return ノード;
        }
  }
```

## add
従来のexprの中身はこのaddに継承されています。
adの日本語化した関数名は下記のとおりとしています。
加減式

```c:chibicc.c
    // add = mul ("+" mul | "-" mul)*
    Node *add() {
      Node *node = mul();
    
      for (;;) {
        if (consume("+"))
          node = new_binary(ND_ADD, node, mul());
        else if (consume("-"))
          node = new_binary(ND_SUB, node, mul());
        else
          return node;
      }
    }
```

```cs:Program.cs
    static ノード型 加減式(List<トークン型> トークンリスト,ref int 現索引 {
        ノード型 ノード = 乗除式(トークンリスト,ref 現索引);
        トークン型 トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
        for (;;) {
            if (使用する(トークン,"+",ref 現索引)){
                ノード = 新しい二分木(ノード種類.加算記号,ノード, 乗除式(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
                }
            else if (使用する(トークン,"-",ref 現索引)){
                ノード = 新しい二分木(ノード種類.減算記号, ノード, 乗除式(トークンリスト,ref 現索引));
                トークン = トークンを取得する(トークンリスト,現索引);//次のトークン
                }
            else
                return ノード;
        }
    }
```
C#側は文字の引数型は文字列にしていたので変更ありませんが、C側は下記の関数が変更の影響を受けています。
unary mul primary
C#側の記述は本記事では割愛しています。日本語化した関数名は下記のとおりとしています。
単項式 乗除式 優先順位

# C#版トークナイザの全文
C#で書き換えたトークナイザの全文です。chibcc側は長くなるので割愛します。

## tokenize
tokenizeの日本語化した関数名は下記のとおりとしています。
トークナイズする

下記のサポート関数の関数名を
isspace　iscomparison　iscomparisonhead　isdigit isarithmetic　new_token
日本語化した関数名は下記のとおりとしています。
空白か判定する　比較記号か判定する　比較記号頭文字か判定する　数字か判定する 演算子か判定する　新しいトークン

```cs:Program.cs
    // 入力文字列をトークナイズしてトークンリストを返す
    static List<トークン型> トークナイズする(string 入力文字列) {
        int 次索引 = 1;
        トークン型 現トークン = new();
        List<トークン型> トークンリスト =new List<トークン型>();

        var 入力文字列配列 = 入力文字列.ToCharArray();
        int i= 0;
        while(i<入力文字列配列.Length) {
            // 空白文字をスキップ
            if (空白か判定する(入力文字列配列[i].ToString())) {
                i++;
                continue;
            }
            // Multi-letter punctuator
            if (比較記号頭文字か判定する(入力文字列配列[i].ToString())) {
                if(i+1<入力文字列配列.Length){
                    var comp =入力文字列配列[i].ToString()+入力文字列配列[i+1].ToString();
                    if (比較記号か判定する(comp)) {
                        現トークン = 新しいトークン(トークン種類.予約語, 次索引, comp,2);
                        トークンリスト.Add(現トークン);
                        次索引++;
                        i+=2;
                        continue;
                    }
                }
            }

            // Single-letter punctuator
            if (演算子か判定する(入力文字列配列[i].ToString())) {
                現トークン = 新しいトークン(トークン種類.予約語, 次索引, 入力文字列配列[i].ToString(),1);
                トークンリスト.Add(現トークン);
                次索引++;
                i++;
                continue;
            }

            if (数字か判定する(入力文字列配列[i].ToString())) {

                string 数字文字列 = 入力文字列配列[i].ToString();
                i++;
                if(i<入力文字列配列.Length){
                    while(数字か判定する(入力文字列配列[i].ToString())) {
                        数字文字列+= 入力文字列配列[i].ToString();
                        i++;
                        if(i>=入力文字列配列.Length)break;
                    }
                }
                現トークン = 新しいトークン(トークン種類.整数,次索引, 数字文字列,i);
                現トークン.値 = strtol(数字文字列);
                トークンリスト.Add(現トークン);
                次索引++;
                continue;
            }
    
            //ここに進んだら例外
            error("トークナイズできません");
            i++;
        }

        現トークン = 新しいトークン(トークン種類.終端,次索引, "",0);
        トークンリスト.Add(現トークン);
        return トークンリスト;
    }
```
Cでは文字列ポインタでループしているため、2文字合致したらポインタを2加算してと、シンプルに記述していますが、このC#版は1文字づつ回しているので2文字の比較演算子の先頭1文字と合致したら1文字先読みして2文字合致したらカウンタを2加算してとしています。

# chibicc移行リファクタリング（「ステップ6：単項プラスと単項マイナス」の転記）
## new_nodeとnew_binary
new_nodeがメモリ確保とノード種類のセットの単機能となり、new_binaryが従来のnew_nodeの役割を担っています。

```c:chibicc.c
    Node *new_node(NodeKind kind) {
      Node *node = calloc(1, sizeof(Node));
      node->kind = kind;
      return node;
    }
    
    Node *new_binary(NodeKind kind, Node *lhs, Node *rhs) {
      Node *node = new_node(kind);
      node->lhs = lhs;
      node->rhs = rhs;
      return node;
    }
```

```cs:Program.cs
    static ノード型 新しいノード(ノード種類 種類) {
        ノード型 ノード = new();
        ノード.種類 = 種類;
        return ノード;
    }

    static ノード型 新しい二分木(ノード種類 種類, ノード型 左辺, ノード型 右辺) {
        ノード型 ノード = 新しいノード(種類);
        ノード.左辺 = 左辺;
        ノード.右辺 = 右辺;
        return ノード;
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
GitHub準備中

# おわりに

局所的な変数の変数名は英字の場合は意外と略字が使えますが、日本字だと略すと意味が逆につかみづらくなる場合があるので、そのような場合は英字のままでもよいかもしれません。

また、クラス名とインスタンス名は英字の先頭大文字か小文字かでの識別子としてわけることができないので、この例ではクラス名としての型名は、クラス名＋「型」というように割り切っています。インスタンス名がクラス名から「型」を除くとしています。

記事のなりが参考資料の「ステップ6：単項プラスと単項マイナス」からの差分の説明となっているので、全体像が少しつかいにく印象を書いていて感じました。あとで、ロジック仕様をまとめてみようと考えています。

# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c
