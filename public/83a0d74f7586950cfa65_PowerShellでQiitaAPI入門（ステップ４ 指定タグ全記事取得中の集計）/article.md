# はじめに
PowerShellでQiitaAPI入門のステップ４です。今回は指定タグの全記事取得中の集計です。ステップ３ではいったん全記事をためこんでから集計しましたが、件数が甚大のタグの場合はメモリ不足に陥る可能性がありますので、バッファリングしながら集計するロジックに調整します。公式解説は基本的な使用例の説明はないので、基本的な事柄についてわかりづらく手が出せにくかった方を対象にしつつ自分用のメモを兼ねます。

https://qiita.com/api/v2/docs


# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ４）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1

## 指定タグの記事取得（ページネーション指定してループ　重複ID除外＋集計）

全件の記事をためこまず、ページネーション中に集計を行います。

### コマンド文
```powershell:
# 特定のタグ名 
$tag_name = (タグ名)
# ページネーション設定 
$page = (ページ位置初期値)
$per_page = (1ページあたりの記事数)
# 記事ID格納変数
$articleIds = @() 
# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 

# 〇ループ開始
# 1ページあたり記事格納変数初期化
# APIエンドポイントのURL(ページネーションのページ位置変化)
# APIリクエストを送信 
# 　〇レスポンスのアイテムでループ開始
# 　◇記事ID格納変数にレスポンスアイテムの記事IDが含まれない場合 
# 　　　レスポンスアイテムを1ページあたり記事格納変数に追加
# 　　　レスポンスアイテムの記事IDを記事ID格納変数に追加
# 　〇レスポンスのアイテムでループ終端
# 　〇1ページあたり記事格納変数でループ開始
# 　　記事の年を年変数にセット
# 　　◇年度別の集計用ハッシュテーブルのキーに年変数が存在しない場合
# 　　　　年変数のハッシュテーブルを初期化
# 　　各記事の投稿年の記事数といいね数を集計 
# 　〇1ページあたり記事格納変数でループ終端
# 次のページへ (ページネーションのページ位置カウントアップ)
# 〇ループ終端◇最後のページに到達したかを確認 

do { 
$apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page" 
$res = Invoke-RestMethod -Uri $apiUrl -Method Get 
foreach ($article in $res) 
{ if (-not $articleIds.Contains($article.id)) { 
    $all_articles += $article 
    $articleIds += $article.id } 
}
foreach ($article in $page_articles) 
{ $year = (Get-Date $article.created_at).Year 
	if (-not $yearlyStats.ContainsKey($year)) 
	{ 
		$yearlyStats[$year] = @{ 
		ArticleCount = 0 
		TotalLikes = 0 } 
	} 
	$yearlyStats[$year].ArticleCount++ 
	$yearlyStats[$year].TotalLikes += $article.likes_count
}
$page++ 
} while($res.Count -eq $per_page)

# 年度別の集計結果を表示 
foreach ($year in $yearlyStats.Keys | Sort-Object) 
{ 
    $stats = $yearlyStats[$year] 
    Write-Output "年度: $year" 
    Write-Output " 記事数: $($stats.ArticleCount)" 
    Write-Output " 合計いいね数: $($stats.TotalLikes)"
}
```

### 実行結果
念のため初期設定から再実行しています。

```powershell:
PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $yearlyStats = @{}
PS C:\pmind> $articleIds = @()
PS C:\pmind>
PS C:\pmind> do {
>> $page_articles = @()
>> $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>> $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>> foreach ($article in $res)
>> { if (-not $articleIds.Contains($article.id)) {
>> $page_articles += $article
>> $articleIds += $article.id }
>> }
>> foreach ($article in $page_articles)
>> { $year = (Get-Date $article.created_at).Year
>> if (-not $yearlyStats.ContainsKey($year))
>> {
>> $yearlyStats[$year] = @{
>> ArticleCount = 0
>> TotalLikes = 0 }
>> }
>> $yearlyStats[$year].ArticleCount++
>> $yearlyStats[$year].TotalLikes += $article.likes_count
>> }
>> $page++ #
>> } while ($res.Count -eq $per_page)
PS C:\pmind>
PS C:\pmind> foreach ($year in $yearlyStats.Keys | Sort-Object)
>> {
>> $stats = $yearlyStats[$year]
>> Write-Output "年度: $year"
>> Write-Output " 記事数: $($stats.ArticleCount)"
>> Write-Output " 合計いいね数: $($stats.TotalLikes)"
>> }
年度: 2017
 記事数: 16
 合計いいね数: 74
年度: 2018
 記事数: 3
 合計いいね数: 6
年度: 2019
 記事数: 5
 合計いいね数: 15
年度: 2020
 記事数: 32
 合計いいね数: 8
年度: 2023
 記事数: 88
 合計いいね数: 650
年度: 2024
 記事数: 155
 合計いいね数: 358
```
重複IDの除去処理は現状むだっぽいですが、複数タグにまたがって集計する場合は効果を発揮します。

# おわりに
いかがでしたか？なにかの参考になれば幸いです。
