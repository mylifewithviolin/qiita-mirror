# はじめに
PowerShellでQiitaAPI入門のステップ５です。今回は指定タグの全記事取得中の集計その２として複数キーによる集計を行います。具体的には年度別ユーザー別のような集計です。

# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ５）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。
## 指定タグの記事取得（ページネーション指定してループ　重複ID除外＋複数キー集計）

ステップ４を継承して全件の記事をためこまず、ページネーション実行中に集計を行います。その際にキー集計を入れ子にします。
具体的にはユーザ別の記事数といいね数を年度別に集計してみます。そのためには、ハッシュテーブルの構造を年度別にユーザ別データを保持するようにします。

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
#
# 　〇1ページあたり記事格納変数でループ開始
# 　　記事の年を年変数にセット
# 　　記事のユーザーIDをユーザーID変数にセット
# 　　◇年度別の集計用ハッシュテーブルのキーに年変数が存在しない場合
# 　　　　年変数のハッシュテーブルを初期化
# 　　◇年度別ユーザーIDの集計用ハッシュテーブル[年変数]のキーにユーザーID変数が存在しない場合
# 　　　　年変数ユーザーIDの集計用ハッシュテーブル[年変数]を初期化
#
# 　　各記事の投稿年ユーザーIDの記事数といいね数を集計 
# 　〇1ページあたり記事格納変数でループ終端
#
# 次のページへ (ページネーションのページ位置カウントアップ)
# 〇ループ終端◇最後のページに到達したかを確認 


# 年度別の集計用ハッシュテーブル
$yearlyStats = @{}

do {
    $page_articles = @()
    $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
    $res = Invoke-RestMethod -Uri $apiUrl -Method Get

    foreach ($article in $res) {
        if (-not $articleIds.Contains($article.id)) {
            $page_articles += $article
            $articleIds += $article.id
        }
    }

    foreach ($article in $page_articles) {
        $year = (Get-Date $article.created_at).Year
        $userId = $article.user.id

        if (-not $yearlyStats.ContainsKey($year)) {
            $yearlyStats[$year] = @{}
        }

        if (-not $yearlyStats[$year].ContainsKey($userId)) {
            $yearlyStats[$year][$userId] = @{
                ArticleCount = 0
                TotalLikes = 0
            }
        }

        $yearlyStats[$year][$userId].ArticleCount++
        $yearlyStats[$year][$userId].TotalLikes += $article.likes_count
    }

    $page++ 
} while ($res.Count -eq $per_page)


# 年度別ユーザー別の集計結果を表示 
foreach ($year in $yearlyStats.Keys | Sort-Object) {
    Write-Output "年度: $year"
    $stats = $yearlyStats[$year]
    
    foreach ($userId in $stats.Keys) {
        $userStats = $stats[$userId]
        Write-Output " ユーザーID: $userId"
        Write-Output "  記事数: $($userStats.ArticleCount)"
        Write-Output "  合計いいね数: $($userStats.TotalLikes)"
    }
}

```

### 実行結果
念のため初期設定から再実行しています。

```powershell:

PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $all_articles = @()
PS C:\pmind> $articleIds = @()
PS C:\pmind> $yearlyStats = @{}
PS C:\pmind> do {
>>     $page_articles = @()
>>     $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>     $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>
>>     foreach ($article in $res) {
>>         if (-not $articleIds.Contains($article.id)) {
>>             $page_articles += $article
>>             $articleIds += $article.id
>>         }
>>     }
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
>>     $page++
>> } while ($res.Count -eq $per_page)
PS C:\pmind> foreach ($year in $yearlyStats.Keys | Sort-Object) {
>>     Write-Output "年度: $year"
>>     $stats = $yearlyStats[$year]
>>
>>     foreach ($userId in $stats.Keys) {
>>         $userStats = $stats[$userId]
>>         Write-Output " ユーザーID: $userId"
>>         Write-Output "  記事数: $($userStats.ArticleCount)"
>>         Write-Output "  合計いいね数: $($userStats.TotalLikes)"
>>     }
>> }
年度: 2017
 ユーザーID: Kosen-amai
  記事数: 1
  合計いいね数: 2
 ユーザーID: MindZanmai
  記事数: 4
  合計いいね数: 8
 ユーザーID: killy
  記事数: 5
  合計いいね数: 35
 ユーザーID: t-tkd3a
  記事数: 6
  合計いいね数: 29
年度: 2018
 ユーザーID: killy
  記事数: 3
  合計いいね数: 6
