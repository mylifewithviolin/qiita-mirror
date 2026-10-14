# はじめに
今回はプロデルでデータベースSQLServer2022のステップ２で、トランザクションを構成してみます。

https://qiita.com/advent-calendar/2023/produire


## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Produire Version 2.0.1197 for Windows
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2

# お題のデータべース
こんなテーブル構成のデータベースを作成しております。
データベース名は「日本語プログラミング言語」です。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
#### プロデル
```mind:mssq2.rdr
※コンソール
【conn:SQLServerデータベース】

【sql1:文字列】は、「INSERT INTO 後継言語  (言語ID,後継言語ID) VALUES (@p1, @p2)」
【sql2:文字列】は、「UPDATE 後継言語 SET 後継言語ID =@p1 WHERE 言語ID =@p2」
【sql3:文字列】は、「SELECT LN.言語名,LN.公開年,LN.よみがな,KLN.言語名 AS 後継言語名 
FROM 言語名 AS LN
LEFT JOIN 後継言語　AS KL ON LN.言語ID=KL.言語ID
LEFT JOIN 言語名　AS KLN ON KL.後継言語ID=KLN.言語ID
WHERE LN.言語ID =@p1」
param1は｛@p1=2,@p2=8｝
param2は｛@p1=6,@p2=2｝
param3は｛@p1=2｝

メイン実行する。

メイン実行する手順
	接続構成する
	connへ接続する
	connでトランザクションを開始する
	例外監視
		sql1をparam1としてconnで実行して、結果1とする
		sql2をparam2としてconnで実行して、結果2とする
   
	   	connでトランザクションを完了する
　　発生した場合
		connでトランザクションを取り消す
    監視終わり	
    
	connからsql3をparam3として取得して、結果3とする
	結果3の内容をコンソールへ表示して改行する

	connから切断する
終わり

接続構成する手順
	connというSQLServerデータベースを作る
	connのデータソースは「DESKTOP-078KPRA\SQLEXPRESS」
	connのデータベースは「日本語プログラミング言語」
	connのWindows認証は、○
終わり
```
https://produ.irelang.jp/docs/data/db/dbsqlserver.htm

↑こちらの詳しい説明を拝見して書いています。

# 実行結果
それでは実行してみましょう。コンパイルはプロデルデザイナで実行ファイルの作成するで行っています。

```
C:\produire\sample2>mssql2.exe
{{ＴＴＳ,2000,てぃーてぃーえす,プロデル},{ＴＴＳ,2000,てぃーてぃーえす,スミレ}}

C:\produire\sample2>
```

ちょっとわかりやすくするため結果を改行してみます。

```
{
{ＴＴＳ,2000,てぃーてぃーえす,プロデル},
{ＴＴＳ,2000,てぃーてぃーえす,スミレ}
}
```

# おわりに
次回は例外をスローしてロールバックを検証してみます。
