# はじめに
日本語プログラミング言語あおいがネィティブにコード生成するとしたらどれがいいですかね、やっぱRustですかねとかMicrosoft Copilotさんと雑談しておりましたら、いまはZigってのもあるよと教えていただいたところでございました。というわけでさっそく環境をご用意。

# 使用AI
## Microsoft Copilot
本件Zig言語の存在をおしえていただいた形となります。プロンプトには直接かかわっていません。
## GitHub Copilot
とりあえず環境つくっていただきました。ダウンロードしたzigのバージョンが当初想定していたのより新しく、事前につくっておいたbuild.zigの内容が一部不適合だったみたいで苦戦していました。

# Zig Hello World 処理概要
Zig言語は今回初めてみたので、build.zigってなにという感じでした。見た感じビルドスクリプトが書いてある感じ。
そこでプロジェクト構成をGitHub Copilotに説明してもらう処理概要.mdを作成してもらいました。

```md
# Zig Hello World 処理概要

## プロジェクト構成

build.zig      … ビルド手順を定義するビルドスクリプト
src/main.zig   … プログラム本体（エントリポイント）

## build.zig

`zig build` コマンド実行時に、Zigコンパイラ自身によってコンパイル・実行される
特殊なビルドスクリプト。C/C++の `Makefile` や CMake の `CMakeLists.txt` に相当する。
```
```zig:build.zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const executable = b.addExecutable(.{
        .name = "hello",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    b.installArtifact(executable);

    const run_command = b.addRunArtifact(executable);
    const run_step = b.step("run", "Run the Hello World program");
    run_step.dependOn(&run_command.step);
}
```
>C/C++の `Makefile` や CMake の `CMakeLists.txt` に相当する。

なるほど、そういわれると納得。

表はmdソースのままだとわかりづらいので、Qiitaのmdとしました。

| 部分 | 役割 |
|---|---|
| `build(b: *std.Build) void` | `zig build` 実行時に呼ばれるエントリポイント関数。`b` はビルドグラフを構築するビルダー。 |
| `standardTargetOptions` / `standardOptimizeOption` | `-Dtarget=...` や `-Doptimize=ReleaseFast` などのコマンドライン引数を受け取る標準オプションを追加する。 |
| `addExecutable` | 実行ファイル `hello` を作成するステップを追加する。`root_module` の `root_source_file` で、実際のプログラムのソース（src/main.zig）を指定する。 |
| `installArtifact` | `zig build` のデフォルトステップで `zig-out/bin/hello.exe` として出力するよう登録する。 |
| `addRunArtifact` + `step("run", ...)` | `zig build run` 用の独自ステップ `run` を定義。「実行ファイルをビルドしてから実行する」という依存関係を張る。 |

```md
## src/main.zig

実際のプログラムのエントリポイント。`pub fn main()` がプログラム開始時に呼ばれる関数。
```
```zig:main.zig
const std = @import("std");

pub fn main() void {
    std.debug.print("Hello, world!\n", .{});
}
```
```md
- `@import("std")` … Zig標準ライブラリを読み込む。
- `std.debug.print` … デバッグ用の標準出力関数。フォーマット文字列と引数タプル `.{}` を渡す。

## ビルド・実行コマンド

| コマンド | 内容 |
|---|---|
| `zig build` | `zig-out/bin/hello.exe` を生成する。 |
| `zig build run` | ビルド後に生成した実行ファイルを実行する。 |

## 実行結果

Hello, world!

## 補足：使用したZigバージョンでのAPI差異

使用した `0.17.0-dev` 系のZigでは、`addExecutable` の引数構造体 `ExecutableOptions` に `root_source_file` / `target` / `optimize` を
直接渡すAPIは廃止されており、`root_module` に `b.createModule(...)` で作成した
 `*Module` を渡す形式に変更されている。
旧形式のまま書くと以下のようなビルドエラーになる。

error: no field named 'root_source_file' in struct 'Build.ExecutableOptions'
```
ダウンロードはすぐ完了しましたが、zipファイルの解凍にものすごく時間がかかり、昨晩就寝前に終わらなかったのでPC電源つけっぱで解凍完了し、本日無事にHelloworldを実行できました。

# フォルダ構成
```cmd
C:\developments\vscode\ziglang>tree
C:.
├─.vscode
├─.zig-cache
│  ├─c
│  ├─h
│  ├─o
│  │  ├─1f884abb3834d240834619c051abf96b
│  │  ├─221b2b42d9b79f7598a8a6516c56f204
│  │  └─7f6a626a61bff26e96127101259db266
│  ├─tmp
│  └─z
├─docs
├─src
└─zig-out
    └─bin

```
## 生成された実行ファイル
以外と実行ファイルはでかい感じ。
```cmd
C:\developments\vscode\ziglang>dir zig-out\bin
2026/09/29  21:10         1,932,288 hello.exe
2026/09/29  21:10         2,928,640 hello.pdb
               2 個のファイル           4,860,928 バイト
```

## 実行結果
```cmd
C:\developments\vscode\ziglang\zig-out\bin>hello
Hello, world!

```
## 参考情報
VSCode-ZigというVSCodeエクステンションも入れたので、ソースは見やすくなっています。

# おわりに
以上です。いかがでしたでしょうか？何かの参考になれば幸いです。
