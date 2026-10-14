# はじめに
PowerShellでQiitaAPI入門のステップ３です。今回は指定タグの全記事取得後の重複除外と集計です。（重複除外は取得中）公式解説はチームに関連した機能が詳しく解説されていて、基本的な使用例とかはすっとばされている感じがしたので、このあたりわかりにくくて手が出せにくかった方を対象にしつつ自分用のメモを兼ねます。

https://qiita.com/api/v2/docs


# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ３）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1

## 指定タグの記事取得（ページネーション指定してループ　重複ID除外）

### コマンド文
```powershell:
# 特定のタグ名 
$tag_name = (タグ名)
# ページネーション設定 
$page = (ページ位置初期値)
$per_page = (1ページあたりの記事数)
# 全記事格納変数
$all_articles = @() 
# 記事ID格納変数
$articleIds = @() 

# 〇ループ開始
# APIエンドポイントのURL(ページネーションのページ位置変化)
# APIリクエストを送信 
# 　〇レスポンスのアイテムでループ開始
# 　◇記事ID格納変数にレスポンスアイテムの記事IDが含まれない場合 
# 　　　レスポンスアイテムを全記事格納変数に追加
# 　　　レスポンスアイテムの記事IDを記事ID格納変数に追加
# 　〇レスポンスのアイテムでループ終端
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
$page++ 
} while($res.Count -eq $per_page)
```

### 実行結果
```powershell:
PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $all_articles = @()
PS C:\pmind> $articleIds = @()
PS C:\pmind> do {
>> $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>> $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>> foreach ($article in $res) 
>> { if (-not $articleIds.Contains($article.id)) { 
>> $all_articles += $article 
>> $articleIds += $article.id } 
>> }
>> $page++ 
>> } while ($res.Count -eq $per_page)
PS C:\pmind>
PS C:\pmind> $all_articles.count
299
PS C:\pmind> $articleIds.count
299
```
mindタグのページに公開されている記事数より＋１となっていますが、記事IDの重複はないようです。この差分数からは限定共有記事は無関係と推定していて、この差異１の理由はちょっと不明です。 $articleIdsにすべての記事IDが格納されていますので、これをつかってさらに深堀すればなにか原因がわかるかもしれません。

## 指定タグの記事取得後の集計（投稿日より年度別集計 一括集計版）

以下は前記の前記事取得を実行した後の処理内容です。

### コマンド文
```powershell:
# 年度別の集計用ハッシュテーブル 
$yearlyStats = @{} 
# 〇全記事格納変数でループ開始
# 　記事の年を年変数にセット
# 　◇年度別の集計用ハッシュテーブルのキーに年変数が存在しない場合
# 　　　年変数のハッシュテーブルを初期化
# 　各記事の投稿年の記事数といいね数を集計 
# 〇全記事格納変数でループ終端

foreach ($article in $all_articles) 
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
念のため前記処理内容から再実行しています。

```powershell:
PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $all_articles = @()
PS C:\pmind> $articleIds = @()
PS C:\pmind> do {
>> $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>> $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>> foreach ($article in $res)
>> { if (-not $articleIds.Contains($article.id)) {
>>     $all_articles += $article
>>     $articleIds += $article.id }
>> }
>> $page++
>> } while($res.Count -eq $per_page)
PS C:\pmind> foreach ($article in $all_articles)
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
 合計いいね数: 357
```
この処理ロジックでは、記事数の甚大なタグの場合、いったん全件の記事内容を変数に格納というところでメモリ不足になる場合がありますので、次回はその点改良します。今回実装している重複IDのチェックの入れ子ループのあたりでページネーションしながら集計していく感じになります。

# おわりに
いかがでしたか？参考になれば幸いです。
