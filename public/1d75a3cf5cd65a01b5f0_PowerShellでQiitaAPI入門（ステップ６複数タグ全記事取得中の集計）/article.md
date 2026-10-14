# はじめに
PowerShellでQiitaAPI入門のステップ６です。今回は複数タグを指定して全記事取得中の集計を行います。最初は少しシンプルな単一タグで集計し、その後複数タグで集計します。集計を複数キー、複数項目で行うのは少しスクリプトが複雑になりますので次回とします。今回はなるべくシンプルな状態で動作原理を確認します。

# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ６）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 指定タグの記事取得（ページネーション指定してループ　ループ内集計）

ステップ４を継承して全件の記事をためこまず、ページネーション実行中に集計を行います。集計ロジックはステップ２なみに単純化します。

### コマンド文
```powershell:
# 特定のタグ名 
# ページネーション設定 
# 記事カウンタ初期化
$tag_name = (タグ名)
$page = (ページ位置初期値)
$per_page = (1ページあたりの記事数)
$ArticleCount=0

# 集計ループ
do {
    $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
    $res = Invoke-RestMethod -Uri $apiUrl -Method Get
    $ArticleCount += $res.count
    $page++
} while ($res.Count -eq $per_page)
Write-Output "  記事数: $($ArticleCount)"
```

### 実行結果
念のため初期設定から再実行しています。

```powershell:
PS C:\pmind> $page = 1
PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $all_articles = @()
PS C:\pmind> $ArticleCount=0
PS C:\pmind> do {
>>     $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>     $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>     $ArticleCount += $res.count
>>     $page++
>> } while ($res.Count -eq $per_page)
PS C:\pmind> Write-Output "  記事数: $($ArticleCount)"
  記事数: 300
```

## 複数タグの記事取得（ページネーション指定してループ　ループ内集計　タグまたぎ記事重複あり）

複数タグを指定してページネーション実行中に集計を行います。集計ロジックは全記事の記事数に単純化しています。タグ毎の記事重複はこのロジックでは無視しています。
ページネーションはタグが変わるごとにリセットするため外側ループ内へ移動します。

### コマンド文
```powershell:
# 集計したいタグのリストを作成
# 記事数カウンタ初期化
$tag_names = @((タグ名1), (タグ名2), (タグ名3))
$ArticleCount=0

# 集計ループ
foreach ($tag_name in $tag_names) {
    # ページネーション設定 
    $page = 1
    $per_page = 100
    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
        $ArticleCount += $res.count
        $page++
    } while ($res.Count -eq $per_page)
}
Write-Output "  記事数: $($ArticleCount)"
```

### 実行結果
念のため初期設定から再実行しています。

```powershell:
PS C:\pmind> $tag_names = @("mind", "なでしこ", "プロデル")
PS C:\pmind> $ArticleCount=0
PS C:\pmind>
PS C:\pmind> # 集計ループ
PS C:\pmind> foreach ($tag_name in $tag_names) {
>> # ページネーション設定
>>     $page = 1
>>     $per_page = 100
>>     do {
>>         $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>         $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>         $ArticleCount += $res.count
>>         $page++
>>     } while ($res.Count -eq $per_page)
>> }
PS C:\pmind> Write-Output "  記事数: $($ArticleCount)"
  記事数: 635
```

## 複数タグの記事取得（ページネーション指定してループ　ループ内タグ別集計）

つづいて、複数タグを指定してページネーション実行中に集計を行い、集計ロジックはタグ別の記事数にします。

### コマンド文
```powershell:
# 集計したいタグのリストを作成
# タグ別記事数を格納するハッシュテーブルを初期化
$tag_names = @((タグ名1), (タグ名2), (タグ名3))
$tag_article_counts = @{}

# 集計ループ
foreach ($tag_name in $tag_names) {
    # ページネーション設定 
    # 記事数カウンタ初期化
    $page = 1
    $per_page = 100
    $ArticleCount=0
    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
        $ArticleCount += $res.count
        $page++
    } while ($res.Count -eq $per_page)
    # タグ別記事数ハッシュテーブルに記事数カウンタをセット
    $tag_article_counts[$tag_name] = $ArticleCount
}
# 結果を表示（ForEach-Objectを使用）
$tag_article_counts.GetEnumerator() | ForEach-Object {
    Write-Output "Tag: $($_.Key)"
    Write-Output "Article Count: $($_.Value)"
}
# 結果を表示（Format-Tableを使用）
$tag_article_counts.GetEnumerator() | Format-Table -Property Name, Value -AutoSize
# 結果を表示（Out-Stringを使用）
$tag_article_counts.GetEnumerator() | Out-String
```

