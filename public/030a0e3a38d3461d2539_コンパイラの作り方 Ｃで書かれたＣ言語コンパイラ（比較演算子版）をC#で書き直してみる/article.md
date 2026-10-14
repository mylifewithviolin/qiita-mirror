# はじめに

[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみます。（比較演算子対応）だんだん１ステップの実装量が増えてきている感じです。

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。参考サイトの9ccの「ステップ7: 比較演算子」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため、段階的に対応構文が増えていきます。

## この記事内容の作業環境
Windows11
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
# 実装のポイント
## トークン長さの追加とconsume関数の引数型変更
参考サイトの9ccの「ステップ6：単項プラスと単項マイナス」につづく「ステップ7: 比較演算子」では、ソースコード上の差分としては、下記の関数２つが説明されており、レファレンスとして9cc後継のchibiccソースコードのgithub上の最も近い状態のコミットへのリンクが記載されています。

```c:9cc.c
    struct Token {
      TokenKind kind; // トークンの型
      Token *next;    // 次の入力トークン
      int val;        // kindがTK_NUMの場合、その数値
      char *str;      // トークン文字列
      int len;        // トークンの長さ
    };

    bool consume(char *op) {
      if (token->kind != TK_RESERVED ||
          strlen(op) != token->len ||
          memcmp(token->str, op, token->len))
        return false;
      token = token->next;
      return true;
    }
```
```c:chibicc.c
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
C#側のソースでは[前回記事](https://qiita.com/mylifewithviolin/items/fb8dc06460855928162f)の状態のコードをコメントアウトで残しておきます。C側の対応ソースはchibicc状態とします。

```cs:Program.cs
    class Token {
        public TokenKind kind; // トークンの型
        public  int next;    // 次の入力トークン
        public int val;        // kindがTK_NUMの場合、その数値
        public string? str;      // トークン文字列
        public int len;        // トークンの長さ
        
    };

    // 次のトークンが期待している記号のときには、トークンを1つ読み進めて
    // 真を返す。それ以外の場合には偽を返す。
    static bool consume(Token token,string op, ref int next) {
        //if (token.kind != TokenKind.TK_RESERVED || token.str != op)
        if (token.kind != TokenKind.TK_RESERVED || op.Length  != token.len || 
                    token.str != op)
            return false;
        next = token.next;
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
```

```cs:Program.cs
    // 抽象構文木のノードの種類
    enum NodeKind{
        ND_ADD, // +
        ND_SUB, // -
        ND_MUL, // *
        ND_DIV, // /
        ND_EQ,  // ==
        ND_NE,  // !=
        ND_LT,  // <
        ND_LE,  // <=
        ND_NUM, // 整数
    } ;
```
この変更(追加)に伴い、直感的にわかりやすい変更は、コード生成関数genです。

## genの変更

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
case文にもノード種類が追加されました。

## expectの変更
```c:chibicc.c
    void expect(char *op) {
      if (token->kind != TK_RESERVED || strlen(op) != token->len ||
          memcmp(token->str, op, token->len))
        error_at(token->str, "expected \"%s\"", op);
      token = token->next;
    }
```
```cs:Program.cs
   static  void expect(Token token,string op, ref int next) {
        //if (token.kind != TokenKind.TK_RESERVED || token.str != op)
        if (token.kind != TokenKind.TK_RESERVED || op.Length  != token.len || 
                token.str != op)
            error($"'{op}'ではありません");
        next = token.next;
    }
```
基本的にトークン長チェックの追加です。
## exprの変更

```c:chibicc.c
    // expr = equality
    Node *expr() {
      return equality();
    }
```
```cs:Program.cs
    static Node expr(List<Token> tokenList,ref int curIndex) {
        return equality(tokenList,curIndex);
    }
```
exprは演算子の優先順位の変更に伴い、equalityを返すだけに変更されます。従来のexprの中身はこの後に追加されるaddに継承されます。

# 比較演算子対応関数の追加

いよいよ比較演算子対応関数の追加です。

## equality
等しい、等しくない。
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
```

## add
従来のexprの中身はこのaddに継承されています。
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
    static Node add(List<Token> tokenList,ref int curIndex) {
        Node node = mul(tokenList,ref curIndex);
        Token token = getToken(tokenList,curIndex);//次のトークン
        for (;;) {
            if (consume(token,"+",ref curIndex)){
                //node = new_node(NodeKind.ND_ADD, node, mul(tokenList,ref curIndex));
                node = new_binary(NodeKind.ND_ADD, node, mul(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else if (consume(token,"-",ref curIndex)){
                //node = new_node(NodeKind.ND_SUB, node, mul(tokenList,ref curIndex));
                node = new_binary(NodeKind.ND_SUB, node, mul(tokenList,ref curIndex));
                token = getToken(tokenList,curIndex);//次のトークン
                }
            else
                return node;
        }
    }
```
C#側は文字の引数型は文字列にしていたので変更ありませんが、C側は下記の関数が変更の影響を受けています。
unary mul primary

# C#版トークナイザの全文
C#で書き換えたトークナイザの全文です。chibcc側は長くなるので割愛します。
## tokenize
```cs:Program.cs
    // 入力文字列pをトークナイズしてトークンリストを返す
    static List<Token> tokenize(string p) {
        int next = 1;
        Token cur = new();
        List<Token> tokenList =new List<Token>();

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
Cでは文字列ポインタでループしているため、2文字合致したらポインタを2加算してと、シンプルに記述していますが、このC#版は1文字づつ回しているので2文字の比較演算子の先頭1文字と合致したら1文字先読みして2文字合致したらカウンタを2加算してとしています。

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
GitHub [9cc2cs 9cc comparison operator version](https://github.com/mylifewithviolin/9cc2cs/commit/636d4d695a572da46994fbcfa6dd185f357c0264)
# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c
