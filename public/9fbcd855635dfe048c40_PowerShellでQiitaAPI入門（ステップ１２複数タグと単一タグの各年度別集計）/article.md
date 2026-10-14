# はじめに
PowerShellでQiitaAPI入門のステップ１１で日本語プログラミング言語なでしことMindとRe:Mindについて記事数といいね数の年次集計を行ったので、この数字の中で自分がどの程度貢献しているのかを知ってみたくなりました。ということで、なでしこ関連タグ４つの間で重複する記事IDは一つとカウントし、MindとRe:Mindとなでしこ関連タグの間で重複する記事IDはそれぞれのタグにカウントするの自分ID限定バージョンを実行してみます。

# 前提条件
Windows11 Pro 22H2 22621.4317
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ１２）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 複数タグと単一タグのグループ化記事取得（ページネーション指定してループ　ループ内集計　タグまたぎ記事重複ID除外＋複数キー集計　自己ID限定）


### コマンド文
```powershell:
# Qiita IDとアクセストークン
$qiitaId = "mylifewithviolin"
$token = "*****************************"
$headers = @{
    Authorization = "Bearer $token"
}
# 集計したいタグのリストを作成
$tag_names = @("なでしこ","mind","re_mind")
# なでしこの場合に集計したいタグのリストを作成
$tag_names2 = @("なでしこ", "なでしこ3", "なでしこさん", "Nadesiko")
# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 

foreach ($tag_name in $tag_names) {
    Write-Output "集計中: $tag_name"
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
		        $res = Invoke-RestMethod -Uri $apiUrl -Method Get  -Headers $headers
		        foreach ($article in $res) 
		        { 
			        if ($article.user.id -eq $qiitaId) { # 指定ユーザーID以外は除外
			        	if (-not $articleIds.Contains($article.id)) { # 重複する記事IDは含めない
			            $articleIds += $article.id 
			            $page_articles += $article
			            } 
		            }
		        }

			    foreach ($article in $page_articles) {
			        $year = (Get-Date $article.created_at).Year

			        if (-not $yearlyStats[$tag_name].ContainsKey($year)) {
			            $yearlyStats[$tag_name][$year] = @{
			                ArticleCount = 0
			                TotalLikes   = 0
			                TotalViews   = 0
			            }
			        }

			        $yearlyStats[$tag_name][$year].ArticleCount++
			        $yearlyStats[$tag_name][$year].TotalLikes += $article.likes_count
			        $yearlyStats[$tag_name][$year].TotalViews += $article.page_views_count
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
	        $res = Invoke-RestMethod -Uri $apiUrl -Method Get  -Headers $headers

	        foreach ($article in $res) {
		        if ($article.user.id -eq $qiitaId) { # 指定ユーザーID以外は除外
		            $page_articles += $article
		        }
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
	                TotalViews   = 0
	            }
	        }

	        $yearlyStats[$tag_name][$year].ArticleCount++
	        $yearlyStats[$tag_name][$year].TotalLikes += $article.likes_count
			$yearlyStats[$tag_name][$year].TotalViews += $article.page_views_count
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
        Write-Output "年度: $year 記事数: $($yearStats.ArticleCount) 合計いいね数: $($yearStats.TotalLikes) 合計View数: $($yearStats.TotalViews)"
    }
}
```

### 実行結果
結果は現状有姿の参考情報です。

```powershell:
タグ: mind
年度: 2025 記事数: 131 合計いいね数: 426 合計View数: 199758
年度: 2024 記事数: 101 合計いいね数: 272 合計View数: 135369
年度: 2023 記事数: 42 合計いいね数: 318 合計View数: 194214
タグ: re_mind
年度: 2025 記事数: 39 合計いいね数: 116 合計View数: 38831
年度: 2024 記事数: 6 合計いいね数: 18 合計View数: 4892
年度: 2023 記事数: 17 合計いいね数: 49 合計View数: 40849
タグ: なでしこ
年度: 2025 記事数: 36 合計いいね数: 80 合計View数: 21624
年度: 2024 記事数: 45 合計いいね数: 166 合計View数: 52420
年度: 2023 記事数: 78 合計いいね数: 875 合計View数: 484315
```

# おわりに
いかがでしたか？集計結果はなまのテキストでわかりにくくてすみません。結果はあくまで参考値ということでお願いします。なにかの参考になれば幸いです。


以下はほぼ自分用の備忘録ですが、PowerShellでQiitaAPI入門の過去記事リストです。
[ステップ１１複数タグと単一タグの各年度別集計](
https://qiita.com/mylifewithviolin/items/16bc52687e715126bea3)
[ステップ１０ 記事タイトルとURLを並べ替えてQiita記事用に整形](
https://qiita.com/mylifewithviolin/items/4242b0caa3cfde772991)
[ステップ９ 記事タイトルの特定ワードのいいね数とView数を集計し並べ替え](
https://qiita.com/mylifewithviolin/items/cdf896c9a88ccc8ab5f3)
[ステップ８ 記事タイトルの特定ワードのいいね数とView数を集計](
https://qiita.com/mylifewithviolin/items/9ee09fb43b7517ec55a9)
[ステップ７複数タグ全記事取得中の複数キー集計](https://qiita.com/mylifewithviolin/items/e704fdfdbc151eda4c62)
[ステップ６複数タグ全記事取得中の集計](https://qiita.com/mylifewithviolin/items/1d75a3cf5cd65a01b5f0)
[ステップ５指定タグ全記事取得中の複数キー集計](https://qiita.com/mylifewithviolin/items/8a73f565625c09c69d41)
[ステップ４ 指定タグ全記事取得中の集計](https://qiita.com/mylifewithviolin/items/83a0d74f7586950cfa65)
[ステップ３ 指定タグ全記事取得後の集計](https://qiita.com/mylifewithviolin/items/6e9bfaa64477daa7b1ab)
[ステップ２ 指定タグ全記事取得](https://qiita.com/mylifewithviolin/items/fd7a4ef9de1fa9809b15)
[ステップ１ 単純記事取得](https://qiita.com/mylifewithviolin/items/7f38beacb069ade3db8e)
