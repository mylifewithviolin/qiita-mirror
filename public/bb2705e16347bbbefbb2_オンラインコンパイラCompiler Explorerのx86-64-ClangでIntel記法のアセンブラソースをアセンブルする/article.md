# はじめに

[トランスコンパイラ試作品の内部設計に進行しています](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)が、これがけっこう難航しておりまして、こっちはあまり進捗がないまま記事の未投稿が続くのもなんですので、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみているのですが、これまで出力結果のアセンブラソースはオリジナルの9ccの出力結果と文字列比較として合否判定していました。

あくまでトランスコンパイラを実装するのが目的で、低レイヤを知りたいわけではないのですが、行き掛かり上、オンラインコンパイラCompiler Explorerのx86-64-ClangでIntel記法のアセンブラソースをアセンブルできるようにしておきます。

## この記事内容の作業目的
あくまで行き掛かり上、オンラインコンパイラCompiler Explorer上のx86-64-ClangでIntel記法のアセンブラソースをアセンブルできるようにしておきます。

## この記事内容の作業環境
Windows11 Pro 22H2
Edge 114.0.1823.37 
Compiler Explorer(Execution モード)　x86-64-Clang 16.0.0


## この記事内容の保証
※この記事には実装的な情報が含まれます。アセンブラで書かれた内容の等価性・妥当性は保証されません。

## 参考記事
[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)
[Compiler Explorer  ( https://godbolt.org/ )](https://godbolt.org/)

# オンラインコンパイラCompiler Explorerのサポート言語

Compiler Explorer は、C, C++, C#, Java などのソースコードをコンパイルできるオンラインコンパイラです。言語を選定した後はコンパイラの実装やバージョンを指定したり、コンパイルオプションを指定して結果を比較できます。

Javaだけでなく.NETのC#やVisualBasicもサポートされているのに驚きました。コンパイル結果としてアセンブリソースを出力させることができる他、ソース言語としてアセンブラもサポートしていて、Assemblyを選択した後、各アセンブラの実装とバージョンを選択できます。また、ソース言語としてCを選択してコンパイラオプションでアセンブラを指定することで、アセンブラソースを実行することもできます。

# アセンブル対象のソースコード
サンプルイメージ1は、Cコンパイラ作成入門参考サイトの推奨実装の、historical/oldブランチのコミット[4216d6c]のSupport single-letter local variablesをビルドして実行してみました結果です。sample.asmとします。

<details><summary>アセンブルコード サンプルイメージ1</summary>

```:a = 3;b = 5 * 6 - 8;a + b / 2;
$ ./chibicc 'a = 3;b = 5 * 6 - 8;a + b / 2;'
.intel_syntax noprefix
.global main
main:
  push rbp
  mov rbp, rsp
  sub rsp, 208
  lea rax, [rbp-8]
  push rax
  push 3
  pop rdi
  pop rax
  mov [rax], rdi
  push rdi
  add rsp, 8
  lea rax, [rbp-16]
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
  add rsp, 8
  lea rax, [rbp-8]
  push rax
  pop rax
  mov rax, [rax]
  push rax
  lea rax, [rbp-16]
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
  add rsp, 8
.L.return:
  mov rsp, rbp
  pop rbp
  ret
```
</details>

サンプルイメージ2は、[Cコンパイラ作成入門参考サイトの「ステップ9：1文字のローカル変数」に相当する実装をC#で書き直した実装](https://qiita.com/mylifewithviolin/items/47b5cda334b5bddbc63c)を実行した結果の出力です。sample2.asmとします。

<details><summary>アセンブルコード サンプルイメージ2</summary>

```:a = 3;b = 5 * 6 - 8;a + b / 2;
>9cc2cs s "a = 3;b = 5 * 6 - 8;a + b / 2;" 
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


# アセンブルソースコードの実行結果
## Compiler Explorerの操作手順（アセンブルソースコードの実行準備)
[https://godbolt.org/](https://godbolt.org/)に遷移すると、未設定の画面が展開したところから説明します。

・タイトルバーの右の[Add]という文字をクリックして開くショートカットメニューから[SouceEditor]をクリックします。
・ソースエディタのメニューバーの右端の言語リストは既定でC++が選択されています。
ソースエディタには下記のようなサンプルコードが展開します。
```C++:
/* Type your code here, or load an example. */
int square(int num) {
    return num * num;
}
```
・言語リストでCを選択します。（C++の１つ上がC#でその1つ上がCとなっています。）
サンプルコードはC++のときと同じです。

・ソースエディタのメニューバーの[+Add new..]という文字をクリックして開くショートカットメニューから[Execute Only]をクリックします。
・ソースエディタペインが左半分に寄って、右半分にエクゼキュータペインが展開して、既定のコンパイラ実装バージョンは[x86-64 gcc 13.1]となり、コンパイラオプションはブランクとなっています。

すぐにソースエディタのサンプルコードがコンパイル実行されますが、オプション未設定のせいか下記のようなエラーとなります。
```:
Executor x86-64 gcc 13.1 (C, Editor #1)

x86-64 gcc 13.1　Compiler options...
Could not execute the program
Compiler returned: 1
Compiler stderr
```

・コンパイラ実装バージョンを[x86-64 Clang 16.0.0]に変更します。
```:
Executor x86-64 clang 16.0.0 (C, Editor #1)

x86-64 clang 16.0.0　Compiler options...
Could not execute the program
Compiler returned: 1
Compiler stderr
```

・このエラーは気にせず、コンパイラオプションに -x assemblerを設定します。
```:
Executor x86-64 clang 16.0.0 (C, Editor #1)

x86-64 clang 16.0.0　-x assembler
Could not execute the program
Compiler returned: 1
Compiler stderr
```
さきほどまでは割愛していましたが、Compiler stderrの下に詳しいエラー内容が出力されていて、今回コンパイラオプション-x assemblerを指定したので、ソースエディタ上のCのサンプルソースコードが完全に認識されなくなったことがわかります。
```:
<source>:2:12: error: expected register here
int square(int num) {
           ^
<source>:3:5: error: invalid instruction mnemonic 'return'
    return num * num;
    ^~~~~~
<source>:4:1: error: invalid instruction mnemonic '}'
}
^
```

## アセンブルソースコードの実行結果 sample.asm
ソースエディタにサンプルソースコードsample.asmを貼り付けます。
エクゼキュータペインが更新されて下記の状態となります。

```:
Executor x86-64 clang 16.0.0 (C, Editor #1)

x86-64 clang 16.0.0 -x assembler
Program returned: 14
```

## アセンブルソースコードの実行結果 sample2.asm
ソースエディタにサンプルソースコードsample2.asmを貼り付けます。
エクゼキュータペインが更新されて下記の状態となります。
```:
Executor x86-64 clang 16.0.0 (C, Editor #1)

x86-64 clang 16.0.0 -x assembler
Program returned: 14
```
# おわりに
アセンブラの出力ソースコードの内容には若干の相違はありましたが、実行結果は同一で期待値どおりであることがわかりました。

# 謝辞
このツールの存在をご提示いただいた@fujitanozomuさんにお礼申し上げます。

# 参考リンク
https://qiita.com/mylifewithviolin/items/c6821d8ef2ba22d6b642
