# はじめに
PowerShellでQiitaAPI入門のステップ７です。今回は複数タグを指定して全記事取得中の集計を続きです。前回は少しシンプルな単一タグで集計し、その後複数タグで集計しました。今回は複数タグまたがった集計を複数キー、複数項目で行います。

# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ７）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 複数タグの記事取得（ページネーション指定してループ　ループ内集計　タグまたぎ記事重複ID除外＋複数キー集計　）

複数タグを指定して全記事の記事数を集計する場合、１つの記事には複数のタグを設定できますので、複数のタグが設定された記事を設定された複数タグで集計する際になにもしないと加算集計します。ここではタグ毎の記事重複を除外するロジックを復活させたステップ６を継承し、さらにキー集計を入れ子にします。

具体的にはステップ５と同じくユーザ別の記事数といいね数を年度別に集計してみます。そのためには、ハッシュテーブルの構造を年度別にユーザ別データを保持するようにします。


### コマンド文
```powershell:
# 集計したいタグのリストを作成
$tag_names = @((タグ名1), (タグ名2), (タグ名3))
# 記事ID格納変数
$articleIds = @() 
# タグごとの記事数を格納するハッシュテーブルを初期化
$tag_article_counts = @{}

# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 

# 〇ループ開始　各タグについてループして記事を集計
foreach ($tag_name in $tag_names) {
    $page_articles = @()
    # ページネーション設定 
    $page = 1
    $per_page = 100
    # 〇ループ開始
    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
        
        # 　〇レスポンスのアイテムでループ開始
        foreach ($article in $res) 
        { 
        # ◇記事ID格納変数にレスポンスアイテムの記事IDが含まれない場合 
        # 　　　レスポンスアイテムの記事IDを記事ID格納変数に追加
        # 　　　レスポンスアイテムを1ページあたり記事格納変数に追加
            if (-not $articleIds.Contains($article.id)) { 
                $articleIds += $article.id 
                $page_articles += $article
            } 
        }
        
        # 〇1ページあたり記事格納変数でループ開始
	    foreach ($article in $page_articles) {
	        $year = (Get-Date $article.created_at).Year
	        $userId = $article.user.id
            # ◇年度別の集計用ハッシュテーブルのキーに年変数が存在しない場合
            # 　　年変数のハッシュテーブルを初期
	        if (-not $yearlyStats.ContainsKey($year)) {
	            $yearlyStats[$year] = @{}
	        }
            # 　　◇年度別ユーザーIDの集計用ハッシュテーブル[年変数]のキーにユーザーID変数が存在しない場合
            # 　　　　年変数ユーザーIDの集計用ハッシュテーブル[年変数]を初期化
	        if (-not $yearlyStats[$year].ContainsKey($userId)) {
	            $yearlyStats[$year][$userId] = @{
	                ArticleCount = 0
	                TotalLikes = 0
	            }
	        }

	        $yearlyStats[$year][$userId].ArticleCount++
	        $yearlyStats[$year][$userId].TotalLikes += $article.likes_count
	    }

        # 次のページへ (ページネーションのページ位置カウントアップ)
        $page++
        
    # 〇ループ終端◇最後のページに到達したかを確認 
    } while ($res.Count -eq $per_page)
# 〇ループ終端
}



# 年度別の集計結果を表示
foreach ($year in $yearlyStats.Keys | Sort-Object) {
    Write-Output "年度: $year"
    $stats = $yearlyStats[$year]
    
    # ユーザー集計を記事数降順にソート
    $sortedStats = $stats.GetEnumerator() | Sort-Object -Property {$_.Value.ArticleCount} -Descending
    
    foreach ($entry in $sortedStats) {
        $userId = $entry.Key
        $userStats = $entry.Value
        Write-Output " ユーザーID: $userId"
        Write-Output "  記事数: $($userStats.ArticleCount)"
        Write-Output "  合計いいね数: $($userStats.TotalLikes)"
    }
}

```

### 実行結果
念のため初期設定から再実行しています。複数タグは日本語プログラミング言語なでしこのタグファミリーです。

