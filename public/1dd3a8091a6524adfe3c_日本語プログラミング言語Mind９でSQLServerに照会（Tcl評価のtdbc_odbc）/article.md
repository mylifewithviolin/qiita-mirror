# はじめに
日本語プログラミング言語Mindのバージョン９の言語拡張機能「評価」でTclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しております。今回はSQLServerでの動作を検証します。[Mind9ベータ版で実装](https://qiita.com/mylifewithviolin/items/77dafdc556568a5a8ddc)のリリース版での追検証となります。本記事はマニュアル未記載な内容でMind９の本来のサポートレベルを超えた内容です。

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 9.03

SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# Mind９の言語拡張機能「評価」とは
ご関心があるようでしたならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLServerです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
前記ODBC接続用パッケージを使ったMind記述のodbctclライブラリを使用します。ODBC接続用TclランタイムはMind9パッケージに含まれていますが、当ライブラリはユーザー作成ライブラリです。また、TclはMind9の場合Tcl/Tkを利用するために導入されているため、GUIライブラリに依存する関係となります。

## ライブラリ
tclDatabaseのtdbc:odbcというODBC接続用パッケージを使ったMind記述のodbctclライブラリの一部です。

```mind:odbctcl3.src

結果を取得とは 	　（・　→　結果文字列 1:成功/0:失敗）
    「set result [$stmt execute]」を　改行コマンドトークン設定し
    「set outputList {}」を　改行コマンドトークン追加し
    「$result foreach row {」を　改行コマンドトークン追加し
    「set fields [dict values $row]」を　改行コマンドトークン追加し
    「set line [join $fields "\t"]」を　改行コマンドトークン追加し
    「lappend outputList $line」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    「return [join $outputList "\t\n"]」を　改行コマンドトークン追加し
    ※コマンドラインをモニタ
    コマンドラインを　評価した値０すること。 
```

たいへんお手数ですが、「結果を取得」の定義部以外のソースコード全体は[こちらの記事](https://qiita.com/mylifewithviolin/items/12bd2c6ee6aea2d39ee8)をご参照ください。この範囲のコードはMind9依存です。


## 結果セットを構造体に格納するコード
こちらのコードが本記事の実質お題です。型のキャストは行っていない簡易コードなので、各DB共通コードとなっています。その他、あまり手の込んだことは実装していないので、いろいろ簡易版となっています。

```mind:wordsSeparate.src
指定切り出しコードは　変数。

指定切り出しコードをセットするとは　（文字コード　→　・）
    指定切り出しコードに　入れること。

指定コードで単語を切り出すとは　処理単語　.J　（文字列実体　→　切り出し文字列）
        文字位置は　変数
        親側文字列は　文字列実体情報

    親側文字列に　入れ
    親側文字列を　指定切り出しコードで　一文字検索し　文字位置に　入れ
    文字位置が　　ゼロ以外
    ならば
        文字位置で　親側文字列を　分断し
    さもなければ
        空列を　返し
    つぎに。
```
```mind:viewmodel2.src
結果セット最大行数は　定数　1000行。
VIEW結果は　文字列実体　長さ 5000。

VIEW開発言語型は　型紙
        言語IDは　文字列実体　長さ　10
        言語名は　文字列実体　長さ　200
        よみがなは　文字列実体　長さ　200
        公開年は　　文字列実体　長さ　10
        開発言語IDは　文字列実体　長さ　10
        開発言語名は　文字列実体　長さ　200
    行データは　言語IDと　言語名と　よみがなと　公開年と　開発言語IDと　開発言語名
    行数は　変数
    全体は
　　    行数と　結果セット最大行数の　行データ。

VIEW開発言語は　構造体　VIEW開発言語型。

結果をVIEW開発言語に格納するとは　（結果文字列　→　・）
        VIEW行数は　変数
        打ち切りフラグは　変数
        初回フラグは　変数
    「結果をVIEW開発言語に格納する開始」を　一行表示し
    VIEW結果に　入れ
    VIEW結果を　一行表示し　改行し
    TABを　指定切り出しコードにセットし
    VIEW結果に　TABを　一文字追加し
    VIEW行数に　０を　入れ
    打ち切りフラグを　クリアし
    初回フラグを　セットし
    ここから
        結果セット最大行数で　回数指定し
            VIEW結果から　指定コードで単語を切り出して　複写し　
            空列？　
            ならば
                捨て　
                打ち切りフラグを　セットし
                打ち切り　
            さもなければ
                初回フラグが　１に　等しい
                ならば　VIEW行数に　１を　入れ　初回フラグを　クリアし
                さもなければ　VIEW行数を　一つ増加し
                つぎに
                VIEW開発言語の　言語ID(VIEW行数)に　入れ　
            つぎに
            VIEW結果から　指定コードで単語を切り出して　VIEW開発言語の　言語名(VIEW行数)に　入れ　
            VIEW結果から　指定コードで単語を切り出して　VIEW開発言語の　よみがな(VIEW行数)に　入れ
            VIEW結果から　指定コードで単語を切り出して　VIEW開発言語の　公開年(VIEW行数)に　入れ
            VIEW結果から　指定コードで単語を切り出して　VIEW開発言語の　開発言語ID(VIEW行数)に　入れ
            VIEW結果から　指定コードで単語を切り出して　VIEW開発言語の　開発言語名(VIEW行数)に　入れ
            VIEW結果から 一文字削除し
        繰り返す
        打ち切りフラグが　１に　等しい
        ならば　打ち切り　つぎに
    繰り返し
    VIEW開発言語の　行数に　VIEW行数を　入れること。

    
VIEW開発言語を出力とは　（・　→　・）
    「結果の行数：」を　表示し
    VIEW開発言語の　行数を　数値表示し　改行し
    VIEW開発言語の　行数で　回数指定し
        VIEW開発言語の　言語ID(回数)を　表示し　「|」を　表示し
        VIEW開発言語の　言語名(回数)を　表示し　「|」を　表示し
        VIEW開発言語の　よみがな(回数)を　表示し　「|」を　表示し
        VIEW開発言語の　公開年(回数)を　表示し　「|」を　表示し
        VIEW開発言語の　開発言語ID(回数)を　表示し　「|」を　表示し
        VIEW開発言語の　開発言語名(回数)を　表示し　改行し
    繰り返す。
```

この範囲のコードはMind7/8/9で動作します。

## SQLServer版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。

```mind:sqlsvrodbctcl2.src
"odbctcl3.src"を　コンパイル。
"wordsSeparate.src"を　コンパイル。
"viewmodel2.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=*******;」。

TCLのODBCで照会するとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,LN.公開年,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
        「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
        「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourceSqlsvrで　DB接続し　成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし　終わり
    つぎに

    SELECTで　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　失敗に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
 
    結果をVIEW開発言語に格納し
    VIEW開発言語を出力し

    DB切断し　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに。

※ テスト用
メインとは
    コンソールを開く

    TCLのODBCで照会すること。
```


# お題のソースコードのMind9でのビルド
TclはMind9の場合Tcl/Tkを利用するために導入されているため、ＧＵＩアプリケーション用のライブラリからのコンパイルが必要となります。
```cmd:
C:\developments\vscode\mind9\odbc>mind sqlsvrodbctcl2 guilib

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\Mind9\bin\mindexw.exe --> sqlsvrodbctcl2.exe
```

# お題のMind9での実行の様子
それでは実行してみます。
```cmd:
set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな,LN.公開年,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7


結果をVIEW開発言語に格納する開始
1       Ｍｉｎｄ        まいんど        1985    1       C
1       Ｍｉｎｄ        まいんど        1985    8       Mind
1       Ｍｉｎｄ        まいんど        1985    10      Tcl/Tk
7       Mind for Android        まいんどふぉーあんどろいど      2012    3       Java

結果の行数：4
1|Ｍｉｎｄ|まいんど|1985|1|C
1|Ｍｉｎｄ|まいんど|1985|8|Mind
1|Ｍｉｎｄ|まいんど|1985|10|Tcl/Tk
7|Mind for Android|まいんどふぉーあんどろいど|2012|3|Java
```
無事に動作しました。
「結果をVIEW開発言語に格納する開始」という出力の後、「結果の行数：4」までの間がTclが返している結果セットの文字列をそのまま出力したものです。
「結果の行数：4」の後が、結果セットの文字列を構造体配列に格納してから、それをパイプ区切りでコンソール出力したものです。

実際には下記のコードでMindがコンソールウィンドウを開いています。
```mind:sqlsvrodbctcl2.src
メインとは
    コンソールを開く
```
![tclodbcsqlsvr.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/d498f0d5-35a8-401d-9142-86b03a33458f.jpeg)

上記のテキスト出力は上図のCUI出力を示したものとなります。

今回はSELECTの結果でしたが、INSERTやUPDATE、DELETEをβ版で実行した実装が過去にありますので、漸次リリース版で追検証して参ります。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。普段はJavaの場合はSpringBootといっしょにmybatisを、C#の場合はEntityFrameworkをよく使います。
