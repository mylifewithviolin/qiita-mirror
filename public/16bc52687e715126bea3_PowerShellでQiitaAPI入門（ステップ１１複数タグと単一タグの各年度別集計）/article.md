# はじめに
PowerShellでQiitaAPI入門のステップ１１です。今回は複数タグまたがった集計と単一タグでの記事数、いいね数の年度別集計を行います。具体的には日本語プログラミング言語なでしことMindとRe:Mindについて行います。MindとRe:Mindはタグがいまのところ１つですが、なでしこは４つくらいタグがあるのでそれらは１つにまとめて集計するのがミソです。なでしこ関連タグの間で重複する記事IDは一つとカウントし、MindとRe:Mindとなでしこ関連タグの間で重複する記事IDはそれぞれのタグにカウントします。

# 前提条件
Windows11 Pro 22H2 22621.4317
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ１１）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 複数タグと単一タグのグループ化記事取得（ページネーション指定してループ　ループ内集計　タグまたぎ記事重複ID除外＋複数キー集計　）

まずおさらいとして関連するタグから重複する記事IDを除いて年度別集計します。
複数タグは日本語プログラミング言語なでしこのタグファミリーです。これらのタグはカテゴリとしてユニークと扱うので、重複する記事IDを除いて年度別集計します。

### コマンド文
```powershell:
# 集計したいタグのリストを作成
$tag_names = @("なでしこ", "なでしこ3", "なでしこさん", "Nadesiko")

# 記事IDを格納するハッシュテーブルを初期化
$articleIds = @()
# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 
# 各タグについてループして記事を集計
foreach ($tag_name in $tag_names) {
    $page_articles = @()
    # ページネーション設定 
    $page = 1
    $per_page = 100
    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
        foreach ($article in $res) 
        { 
        	if (-not $articleIds.Contains($article.id)) { # 重複する記事IDは含めない
            $articleIds += $article.id 
            $page_articles += $article
            } 
        }

	    foreach ($article in $page_articles) {
	        $year = (Get-Date $article.created_at).Year

	        if (-not $yearlyStats.ContainsKey($year)) {
	            $yearlyStats[$year]  = @{
	                ArticleCount = 0
	                TotalLikes   = 0
	            }
	        }

	        $yearlyStats[$year].ArticleCount++
	        $yearlyStats[$year].TotalLikes += $article.likes_count
	    }
        
        $page++
    } while ($res.Count -eq $per_page)
}
# 年度別の集計結果を表示
foreach ($year in $yearlyStats.Keys | Sort-Object -Descending) {
    $stats = $yearlyStats[$year]
    Write-Output "年度: $year 記事数: $($stats.ArticleCount) 合計いいね数: $($stats.TotalLikes)"
}

```

### 実行結果
結果は現状有姿の参考情報です。QiitaAPIが返す記事数とQiitaWebサイトのタグページの記事数は値が異なる場合があるようです。

```powershell:
年度: 2025 記事数: 209 合計いいね数: 351
年度: 2024 記事数: 241 合計いいね数: 464
年度: 2023 記事数: 205 合計いいね数: 1055
年度: 2022 記事数: 87 合計いいね数: 364
年度: 2021 記事数: 72 合計いいね数: 203
年度: 2020 記事数: 101 合計いいね数: 348
年度: 2019 記事数: 10 合計いいね数: 60
年度: 2018 記事数: 10 合計いいね数: 34
年度: 2017 記事数: 8 合計いいね数: 14
年度: 2016 記事数: 7 合計いいね数: 71
年度: 2015 記事数: 3 合計いいね数: 12
年度: 2014 記事数: 1 合計いいね数: 0
年度: 2011 記事数: 1 合計いいね数: 1
```

## 複数タグの記事取得（ページネーション指定してループ　ループ内集計　タグ別複数キー集計　）

つぎにこれもおさらいとして集計対象の複数タグを年度別集計します。このタグの間では重複記事IDもそれぞれのタグに集計カウントします。
タグは日本語プログラミング言語MindとRe:Mindです。

