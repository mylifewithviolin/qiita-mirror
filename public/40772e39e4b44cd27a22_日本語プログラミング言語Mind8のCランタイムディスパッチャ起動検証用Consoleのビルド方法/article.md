# はじめに
[こちらの記事](https://qiita.com/mylifewithviolin/items/37d0af60ef8dc0b8a8a1)「Mind8のランタイムディスパッチャC実装の代替実装をC#で行う（zzNotif）」へMind開発者の@killyさんより重要な情報共有がございまして、本記事はそのご提供情報の検証記事となります。

killyさんよりご提供いただいた重要な情報の内容とは、うまくまとまっていませんが本記事の件名のとおりでございます。興味を持たれた方は該当記事のkillyさんのコメントもご参照ください。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows
C# 12 
dotnet-sdk-8.0.204-win-x64

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
.NET Install Tool 2.0.2 Microsoft
Base language support for C# 2.18.16 Microsoft

### 2つのVSCode環境
ちょっと紛らわしいのですが、本記事に関連しては2つのVSCode環境がございます。
* 1つは、Cで実装されているMind8kernelの動作をデバッグ実行で探るための[こちらの記事](https://qiita.com/mylifewithviolin/items/2804356ae2f39b055b8c)の環境
* 2つめは、そのMind8kernelのディスパッチャをC#で代替実装しようという試みの[こちらの記事](https://qiita.com/mylifewithviolin/items/7f0878469e068baccf90)の環境
 
となります。

### 2つのVSCode環境を使った本記事作業のおおまかな流れ
本記事ではMind8のCランタイムディスパッチャ起動検証用Consoleのビルド環境として1つめを使います。こちらはランタイムのカスタマイズ環境としてMind8のランタイムソースが具備されています。

そして、ビルドされた検証用Consoleを使って、C#代替実装検証用の中間コードhello.mcoを2つめの環境でビルドします。

そしてさらに、この検証用ConsoleでリビルドされたC#代替実装検証用の中間コードhello.mcoを1つめの環境にコピーして、短縮されたスタートアップでのディスパッチャの動きを確認します。

# 検証用Consoleのビルド
killyさんよりご提供いただいた情報に従い、下記のように検証用Consoleのビルド用のフォルダfiledummyを作成します。

## ビルド用フォルダ構成
下図の.vscodeフォルダの位置からわかりますようにMind8kernelのデバッグ実行時はkernelフォルダを作業ルートにVSCodeを起動しますが、Mind8でビルドするだけの場合はMind8フォルダを作業ルートにして起動します。
```
C:\developments\vscode\mind8>tree
C:.
├─bin
├─file
│  └─obj
├─filedummy
│  └─obj
├─kernel
│  └─.vscode
├─lib
├─libY
└─sample
```

filedummyフォルダには下記のようなファイルを格納します。
consdumy.srcはfileフォルダより、asmword.*はfile/objフォルダよりコピーします。batファイル2つはkillyさん情報による新規作成です。

```
C:\developments\vscode\mind8\filedummy>tree /f
C:.
│  ccond.bat
│  ccond0.bat
│  consdumy.src
│
└─obj
        asmword.his
        asmword.mco
        asmword.sym
```

## ビルド実行
ビルドの実行はccond0.batを実行します。Mind8コンパイラへのパスは通しておきます。
```
C:\developments\vscode\mind8\filedummy>mind

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
Usage(1): mind -help (オプション詳細を表示)
Usage(1): mind source library [objectdir\][objfile]

C:\developments\vscode\mind8\filedummy>ccond0.bat

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 ..「$$SLITERAL_EVEN」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 ASM .. 送り検=無し
　　ロケーション=00000000 インデックス=00A5 式演算番号=0 
「$$SLITERAL_ODD」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 ASM .. 送り検=無し
　　ロケーション=00000000 インデックス=00A4 式演算番号=0
「$$JMP_NEAR」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000
「$$JMP_FAR0」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000
「$$EXIT1W」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000
「$$COLD_FORTH」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 仮定義 .. 送り検=無し 
　　ロケーション=00000064 インデックス=0019 式演算番号=0
「$$COLD_USER」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000
「＄＄対話モード？」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000 
「$$TRAP2_ENTRY」：
　　【雑単語の未定義語】module=0 (データ型不使用) 値=00000000
「プロセス終り０」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 ASM .. 送り検=無し
　　ロケーション=00000000 インデックス=0014 式演算番号=0
「実行終り時の処理」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 仮定義 .. 送り検=無し
い型=数値扱 整数入力 整数出力 ASM .. 送り検=無し
　　ロケーション=00000000 インデックス=00C1 式演算番号=0
「＄＄改行」：
　　【処理単語の純処理単語】module=1 扱い型=数値扱 整数入力 整数出力 ASM .. 送り検=無し
　　ロケーション=00000000 インデックス=00C4 式演算番号=0
 終了

C:\developments\vscode\mind8\filedummy>
```
consdumyのオブジェクトライブラリファイルが生成されていることを確認します。
```
C:\developments\vscode\mind8\filedummy>dir obj\consdumy.* 
2024/05/12  11:49               309 consdumy.his
2024/05/12  11:49               898 consdumy.mco
2024/05/12  11:49            20,084 consdumy.sym
               3 個のファイル              21,291 バイト
```

ここまででMind8のCランタイムディスパッチャ起動検証用Consoleのビルドは完了です。

# 検証用Consoleライブラリを使った検証用中間コードのリビルド
正規のスタートアップルーチンを起動する中間コードファイルと区別するため、ソースコードファイル名を下記のように変更します。
hello.src → hellodummy.src

```
C:\developments\vscode\mind8dispatch>dir *.src
2024/04/18  20:49                56 hello.src
2024/05/12  11:55                56 hellodummy.src
               2 個のファイル                 112 バイト
```               
## お題のMind8のソースファイル
```mind:hellodummy.src
メインとは
　　　　「Hello by mind8」を　表示すること。
```

## ビルド実行
横スクロールしてわかりずらいですが、こちらはC#用環境のため、Mind8コンパイラのライブラリ指定パスにはさきほどのC用環境の上にあるfiledummy\objフォルダのconsdumyを指定します。
```
C:\developments\vscode\mind8dispatch>mind hellodummy C:\developments\vscode\mind8\filedummy\obj\consdumy    

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
1 個のエラーが有ります。
```
ここでエラーとなります。これは「表示」する単語が検証用コンソールでは未定義のためです。

```mind:hellodummy.inf
hellodummy.src 2 行目でエラー。行内容は、
　　　　「Hello by mind8」を　表示すること。
      要因１："表示"は未定義の単語です。

1 個のエラーが有ります。
```

## お題のMind8のソースファイル（訂正版）
お題のソースを下記のように訂正します。
```mind:hellodummy.src
メインとは
　　　　「Hello by mind8」を　＄＄表示すること。
```
## ビルド実行（訂正版）
こんどは無事にビルド成功しました！:tada:
```
C:\developments\vscode\mind8dispatch>mind hellodummy C:\developments\vscode\mind8\filedummy\obj\consdumy

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> hellodummy.exe
```
無事に新しい中間コードファイルhellodummy.mcoファイルも生成されています。

```
C:\developments\vscode\mind8dispatch>dir hellodummy.*
2024/05/12  13:06            74,752 hellodummy.exe
2024/05/12  13:06               402 hellodummy.his
2024/05/12  13:06               938 hellodummy.mco
2024/05/12  13:06                60 hellodummy.src
2024/05/12  13:06            19,048 hellodummy.sym
               5 個のファイル              95,200 バイト
```
ただし、こちらの環境での実行ではこれまでの検証の影響でランタイムシリアルNo不整合エラーとなりますが、ここでは問題にしません。

```
C:\developments\vscode\mind8dispatch>hellodummy
kermain: Serial number missmatch.
```

C側検証環境でhellodummy.mcoでのスタートアップ処理を検証するため、hellodummy.mcoをmindexec.mcoにリネームしてC側検証環境のkernelフォルダにコピーします。下図は従来の正規のスタートアップのhello.mcoがリネームされたmindexec.mcoです。
```
C:\developments\vscode\mind8\kernel>dir mindexec.mco
2024/04/18  20:53            43,544 mindexec.mco
               1 個のファイル              43,544 バイト
```
ではコピーします。
```
C:\developments\vscode\mind8dispatch>copy hellodummy.mco C:\developments\vscode\mind8\kernel\mindexec.mco
C:\developments\vscode\mind8\kernel\mindexec.mco を上書きしますか? (Yes/No/All):
 Y
        1 個のファイルをコピーしました。
```
だいぶファイルサイズが小さくなりました:joy:
```
C:\developments\vscode\mind8\kernel>dir mindexec.mco                    
2024/05/12  13:06               938 mindexec.mco
               1 個のファイル                 938 バイト
```

# お題のMind8の中間コード実行リスト
C側検証環境で、前記手順でコピーしたお題の中間コードファイルをディスパッチャで処理させます。

下図はオリジナルのC実装のディスパッチャモニタ関数に対して出力情報を追加したモニタ関数を実行しているため少しわかりづらくなっていますが、左端から1列目がディスパッチャが処理したステップ数、2列目が16進数表記のmcode、3列目が10進数表記のmcode、4列目がデータスタックのアドレスポインタ変数のオフセット値などとなっています。
```
   1 8019  32793   1024        0        0        0        0        0        0   1024        0        0
   2 002F     47   1024        0        0        0        0        0        0   1023        0        0
   3 00A5    165   1024        0        0        0        0        0        0   1023        0        0
   4 00C1    193   1022       14  6889596        0        0        0        0   1023       14        0
$$COLD_FORTH
   5 0020     32   1024        0        0        0        0        0        0   1023        0        0
   6 8029  32809   1024        0        0        0        0        0        0   1024        0        0
   7 00A5    165   1024        0        0        0        0        0        0   1023        0        0
   8 00C1    193   1022       14  6890092        0        0        0        0   1023       14        0
Hello by mind8
   9 0020     32   1024        0        0        0        0        0        0   1023        0        0
  10 801A  32794   1024        0        0        0        0        0        0   1024        0        0
1022        0  6889582
  16 00A5    165   1024        0        0        0        0        0        0   1022        0  6889582
  17 00C1    193   1022       18  6889618        0        0        0        0   1022       18  6889582
実行終り時の処理
  18 0020     32   1024        0        0        0        0        0        0   1022        0  6889582
  19 004D     77   1024        0        0        0        0        0        0   1023        0        0
  20 0014     20   1022        0        0        0        0        0        0   1023        0        0
```
お題の「Hello by mind8」のコンソール出力までは7（同一コード含む）のmcodeを処理すればよいことがあかりました！！:confetti_ball:

# お題のMind8の中間コード実行リスト（正規のスタートアップ）
[こちらの記事](https://qiita.com/mylifewithviolin/items/c24cac3a0788cc2ad6f5)に正規のスタートアップのMCodeをC版オリジナルがディスパッチしたリストを確認しています。お題の「Hello by mind8」のコンソール出力までは649（同一コード含む）のmcodeを処理します。

# つづく
生成されたhello.mcoを解釈して、C#側で「Hello by mind8」が出力されるようにするまでの長い道のりですが、とりあえず構想段階のソースコードの確度をざくっと引き上げて「三段目」とかかなという感じでしたが、最近は道の険しさにひるんでいました。54/649みたいな状況。@killyさんの情報ご提供でいったんは完走させる近道があることがわかって少し安心したところです。killyさんに重ねてお礼申し上げます。
