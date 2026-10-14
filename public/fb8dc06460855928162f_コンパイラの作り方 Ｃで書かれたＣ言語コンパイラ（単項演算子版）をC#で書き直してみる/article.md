
# はじめに

[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみます。（単項演算子対応）

## この記事内容の作業目的
言語処理系の基礎知識、基礎技能として、トークンや抽象構文木、パーサーといった基礎概念の獲得。本記事の解釈可能ソース状態はCとすら言えない単項演算を含む四則演算です。当面は目的達成のためのスキルと知見の獲得途上ということでご容赦願います。（参考サイトの9ccの「ステップ6：単項プラスと単項マイナス」に相当します。9ccは後半にいくほど解釈可能範囲を広げるインクリメンタル実装のため）

## この記事内容の作業環境
Windows11
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
gcc 11
C# 10 dotnet-sdk-6.0.404-win-x64

## この記事内容の保証
※この記事には実装的な情報が含まれます。Cで書かれた引用ソースに対して、C#で書かれた内容の等価性・妥当性は保証されません。

## 関連記事
参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」までに相当する内容を下記の記事で解説しております。
[コンパイラの作り方 Ｃで書かれたＣ言語コンパイラ（四則演算版）をC#で書き直してみる](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)

# 実装のポイント
## 単項演算子の追加
参考サイトの9ccの「ステップ5：四則演算のできる言語の作成」につづく「ステップ6：単項プラスと単項マイナス」では、ソースコード上の差分としては、下記の関数のみ説明されており、レファレンスとして9cc後継のchibiccソースコードのgithub上の最も近い状態のコミットへのリンクが記載されています。

```c:9cc.c
    Node *unary() {
      if (consume('+'))
        return primary();
      if (consume('-'))
        return new_node(ND_SUB, new_node_num(0), primary());
      return primary();
    }
```
```c:chibicc.c
    // unary = ("+" | "-")? unary
    //       | primary}
    Node *unary() {
      if (consume('+'))
        return unary();
      if (consume('-'))
        return new_binary(ND_SUB, new_num(0), unary());
      return primary();
    }
```

### chibiccソースコードベースに移行
「ステップ5：四則演算のできる言語の作成」までは、本文中に説明されたソースコードを組み立てれば、実行できるようになりましたが、「ステップ6：単項プラスと単項マイナス」では、実行可能な状態にするためには、本文中のソースコードと若干異なるchibiccソースコードベースに移行する必要があります。

```diff_c:上9cc 下chibicc
    -return new_node(ND_SUB, new_node_num(0), primary());
    +return new_binary(ND_SUB, new_num(0), unary());
```

github上のchibiccソースコード同士の直前コミットとの差分も手掛かりにはなります。
C#側のソースでは[前回記事](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)の9cc相当状態のコードをコメントアウトで残しておきます。C側の対応ソースはchibicc状態とします。

# chibicc移行リファクタリング
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
    static Node new_node(NodeKind kind) {
        Node node = new();
        node.kind = kind;
        // node.lhs = lhs;
        // node.rhs = rhs;
        return node;
    }

    static Node new_binary(NodeKind kind, Node lhs, Node rhs) {
        Node node = new_node(kind);
        node.lhs = lhs;
        node.rhs = rhs;
        return node;
    }

```
この変更に伴い、従来new_nodeを呼び出していたところを複数ヶ所new_binaryに変更する必要があります。（後述）

また、従来Node *node = calloc(1, sizeof(Node))とメモリアロケートしてnode->kind = ノード種類としていたところはnew_nodeの呼び出しになります。次の節のnew_node_numのnew_numへの変更は、そのような変更のついでに関数名も変更されたようです。

## new_node_numのnew_numへの変更

```c:chibicc.c
    Node *new_num(int val) {
      Node *node = new_node(ND_NUM);
      node->val = val;
      return node;
    }
```

```cs:Program.cs
    // static Node new_node_num(int val) {
    //     Node node = new();
    //     node.kind = NodeKind.ND_NUM;
    //     node.val = val;
    //     return node;
    // }
    static Node new_num(int val) {
        Node node = new_node(NodeKind.ND_NUM);
        node.val = val;
        return node;
    }
```

## primary

new_node_numのnew_numへの変更のため、primaryは若干影響を受けました。

```c:chibicc.c
    // primary = "(" expr ")" | num
    Node *primary() {
      if (consume('(')) {
        Node *node = expr();
        expect(')');
        return node;
      }
    
      return new_num(expect_number());
    }
```
```cs:Program.cs
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

## expr

exprはnew_binaryが従来のnew_nodeの役割を担う変更の影響を受けました。
```c:chibicc.c
    // expr = mul ("+" mul | "-" mul)*
    Node *expr() {
      Node *node = mul();
    
      for (;;) {
        if (consume('+'))
          node = new_binary(ND_ADD, node, mul());
        else if (consume('-'))
          node = new_binary(ND_SUB, node, mul());
        else
          return node;
      }
    }
```
```cs:Program.cs
    static Node expr(List<Token> tokenList,ref int curIndex) {
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
chibicc移行リファクタリングは以上です。
# 単項演算子の追加

いよいよ本題のunaryの追加です。トークン自体は2項演算子のそれと同じなのでトークン種に変更はありません。

## unary

```c:chibicc.c
    // unary = ("+" | "-")? unary
    //       | primary}
    Node *unary() {
      if (consume('+'))
        return unary();
      if (consume('-'))
        return new_binary(ND_SUB, new_num(0), unary());
      return primary();
    }
```

```cs:Program.cs
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

## mul
unaryの追加で直接の変更を受けたのはmul関数です。こちらは9ccの状態をコメントで残しておきました。
```c:chibicc.c
    Node *mul() {
      //Node *node = primary();
      Node *node = unary();
    
      for (;;) {
        if (consume('*'))
          //node = new_binary(ND_MUL, node, primary());
          node = new_binary(ND_MUL, node, unary());
        else if (consume('/'))
          //node = new_binary(ND_DIV, node, primary());
          node = new_binary(ND_DIV, node, unary());
        else
          return node;
      }
    }
```

```cs:Program.cs
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
# C#版トークナイザの全文
C#で書き換えたトークナイザの全文です。こちらは変更ありませんが、[前回記事](https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c)で一部割愛していましたので、今回全文を載せました。chibcc側は長くなるので割愛します。
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

            if (isarithmetic(cs[i].ToString())) {
                cur = new_token(TokenKind.TK_RESERVED, next, cs[i].ToString());
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
                cur = new_token(TokenKind.TK_NUM,next, numberStr);
                cur.val = strtol(numberStr);
                tokenList.Add(cur);
                next++;
                continue;
            }

            //ここに進んだら例外
            error("トークナイズできません");
            i++;
        }

        cur = new_token(TokenKind.TK_EOF, next, "");
        tokenList.Add(cur);
        return tokenList;
    }
```

# 入出力コード サンプルイメージ
この記事が対象としているchibicc(9cc)の対象構文は優先順位対応の四則演算に単項演算を加えただけですから、変数も導入前のものですから、解釈できるのは下記のような四則演算だけです。
```C:C
5 + 6 * 7
5 * ( 9 - 6 )
( 3 + 5 ) / 2
- 10 + 20
```
これらの式のうち上３つは前回記事であつかったので、今回は４つ目を対象にchibicc(9cc)と同じアセンブラを出力します。
## chibicc(9cc)単項演算子版の実行結果
まずオリジナルのchibicc(9cc)をgccでコンパイルします。
```
$ gcc main.c
$ ls -l
-rwxr-xr-x 1 puremind puremind 17024 Feb  4 19:35  a.out
-rw-r--r-- 1 puremind puremind  5641 Feb  4 19:35  main.c
```

C#との比較用の期待結果として9ccを実行してみます。
実行環境はWindows11上のVSCode統合のUbuntuターミナル(bash)です。
```:- 10 + 20
$ ./a.out "- 10 + 20"
.intel_syntax noprefix
.global main
main:
  push 0
  push 10
  pop rdi
  pop rax
  sub rax, rdi
  push rax
  push 20
  pop rdi
  pop rax
  add rax, rdi
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
2023/02/04  20:13               401 9cc.deps.json
2023/02/04  20:42            18,944 9cc.dll
2023/02/04  20:42           147,968 9cc.exe
2023/02/04  20:42            18,224 9cc.pdb
2023/02/04  20:13               147 9cc.runtimeconfig.json
```
9cc四則演算版と同じ四則演算文字列を与えて実行すると、下図のようになりました。
実行環境はWindows11上のVSCodeのターミナルです。
```:- 10 + 20
>9cc s "-10 + 20"  
.intel_syntax noprefix
.globl main
main:
  push 0
  push 10
  pop rdi
  pop rax
  sub rax, rdi
  push rax
  push 20
  pop rdi
  pop rax
  add rax, rdi
  push rax
  pop rax
  ret
```

# ソースコード
GitHub [9cc2cs 9cc unary operator version](https://github.com/mylifewithviolin/9cc2cs/commit/72dd79a67db73233ea9fd6a007bfb7dbab909a2f)
# 参考リンク
https://www.sigbus.info/compilerbook

https://qiita.com/ruiu/items/4d471216b71ab48d8b74

https://qiita.com/mylifewithviolin/items/f4dee1cf96fffc57bd0c

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c
