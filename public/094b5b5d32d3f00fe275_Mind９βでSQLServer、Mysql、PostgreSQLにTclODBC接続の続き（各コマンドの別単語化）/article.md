# はじめに
今年の1月にMind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、[前回の記事](https://qiita.com/mylifewithviolin/items/7e8d5ff88eb227a8bbf4)では、TclのODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQLに接続してエラー処理を追加しました。今回は前回までTclスクリプトを一本書きしていた点を改め（まったく不慣れなため試作としての最初のステップでした）DB接続、SQL実行、DB切断などの各コマンドを別単語化します。前回までSQL実行としていました単語は結果セットを文字列として返す点まで含めた単語となっておりますので、SELECT実行に変更しました。SQL実行はINSERT/UPDATE/DELTEなどのコマンド用に移行する予定です。今回はこのコマンド未対応で次回以降の予定です。


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
前回より「評価した値」ではなく、エラー結果を返す「評価した値０」を使用しています。また、エラー情報の取得はTcl_GetValueを使った単語「参照０」を使用します。

## 参考情報
tclDatabaseにはMysql、PostgreSQL、SQLLite固有のパッケージがありますが、今回評価しているのはtdbc:odbcというODBC接続用パッケージです。

https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

# お題のデータべース
SQLServer、Mysql、PostgreSQLでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
今回は前回までSQL実行のTclスクリプトを一本書きしていた点を改め、DB接続、SQL実行、DB切断などの各コマンドを別単語化します。前回までSQL実行としていました単語は結果セットを文字列として返す点まで含めた単語となっておりますので、SELECT実行に変更しました。
標準出力チャネル設定は結果セットを文字列で返していることにより必要となっているコマンドですが、SELECT実行のTCLスクリプトで一本書きのままでもよかったのですが、いちおう分離しました。

## ライブラリ
```mind:odebctcl.src
コマンドトークン設定は　コマンドラインにトークンを設定と　等価。
コマンドトークン追加は　コマンドラインにトークンを追加と　等価。
値を取得は             参照０と  等価。

接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　定数　2000バイト。

改行コマンドトークン設定とは　（トークン　→　・）
    コマンドトークン設定し
    「＆ＬＦ＆」を　コマンドトークン追加すること。

改行コマンドトークン追加とは　（トークン　→　・）
    コマンドトークン追加し
    「＆ＬＦ＆」を　コマンドトークン追加すること。

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

SELECT実行０とは 	　（SQL文字列　→　結果文字列 1:成功/0:失敗）
        commandStrは　文字列実体　長さ　SQL文字列最大長
    commandStrに　入れ
    「set stmt [$db prepare {」を　コマンドトークン設定し
    commandStrを　コマンドトークンを追加し
    「}]」を　改行コマンドトークン追加し
    「set result [$stmt execute]」を　改行コマンドトークン追加し
    「$result foreach row {」を　改行コマンドトークン追加し
    「puts $stdout [dict get $row]」を　改行コマンドトークン追加し
    「}」を　改行コマンドトークン追加し
    「$result close」を　改行コマンドトークン追加し
    「$stmt close」を　改行コマンドトークン追加し
    コマンドラインを　評価した値０すること。 

SELECT実行とは 	　（SQL文字列　→　結果文字列 1:成功/0:失敗）
        成否は　変数
    標準出力チャネル設定し　成否に　入れ
    成否が　０に　等しい
    ならば　空列と　成否を　返し
    さもなければ
        SELECT実行０し
        ※成否に関わらず
        標準出力チャネルクローズし　成否に　入れ
        成否が　０に　等しい
        ならば　捨て　捨て　空列と　成否を　返し
        つぎに
    つぎに
。
```

## テスト用コード
前回までSQL実行としていました単語は結果セットを返す点まで含めた単語となっておりますので、SELECT実行に変更しました。
```mind:testodebctcl.src
"odbctcl.src"を　コンパイル。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=****;charset=cp932」。
datasourcePgsqlは 文字列定数 「Driver={PostgreSQL UNICODE};Server=localhost;Port=5432;Database=日本語プログラミング言語;UID=postgres;PWD=****;」。
SELECT1は　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」。
SELECT2は　　　文字列定数　「SELECT * FROM 言語名 言語名 WHERE "言語ID" IN (1,7)」。

TCLのODBCでクエリするとは　（・　→　・）
        成否は　変数

    ODBCライブラリをロードし 成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに

    datasourceSqlsvrで　DB接続し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし　 
            終わり
    つぎに

    SELECT1で　SELECT実行し 成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 捨て　
            DB切断し　捨て
            終わり    
    つぎに
    結果をモニタし
    コマンドラインをモニタし

    DB切断し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに

    datasourceMySqlで　DB接続し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに

    SELECT1で　SELECT実行し 成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 捨て　
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし
    コマンドラインをモニタし

    DB切断し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに

    datasourcePgsqlで　DB接続し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    　
    SELECT2で　SELECT実行し 成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 捨て　
            DB切断し　捨て　終わり
    つぎに
    結果をモニタし
    コマンドラインをモニタし
    
    DB切断し　成否に　入れ
    成否が　０に　等しい
    ならば　エラーをモニタし 終わり
    つぎに
    。

※ テスト用
メインとは
    コンソールを開く
    
    TCLのODBCでクエリすること。
```


# お題のMind9βでの実行の様子
各DBに対するSELECT結果が先に出力され、その後SQLスクリプトが出力されます。

```cmd:
言語ID 1 言語名 Ｍｉｎｄ 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいど


set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close


言語ID 1 言語名 Mind 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいど


set stmt [$db prepare {SELECT * FROM 言語名 WHERE 言語ID IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close


言語ID 1 言語名 Mind 公開年 1985 よみがな まいんど
言語ID 7 言語名 {Mind for Android} 公開年 2012 よみがな まいんどふぉーあんどろいど


set stmt [$db prepare {SELECT * FROM 言語名 言語名 WHERE "言語ID" IN (1,7)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close

```

エラー判定の他、賞味のSQL実行の前後処理を分割実行できるようになりましたので、次回はいよいよトランザクションの記述方法などを検討してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。まだほんのさわりの部分ですが、今年で生誕４０周年を迎える日本語プログラミング言語Mind、ついに新バージョンがベールをぬぎはじめます！
