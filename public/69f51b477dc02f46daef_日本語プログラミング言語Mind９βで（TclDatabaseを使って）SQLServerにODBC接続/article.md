# はじめに
Qiitaに参加して３年目に突入しました。２年目にあたる昨年2024年のいまごろは
[MindでデータベースSQLServer2022 トランザクションしてみる（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/47edb441d94d2aa7f0a5)というような記事を投稿していたようです。

これはマイクロソフトのODBC規格のインターフェースをC/C++で実装された公開サンプルをCで調整実装してMind用のインターフェースとしてDLL化した事案でした。

そして、今年の1月にMind９βを開発元@killyさんの御厚意により評価用としてご提供いただきましたので、Mind関係者の中では以前から話題となっていた[Tclのデータベースアクセス機能](https://qiita.com/ITvision/items/19b3749e015aabd0c331)について検討してみました。TclのODBCデータベース操作ライブラリやTcl自体についてほぼ知識がないので手探り状態からのスタートです。

# 前提条件
Windows11 Pro 22H2 22621.4169
mind version9-BETA-6
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2


# ９βの言語拡張機能「評価」とは
ご関心があるようでしならば、たいへんお手数ですが、[こちらの記事](https://qiita.com/mylifewithviolin/items/172f91ba20abbb2b3869)をご参照ください。

# お題のデータべース
データベース名 sample
テーブル名 language 
|項目名|項目型|
|:-:|:-:|
|id| int  |
| name  |  nvarchar(50) |

# お題のソースコード
ODBC接続文字列は前記の昨年のC言語での検証時の環境を流用しているためSQLServerとMySqlを定義していますが、今回検証しているのはSQLServerです。
当初のうち実行時エラーがいろいろ出ていた時はいったん日本語テーブルという要素を除いたため、SQLServer接続先は同じく当時評価用につかっていた英字テーブルとしております。

## 参考情報
https://www.tcl-lang.org/man/tcl9.0/TdbcodbcCmd/tdbc_odbc.html

## ライブラリ
```mind:odebctcl.src
コマンドトークン設定は　コマンドラインにトークンを設定と　等価。
コマンドトークン追加は　コマンドラインにトークンを追加と　等価。

接続文字列最大長は　定数　400バイト。
SQL文字列最大長は　定数　2000バイト。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=sample;UID=sa;PWD=****;」。
datasourceMysqlは 文字列定数 「Driver={MySQL ODBC 8.0 Unicode Driver};Server=localhost;Port=3306;Database=日本語プログラミング言語;UID=root;PWD=*****;charset=cp932」。
SELECT1は　　　文字列定数　「SELECT * FROM language WHERE id IN (1,2,3,4,5)」。
SELECT2は　　　文字列定数　「SELECT * FROM 言語名 WHERE 言語ID IN (1,7)」。


ODBCライブラリをロードとは　（・　→　・）
    "package require tdbc::odbc"を　評価すること。

SQL実行とは 	　（接続文字列　SQL文字列　→　・）
        connectStrは　文字列実体　長さ　接続文字列最大長
        commandStrは　文字列実体　長さ　SQL文字列最大長
    commandStrに　入れ
    connectStrに　入れ
    「set stdout [open "CONOUT$" "w"]＆ＬＦ＆」を　コマンドトークン設定し
    「fconfigure $stdout -buffering line＆ＬＦ＆」を　コマンドトークン追加し
    「set connectionString {」を　コマンドトークン追加し
    connectStrを　コマンドトークン追加し
    「}＆ＬＦ＆」を　コマンドトークン追加し
    「set db [tdbc::odbc::connection create db $connectionString]＆ＬＦ＆」を　コマンドトークン追加し
    「set stmt [$db prepare {」を　コマンドトークン追加し
    commandStrを　コマンドトークンを追加し
    「}]＆ＬＦ＆」を　コマンドトークン追加し
    「set result [$stmt execute]＆ＬＦ＆」を　コマンドトークン追加し
    「$result foreach row {＆ＬＦ＆」を　コマンドトークン追加し
    「puts $stdout [dict get $row]＆ＬＦ＆」を　コマンドトークン追加し
    「}＆ＬＦ＆」を　コマンドトークン追加し
    「$result close＆ＬＦ＆」を　コマンドトークン追加し
    「$stmt close＆ＬＦ＆」を　コマンドトークン追加し
    「$db close＆ＬＦ＆」を　コマンドトークン追加し
    「close $stdout」を　コマンドトークン追加し
    コマンドラインを　表示し　改行し　改行し
    コマンドラインを　評価した値を　表示し　改行すること。   


TCLのODBCでクエリするとは　（・　→　・）

    ODBCライブラリをロードし
    datasourceSqlsvrと　SELECT1で　SQL実行すること。
```

## テスト用コード
```mind:sqlsevertcl.src
"odbctcl.src"を　コンパイルする。

    ※ テスト用
メインとは
   
    TCLのODBCでクエリすること。
```

# お題のソースコードのMind9βでのビルド

```cmd:
C:\developments\vscode\mind9>mind sqlsvrtcl guilib 

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\mind9-beta\mind9-beta\bin\mindexw.exe --> sqlsvrtcl.exe
```
ビルド成功しました！:tada:
実はビルド成功はすんなりいくのですがTclスクリプトの実行時エラーを解消するのにだいぶ手間どりました。

# お題のMind9βでの実行の様子
今回はコンソールウィンドウを展開していますので、CUI出力を以下に示します。
前半はMindのTcl評価へ与えたTclスクリプトの確認用出力です。このスクリプトを与えて実行した結果がその下のプログラミング言語名のような出力です。

```cmd:
set stdout [open "CONOUT$" "w"]
fconfigure $stdout -buffering line
set connectionString {Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=sample;UID=sa;PWD=mind;}
set db [tdbc::odbc::connection create db $connectionString]
set stmt [$db prepare {SELECT * FROM language WHERE id IN (1,2,3,4,5)}]
set result [$stmt execute]
$result foreach row {
puts $stdout [dict get $row]
}
$result close
$stmt close
$db close
close $stdout

id 1 name C
id 2 name C++
id 3 name Java
id 4 name C#
id 5 name Mind
```
動きました:tada:

どんな風に出力されるのかもわかってはいなかったので、とりあえずフィールド名と値が空白区切りで出力されることがわかりました。

次回は日本語データベースに接続してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。まだほんのさわりの部分ですが、今年で生誕４０周年を迎える日本語プログラミング言語Mind、ついに新バージョンがベールをぬぎはじめます！

Qiitaに参加して３年目に突入しました。最初の記事が2023年1月22日の
[トランスコンパイラの作り方 Ｃ言語を日本語プログラミング言語Mindにトランスコンパイルしてみる（四則演算版](https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c)
という記事でした。
