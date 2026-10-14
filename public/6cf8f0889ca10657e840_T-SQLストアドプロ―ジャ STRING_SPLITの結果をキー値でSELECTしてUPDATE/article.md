# はじめに
JavaのMybatisやC#のEFCoreのデータアクセスモデルでUPDATEを数1000回以上ループさせて処理させますと完走時間が現実的でなくなります。そのような場合、それぞれのモデルの生SQL実行機能でストアドプロシージャで処理する際に、UPDATE対象データのキー値にランダム値を含むような場合はどうしてもその項目の値全体をアプリケーションからSQLServerに伝送する必要があります。

本記事は1000万件くらいのランダム値をCSVとしてSQLServerに伝送して、T-SQLストアドプロ―ジャ内でSTRING_SPLITの結果で対象データをSELECTしてUPDATEする事例です。

https://learn.microsoft.com/ja-jp/sql/t-sql/functions/string-split-transact-sql?view=sql-server-ver17

# 適応対象 
Sql Server 2016 (13.x) 以降

# STRING_SPLITの基本構文
SELECTにはvalueと書くことがお約束です。SQLServerのバージョンがいけていてもSSMSのバージョンが低いとvalueが怒られますが気にしないで実行すると完走します。

```
SELECT value FROM STRING_SPLIT('123,12345,12345678', ',');
```
# STRING_SPLITを使ったUPDATE文
```
UPDATE tn (
SET 列１= @param1,
列２ = @param2,
列３ = @param3
FROM table_name AS tn
WHERE tn.Key IN 
(SELECT CAST(value AS INT) FROM STRING_SPLIT(@valuesList, ','));
```

@param1,@param2,@param3はストアドプロシージャのパラメータで、数100万件UPDATEするtable_nameテーブルに対して同一値となります。

@valuesListはCSVとしてキー項目をカンマ区切りで含んだ文字列です。(上記の場合は数字)パラメータ宣言文ではVARCHAR(MAX)としておくと安全です。valueに@valuesListの値が１件づつ入ってきますので、それをUPDATEしたいレコードのWHERE句のキーのIN句の範囲指定にSELECT文で記述します。



# １回で転送するCSVの項目数
1000万件のUPDATEとなると、CSVの文字列上限やアプリケーションサーバーからDBサーバーへの転送処理も問題になってきますので、現実には分割して処理することになります。

筆者の環境では5000件づつ処理する場合で検証してみました。1000万件を処理するためには5000件づつにいたっては2000回の反復となります。

# 性能（参考情報）

UPDATE対象のテーブルの列数やサーバーの性能にも依存して結果は変動しますが、筆者の環境で1000万件はC#のEFモデルのaddによるループ処理では１時間たっても終わらなかったのに対して10分弱で完了するようになりました。（5000件づつ2000回の反復）

100万件の場合は数10秒強で終わりましたので、だいたいリニアに処理時間が増加していると考えらます。ただし、トリガーなどで別テーブルへINSERTが発生しているような場合は非線形に遅くなる場合があります。

# おわりに
ユーザーが見ている前で処理しなければならない場合、完了時間が10分というのもなかなか厳しいですが、数100万件ならばなんとか実用的な構成と言えます。1000万件を１分以内で終わらせるにはUPDATE対象のテーブルをオンメモリにするとしか思いつきませんが、未検証です。
