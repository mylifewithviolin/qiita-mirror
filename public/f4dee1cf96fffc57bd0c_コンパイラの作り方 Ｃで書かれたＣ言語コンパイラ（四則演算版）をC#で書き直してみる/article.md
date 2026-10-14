# はじめに
[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみます。（まずは四則演算対応）

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。本記事の解釈可能ソース状態はCとすら言えない四則演算です。当面は目的達成のためのスキルと知見の獲得途上ということでご容赦願います。（参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため）
## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
gcc 11
C# 10 dotnet-sdk-6.0.404-win-x64

## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。
## 類似した記事
コード生成部分の9ccオリジナルがアセンブラを出力するのに対して、そこを若干書き換えてスタック志向言語のMindのソースを出力するとした記事が別にございまして、前半部分はテキストリソースをかなり共有しております。当記事ではそちらの記事の補足もかねてCっぽい点をどのようにC#に書き換えたかを少し詳しく説明し、9ccをC#で書いてみたいと思われた方の参考になればと考えております。

# 実装のポイント
## トークンリスト
上段がオリジナルのCで書かれたソース（以下引用元は[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)）、下段が今回c#で書いた対応コードです。

まず、トークンまわりを下記のように書き換えてみました。

```c:9cc.c
        // トークン型
        struct Token {
            TokenKind kind; // トークンの型
            Token *next;    // 次の入力トークン
            int val;        // kindがTK_NUMの場合、その数値
            char *str;      // トークン文字列
        };

```
```cs:Program.cs
        // トークン型
        class Token {
            public TokenKind kind; // トークンの型
            public  int next;    // 次の入力トークン
            public int val;        // kindがTK_NUMの場合、その数値
            public string? str;      // トークン文字列
        };
```
Cは構造体で宣言されていますが、C#は変数だけのクラスにしました。最初のメンバkindは列挙型で下記のように宣言しています。

```c:9cc.c
    // トークンの種類
    typedef enum {
      TK_RESERVED, // 記号
      TK_NUM,      // 整数トークン
      TK_EOF,      // 入力の終わりを表すトークン
    } TokenKind;
```
```cs:Program.cs
    // トークンの種類
    enum TokenKind{
        TK_RESERVED, // 記号
        TK_NUM,      // 整数トークン
        TK_EOF,      // 入力の終わりを表すトークン
    } ;
```

9ccでは自Token型のポインタをToken型のメンバにして、再帰的ないもづる参照を図っている感じでしたが、c#では自型の参照を持たない単純なToken型のLISTにして、LINQで配列みたいにするとしてみました。
```c:9cc.c
        // 入力文字列pをトークナイズしてそれを返す
        Token *tokenize(char *p) {
            Token head;
            head.next = NULL;
            Token *cur = &head;

            while (*p) {
                // 空白文字をスキップ略
                 if (*p == '+' || *p == '-') {
                     cur = new_token(TK_RESERVED, cur, p++);
                     continue;
                 }
                //ループ内略
            }

            new_token(TK_EOF, cur, p);
            return head.next;
        }

```
```cs:Program.cs
        // 入力文字列pをトークナイズしてトークンリストを返す
        static List<Token> tokenize(string p) {
            int next = 1;
            Token cur = new();
            List<Token> tokenList =new();

            var cs = p.ToCharArray();
            int i= 0;
            while(i<cs.Length) {
                // 空白文字をスキップ略

                if (isarithmetic(cs[i].ToString())) {
                    cur = new_token(TokenKind.TK_RESERVED, next, cs[i].ToString());
                    tokenList.Add(cur);
                    next++;
                    i++;
                    continue;
                }
                //ループ内略
            }
            cur = new_token(TokenKind.TK_EOF, next, "");
            tokenList.Add(cur);
            return tokenList;
        }
```
LINQでリストを配列みたいにしているところです。コンパイラの実装にLINQなんか使っていいんだろうか？という一抹の疑念あり。
```cs:Program.cs
    static Token getToken(List<Token> tokenList,int curIndex) {
        if(curIndex>=tokenList.Count) return new Token();
        Token token = tokenList.ElementAt(curIndex);//次のトークン
        return token;
    }

```
次の節にでてくるパーサの中でどかどか使われています。

下記のnew_tokenもCっぽいところをC#っぽく書き換えたと筆者的には思っている箇所です。実行速度という点ではやはりポインタ演算のが速いのでしょうね。

```c:9cc.c
    // 新しいトークンを作成してcurに繋げる
    Token *new_token(TokenKind kind, Token *cur, char *str) {
      Token *tok = calloc(1, sizeof(Token));
      tok->kind = kind;
      tok->str = str;
      cur->next = tok;
      return tok;
    }
```
```cs:Program.cs
    // 新しいトークンを作成してnextインデックスをセットする
    static Token new_token(TokenKind kind, int next, string str) {
        Token tok = new();
        tok.kind = kind;
        tok.str = str;
        tok.next = next;
        return tok;
    }
```
## 抽象構文木
続いて、抽象構文木ですが、こちらはそんなにCと変わらないです。ただし、ポインタの左辺、右辺はヌラブルのNode型としてみました。
```c:9cc.c
typedef struct Node Node;

// 抽象構文木のノードの型
struct Node {
  NodeKind kind; // ノードの型
  Node *lhs;     // 左辺
  Node *rhs;     // 右辺
  int val;       // kindがND_NUMの場合のみ使う
};

```
```cs:Program.cs
     // 抽象構文木のノードの型
    class  Node {
        public NodeKind kind; // ノードの型
        public Node? lhs;     // 左辺
        public Node? rhs;     // 右辺
        public int val;       // kindがND_NUMの場合のみ使う
    };
```
最初のメンバのkindは列挙型です。
```c:9cc.c
    // 抽象構文木のノードの種類
    typedef enum {
      ND_ADD, // +
      ND_SUB, // -
      ND_MUL, // *
      ND_DIV, // /
      ND_NUM, // 整数
    } NodeKind;
```
```cs:Program.cs
    // 抽象構文木のノードの種類
    enum NodeKind{
        ND_ADD, // +
        ND_SUB, // -
        ND_MUL, // *
        ND_DIV, // /
        ND_NUM, // 整数
    } ;
```
トークンリストをmain関数内のローカル変数にしてしまったため、各関数に引数渡ししなければならない点がちょっとあとで後悔しています。次の要素を示すインデックスが露出しているのも不細工ですが、試作ということでご笑覧ください。
```c:9cc.c
        // パースする
        Node *expr() {
          Node *node = mul();

          for (;;) {
            if (consume('+'))
              node = new_node(ND_ADD, node, mul());
            else if (consume('-'))
              node = new_node(ND_SUB, node, mul());
            else
              return node;
          }
        }
```
```cs:Program.cs
        // パースする
         static Node expr(List<Token> tokenList,ref int curIndex) {
            Node node = mul(tokenList,ref curIndex);
            Token token = getToken(tokenList,curIndex);//次のトークン
            for (;;) {
                if (consume(token,"+",ref curIndex)){
                    node = new_node(NodeKind.ND_ADD, node, mul(tokenList,ref curIndex));
                    token = getToken(tokenList,curIndex);//次のトークン
                    }
                else if (consume(token,"-",ref curIndex)){
                    node = new_node(NodeKind.ND_SUB, node, mul(tokenList,ref curIndex));
                    token = getToken(tokenList,curIndex);//次のトークン
                    }
                else
                    return node;
            }
        }
```


# 入出力コード サンプルイメージ
この記事が対象としている9ccの対象構文は優先順位対応の四則演算で変数も導入前のものですから、解釈できるのは下記のような四則演算だけです。
```C:C
5 + 6 * 7
5 * ( 9 - 6 )
( 3 + 5 ) / 2
```
これらの式を対象に9ccと同じアセンブラを出力します。
## 9cc四則演算版の実行結果
まずオリジナルの9ccをgccでコンパイルします。
```
$ gcc main.c
$ ls -l
total 40
-rwxr-xr-x 1 puremind puremind 16984 Jan 26 20:43 a.out
-rw-r--r-- 1 puremind puremind  5069 Jan 26 20:30 main.c
-rw-r--r-- 1 puremind puremind  8408 Jan 26 20:35 main.o
```
main.oはcオプションでコンパイルした結果です。
C#との比較用の期待結果として9ccを実行してみます。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
```:5 + 6 * 7
$ ./a.out '5 + 6 * 7'
.intel_syntax noprefix
.global main
main:
  push 5
  push 6
  push 7
  pop rdi
  pop rax
  imul rax, rdi
  push rax
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rax
  ret
```
```:5 * ( 9 - 6 )
$ ./a.out '5 * ( 9 - 6 )'
.intel_syntax noprefix
.global main
main:
  push 5
  push 9
  push 6
  pop rdi
  pop rax
  sub rax, rdi
  push rax
  pop rdi
  pop rax
  imul rax, rdi
  push rax
  pop rax
  ret
```
~~re~~ 2023/01/27上記行訂正
```:( 3 + 5 ) / 2
$ ./a.out '( 3 + 5 ) / 2'
.intel_syntax noprefix
.global main
main:
  push 3
  push 5
  pop rdi
  pop rax
  add rax, rdi
  push rax
  push 2
  pop rdi
  pop rax
  cqo
  idiv rdi
  push rax
  pop rax
  ret
```
# 実行結果
## コンパイラの出力コード
続いてC#をコンパイルします。ビルド（コンパイル）はVSCodeのタスクで実行しました。下記のようなファイルが生成されました。
```
>dir
C:\developments\cs6\9cc\bin\Debug\net6.0 のディレクトリ
2023/01/26  21:21               401 9cc.deps.json
2023/01/26  21:21            15,872 9cc.dll
2023/01/26  21:21           147,968 9cc.exe
2023/01/26  21:21            16,216 9cc.pdb
2023/01/26  21:21               147 9cc.runtimeconfig.json
```
9cc四則演算版と同じ四則演算文字列を与えて実行すると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。
```:5 + 6 * 7
>9cc s "5 + 6 * 7"
.intel_syntax noprefix
.globl main
main:
  push 5
  push 6
  push 7
  pop rdi
  pop rax
  imul rax, rdi
  push rax
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rax
  ret
```
```:5 * ( 9 - 6 )
>9cc s "5 * ( 9 - 6 )" 
.intel_syntax noprefix
.globl main
main:
  push 5
  push 9
  push 6
  pop rdi
  pop rax
  sub rax, rdi
  push rax
  pop rdi
  pop rax
  imul rax, rdi
  push rax
  pop rax
  ret
```
```:( 3 + 5 ) / 2
>9cc s "( 3 + 5 ) / 2"              
.intel_syntax noprefix
.globl main
main:
  push 3
  push 5
  pop rdi
  pop rax
  add rax, rdi
  push rax
  push 2
  pop rdi
  pop rax
  cqo
  idiv rdi
  push rax
  pop rax
  ret
```

## コード生成部
下記は9cc四則演算版のメイン関数とコード生成関数を書き換えたものです。

```CS:Program.cs
    static int Main3(string[] args)
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

```CS:Program.cs
 	  // 抽象構文木を下りながらコード生成
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
        }

        Console.Write("  push rax\n");
    }
```
このあたりの演算命令は、試作のため9ccと同様リテラルで書いています。

## Cライク関数
また、しばらくの間はバグを埋め込まないようなるべく構文構造を同じようにすべく書き換えておりますので、C#になく9ccで使われているCの標準関数などに相当する下記のようなユーティリティ関数も書き足しています。
```cs:Program.cs
    static bool isspace( string input )
    {
         return( Regex.IsMatch( input,"\\s" ) );
    }
```
```cs:Program.cs
    static bool isdigit( string input )
    {
         return( Regex.IsMatch( input, "[0-9]" ) );
    }
```
```cs:Program.cs
    static bool isarithmetic( string input )
    {
         return( Regex.IsMatch( input,"[\\+\\-\\*\\/\\(\\)]" ) );
    }
```
```cs:Program.cs
    static int strtol(string str){
        return  int.Parse(str);
    }

```
# ソースコード
GitHub [9cc2cs first commit 9cc four arithmetic operation version](https://github.com/mylifewithviolin/9cc2cs/commit/74e8900619bc4128253f2c36fc6d2f3103a291bc)
# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/doz13189/items/04988e60905f4e933f6f

https://qiita.com/pocari/items/d272e87274a1486298bc