### 実行結果
念のため初期設定から再実行しています。

```powershell:
PS C:\pmind> $tag_names = @("mind", "なでしこ", "プロデル")
PS C:\pmind> $tag_article_counts = @{}
PS C:\pmind>
PS C:\pmind> # 集計ループ
PS C:\pmind> foreach ($tag_name in $tag_names) {
>>     # ページネーション設定
>>     # 記事数カウンタ初期化
>>     $page = 1
>>     $per_page = 100
>>     $ArticleCount=0
>>     do {
>>         $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>         $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>         $ArticleCount += $res.count
>>         $page++
>>     } while ($res.Count -eq $per_page)
>>     # タグ別記事数ハッシュテーブルに記事数カウンタをセット
>>     $tag_article_counts[$tag_name] = $ArticleCount
>> }
PS C:\pmind> # 結果を表示（ForEach-Objectを使用）
PS C:\pmind> $tag_article_counts.GetEnumerator() | ForEach-Object {
>>     Write-Output "Tag: $($_.Key)"
>>     Write-Output "Article Count: $($_.Value)"
>> }
Tag: mind
Article Count: 300
Tag: なでしこ
Article Count: 209
Tag: プロデル
Article Count: 126
PS C:\pmind> # 結果を表示（Format-Tableを使用）
PS C:\pmind> $tag_article_counts.GetEnumerator() | Format-Table -Property Name, Value -AutoSize

Name     Value
----     -----
mind       300
なでしこ   209
プロデル   126


PS C:\pmind> # 結果を表示（Out-Stringを使用）
PS C:\pmind> $tag_article_counts.GetEnumerator() | Out-String

Name                           Value
----                           -----
mind                           300
なでしこ                           209

プロデル                           126
```

結果の表示は３パターン行ってみましたが、Out-Stringを使用した場合、空改行が出力されて少しレイアウトがくずれました。

## 複数タグの記事取得（ページネーション指定してループ　ループ内集計　タグまたぎ記事重複のぞく）

複数タグを指定して全記事の記事数を集計する場合、１つの記事には複数のタグを設定できますので、複数のタグが設定された記事をなにもしないと加算集計します。ここではタグ毎の記事重複を除外するロジックを復活させます。（ステップ３で検証）

### コマンド文
```powershell:
# 集計したいタグのリストを作成
# 記事数カウンタ初期化
$tag_names = @((タグ名1), (タグ名2), (タグ名3))
# 記事ID格納変数
$articleIds = @() 

# 集計ループ
foreach ($tag_name in $tag_names) {
    # ページネーション設定 
    $page = 1
    $per_page = 100
    do {
        $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
        $res = Invoke-RestMethod -Uri $apiUrl -Method Get
        foreach ($article in $res) 
        { if (-not $articleIds.Contains($article.id)) { 
            $articleIds += $article.id } 
        }
        $page++
    } while ($res.Count -eq $per_page)
}
Write-Output "  記事数: $($articleIds.Count)"
```

### 実行結果
念のため初期設定から再実行しています。

```powershell:
PS C:\pmind> $tag_names = @("mind", "なでしこ", "プロデル")
PS C:\pmind> $articleIds = @()
PS C:\pmind>
PS C:\pmind> # 集計ループ
PS C:\pmind> foreach ($tag_name in $tag_names) {
>>     # ページネーション設定
>>     $page = 1
>>     $per_page = 100
>>     do {
>>         $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>>         $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>>         foreach ($article in $res)
>>         { if (-not $articleIds.Contains($article.id)) {
>>             $articleIds += $article.id }
>>         }
>>         $page++
>>     } while ($res.Count -eq $per_page)
>> }
PS C:\pmind> Write-Output "  記事数: $($articleIds.Count)"
  記事数: 591
```

記事IDの重複を除いた結果は除かない結果635に対して591となりました。タグが３つ以上となると３つのタグに対して重複する場合がありますので、上記の差が重複記事数とも言えないので、そのあたりの分析は次回にゆずります。

# おわりに
いかがでしたか？なにかの参考になれば幸いです。
