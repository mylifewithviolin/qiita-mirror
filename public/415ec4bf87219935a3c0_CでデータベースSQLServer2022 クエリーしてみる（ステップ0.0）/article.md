# はじめに

この記事のお題はCでデータベースSQLServer2022にクエリーしてみる（ステップ0.0）」です。ステップ0.0ということはスタートラインに立ったことを意味します。


## この記事内容の作業環境
Windows11 Pro 22H2
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz
Microsoft Visual Studio Community 2022 Version 17.4.4
Microsoft Visual C++ 2022
SQL Server 16.0.1000.6 Express Edition
SQL Server Management Studio	19.2.56.2


# お題のデータべース
データベース名 日本語プログラミング言語
こんなテーブル構成のデータベースを作成しております。
![db.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/5482f410-d924-34ca-392d-a26461bf624f.png)

# お題のソースコード
learn.microsoft.comの日本語サイトの下記に公開されているソースコードを使用します。しかし、このオリジナル状態ではちょっとソースコードの全貌を認識するのが煩雑となるので、かなりシンプル化した状態で接続を試みています。

 https://learn.microsoft.com/ja-jp/sql/connect/odbc/cpp-code-example-app-connect-access-sql-db?view=sql-server-ver16

シンプル化にあたっては下記の記事を参考にしています。

https://segakuin.com/c/odbc/

https://www.kkaneko.jp/cc/mysql/odbcvisualcpp.html

https://learn.microsoft.com/ja-jp/sql/odbc/reference/syntax/sqldriverconnect-function?view=sql-server-ver16

# C状態での変更点
今回はmainの接続文字列情報とSELECT文のFROM句を変更しただけです。

```c:mssql5.c
void main() {
    RETCODE    ret;
    HENV    henv;    //環境ハンドル
    HDBC    hdbc;    //接続ハンドル
    HSTMT   hstmt;   //ステートメントハンドル

    SQLWCHAR datasouce[] = L"Driver={ODBC Driver 17 for SQL Server};Server=(local)\\SQLEXPRESS;Database=日本語プログラミング言語;UID=sa;PWD=****;";
    SQLWCHAR select[] = L"SELECT * FROM 言語名";

    //接続を開く
    ret = openConn(&henv, &hdbc, &hstmt, datasouce);
    if (ret == 0) {
        printf("SUCCESS OPEN\n");
    }else{
        printf("ERROR OPEN\n"); return;
    }
    //照会する
     doSelect(henv, hdbc, hstmt, select);

    //接続を閉じる
    ret = closeConn(&henv, &hdbc);
    if (ret == 0){
        printf("SUCCESS CLOSE\n");
    }else{
        printf("ERROR CLOSE\n"); return;
    }
    return;    

}
```
日本語表示のため、とりあえず結果を表示するDisplayResults()に
setlocale(LC_ALL, "ja_JP.UTF-8");を追記しました。

```diff_c:mssql5.c
//結果を表示する
void DisplayResults(HSTMT hStmt,SQLSMALLINT cCols){

    BINDING* pFirstBinding, * pThisBinding;
    SQLSMALLINT     cDisplaySize;
    SQLRETURN       rc = SQL_SUCCESS;
    int             iCount = 0;

    AllocateBindings(hStmt, cCols, &pFirstBinding, &cDisplaySize);

+   setlocale(LC_ALL, "ja_JP.UTF-8");
    DisplayTitles(hStmt, cDisplaySize + 1, pFirstBinding); 
    
    // Fetch and display the data
    int fNoData = 0;
    do {
        // Fetch a row
        rc = SQLFetch(hStmt);
        if (rc == SQL_NO_DATA_FOUND) {
            fNoData = 1;
        }else {

            // Display the data.   Ignore truncations
            for (pThisBinding = pFirstBinding;
                pThisBinding;
                pThisBinding = pThisBinding->sNext) {
                if (pThisBinding->indPtr != SQL_NULL_DATA)
                {
                    wprintf(pThisBinding->fChar ? DISPLAY_FORMAT_C : DISPLAY_FORMAT,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        pThisBinding->wszBuffer);
                } else {
                    wprintf(DISPLAY_FORMAT_C,
                        PIPE,
                        pThisBinding->cDisplaySize,
                        pThisBinding->cDisplaySize,
                        L"<NULL>");
                }
            }
            wprintf(L" %c\n", PIPE);
        }
    } while (!fNoData);

    wprintf(L"%*.*s", cDisplaySize + 2, cDisplaySize + 2, L" ");
    wprintf(L"\n");

    // Clean up the allocated buffers
    while (pFirstBinding)
    {
        pThisBinding = pFirstBinding->sNext;
        free(pFirstBinding->wszBuffer);
        free(pFirstBinding);
        pFirstBinding = pThisBinding;
    }
}
```

 # 実行結果
 それでは実行してみます。
 ```cmd:
 SQLAllocEnv --> 0
SQLAllocConnect --> 0
SQLConnect --> 1
SQLAllocStmt --> 0
SUCCESS OPEN
SQLExecDirect --> 0
| 言語ID        | 言語名                  | 公開年         | よみがな                  |
|           1 |                 Ｍｉｎｄ |        1985 |                 まいんど  |
|           2 |                  ＴＴＳ |        2000 |             てぃーてぃーえす  |
|           3 |                 ひまわり |        2001 |                 ひまわり  |
|           4 |                 ドリトル |        2003 |                 どりとる  |
|           5 |                 なでしこ |        2004 |                 なでしこ  |
|           6 |                 プロデル |        2007 |                 ぷろでる  |
|           7 |     Mind for Android |        2012 |        まいんどふぉーあんどろいど  |
|           8 |                  スミレ |        2018 |                  すみれ  |
|           9 |                なでしこ３ |        2018 |               なでしこさん  |
|          10 |                 スミレ畑 |        2020 |               すみればたけ  |

SQLDisconnect --> 0
SQLFreeConnect --> 0
SQLFreeEnv --> 0
SUCCESS CLOSE

C:\developments\odbcsql\x64\Debug\odbcsql.exe (プロセス 14584) は、コード 0 で終了しました。
デバッグが停止したときに自動的にコンソールを閉じるには、[ツール] -> [オプション] -> [デバッグ] -> [デバッグの停止時に自 動的にコンソールを閉じる] を有効にします。
このウィンドウを閉じるには、任意のキーを押してください...
 ```
 無事に結果が返りました。ちょっとパイプ文字の位置がよたっていますが、細かいことは気にしません。

 # おわりに
 すみません、タイムアウトです。無事に日本語に対応させられました。ようやくスタートラインに立ちました。C言語でのODBCでのSQLServer接続の情報は少ないので何かの参考になれば幸いです。