年度: 2019
 ユーザーID: killy
  記事数: 3
  合計いいね数: 6
 ユーザーID: Snowman-s
  記事数: 2
  合計いいね数: 9
年度: 2020
 ユーザーID: ohisama@github
  記事数: 29
  合計いいね数: 2
 ユーザーID: Snowman-s
  記事数: 2
  合計いいね数: 5
 ユーザーID: Since1967
  記事数: 1
  合計いいね数: 1
年度: 2023
 ユーザーID: mylifewithviolin
  記事数: 43
  合計いいね数: 329
 ユーザーID: ohisama@github
  記事数: 29
  合計いいね数: 44
 ユーザーID: ITvision
  記事数: 5
  合計いいね数: 8
 ユーザーID: killy
  記事数: 6
  合計いいね数: 235
 ユーザーID: MindZanmai
  記事数: 2
  合計いいね数: 4
 ユーザーID: jpl_produire
  記事数: 1
  合計いいね数: 27
 ユーザーID: Mind-Club_2017
  記事数: 2
  合計いいね数: 3
年度: 2024
 ユーザーID: mylifewithviolin
  記事数: 88
  合計いいね数: 218
 ユーザーID: ohisama@github
  記事数: 33
  合計いいね数: 50
 ユーザーID: ITvision
  記事数: 12
  合計いいね数: 26
 ユーザーID: killy
  記事数: 13
  合計いいね数: 43
 ユーザーID: MindZanmai
  記事数: 2
  合計いいね数: 4
 ユーザーID: Chairs
  記事数: 1
  合計いいね数: 0
 ユーザーID: KajizukaTaichi
  記事数: 1
  合計いいね数: 2
 ユーザーID: Mind-Club_2017
  記事数: 6
  合計いいね数: 15
```

## 指定タグの記事取得（ページネーション指定してループ　重複ID除外＋複数キー集計＋並べ替え）

今度は記事数降順で並べ替えを行って集計値を出力してみます。GetEnumerator()メソッドを使ってハッシュテーブルを列挙し、Sort-ObjectでArticleCountプロパティに基づいて降順にソートします。

### コマンド文
```powershell:
# 年度別ユーザー別の集計結果を表示（並べかえて出力） 
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
記事取得中の集計元データはリセットされていませんので、並べ替え集計表示のみ実行しています。

```powershell:
年度: 2017
 ユーザーID: t-tkd3a
  記事数: 6
  合計いいね数: 29
 ユーザーID: killy
  記事数: 5
  合計いいね数: 35
 ユーザーID: MindZanmai
  記事数: 4
  合計いいね数: 8
 ユーザーID: Kosen-amai
  記事数: 1
  合計いいね数: 2
年度: 2018
 ユーザーID: killy
  記事数: 3
  合計いいね数: 6
年度: 2019
 ユーザーID: killy
  記事数: 3
  合計いいね数: 6
 ユーザーID: Snowman-s
  記事数: 2
  合計いいね数: 9
年度: 2020
 ユーザーID: ohisama@github
  記事数: 29
  合計いいね数: 2
 ユーザーID: Snowman-s
  記事数: 2
  合計いいね数: 5
 ユーザーID: Since1967
  記事数: 1
  合計いいね数: 1
年度: 2023
 ユーザーID: mylifewithviolin
  記事数: 43
  合計いいね数: 329
 ユーザーID: ohisama@github
  記事数: 29
  合計いいね数: 44
 ユーザーID: killy
  記事数: 6
  合計いいね数: 235
 ユーザーID: ITvision
  記事数: 5
  合計いいね数: 8
 ユーザーID: Mind-Club_2017
  記事数: 2
  合計いいね数: 3
 ユーザーID: MindZanmai
  記事数: 2
  合計いいね数: 4
 ユーザーID: jpl_produire
  記事数: 1
  合計いいね数: 27
年度: 2024
 ユーザーID: mylifewithviolin
  記事数: 88
  合計いいね数: 218
 ユーザーID: ohisama@github
  記事数: 33
  合計いいね数: 50
 ユーザーID: killy
  記事数: 13
  合計いいね数: 43
 ユーザーID: ITvision
  記事数: 12
  合計いいね数: 26
 ユーザーID: Mind-Club_2017
  記事数: 6
  合計いいね数: 15
 ユーザーID: MindZanmai
  記事数: 2
  合計いいね数: 4
 ユーザーID: Chairs
  記事数: 1
  合計いいね数: 0
 ユーザーID: KajizukaTaichi
  記事数: 1
  合計いいね数: 2
```


# おわりに
いかがでしたか？なにかの参考になれば幸いです。