```powershell:
PS C:\pmind> $tag_names = @("なでしこ", "なでしこ3", "なでしこさん")
PS C:\pmind> $tag_article_counts = @{}
PS C:\pmind> $articleIds = @()
PS C:\pmind> $yearlyStats = @{}
PS C:\pmind> foreach ($tag_name in $tag_names) {
>>     $page_articles = @()
>>     # ページネーション設定
>>     $page = 1
>>     $per_page = 100
>>     do {
>>         $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>         $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>         foreach ($article in $res)
>>         { if (-not $articleIds.Contains($article.id)) {
>>             $articleIds += $article.id
>>             $page_articles += $article
>>             }
>>         }
>>
>>
>>     foreach ($article in $page_articles) {
>>         $year = (Get-Date $article.created_at).Year
>>         $userId = $article.user.id
>>
>>         if (-not $yearlyStats.ContainsKey($year)) {
>>             $yearlyStats[$year] = @{}
>>         }
>>
>>         if (-not $yearlyStats[$year].ContainsKey($userId)) {
>>             $yearlyStats[$year][$userId] = @{
>>                 ArticleCount = 0
>>                 TotalLikes = 0
>>             }
>>         }
>>
>>         $yearlyStats[$year][$userId].ArticleCount++
>>         $yearlyStats[$year][$userId].TotalLikes += $article.likes_count
>>     }
>>
>>         $page++
>>     } while ($res.Count -eq $per_page)
>> }
PS C:\pmind> foreach ($year in $yearlyStats.Keys | Sort-Object) {
>>     Write-Output "年度: $year"
>>     $stats = $yearlyStats[$year]
>>
>>     # ユーザー集計を記事数降順にソート
>>     $sortedStats = $stats.GetEnumerator() | Sort-Object -Property {$_.Value.ArticleCount} -Descending
>>
>>     foreach ($entry in $sortedStats) {
>>         $userId = $entry.Key
>>         $userStats = $entry.Value
>>         Write-Output " ユーザーID: $userId"
>>         Write-Output "  記事数: $($userStats.ArticleCount)"
>>         Write-Output "  合計いいね数: $($userStats.TotalLikes)"
>>     }
>> }
年度: 2011
 ユーザーID: yamitake@github
  記事数: 1
  合計いいね数: 1
年度: 2014
 ユーザーID: dharry
  記事数: 1
  合計いいね数: 0
年度: 2015
 ユーザーID: wnoguchi
  記事数: 1
  合計いいね数: 2
 ユーザーID: yamamoto-gw
  記事数: 1
  合計いいね数: 0
 ユーザーID: aratech
  記事数: 1
  合計いいね数: 9
年度: 2016
 ユーザーID: m0t0k1m0t0k1
  記事数: 1
  合計いいね数: 1
 ユーザーID: tukiyo3
  記事数: 1
  合計いいね数: 6
 ユーザーID: ynomura
  記事数: 1
  合計いいね数: 4
 ユーザーID: wnoguchi
  記事数: 1
  合計いいね数: 14
 ユーザーID: mattn
  記事数: 1
  合計いいね数: 26
年度: 2017
 ユーザーID: SUZUKI_Masaya
  記事数: 1
  合計いいね数: 1
 ユーザーID: ohisama@github
  記事数: 1
  合計いいね数: 1
 ユーザーID: wnoguchi
  記事数: 1
  合計いいね数: 3
 ユーザーID: nakkaa
  記事数: 1
  合計いいね数: 2
年度: 2018
 ユーザーID: ohisama@github
  記事数: 3
  合計いいね数: 0
 ユーザーID: tmy
  記事数: 1
  合計いいね数: 13
 ユーザーID: ariaki
  記事数: 1
  合計いいね数: 4
年度: 2019
 ユーザーID: Hisaku
  記事数: 1
  合計いいね数: 2
 ユーザーID: n_chiba_
  記事数: 1
  合計いいね数: 14
 ユーザーID: nakkaa
  記事数: 1
  合計いいね数: 2
 ユーザーID: kaizen_nagoya
  記事数: 1
  合計いいね数: 0
 ユーザーID: re_sai
  記事数: 1
  合計いいね数: 12
年度: 2020
 ユーザーID: snowdrops89
  記事数: 26
  合計いいね数: 63
 ユーザーID: oza-jv
  記事数: 18
  合計いいね数: 30
 ユーザーID: ohisama@github
  記事数: 7
  合計いいね数: 4
 ユーザーID: kujirahand
  記事数: 6
  合計いいね数: 39
 ユーザーID: j5c8k6m8
  記事数: 3
  合計いいね数: 27
 ユーザーID: n_chiba_
  記事数: 2
  合計いいね数: 46
 ユーザーID: e99h2121
  記事数: 1
  合計いいね数: 10
 ユーザーID: schrosis
  記事数: 1
  合計いいね数: 2
 ユーザーID: programanic
  記事数: 1
  合計いいね数: 4
 ユーザーID: takesiSKTtofuya
  記事数: 1
  合計いいね数: 2
年度: 2021
 ユーザーID: snowdrops89
  記事数: 40
  合計いいね数: 100
 ユーザーID: kujirahand
  記事数: 16
  合計いいね数: 36
 ユーザーID: sonota88
  記事数: 4
  合計いいね数: 14
 ユーザーID: naoki-iso
  記事数: 4
  合計いいね数: 8
 ユーザーID: azumabashi
  記事数: 2
  合計いいね数: 4
 ユーザーID: EasyCording
  記事数: 2
  合計いいね数: 3
 ユーザーID: kurea2020
  記事数: 2
  合計いいね数: 2
 ユーザーID: eznavi
  記事数: 2
  合計いいね数: 4
 ユーザーID: h_ishd
  記事数: 2
  合計いいね数: 28
年度: 2022
 ユーザーID: snowdrops89
  記事数: 26
  合計いいね数: 108
 ユーザーID: kujirahand
  記事数: 16
  合計いいね数: 48
 ユーザーID: mikecat_mixc
  記事数: 10
  合計いいね数: 36
 ユーザーID: JKyumekamui
  記事数: 4
  合計いいね数: 12
 ユーザーID: knakano-gxp
  記事数: 2
  合計いいね数: 44
 ユーザーID: dzonesasaki
  記事数: 2
  合計いいね数: 4
 ユーザーID: eznavi
  記事数: 2
  合計いいね数: 8
年度: 2023
 ユーザーID: mylifewithviolin
  記事数: 72
  合計いいね数: 774
 ユーザーID: ohisama@github
  記事数: 53
  合計いいね数: 2
 ユーザーID: snowdrops89
  記事数: 32
  合計いいね数: 85
 ユーザーID: kujirahand
  記事数: 7
  合計いいね数: 22
 ユーザーID: Osane
  記事数: 6
  合計いいね数: 21
 ユーザーID: JKyumekamui
  記事数: 3
  合計いいね数: 9
 ユーザーID: tetonatk
  記事数: 3
  合計いいね数: 9
 ユーザーID: avaice
  記事数: 3
  合計いいね数: 24
年度: 2024
 ユーザーID: ohisama@github
  記事数: 69
  合計いいね数: 9
 ユーザーID: mylifewithviolin
  記事数: 36
  合計いいね数: 138
 ユーザーID: Osane
  記事数: 21
  合計いいね数: 39
 ユーザーID: snowdrops89
  記事数: 18
  合計いいね数: 48
 ユーザーID: kujirahand
  記事数: 11
  合計いいね数: 32
 ユーザーID: JKyumekamui
  記事数: 6
  合計いいね数: 21
 ユーザーID: mikecat_mixc
  記事数: 6
  合計いいね数: 6
 ユーザーID: avaice
  記事数: 3
  合計いいね数: 9
 ユーザーID: atsushi0919
  記事数: 3
  合計いいね数: 15
 ユーザーID: kyad
  記事数: 3
  合計いいね数: 6
 ユーザーID: nakadate00
  記事数: 3
  合計いいね数: 12
 ユーザーID: tetonatk
  記事数: 3
  合計いいね数: 6
 ユーザーID: Mymt_aggw2208
  記事数: 3
  合計いいね数: 0
 ユーザーID: stpete_ishii
  記事数: 3
  合計いいね数: 6
 ユーザーID: bicstone
  記事数: 3
  合計いいね数: 3
年度: 2025
 ユーザーID: mylifewithviolin
  記事数: 3
  合計いいね数: 6
PS C:\pmind>
```



# おわりに
いかがでしたか？集計結果はなまのテキストでわかりにくくてすみません。またなにか不具合で集計不良がありましたら関係者にお詫び申し上げます。結果はあくまで参考値ということでお願いします。なにかの参考になれば幸いです。