### コマンド文
```powershell:
# 集計したいタグのリストを作成
$tag_names = @("mind","re_mind")

# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 

foreach ($tag_name in $tag_names) {
    $page_articles = @()
    $page = 1
    $per_page = 100

    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get

        foreach ($article in $res) {
            $page_articles += $article
        }

        $page++
    } while ($res.Count -eq $per_page)

    foreach ($article in $page_articles) {
        $year = (Get-Date $article.created_at).Year

        if (-not $yearlyStats.ContainsKey($tag_name)) {
            $yearlyStats[$tag_name] = @{}
        }

        if (-not $yearlyStats[$tag_name].ContainsKey($year)) {
            $yearlyStats[$tag_name][$year] = @{
                ArticleCount = 0
                TotalLikes   = 0
            }
        }

        $yearlyStats[$tag_name][$year].ArticleCount++
        $yearlyStats[$tag_name][$year].TotalLikes += $article.likes_count
    }
}

# 年度別の集計結果を表示
foreach ($tag_name in $yearlyStats.Keys | Sort-Object) {
    Write-Output "タグ: $tag_name"
    $stats = $yearlyStats[$tag_name]

    $sortedStats = $stats.GetEnumerator() | Sort-Object -Property key -Descending

    foreach ($entry in $sortedStats) {
        $year = $entry.Key
        $yearStats = $entry.Value
        Write-Output "年度: $year 記事数: $($yearStats.ArticleCount) 合計いいね数: $($yearStats.TotalLikes)"
    }
}
```

### 実行結果
```powershell:
タグ: mind
年度: 2025 記事数: 147 合計いいね数: 471
年度: 2024 記事数: 179 合計いいね数: 456
年度: 2023 記事数: 87 合計いいね数: 658
年度: 2020 記事数: 32 合計いいね数: 9
年度: 2019 記事数: 5 合計いいね数: 15
年度: 2018 記事数: 3 合計いいね数: 6
年度: 2017 記事数: 16 合計いいね数: 75
タグ: re_mind
年度: 2025 記事数: 38 合計いいね数: 116
年度: 2024 記事数: 6 合計いいね数: 18
年度: 2023 記事数: 17 合計いいね数: 49
```

## 複数タグと単一タグの各年度別集計
おさらいの前記２集計を合体します。なでしこパターンをMindパターンの中に組み入れて集計変数を共有させます。Mindパターンのタグリストの先頭に代表タグ名"なでしこ"も追加して、タグ名が"なでしこ"だったらで処理を分岐させ、入れ子のタグループなでしこパターンで集計します。

### コマンド文
```powershell:
# 集計したいタグのリストを作成
$tag_names = @("なでしこ","mind","re_mind")
# なでしこの場合に集計したいタグのリストを作成
$tag_names2 = @("なでしこ", "なでしこ3", "なでしこさん", "Nadesiko")
# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 

foreach ($tag_name in $tag_names) {

	if ($tag_name -eq "なでしこ") { # なでしこファミリー


   		# 記事IDを格納するハッシュテーブルを初期化
		$articleIds = @()

   	    if (-not $yearlyStats.ContainsKey($tag_name)) {
            $yearlyStats[$tag_name] = @{}
        }

		# 各タグについてループして記事を集計
		foreach ($tag_name2 in $tag_names2) {
		
		    $page_articles = @()
		    $page = 1
		    $per_page = 100
		    
		    do {
		        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name2/items?page=$page&per_page=$per_page"
		        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
		        foreach ($article in $res) 
		        { 
		        	if (-not $articleIds.Contains($article.id)) { # 重複する記事IDは含めない
		            $articleIds += $article.id 
		            $page_articles += $article
		            } 
		        }

			    foreach ($article in $page_articles) {
			        $year = (Get-Date $article.created_at).Year

			        if (-not $yearlyStats[$tag_name].ContainsKey($year)) {
			            $yearlyStats[$tag_name][$year] = @{
			                ArticleCount = 0
			                TotalLikes   = 0
			            }
			        }

			        $yearlyStats[$tag_name][$year].ArticleCount++
			        $yearlyStats[$tag_name][$year].TotalLikes += $article.likes_count
			    }
		        
		        $page++
		    } while ($res.Count -eq $per_page)
		}   
    
   }else{
   
   	    $page_articles = @()
	    $page = 1
	    $per_page = 100
	    
	    do {
	        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
	        $res = Invoke-RestMethod -Uri $apiUrl -Method Get

	        foreach ($article in $res) {
	            $page_articles += $article
	        }

	        $page++
	    } while ($res.Count -eq $per_page)

	    foreach ($article in $page_articles) {
	        $year = (Get-Date $article.created_at).Year

	        if (-not $yearlyStats.ContainsKey($tag_name)) {
	            $yearlyStats[$tag_name] = @{}
	        }

	        if (-not $yearlyStats[$tag_name].ContainsKey($year)) {
	            $yearlyStats[$tag_name][$year] = @{
	                ArticleCount = 0
	                TotalLikes   = 0
	            }
	        }

	        $yearlyStats[$tag_name][$year].ArticleCount++
	        $yearlyStats[$tag_name][$year].TotalLikes += $article.likes_count
	    }
   
   }
    
}

# 年度別の集計結果を表示
foreach ($tag_name in $yearlyStats.Keys | Sort-Object) {
    Write-Output "タグ: $tag_name"
    $stats = $yearlyStats[$tag_name]

    $sortedStats = $stats.GetEnumerator() | Sort-Object -Property {$_.Key}  -Descending

    foreach ($entry in $sortedStats) {
        $year = $entry.Key
        $yearStats = $entry.Value
        Write-Output "年度: $year 記事数: $($yearStats.ArticleCount) 合計いいね数: $($yearStats.TotalLikes)"
    }
}
```

