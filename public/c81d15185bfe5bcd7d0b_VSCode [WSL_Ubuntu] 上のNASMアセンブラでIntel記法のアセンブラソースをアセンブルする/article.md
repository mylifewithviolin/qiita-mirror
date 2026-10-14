# はじめに

[トランスコンパイラを実装してみたい](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)のですが、とりあえずコンパイラ作ったことないので、ネット上でよくヒットして前半部分は説明もたいへん詳しい[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)の前半部分をC#で書いてみているのですが、これまで出力結果のアセンブラソースはオリジナルの9ccの出力結果と文字列比較として合否判定していました。
あくまでトランスコンパイラを実装するのが目的で、低レイヤを知りたいわけではないのですが、行き掛かり上、VSCode [WSL:Ubuntu] 上でNASMアセンブラでIntel記法のアセンブラソースをアセンブルできるようにしておきます。

## この記事内容の作業目的
あくまで行き掛かり上、VSCode [WSL:Ubuntu] 上でNASMアセンブラでIntel記法のアセンブラソースをアセンブルできるようにしておきます。

## この記事内容の作業環境
Windows11 Pro 22H2
Windows11WSL（Ubuntu）
VSCode(Visual Studo Code)　1.78.0
NASM 2.15.05

## この記事内容の保証
※この記事には実装的な情報が含まれます。アセンブラで書かれた内容の等価性・妥当性は保証されません。

## 参考記事
[低レイヤを知りたい人のためのCコンパイラ作成入門](https://www.sigbus.info/compilerbook)
[Linux で64bitアセンブリプログラミング (02)](https://www.mztn.org/lxasm64/amd02.html)

# WSL:UbuntuへのNASMのインストール

VSCode [WSL:Ubuntu]のbashターミナルから下記のコマンドを投入

sudo apt-get install nasm

```bash:

bashプロンプト:~$ sudo apt-get install nasm
[sudo] password for ******: 
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  nasm
～略～
Selecting previously unselected package nasm.
(Reading database ... 36035 files and directories currently installed.)
Preparing to unpack .../nasm_2.15.05-1_amd64.deb ...
Unpacking nasm (2.15.05-1) ...
Setting up nasm (2.15.05-1) ...
Processing triggers for man-db (2.10.2-1) ...

```

念のためバージョンチェック。VSCode [WSL:Ubuntu]のbashターミナルから下記のコマンドを投入。

nasm -v

```bash:
bashプロンプト:~$ nasm -v
NASM version 2.15.05
```

# VSCode [WSL:Ubuntu]へのNASM拡張機能のインストール
nasm x86 syntax highlighting

これでシンタックスハイライトがつくようになりました。

# アセンブル対象のソースコード
サンプルイメージ1は、Cコンパイラ作成入門参考サイトの推奨実装の、historical/oldブランチのコミット[4216d6c]のSupport single-letter local variablesをビルドして実行してみました結果です。sample.asmとしています。

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

サンプルイメージ2は、Cコンパイラ作成入門参考サイトの「ステップ9：1文字のローカル変数」に相当する実装をC#で書き直した実装を実行した結果の出力です。sample2.asmとしています。

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


# アセンブルソースコードのアセンブル結果
sample.asm、sample2.asmどちらも、.intel_syntax noprefixというIntel記法を選ぶためのアセンブラコマンドとその直下の.globl mainという行でエラーとなっているようです。

```bash:
bashプロンプト:~$ nasm -f elf64 sample.asm
sample.asm:1: error: parser: instruction expected
sample.asm:2: error: parser: instruction expected

bashプロンプト:~$ nasm -f elf64 sample2.asm
sample2.asm:1: error: parser: instruction expected
sample2.asm:2: error: parser: instruction expected
```

試しにこの2行を仮に削除するとアセンブルは通るようでした。
```bash:
bashプロンプト:~$ nasm -f elf64 sample.asm -l sample.lst && ld -s -o sample sample.o
ld: warning: cannot find entry symbol _start; defaulting to 0000000000401000
bashプロンプト:~$ dir
sample  sample.asm  sample.lst  sample.o  sample2.asm
```

# おわりに
えっ、これでおわっちゃうの！？というつっこみはなしで。なにか分かれば追記するかもしれません。Intel記法だったらNASMだという一般的なにわか知識しかないです。

# 参考リンク
https://qiita.com/mylifewithviolin/items/47b5cda334b5bddbc63c
