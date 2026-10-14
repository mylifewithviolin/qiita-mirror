# はじめに

諸般の流れからMind7とMind8 どちらでもビルドできる環境をVSCodeで構築し、[前回](https://qiita.com/mylifewithviolin/items/36c365224f4bbae5c127)は少し記述量のあるソースをMind7とMind8とでビルドしてみましたが、一部Mind7とMind8で互換性がない定義を確認。Mind開発者の@killyさんよりその点について情報展開いただいたので解決してみました。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Mind Version 7.5 for Windows
Mind Version 8.07 for Windows

Mindはそれぞれのバージョンのパスが構成されていることを前提とします。

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 

C/C++のデバッガは直接使わないのですが、Mindアプリケーションをデバッグ実行でローンチするために流用しています。

# Mind7でビルドできなかったMind8のソースコード
## 関数の属性定義
処理単語を下記のような関数形式にした場合はMind7でビルドできませんでした。
```mind:callfunc.src
カウントアップとは　関数　整数入力　整数出力（c　→　c）
	cは　変数
	cに　入れ
    	cを　一つ増加し
	cを　返す。
```
これは下記のような関数形式で実行するための宣言です。
```
        ※countを　カウントアップし　countに　入れ
	    [count :=  カウントアップ(count)]
```     
```:callfunc.inf
C:\developments\vscode\pmind\odbcsql\callfunc.src 1 行目でエラー。行内容は、
カウントアップとは　関数　整数入力　整数出力（c　→　c）
      要因１："整数入力"は未定義の単語です。
      要因２：かっこ表記に誤りが有ります。
      要因３："整数出力"は未定義の単語です。
```

これはMind7でいったん関数の属性定義が廃止されてMind8で復活したためでした。

てっとりばやくどちらでもビルドできるようにするには、関数定義から属性定義を削除してしまえばよいのですが、（Mind8は属性定義なくても可。）本記事では下記のような条件コンパイル文を使ってMind7とMind8の定義文を分けてみました。

```mind:callfunc.src
Mind7は　　　　　　数値　１。

        定義済み条件コンパイル　Mind7。
カウントアップとは　関数 （c　→　c）
        条件コンパイル終り。
        未定義条件コンパイル　Mind7。
カウントアップとは　関数　整数入力　整数出力（c　→　c）
        条件コンパイル終り。

	cは　変数
	cに　入れ
    	cを　一つ増加し
	cを　返す。
 ```
 定義済条件コンパイルを使うと「Mind7」の値によらず定義されていればこの配下の構文がコンパイルされます。上記の状態でMind7でビルド成功します。
 ```
  *  実行するタスク: C:/mind7/bin/mind.exe C:\developments\vscode\pmind\odbcsql/callfunc.src C:/mind7/lib/file 

日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:750*****
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe --> C:\developments\vscode\pmind\odbcsql\callfunc.exe
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
上記の状態はMind8とも互換性がありますのでMind8コンパイラでもビルド成功します。
```
 *  実行するタスク: C:/pmind/bin/mind.exe C:\developments\vscode\pmind\odbcsql\callfunc.src C:\pmind\lib\file 


日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\pmind\bin\mindex.exe --> C:\developments\vscode\pmind\odbcsql\callfunc.exe   
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。
```

## 数値定数の宣言
数値定数を「定数」を使用して宣言した場合はMind7でビルドできませんでした。
```mind:mssqlodbc.src
openDbは　		定数　1。
closeDbは　		定数　2。
```
```:mssqlodbc.inf
C:\developments\vscode\pmind\odbcsql\mssqlodbc.src 16 行目でエラー。行内容は、
openDbは　		定数　1。
      要因１："定数"は未定義の単語です。
```
このソースは下記の記事のコードの一部です。
[Mindでトランザクション事始めな書き方を探る（C文字列終端とエラーメッセージ）](
https://qiita.com/mylifewithviolin/items/20deeacfa446e71c5bed)

これは数値定数の宣言がMind7では「数値」だったのがMind8では「文字列定数」に合わせて「定数」が追加されたためです。ソースコードの「定数」を「数値」に書き換えてしまえば両方でビルドできるようになります。

しかし、「定数」と書いてある箇所は多いので、ここは書き換えないで済むように先ほどと同じ「定義済み条件コンパイル」を使います。その中で等価定義で「定数」を「数値」のエイリアスにします。

```mind:mssqlodbc.src
Mind7は　　　　　　数値　１。
        定義済み条件コンパイル　Mind7。
定数は　数値と　等価。
        条件コンパイル終り。
        
openDbは　		定数　1。
closeDbは　		定数　2。
```
「Mind7」が定義されている状態でMind7でビルドすると成功します。

```
 *  実行するタスク: C:/mind7/bin/mind.exe C:\developments\vscode\pmind\odbcsql/mssqlodbc.src C:/mind7/lib/file 

日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:750*****
コンパイル中 ---- 終了
Coping.. C:\mind7\bin\mindexec.exe --> C:\developments\vscode\pmind\odbcsql\mssqlodbc.exe
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
「Mind7」が定義されている状態でMind8でビルドすると失敗します。
```
 *  実行するタスク: C:/pmind/bin/mind.exe C:\developments\vscode\pmind\odbcsql\mssqlodbc.src C:\pmind\lib\file 

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
1 個のエラーが有ります。

 *  ターミナル プロセス "C:\pmind\bin\mind.exe 'C:\developments\vscode\pmind\odbcsql\mssqlodbc.src', 'C:\pmind\lib\file'" が終了コード 1 で終了しました。 
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。 
```
この場合は「定数」が定義済のためエラーとなりますね。「Mind7」の値によらず定義されていなければ、このエイリアス宣言は無効になりますので、Mind8でのビルドは成功するようになります。

```:mssqlodbc.inf
C:\developments\vscode\pmind\odbcsql\mssqlodbc.src 3 行目でエラー。行内容は、
定数は　数値と　等価。
      要因１："定数"は重複定義です（yoyakugoGで定義済み）。

1 個のエラーが有ります。
```

## 文字列定数の文字数制約？
Mind7でのビルドを成功させたソースのSELECT文は下記の短いバージョンです。
```mind:mssqlodbc.src
SELECTは　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」
```
Mind8で実装していたテスト用のsql文字列定数でSELECT文は下記のような少し長め目の文字列でした。
```mind:mssqlodbc.src
	SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
					「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
					「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」
```
この場合Mind7にはなんらかのソース行の文字数制約があるもようで、下記のようなエラーが出力されてビルドは失敗するようでした。
```
 *  実行するタスク: C:/mind7/bin/mind.exe C:\developments\vscode\pmind\odbcsql/mssqlodbc.src C:/mind7/lib/file 

日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:750*****
コンパイル中 -
コンパイルエラー：ソース行の長さが158桁を越えており、処理できません。
　　モジュール名：C:\developments\vscode\pmind\odbcsql\mssqlodbc.src

 *  ターミナル プロセス "C:\mind7\bin\mind.exe 'C:\developments\vscode\pmind\odbcsql/mssqlodbc.src', 'C:/mind7/lib/file'" が終了コード 2 で終了しました。 
 *  ターミナルはタスクで再利用されます、閉じるには任意のキーを押してください。
```
SELECT文定数を複数に分割して文字列変数に代入するなどが考えられます。

# おわりに
条件コンパイル文の導入により非互換の部分はうまく吸収できました。最後のmssqlodbc.srcのSELECT文の文字列定数はなんとかMind7でビルドしたいので、次回対応してみようと考えています。

## 2024/03/18訂正
@killyさんがコメントで解説いただいている通りmind7のソースコード1行あたりの制約は、文字列定数の場合は「続」で連結して改行すれば回避できます。本文中、「続」で連結して改行してもエラーが出ていると思ったのは私の勘違いで、コメントアウトされていた別のソース行が158バイト超えていたためでした。お騒がせいたしました。