### 実行結果
```powershell:
タグ: mind
年度: 2025 記事数: 147 合計いいね数: 472
年度: 2024 記事数: 179 合計いいね数: 456
年度: 2023 記事数: 87 合計いいね数: 658
年度: 2020 記事数: 32 合計いいね数: 9
年度: 2019 記事数: 5 合計いいね数: 15
年度: 2018 記事数: 3 合計いいね数: 6
年度: 2017 記事数: 16 合計いいね数: 75
タグ: re_mind
年度: 2025 記事数: 38 合計いいね数: 116
年度: 2024 記事数: 6 合計いいね数: 18
年度: 2023 記事数: 17 合計いいね数: 49
タグ: なでしこ
年度: 2025 記事数: 209 合計いいね数: 351
年度: 2024 記事数: 241 合計いいね数: 464
年度: 2023 記事数: 205 合計いいね数: 1055
年度: 2022 記事数: 87 合計いいね数: 364
年度: 2021 記事数: 72 合計いいね数: 203
年度: 2020 記事数: 101 合計いいね数: 348
年度: 2019 記事数: 10 合計いいね数: 60
年度: 2018 記事数: 10 合計いいね数: 34
年度: 2017 記事数: 8 合計いいね数: 14
年度: 2016 記事数: 7 合計いいね数: 71
年度: 2015 記事数: 3 合計いいね数: 12
年度: 2014 記事数: 1 合計いいね数: 0
年度: 2011 記事数: 1 合計いいね数: 1
```

# おわりに
いかがでしたか？集計結果はなまのテキストでわかりにくくてすみません。結果はあくまで参考値ということでお願いします。なにかの参考になれば幸いです。

以下はほぼ自分用の備忘録ですが、PowerShellでQiitaAPI入門の過去記事リストです。
[PowerShellでQiitaAPI入門（ステップ１０ 記事タイトルとURLを並べ替えてQiita記事用に整形）](
https://qiita.com/mylifewithviolin/items/4242b0caa3cfde772991)
[PowerShellでQiitaAPI入門（ステップ９ 記事タイトルの特定ワードのいいね数とView数を集計し並べ替え）](
https://qiita.com/mylifewithviolin/items/cdf896c9a88ccc8ab5f3)
[PowerShellでQiitaAPI入門（ステップ８ 記事タイトルの特定ワードのいいね数とView数を集計）](
https://qiita.com/mylifewithviolin/items/9ee09fb43b7517ec55a9)
[PowerShellでQiitaAPI入門（ステップ７複数タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/e704fdfdbc151eda4c62)
[PowerShellでQiitaAPI入門（ステップ６複数タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/1d75a3cf5cd65a01b5f0)
[PowerShellでQiitaAPI入門（ステップ５指定タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/8a73f565625c09c69d41)
[PowerShellでQiitaAPI入門（ステップ４ 指定タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/83a0d74f7586950cfa65)
[PowerShellでQiitaAPI入門（ステップ３ 指定タグ全記事取得後の集計）](https://qiita.com/mylifewithviolin/items/6e9bfaa64477daa7b1ab)
[PowerShellでQiitaAPI入門（ステップ２ 指定タグ全記事取得）](https://qiita.com/mylifewithviolin/items/fd7a4ef9de1fa9809b15)
[PowerShellでQiitaAPI入門（ステップ１ 単純記事取得）](https://qiita.com/mylifewithviolin/items/7f38beacb069ade3db8e)
