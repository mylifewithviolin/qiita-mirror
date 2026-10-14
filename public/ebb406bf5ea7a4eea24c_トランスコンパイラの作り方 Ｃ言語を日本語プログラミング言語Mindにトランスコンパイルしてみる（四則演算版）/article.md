
# はじめに

とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみます。

オリジナルの9ccはアセンブラを出力しますが、目的は低レイヤを知ることではないので、本課題ではスタック志向言語の日本語プログラミング言語Mindの等価処理を出力させてみます。（まずは四則演算対応）

## この記事内容の作業目的
[日本語トランスコンパイラ言語 Re:Mind という自作言語の企画趣旨](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)に書いてあります。
Cをソース言語とすることは目的ではないのですが、当面は目的達成のためのスキルと知見の獲得途上ということでご容赦願います。（本記事の解釈可能ソース状態はCとすら言えない四則演算です。参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため）
## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu 22.04.1 LTS）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
C# 10 dotnet-sdk-6.0.404-win-x64
Mind 8 for Linux　mind-for-linux-8.0.08.tgz
## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。

# 実装のポイント
## トークンリスト
まず、トークンまわりをかきのように書き換えてみました。
上段がオリジナルのCで書かれたソース（以下引用元は[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)）、下段が今回c#で書いた対応コードです。
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
C#ではToken型のLISTにして、LINQで配列みたいにするとしてみました。
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
## 抽象構文木
続いて、抽象構文木ですが、こちらはそんなにCと変わらないです。左辺、右辺はヌラブルのNode型としてみました。
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
### 補足情報
ここまでのコンパイラとしての実装は下記の記事にもう少し詳しく説明しています。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（四則演算版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)

# 入出力コード サンプルイメージ
この記事が対象としている9ccの対象構文は優先順位対応の四則演算で変数も導入前のものですから、解釈できるのは下記のような四則演算だけです。
```C:C
5 + 6 * 7
5 * ( 9 - 6 )
( 3 + 5 ) / 2
```
これらの式をアセンブラではなく、他のC言語系プログラミング言語のソースを出力する場合は、同じ構文を出力することになると思います。
構文解析を通過して構文OKの計算式と判定されたら元のトークン列に復元して出力するなどが考えられますが、逆にそちらのが難度が高い感じがしております。
そこで、ここでは内部的にスタックに処理値をつみあげていく逆ポーランド記法のMindのソースコードを出力するようにします。
```:Mind
５と　６と　７を　掛け　加える
５に　９から　６を　引いて　掛ける
３と　５を　加え　２で　割る
```
~~５と ６を 加え ７を 掛ける~~ 2023/01/23上記1行目訂正

ただし、Mindは予約された特定の送りかな以外のひらがなは無視しますので、機械生成するソースコードでは送りかなは生成しないとします。また全角変換もとりあえずなしでごめんなさい。
# 実行結果
## トランスコンパイラの出力コード
9cc四則演算版の出力するアセンブラから、アセンブラヘッダをMindのメイン関数宣言に、インテルレジスタの掛け算、割り算用のレジスタ操作のコードを除去して、比較的純粋なスタックマシン風に出力すると、下図のようになりました。
```:5 + 6 * 7
メインとは
  5
  6
  7
  掛け
  加え
  数値表示する
```
```:5 * ( 9 - 6 )
メインとは
  5
  9
  6
  引き
  掛け
  数値表示する
```
```:( 3 + 5 ) / 2
メインとは
  3
  5
  加え
  2
  割り
  数値表示する
```
送りかながないことと、スタックに乗せて処理する単純な処理のため、Mind語法の日本語らしさは再現できていませんが、Mindコンパイラは上記のソースコードでも実行可能なはずです。
~~表示する~~ 2023/01/24上記3ヶ所訂正　（「表示する」は文字列型用）
「数値表示する」という結果の出力機能はオリジナルのアセンブラ出力コードにはないのですが、計算結果をコンソールに出力させて結果をわかりやすくするため追加しています。
## コード生成部
下記は9cc四則演算版のメイン関数とコード生成関数を書き換えたものです。オリジナルのアセンブラ出力内容はコメントで残しています。

```CS:Program.cs
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
            // Console.Write(".intel_syntax noprefix\n");
            // Console.Write(".globl main\n");
            // Console.Write("main:\n");
            Console.Write("メインとは\n");


            // 抽象構文木を下りながらコード生成
            gen(node);

              // スタックトップに式全体の値が残っているはずなので
            // それをRAXにロードして関数からの返り値とする
            //Console.Write("  pop rax\n");       
            // Console.Write("  ret\n");
            //Console.Write("  表示する\n");
            Console.Write("  数値表示する\n");
            return 0;
        }
```
~~Console.Write("  表示する\n");~~ 2023/01/24上記1ヶ所訂正　数値表示とは 文字列変換し 表示することに近い感じのMindコンソール出力関数。
```CS:Program.cs
 	  // 抽象構文木を下りながらコード生成
        static void gen(Node node) {
            if (node.kind == NodeKind.ND_NUM) {
                // Console.Write($"  push {node.val}\n");
                Console.Write($"  {node.val}\n");
                return;
            }

            gen(node.lhs);
            gen(node.rhs);

            // Console.Write("  pop rdi\n");
            // Console.Write("  pop rax\n");

            switch (node.kind) {
            case NodeKind.ND_ADD:
                // Console.Write("  add rax, rdi\n");
                Console.Write("  加え\n");
                break;
            case NodeKind.ND_SUB:
                // Console.Write("  sub rax, rdi\n");
                Console.Write("  引き\n");
                break;
            case NodeKind.ND_MUL:
                // Console.Write("  imul rax, rdi\n");
                Console.Write("  掛け\n");
                break;
            case NodeKind.ND_DIV:
                // Console.Write("  cqo\n");
                // Console.Write("  idiv rdi\n");
                Console.Write("  割り\n");
                break;
            }

            // Console.Write("  push rax\n");
        }

```
このあたりMindの演算命令は、試作のためリテラルで書いています。
## Mindコンパイラによる出力ソースの実行結果
~~鋭意執筆中~~ 2023/01/29追記

下記の記事にて、無事にコンパイルして、生成コードを実行することができました。
[VSCode [WSL:Ubuntu] で日本語プログラミング言語Mindのソースをビルドしてみた](https://qiita.com/mylifewithviolin/items/366d1e3b0fea9485acdb)

実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
下記はその結果のターミナルの出力です、
```:5 + 6 * 7
 *  実行するタスク: /home/puremind/pmind/src/qcc/main  

47 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
ちょっとわかりにくいかもですが、47 というのが結果です。
Mindのコンソール出力関数「数値表示」は改行は別途実行のタイプのようです。たしか、「改行する」とか？

6 * 7 は 42で、それ加える 5は 47であってますね。

```:5 * ( 9 - 6 )
 *  実行するタスク: /home/puremind/pmind/src/qcc/main  

15 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
9 - 6 は 3 で、それ掛ける 5は 15であってますね。

```:( 3 + 5 ) / 2

 *  実行するタスク: /home/puremind/pmind/src/qcc/main  

4 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
3 + 5 は 8 で、それ割る 2は 4であってますね。

# ソースコード
GitHub準備中
# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/doz13189/items/04988e60905f4e933f6f

https://qiita.com/pocari/items/d272e87274a1486298bc

https://qiita.com/killy/items/ccec1fbb81c4432757f5

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c
