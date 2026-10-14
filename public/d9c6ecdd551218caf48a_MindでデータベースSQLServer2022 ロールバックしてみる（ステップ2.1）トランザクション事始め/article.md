# はじめに
この記事のお題は「MindでデータベースSQLServer2022 ロールバックしてみる（ステップ2.1）」です。

[CCでデータベースSQLServer2022 ロールバックしてみる（ステップ2.1）トランザクション事始め](https://qiita.com/mylifewithviolin/items/d362007b2b24995b611e)という記事でODBC関数のCライブラリをトランザクションのロールバックに対応させましたので、それらをMindから実行してみます。

## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
Mind Version 8.0.08 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
データベース名 日本語プログラミング言語
こんなテーブル構成のデータベースを作成しております。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)


# お題のソースコード
## C
C側のプロジェクト配置構成は[C（ステップ0.5）](https://qiita.com/mylifewithviolin/items/2615070f9b4cca51e531)をご参照ください。最新のソースコードは[C（ステップ2.1）トランザクション事始め](https://qiita.com/mylifewithviolin/items/d362007b2b24995b611e)をご参照ください。


## Mind
Mindのソース全体像は[Mind（ステップ2.0）トランザクション事始め](https://qiita.com/mylifewithviolin/items/47edb441d94d2aa7f0a5)をご参照ください。

トランザクションは下記の内訳となります。
1)開発言語テーブルに言語ID=7、開発言語ID=3のレコードを挿入したのでMind for Androidの開発言語がNULLからJavaに変わった
2)言語名テーブルの言語ID=7のよみがなを更新したので、Mind for Androidのよみがなが「まいんどふぉーあんどろいど」から「まいんど」に変わった。
3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除したので、Mindの開発言語Forthの行が消えた。

# 実行結果
前回は動作していなかったロールバックを検証します。3)開発言語テーブルから言語ID=1、開発言語ID=7のレコードを削除する際に、存在しない列名言語ID2=1をあたえてここで失敗を起こします。

では実行します。
```
C:\pmind\sample>mssqlodbc.exe
ODBCライブラリをロードする
ロード成功
関数アドレス群を取得
取得成功
DSText --> Driver={ODBC Driver 17 for SQL Server};Server=(local)\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;
SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
DB接続　成功
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|7|Forth|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|<NULL>|<NULL>|
AutoCommit Off  --> 0
SQLSetConnectAttr --> 0
paramCountInt --> 1
paramNumber --> 1
param --> 7
paramCountInt --> 2
paramNumber --> 2
param --> 3
SQLText --> INSERT INTO 開発言語 (言語ID,開発言語ID) VALUES (?,?)
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
paramCountStr --> 1
paramNumber --> 1
param --> まいんど
paramCountInt --> 1
paramNumber --> 2
param --> 7
SQLText --> UPDATE 言語名 SET よみがな = ? WHERE 言語ID = ?
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?
SQLExecDirect --> -1
SQLStatus --> S0022 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]列名 '言語ID2' が無効です。
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
RollbackTran  --> 1
SQLEndTran  --> 0
AutoCommit On --> 1
SQLSetConnectAttr --> 0
paramCountInt --> 1
paramNumber --> 1
param --> 1
paramCountInt --> 2
paramNumber --> 2
param --> 7
SQLText --> SELECT LN.言語ID,LN.言語名,LN.よみがな,DLN.開発言語ID,DLN.開発言語名 FROM 言語名 AS LN LEFT JOIN 開発言語 AS DL ON LN.言語ID = DL.言語ID LEFT JOIN 開発言語名 AS DLN ON DLN.開発言語ID=DL.開発言語ID WHERE LN.言語ID IN (?,?)
resultset --> free
SQLExecDirect --> 0
paramCountInt --> 0
paramCountStr --> 0
paramNumber --> 0
|言語ID|言語名|よみがな|開発言語ID|開発言語名|
|1|Ｍｉｎｄ|まいんど|1|C|
|1|Ｍｉｎｄ|まいんど|7|Forth|
|1|Ｍｉｎｄ|まいんど|8|Mind|
|7|Mind for Android|まいんどふぉーあんどろいど|<NULL>|<NULL>|
SQLText(char) -->
C:\pmind\sample>
```

DELETEの実行で失敗が起きていることがわかります。
```
SQLText --> DELETE 開発言語 WHERE 言語ID2 = ? AND 開発言語ID = ?
SQLExecDirect --> -1
SQLStatus --> S0022 [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]列名 '言語ID2' が無効です。
```

では、以下にSELECTの結果だけを抽出します。

```:トランザクション前
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど | <NULL> |     <NULL> |  
```
```:トランザクション後
|     言語ID |     言語名 |   よみがな | 開発言語ID | 開発言語名 |
 |          1 |   Ｍｉｎｄ |   まいんど |          1 |          C |
 |          1 |   Ｍｉｎｄ |   まいんど |          7 |      Forth |
 |          1 |   Ｍｉｎｄ |   まいんど |          8 |       Mind |
 |          7 | Mind for Android | まいんどふぉーあんどろいど | <NULL> |     <NULL> | 
```
無事に挿入と更新の結果も反映されず元の状態となっていることが確認できました。トランザクションはロールバックしたことがわかります。:tada:


# おわりに
ようやくこぎつけました。道のりはまだ長いです。しばらくお休みしそうな気がします。この状態で他のDBへの横展開はあるかもです。
