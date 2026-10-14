# はじめに
日本語プログラミング言語Mindの小技「起動引数をモニタ」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載があります。
８ 入出力を行う単語
└起動引数

>Mindのプログラムは、起動引数 という名前の関数を呼び出すことで、自分が起動されたときの起動引数を参照することができる。以下のような仕様である。
>
>構文＝
起動引数個数　→　＜個数＞
　　　　　　　　　　↑引数が無い場合は０が返される
>
>　　　　　　　　　　　　↓ｎ番目の引数を表す文字列が返される
起動引数（ｎ）　→　＜文字列＞
　　　　　↑ｎは１～起動引数個数の整数

>起動引数をモニタ　→　・　　　(起動引数の内容をモニタ表示する)

>注１
サンプル testarg.src による起動引数のダンプ処理であるが、本項冒頭の構文のところに示したように、同じことをおこなう処理単語「起動引数をモニタ」が標準で備わっており、この１語を書くだけで起動引数の状況確認ができる。プログラムの動作確認に利用して欲しい。
注２
起動引数に含まれるオプションを解析するのみ便利な「起動引数をシフト」という機能もある。上級編で解説する。

本機能（本記事）は、下記のバージョンに対応しています。

起動引数個数と起動引数はMind7でも動作しますが、「起動引数をモニタ」と「起動引数をシフト」はMind８以降の機能です。これらはMind８のLinux版も対応していると思いますが、本記事では特に検証を行っておりません。

また、起動パラメータにワイルドカードを指定した場合の動作はLinux互換となるようにMind8ラインタイムで実装されている機能です。

# 対応バージョン
□Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
「起動引数」はMindのコンソールアプリケーションがOSのシェルコンソール
などから起動されるときに指定された、いわゆる起動パラメータをアプリケーション側から処理する単語です。

Mindの場合は「起動引数」という文字列実体情報の配列に格納されます。この配列の要素数は「起動引数個数」という数値変数に格納されていますので、この最大値に注意しながら「起動引数」にインデックスを指定して引用します。

「起動引数をモニタ」は起動パラメータの内容をコンソール出力するデバッグ用の機能です。

「起動引数をシフト」は複数指定した起動パラメータの１つ目を捨てて「起動引数」に格納する機能です。「起動引数個数」は実際に指定された数より１つ減ります。

それでは、この記事では「起動引数」に関連した処理単語を使用したコードをサンプルでご説明いたします。
  
# Mindプログラムソース

```mind:consoleParam.src
メインとは  （・　→　・）
    起動引数個数が　ゼロ？
    ならば　
        「起動パラメータがありませんでした。終了します。」を　一行表示し
        実行終わり
    つぎに
    起動引数をモニタし
    「起動引数の数は」を　表示し　
    起動引数個数を　数値表示し　「です。」を　一行表示し
    
    起動引数をシフトし
    起動引数をモニタし
    "「起動引数をシフト」によって起動引数の数は"を　表示し
    起動引数個数を　数値表示し　「になりました。」を　一行表示。
```

# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。

## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind consoleParam file

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> consoleParam.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind consoleParam file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> consoleParam.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind consoleParam file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
3 個のエラーが有ります。
```
```mind:consoleParam.inf
consoleParam.src 7 行目でエラー。行内容は、
    起動引数をモニタし
      要因１："起動引数をモニタ"は未定義の単語です。

consoleParam.src 11 行目でエラー。行内容は、
    起動引数をシフトし
      要因１："起動引数をシフト"は未定義の単語です。

consoleParam.src 12 行目でエラー。行内容は、
    起動引数をモニタし
      要因１："起動引数をモニタ"は未定義の単語です。

3 個のエラーが有ります。
Code=00008390  Data=000A5F24  SymOff=6268
```
# 実行結果
つづいて実行してみます。
Mind8の結果です。記述は割愛していますがMind9βも同じです。

最初は、起動パラメータを指定しない場合の結果です。

```cmd:
c:\developments\vscode\mind9>consoleParam
起動パラメータがありませんでした。終了します。

c:\developments\vscode\mind9>
```

続いて、３つ起動パラメータを指定してみます。

```cmd:
c:\developments\vscode\mind9>consoleParam param1 param2 param3
----------起動引数ここから----------
　Arg(1)=[param1]
　Arg(2)=[param2]
　Arg(3)=[param3]
----------起動引数ここまで----------
起動引数の数は3です。
----------起動引数ここから----------
　Arg(1)=[param2]
　Arg(2)=[param3]
----------起動引数ここまで----------
「起動引数をシフト」によって起動引数の数は2になりました。

C:\developments\vscode\mind9>
```
「起動引数をモニタ」は２回実行されていて、1回目は「起動引数をシフト」の前、2回目はその後です。「起動引数をモニタ」によって起動パラメータの先頭１つが捨てられたことがわかります。

続いて、起動パラメータをワイルドカード指定した場合の動作です。起動パラメータにワイルドカード"*"が指定されたとき、カレントディレクトリに存在するファイルのファイル名として列挙するのはWindows版Mindの場合はMind側の実装によるものです。

```cmd:
c:\developments\vscode\mind9>consoleParam consoleInput* galaxy*
----------起動引数ここから----------
　Arg(1)=[consoleInput.exe]
　Arg(2)=[consoleInput.his]
　Arg(3)=[consoleInput.mco]
　Arg(4)=[consoleInput.src]
　Arg(5)=[consoleInput.sym]
　Arg(6)=[galaxy.exe]
　Arg(7)=[galaxy.his]
　Arg(8)=[galaxy.mco]
　Arg(9)=[galaxy.src]
　Arg(10)=[galaxy.sym]
　Arg(11)=[galaxy2.exe]
　Arg(12)=[galaxy2.his]
　Arg(13)=[galaxy2.mco]
　Arg(14)=[galaxy2.src]
　Arg(15)=[galaxy2.sym]
----------起動引数ここまで----------
起動引数の数は15です。
----------起動引数ここから----------
　Arg(1)=[consoleInput.his]
　Arg(2)=[consoleInput.mco]
　Arg(3)=[consoleInput.src]
　Arg(4)=[consoleInput.sym]
　Arg(5)=[galaxy.exe]
　Arg(6)=[galaxy.his]
　Arg(7)=[galaxy.mco]
　Arg(8)=[galaxy.src]
　Arg(9)=[galaxy.sym]
　Arg(10)=[galaxy2.exe]
　Arg(11)=[galaxy2.his]
　Arg(12)=[galaxy2.mco]
　Arg(13)=[galaxy2.src]
　Arg(14)=[galaxy2.sym]
----------起動引数ここまで----------
「起動引数をシフト」によって起動引数の数は14になりました。

C:\developments\vscode\mind9>
```
起動パラメータにワイルドカード"?"が単独で指定されたときは通常の文字として扱われます。

```cmd:
c:\developments\vscode\mind9>consoleParam consoleInput? galaxy?   
----------起動引数ここから----------
　Arg(1)=[consoleInput?]
　Arg(2)=[galaxy?]
----------起動引数ここまで----------
起動引数の数は2です。
----------起動引数ここから----------
　Arg(1)=[galaxy?]
----------起動引数ここまで----------
「起動引数をシフト」によって起動引数の数は1になりました。

c:\developments\vscode\mind9>
```
起動パラメータにピリオドを指定してワイルドカード"?"を指定するとファイルを探索して列挙します。

```cmd:
c:\developments\vscode\mind9>consoleParam consolePara?.src galaxy?.??o
----------起動引数ここから----------
　Arg(1)=[consoleParam.src]
　Arg(2)=[galaxy.mco]
　Arg(3)=[galaxy2.mco]
----------起動引数ここまで----------
起動引数の数は3です。
----------起動引数ここから----------
　Arg(1)=[galaxy.mco]
　Arg(2)=[galaxy2.mco]
----------起動引数ここまで----------
「起動引数をシフト」によって起動引数の数は2になりました。

c:\developments\vscode\mind9>
```

# 参考情報
この小技「起動引数をモニタ」を使った記述例の記事はまだありません。みつけたら教えてください。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできます。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
