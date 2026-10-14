# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただいておりますので、Mind９βのTclとのインターフェース単語を介しながらTclのODBCデータベースライブラリを使ってSQLServer、Mysql、PostgreSQLに対する共通処理単語を実装しておりました。（昨年2025年の7月ごろまで）最後にSQLServerのSELECT結果を構造体に格納する実装を検証して中断していて、前回はPostgreSQLで検証しましたので今回はMySQLで検証します。


# 前提条件
Windows11 Pro 22H2 22621.4317
mind version9-BETA-7

MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
postgresql-16.1-1-windows-x64
pgAdmin4↑これにはいってたやつ
psqlodbc_16_00_0000-x86


# ９βの言語拡張機能「評価」とは
ご関心があるようでしならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。
また、[こちらの記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用することにより、エラー情報の取得を別途、単語「参照０」を使用して行っています。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはMySQLです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード

## ライブラリ
odbctclライブラリです。前回記事では全文を掲示しましたので割愛します。[こちらの記事](https://qiita.com/mylifewithviolin/items/ce0f273d595b48f93de1)をご参照ください。

この範囲のコードはMind9（β）依存です。

## 結果セットを構造体に格納するコード
こちらのコードが本記事の実質お題です。型のキャストは行っていない簡易コードなので、各DB共通コードとなっています。こちらも前回記事で全文を掲示しましたので割愛します。[こちらの記事](https://qiita.com/mylifewithviolin/items/ce0f273d595b48f93de1)をご参照ください。

この範囲のコードはMind7/8/9（β）で動作します。

## MySQL版テスト用コード
このソースコードはSQL文の記法が若干DB固有コードとなっています。この範囲では接続文字列以外はSQLServerと同じです。

```mind:mysqlodbctcl3.src
"odbctcl3.src"を　コンパイル。
"wordsSeparate.src"を　コンパイル。
"viewmodel2.src"を　コンパイル。

datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=********」。

TCLのODBCで照会するとは　（・　→　・）
　　SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,LN.公開年,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
        「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
        「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　失敗に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourceMysqlで　DB接続し　成否に　入れ
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


# お題のソースコードのMind9βでのビルド

```cmd:
C:\developments\vscode\mind9\odbc>mind mysqlodbctcl3 guilib

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\Mind9-beta-7\bin\mindexw.exe --> mysqlodbctcl3.exe
```

# お題のMind9βでの実行の様子
それでは実行してみます。実際にはMindがコンソールウィンドウを開いています。

```cmd:

set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな,LN.公開年,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7


結果をVIEW開発言語に格納する開始
1       Mind    まいんど        1985    1       C
1       Mind    まいんど        1985    8       Mind
1       Mind    まいんど        1985    10      Tcl/Tk
7       MindforAndroid  あたらしいよみがな      2012    3       Java

結果の行数：4
1|Mind|まいんど|1985|1|C
1|Mind|まいんど|1985|8|Mind
1|Mind|まいんど|1985|10|Tcl/Tk
7|MindforAndroid|あたらしいよみがな|2012|3|Java
```
無事に動作しました:tada:
「結果をVIEW開発言語に格納する開始」という行出力の後の４行が、Tclが返している結果セットの文字列をそのまま出力したものです。
「結果の行数：4」の後が、結果セットの文字列を構造体配列に格納してから、それをパイプ区切りでコンソール出力したものです。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。普段はJavaの場合はSpringBootといっしょにmybatisを、C#の場合はEntityFrameworkをよく使います。
