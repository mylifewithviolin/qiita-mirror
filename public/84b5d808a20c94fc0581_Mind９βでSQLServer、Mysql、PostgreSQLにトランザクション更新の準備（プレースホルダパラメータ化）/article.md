# はじめに
Mind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、[前回の記事](https://qiita.com/mylifewithviolin/items/094b5b5d32d3f00fe275)では、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに対するDB接続、SQL実行、DB切断などの各コマンドを別単語化して実装してみました。今回はSQLコマンド文中のパラメータのプレースホルダに対応します。結合クエリの他、UPDATE文も実行してみます。


# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6

SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2
MySQL Community Server 8.3.0 winx64
mysql-workbench-community-8.0.36-winx64
mysql-connector-odbc-8.0.35-win32
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
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
前回までSQL文では、パラメータの値をSQL文内に埋め込んでいましたが、今回よりSQL文中のプレースホルダに対応します。プレースホルダの記号はSQLServerでも「:」でした。

## ライブラリ
```mind:odebctcl.src
コマンドトークン設定は　コマンドラインにトークンを設定と　等価。
コマンドトークン追加は　コマンドラインにトークンを追加と　等価。
値を取得は             参照０と  等価。
TCL改行は  文字列定数     「＆ＬＦ＆」。

接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　定数　2000バイト。

改行コマンドトークン設定とは　（トークン　→　・）
    コマンドトークン設定し
    TCL改行を　コマンドトークン追加すること。

改行コマンドトークン追加とは　（トークン　→　・）
    コマンドトークン追加し
    TCL改行を　コマンドトークン追加すること。

エラーをモニタするとは　（・　→　・）
    「コマンドの評価実行に失敗しました。」を　表示し　
    「errorInfo」で　値を取得して　表示し　改行すること。

結果をモニタするとは　（結果文字列　→　・）
    表示し　改行すること。

コマンドラインをモニタするとは　（・　→　・）
    改行し
    コマンドラインを　表示し　改行し　改行すること。
    
ODBCライブラリをロードとは　（・　→　1:成功/0:失敗）
        成否は　変数
    "package require tdbc::odbc"を　評価した値０を　成否に　入れ
    捨て
    成否を　返すこと。

標準出力チャネル設定とは　（・　→　1:成功/0:失敗）
        成否は　変数
    「set stdout [open "CONOUT$" "w"]」を　改行コマンドトークン設定し
    「fconfigure $stdout -buffering line」を　コマンドトークン追加し
    コマンドラインを　評価した値０を　成否に　入れ
    捨て
    成否を　返すこと。

標準出力チャネルクローズとは　（・　→　1:成功/0:失敗）
        成否は　変数
    「close $stdout」を　評価した値０を　成否に　入れ
    捨て
    成否を　返すこと。


DB接続とは 	　（接続文字列　→　1:成功/0:失敗）			
        connectStrは　文字列実体　長さ　接続文字列最大長
        成否は　変数
    connectStrに　入れ
    「set connectionString {」を　コマンドトークン設定し
    connectStrを　コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「set db [tdbc::odbc::connection create db $connectionString]」を　コマンドトークン追加し
    コマンドラインを　評価した値０　成否に　入れ
    捨て
    成否を　返すこと。
    
DB切断とは	（・　→　1:成功/0:失敗）
        成否は　変数
    「$db close」を　評価した値０を　成否に　入れ
    捨て
    成否を　返すこと。

結果を取得とは 	　（・　→　結果文字列 1:成功/0:失敗）
    「set result [$stmt execute]」を　改行コマンドトークン設定し
    「$result foreach row {」を　改行コマンドトークン追加し
    「puts $stdout [dict get $row]」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    ※コマンドラインをモニタ
    コマンドラインを　評価した値０すること。 


SQL文をセットとは （SQL文字列　→　・）
	    commandStrは　文字列実体　長さ　SQL文字列最大長
	commandStrに　入れ
    「set stmt [$db prepare 」を　コマンドトークン設定し
    commandStrを　コマンドラインに空白と囲みトークンを追加し
    「]」を　改行コマンドトークン追加。 

パラメータリストを作成とは （・　→　・）
    「set paramList [list」を　コマンドトークン追加。

整数のSQLパラメータをセットとは	 （プレースルダ　変数　→　・）
        プレースホルダは　文字列
        パラメータは　変数
    パラメータに　入れ
    プレースホルダに　入れ    
    「set 」を　コマンドトークン追加
    プレースホルダを　コマンドトークンを追加し
    パラメータを　コマンドラインに空白と数値トークンを追加
    TCL改行を　コマンドトークン追加すること。

文字列のSQLパラメータをセットとは （プレースホルダ　文字列　→　・）
        プレースホルダは　文字列
        パラメータは　文字列
    パラメータに　入れ
    プレースホルダに　入れ
    「set 」を　コマンドトークン追加
    プレースホルダを　コマンドトークンを追加し
    パラメータを　コマンドラインに空白と囲みトークンを追加
    TCL改行を　コマンドトークン追加すること。

    
SELECT実行とは 	　（SQL文字列　→　結果文字列 1:成功/0:失敗）
        成否は　変数
    標準出力チャネル設定し　成否に　入れ
    成否が　０に　等しい
    ならば　空列と　成否を　返し
    さもなければ
        SQL文をセットし　結果を取得し
        ※成否に関わらず
        標準出力チャネルクローズし　成否に　入れ
        成否が　０に　等しい
        ならば　捨て　捨て　空列と　成否を　返し
        つぎに
    つぎに。


結果セット取得とは 	　（・　→　結果文字列 1:成功/0:失敗）
        成否は　変数
    ※SQL文をセットしていること、または、パラメータリスト作成開始していること   
    ※コマンドラインをモニタ
    コマンドラインを　評価した値０　成否に　入れ
    成否が　０に　等しい
    ならば　　空列と　成否を　返し
    さもなければ
        捨て
        標準出力チャネル設定し　成否に　入れ
        成否が　０に　等しい
        ならば　空列と　成否を　返し
        さもなければ
            結果を取得し
            ※成否に関わらず
            標準出力チャネルクローズし　成否に　入れ
            成否が　０に　等しい
            ならば　捨て　捨て　空列と　成否を　返し
            つぎに
        つぎに
    つぎに。

SQLコマンド実行とは　（・　→　1:成功/0:失敗）
        成否は　変数
    ※SQL文をセットしていること、または、パラメータリスト作成開始していること   
    「$stmt execute 」を　改行コマンドトークン追加し
    「$stmt close」を　コマンドトークン追加し
    コマンドラインを　評価した値０　成否に　入れ
    捨て
    成否を　返すこと。

```

## テスト用コード
今回はSQLServerに対してだけ処理を行います。まず結合クエリをパラメータで実行し、UPDATE文を実行してから、結果を同じクエリで確認します。

```mind:testodebctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。


TCLのODBCでトランザクションするとは　（・　→　・）
    SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
    「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
    「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)」
	INSERTは　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (:gid,:dgid)」
	UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id」
	DELETEは　　　文字列定数　「DELETE 開発言語 WHERE 言語ID = :gid AND 開発言語ID = :id」
    成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    datasourceSqlsvrで　DB接続し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし　終わり
    つぎに

    SELECTで　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    コマンドラインをモニタ
    結果セット取得し 成否に　入れ
    成否が　０に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    UPDATEで　SQL文をセットし
    "yomi"と　"あたらしいよみがな"で　文字列のSQLパラメータをセットし
    "id"と　7で　整数のSQLパラメータをセットし
    SQLコマンド実行し 成否に　入れ
    成否が　０に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    コマンドラインをモニタ

    SELECTで　SQL文をセットし
    "id1"と　1で　整数のSQLパラメータをセットし
    "id2"と　7で　整数のSQLパラメータをセットし
    結果セット取得し 成否に　入れ
    成否が　０に　等しい
    ならば　 捨て 
            エラーをモニタし
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし

    DB切断し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに。

※ テスト用
メインとは
    コンソールを開く

    TCLのODBCでトランザクションすること。

```

# お題のMind9βでの実行の様子
結合クエリのSELECT文が先に出力され、次にその結果が出力され、その後UPDATEのSQLスクリプトが出力され、最後に同じ結合クエリの結果が出力されます。

```cmd:

set stmt [$db prepare  {SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (:id1,:id2)}]
set id1 1
set id2 7

言語ID 1 言語名 Ｍｉｎｄ よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Ｍｉｎｄ よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 7 言語名 {Mind for Android} よみがな まいんどふぉーあんどろいど 開発言語ID 3 開発言語名 Java


set stmt [$db prepare  {UPDATE 言語名 SET よみがな = :yomi WHERE 言語ID = :id}]
set yomi {あたらしいよみがな}
set id 7
$stmt execute
$stmt close

言語ID 1 言語名 Ｍｉｎｄ よみがな まいんど 開発言語ID 1 開発言語名 C
言語ID 1 言語名 Ｍｉｎｄ よみがな まいんど 開発言語ID 8 開発言語名 Mind
言語ID 7 言語名 {Mind for Android} よみがな あたらしいよみがな 開発言語ID 3 開発言語名 Java

```
結合クエリを実行しているスクリプトと結果セットを取得しているスクリプトのモニタ出力は割愛しています。



# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。パラメータ化の環境も整いましたので、次回こそはトランザクションの記述方法を検討します。
