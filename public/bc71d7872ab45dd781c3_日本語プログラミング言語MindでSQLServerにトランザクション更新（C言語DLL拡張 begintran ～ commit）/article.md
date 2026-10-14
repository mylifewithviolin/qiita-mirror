# はじめに
日本語プログラミング言語MindのC言語インターフェースの自作ODBCデータベース操作ライブラリをつかってSQLServer、Mysql、PostgreSQL、SQLiteに対する共通処理単語を実装しております。今回はSQLServerでのトランザクション更新動作のコミットを検証します。（[Mind9のTCL評価によるトランザクション更新動作の記事](https://qiita.com/mylifewithviolin/items/4ee809e338389c250da5)も併せてお読みください。ほぼ同じMind単語で動作しているという建付けです。）

# 前提条件
Windows11 Pro 22H2 22621.4317
mind version 9.03
mind version 8.07
mind version 7.5

Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022

SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

SQL Serverの他、下記のRDBに対応しています。
MySQL Community Server 8.3.0 winx64
mysql-connector-odbc-8.0.35-win32
postgresql-16.1-1-windows-x64
psqlodbc_16_00_0000-x86

# お題のデータべース
SQLServer、Mysql、PostgreSQL、SQLiteでは共通のテーブル構成のデータベースを作成しています。データベース名は「日本語プログラミング言語」です。今回もそれを利用します。今回検証しているのはSQLServerです。

![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
## C
C側のプロジェクト配置構成は[こちらの記事](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。

## DLLライブラリ本体
Cで実装されたDLLライブラリ本体のソースコードは[CでODBCデータベース実装 SQLServer2022（ステップ3）結果セットを項目名情報無で返す](https://qiita.com/mylifewithviolin/items/9a1bd4c75a2a3be543f0)をご参照ください。

## Mind
### ライブラリ
Mindで実装されたODBCライブラリ本体のソースコードは[Mind7/8/9 odbcライブラリC言語DLL拡張単語のアップデート（結果セット取得の9βTcl互換調整）](https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a)をご参照ください。

**ライブラリ単語仕様**
Mind9依存のTclのODBCデータベース操作ライブラリと概ねMind単語の仕様を揃えています。

DB接続とDB接続の単語です。
>構文　＝　＜接続文字列＞を　DB接続する　→　＜真／偽＞
構文　＝　DB切断する　→　＜真／偽＞

SQL文とプレースホルダをセットする単語です。ODBCの場合はプレースホルダ名でプレースホルダを識別できず、プレースホルダ？の順番にセットする必要があります。
>構文　＝　＜SQL文字列＞SQL文をセットし
構文　＝　＜数値＞で　整数のSQLパラメータをセット　→　・
構文　＝　＜文字列＞で　文字列のSQLパラメータをセット　→　・

SQL文を実行する単語です。前者が結果セットが返るもの、後者は結果セットが返らないものです。
>構文　＝　結果セット取得　→　＜結果文字列＞
構文　＝　SQLコマンド実行　→　＜真／偽＞

トランザクションを開始する単語です。
>構文　＝　トランザクションを開始　→　・

トランザクションのスコープ（範囲）を指定する単語、脱出する単語です。
※「スコープ開始」が回数指定構文の等価定義です。「ここからトランザクション」が１を返します。
>構文　＝　ここからトランザクションの　スコープ開始
　　　　　※SQLコマンド実行の結果を成否に入れ　成否が偽　ならば
　　　　　　　スコープを抜け出す　→　・　
　　　　　※つぎに
　　ここまでスコープ

トランザクションをコミットまたはロールバックする単語です。
トランザクションスコープ内で各SQLの実行成否を変数に格納しておき、その実行成否変数を評価できるようにしておきます。

>構文　＝　コミットする　→　・
構文　＝　ロールバックする　→　・

こうしてC言語拡張のODBCライブラリのMind単語はTcl評価を使ったodbcライブラリのMind単語よりエラー処理が弱いことがわかります。少し時間を見て強化しておこうと思います。

## SQLServer版テスト用コード
UPDATE文を実行しておきます。ロールバック検証では開発言語IDの10が追加された状態でIDが同じINSERT文を実行していましたが、コミット検証では存在するIDに対してDELETE文を実行しておくことで、最後まで完走するようにしています。


```mind:mssqlodbcctrancmit.src
"odbcc"を　コンパイルする。

datasourceSqlsvrは 文字列定数 「Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=********;」。

ODBCでトランザクションするとは　（・　→　・）
    SELECTは　　　文字列定数　「SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN 」続
    「LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID 」続
    「LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)」
　　SELECT1は　　　文字列定数　「SELECT * FROM 言語名 AS LN  WHERE LN.言語ID IN (?,?)」
　　SELECT2は　　　文字列定数　「SELECT * FROM 開発言語 AS DL WHERE DL.言語ID IN (?,?)」
    SELECT3は　　　文字列定数　「SELECT * FROM 開発言語名 AS DLN WHERE DLN.開発言語ID IN (?,?)」
　　INSERT1は　　　文字列定数　「INSERT INTO 開発言語名 (開発言語ID,開発言語名) VALUES (?,?)」
　　INSERT2は　　　文字列定数　「INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)」
　　UPDATEは　　　文字列定数　「UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?」
　　DELETE1は　　　文字列定数　「DELETE FROM 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?」
　　DELETE2は　　　文字列定数　「DELETE FROM 開発言語名 WHERE 開発言語ID = ?」


    成否は　変数

    API初期処理しておき　成否に　入れ
    成否が　成功に　等しい　
   でなければ　終わり　つぎに

    datasourceSqlsvrで　DB接続し　成否に　入れ
    成否が　失敗に　等しい
    ならば　成否を　数値表示し　終わり
    つぎに

    SELECTを　一行表示し
    SELECTで　SQL文をセットし
    1で　整数のSQLパラメータをセットし
    7で　整数のSQLパラメータをセットし
    結果セット取得し 結果セットを表示し

    改行し
    SELECT1を　一行表示し
    SELECT1で　SQL文をセットし
    1で　整数のSQLパラメータをセットし
    7で　整数のSQLパラメータをセットし
    結果セット取得し 結果セットを表示し

    改行し
    SELECT2を　一行表示し
    SELECT2で　SQL文をセットし
    1で　整数のSQLパラメータをセットし
    7で　整数のSQLパラメータをセットし
    結果セット取得し 結果セットを表示し

    改行し
    SELECT3を　一行表示し
    SELECT3で　SQL文をセットし
    1で　整数のSQLパラメータをセットし
    10で　整数のSQLパラメータをセットし
    結果セット取得し 結果セットを表示し

    トランザクションを開始し

    ここからトランザクションの　スコープ開始
    
        改行し
        UPDATEを　一行表示し
        UPDATEで　SQL文をセットし
        "あたらしいよみがな"で　文字列のSQLパラメータをセットし
        7で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに
        
        改行し
        DELETE1を　一行表示し
        DELETE1で　SQL文をセットし
        10で　整数のSQLパラメータをセットし
        1で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに

        改行し
        DELETE2を　一行表示し
        DELETE2で　SQL文をセットし
        10で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに

        改行し
        INSERT1を　一行表示し
        INSERT1で　SQL文をセットし
        10で　整数のSQLパラメータをセットし
        "Tcl/Tk"で　文字列のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに

        改行し
        INSERT2を　一行表示し
        INSERT2で　SQL文をセットし
        10で　整数のSQLパラメータをセットし
        1で　整数のSQLパラメータをセットし
        SQLコマンド実行し 成否に　入れ
        成否が　失敗に　等しい
        ならば　 スコープを抜け出す
        つぎに

　　ここまでスコープ

　　成否が　成功に　等しい
　　ならば
        コミットし　
　　さもなければ
        SQLエラー取得し Mind文字列に変換し　一行表示し
        ロールバックし
　　つぎに

    改行し
    SELECTを　一行表示し
    SELECTで　SQL文をセットし
    1で　整数のSQLパラメータをセットし
    7で　整数のSQLパラメータをセットし
    結果セット取得し 結果セットを表示し

    DB切断し　API破棄処理すること。

※ テスト用
メインとは

    ODBCでトランザクションすること。

```

# お題のソースコードのビルド
## Mind9
Mind9のTclはTcl/Tkを利用するために導入されているため、GUIアプリケーション用のライブラリguilibからのコンパイルが必須となりますが、本ライブラリはfileからのコンパイルで動作します。guilibからのコンパイルをさまたげるものではありません。

```cmd:
C:\developments\vscode\mind9\odbc>mind mssqlodbcctrancmit file

日本語プログラミング言語 Ｍｉｎｄ Version 9.03 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\Mind9\bin\mindex.exe --> mssqlodbcctrancmit.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind mssqlodbcctrancmit file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> mssqlodbcctrancmit.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind mssqlodbcctrancmit file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> mssqlodbcctrancmit.exe
```

# お題の実行の様子
それでは実行してみます。下記はMind8の結果ですが7／9でも変わりません。

ロールバック検証時のSELECT結果は３テーブル結合クエリーだけでしたが。本検証ではトランザクション開始前の３テーブル単独の状態もクエリーしています。

SQL文が出力されているのは各SQL文を実行前に「一行表示」しています。

```cmd:
C:\developments\vscode\mind9\odbc>mssqlodbcctrancmit
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DB接続　成功
SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|1|Ｍｉｎｄ|まいんど|10|Tcl/Tk|
|7|Mind for Android|まいんどふぉーあんどろいど|3|Java|

SELECT * FROM 言語名 AS LN  WHERE LN.言語ID IN (?,?)
|1|Ｍｉｎｄ|1985|まいんど|
|7|Mind for Android|2012|まいんどふぉーあんどろいど|

SELECT * FROM 開発言語 AS DL WHERE DL.言語ID IN (?,?)
|1|1|
|1|8|
|1|10|
|7|3|

SELECT * FROM 開発言語名 AS DLN WHERE DLN.開発言語ID IN (?,?)
|1|C|<NULL>|
|10|Tcl/Tk|<NULL>|

UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?

DELETE FROM 開発言語 WHERE 言語ID = ? AND 開発言語ID = ?

DELETE FROM 開発言語名 WHERE 開発言語ID = ?

INSERT INTO 開発言語名 (開発言語ID,開発言語名) VALUES (?,?)

INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)

SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|1|Ｍｉｎｄ|まいんど|10|Tcl/Tk|
|7|Mind for Android|あたらしいよみがな|3|Java|
ODBCライブラリを破棄する

C:\developments\vscode\mind9\odbc>
```
無事にコミットが成功しました。よみがなを変えるUPDATE文の結果が反映されていることがわかります。


# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。Mind単語としての仕様をまとめたところでも書きましたが、エラーリターンが弱いので追って改良いたします。その他もろもろ改良点はたくさんありますが、手が回ってないようです。:joy:
