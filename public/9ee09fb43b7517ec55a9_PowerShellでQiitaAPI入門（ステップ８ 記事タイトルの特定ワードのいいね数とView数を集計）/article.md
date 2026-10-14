# はじめに
PowerShellでQiitaAPI入門のステップ８です。今回は特定タグを指定して記事タイトルから特定ワードを条件に記事タイトル、投稿日、いいね数、View数をリスト化して集計してみます。

具体的にはmindタグの件名「日本語プログラミング言語Mindの小技」に対して行ってみます。


# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ８）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 特定タグの特定件名の記事取得（ページネーション指定してループ　ループ内集計　件名の特定ワードでフィルター　一覧出力）

View数は認証トークンを設定して、自分が投稿した記事のみ取得できます。

### コマンド文
```powershell:
$tagId= "mind"
$token = "*****************************"
$headers = @{
    Authorization = "Bearer $token"
}
$keyword = "日本語プログラミング言語Mindの小技"
$page = 1
$perPage = 20
$totalLikes = 0
$totalViews = 0
do {
    $url = "https://qiita.com/api/v2/tags/$tagId/items?page=$page&per_page=$perPage"
    $response = Invoke-RestMethod -Uri $url -Headers $headers

    foreach ($item in $response) {
        if ($item.title -like "*$keyword*") {
            $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
            Write-Output "$formattedDate $($item.title) $($item.likes_count) $($item.page_views_count)  $($item.user.id)"
            $totalLikes += $item.likes_count
            $totalViews += $item.page_views_count
        }
    }

    $page++
} while ($response.Count -eq $perPage)

Write-Output "`n========= 集計結果の表示 ========="
Write-Output "Total Likes: $totalLikes"
Write-Output "Total Views: $totalViews"

```


### 実行結果
念のため初期設定から実行しています。

```powershell:
PS C:\developments\vscode\mind9> $tagId= "mind"
PS C:\developments\vscode\mind9> $token = "********************"
PS C:\developments\vscode\mind9> $headers = @{
>>     Authorization = "Bearer $token"
>> }
PS C:\developments\vscode\mind9> $keyword = "日本語プログラミング言語Mindの小技"
PS C:\developments\vscode\mind9> $page = 1
PS C:\developments\vscode\mind9> $perPage = 20
PS C:\developments\vscode\mind9> $totalLikes = 0
PS C:\developments\vscode\mind9> $totalViews = 0
PS C:\developments\vscode\mind9> do {
>>     $url = "https://qiita.com/api/v2/tags/$tagId/items?page=$page&per_page=$perPage"
>>     $response = Invoke-RestMethod -Uri $url -Headers $headers
>>
>>     foreach ($item in $response) {
>>         if ($item.title -like "*$keyword*") {
>>             $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
>>
>>             Write-Output "$formattedDate $($item.title) $($item.likes_count) $($item.page_views_count)  $($item.user.id)"
>>             $totalLikes += $item.likes_count
>>             $totalViews += $item.page_views_count
>>         }
>>     }
>>
>>     $page++
>> } while ($response.Count -eq $perPage)
2025/07/05 日本語プログラミング言語Mindの小技 「送り仮名」～形式言語としての日本語２～ 2 61  mylifewithviolin
2025/06/28 日本語プログラミング言語Mindの小技 「数値定数を単語定義」～数値定数を表す単語～ 2 84  mylifewithviolin
2025/06/21 日本語プログラミング言語Mindの小技 「空白？」～文字コードを調べる単語～ 2 123  mylifewithviolin
2025/06/14 日本語プログラミング言語Mindの小技 「単語を切り出す」～元文字列も切り出された状態になる～ 2 137  mylifewithviolin
2025/06/07 日本語プログラミング言語Mindの小技 「処理単語の属性指定」～スタック上の変数の数や型チェック～ 4 1920  mylifewithviolin
2025/05/31 日本語プログラミング言語Mindの小技 「処理単語」～複数の戻り値をスタックに置ける～ 5 1497  mylifewithviolin
2025/05/28 日本語プログラミング言語Mindの小技 「小数」～構造体の多次元配列内の小数変数～ 3 158  mylifewithviolin
2025/05/24 日本語プログラミング言語Mindの小技 「二番目を捨てる」～スタックツートップのNo.1を生かしてNo.2を捨てる～ 3 1035  mylifewithviolin
2025/05/17 日本語プログラミング言語Mindの小技 「多次元配列」～構造体の多次元配列～ 4 662  mylifewithviolin
2025/05/10 日本語プログラミング言語Mindの小技 「複写」～スタックトップの値を２つにする～ 3 796  mylifewithviolin
2025/05/03 日本語プログラミング言語Mindの小技 「分ち書き」～形式言語としての日本語～ 3 794  mylifewithviolin
2025/04/26 日本語プログラミング言語Mindの小技 「回数指定」～指定回数くりかえすループ～ 3 820  mylifewithviolin
2025/04/20 日本語プログラミング言語Mindの小技 「関数」～戻り値を複数返せる～ 6 7663  mylifewithviolin
2025/04/12 日本語プログラミング言語Mindの小技 「選択」～処理も選択できる～ 5 2026  mylifewithviolin
2025/04/05 日本語プログラミング言語Mindの小技 「もう一度」～ループの先頭からもう一度やりなおす～ 4 3072  mylifewithviolin
2025/03/30 日本語プログラミング言語Mindの小技 「逆転介入」～計算式日本語表現の語順への逆転介入～ 3 545  mylifewithviolin
2025/03/24 日本語プログラミング言語Mindの小技 「空白を満たす」～文字列に右寄せで空白を満たす？～ 3 273  mylifewithviolin
2025/03/20 日本語プログラミング言語Mindの小技 「リカーシブコール」たらい回し関数 3   ITvision
2025/03/20 日本語プログラミング言語Mindの小技 「つぎに」～条件分岐の終端～ 5 4061  mylifewithviolin
2025/03/15 日本語プログラミング言語Mindの小技 「型紙」～構造体～ 3 549  mylifewithviolin
2025/03/11 日本語プログラミング言語Mindの小技 「局所処理単語」～クロージャっぽい～ 5 3576  mylifewithviolin
2025/03/09 日本語プログラミング言語Mindの小技 「等価」 6 6469  mylifewithviolin
PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> Write-Output "`n========= 集計結果の表示 ========="

========= 集計結果の表示 =========
PS C:\developments\vscode\mind9> Write-Output "Total Likes: $totalLikes"
Total Likes: 79
PS C:\developments\vscode\mind9> Write-Output "Total Views: $totalViews"
Total Views: 36321
PS C:\developments\vscode\mind9>
```

## 自分タグの特定件名の記事取得（ページネーション指定してループ　件名の特定ワードでフィルター　自動整形出力）

View数は認証トークンを設定して、自分が投稿した記事のみ取得できます。
今回は出力書式をPowershellの自動整形にまかせます。

### コマンド文
```powershell:
$qiitaId = "mylifewithviolin"
$token = "*****************************"
$headers = @{
    Authorization = "Bearer $token"
}
$keyword = "日本語プログラミング言語Mindの小技"

# 結果保存用配列
$filteredArticles = @()
$page = 1
$perPage = 20

do {
    $url = "https://qiita.com/api/v2/users/$qiitaId/items?page=$page&per_page=$perPage"
    $response = Invoke-RestMethod -Uri $url -Headers $headers

    foreach ($item in $response) {
        if ($item.title -like "*$keyword*") {
            $filteredArticles += [PSCustomObject]@{
                Title = $item.title
                Author    = $item.user.id
                PostedAt  = $item.created_at
                Likes = $item.likes_count
        		Views = $item.page_views_count
            }
        }
    }

    $page++
} while ($response.Count -eq $perPage) 

# 結果を表示
$filteredArticles
```


### 実行結果


```powershell:
Title    : 日本語プログラミング言語Mindの小技 「送り仮名」～形式言語としての日本語２～
Author   : mylifewithviolin
PostedAt : 2025-07-05T11:42:02+09:00
Likes    : 2
Views    : 61

Title    : 日本語プログラミング言語Mindの小技 「数値定数を単語定義」～数値定数を表す単語～
Author   : mylifewithviolin
PostedAt : 2025-06-28T10:49:21+09:00
Likes    : 2
Views    : 84

Title    : 日本語プログラミング言語Mindの小技 「空白？」～文字コードを調べる単語～
Author   : mylifewithviolin
PostedAt : 2025-06-21T13:00:22+09:00
Likes    : 2
Views    : 123

Title    : 日本語プログラミング言語Mindの小技 「単語を切り出す」～元文字列も切り出された状態になる～
Author   : mylifewithviolin
PostedAt : 2025-06-14T10:36:44+09:00
Likes    : 2
Views    : 137

Title    : 日本語プログラミング言語Mindの小技 「処理単語の属性指定」～スタック上の変数の数や型チェック～
Author   : mylifewithviolin
PostedAt : 2025-06-07T10:34:07+09:00
Likes    : 4
Views    : 1920

Title    : 日本語プログラミング言語Mindの小技 「処理単語」～複数の戻り値をスタックに置ける～
Author   : mylifewithviolin
PostedAt : 2025-05-31T13:33:58+09:00
Likes    : 5
Views    : 1497

Title    : 日本語プログラミング言語Mindの小技 「小数」～構造体の多次元配列内の小数変数～
Author   : mylifewithviolin
PostedAt : 2025-05-28T22:32:23+09:00
Likes    : 3
Views    : 158

Title    : 日本語プログラミング言語Mindの小技 「二番目を捨てる」～スタックツートップのNo.1を生かしてNo.2を捨てる～
Author   : mylifewithviolin
PostedAt : 2025-05-24T18:18:52+09:00
Likes    : 3
Views    : 1035

Title    : 日本語プログラミング言語Mindの小技 「多次元配列」～構造体の多次元配列～
Author   : mylifewithviolin
PostedAt : 2025-05-17T13:24:00+09:00
Likes    : 4
Views    : 662

Title    : 日本語プログラミング言語Mindの小技 「複写」～スタックトップの値を２つにする～
Author   : mylifewithviolin
PostedAt : 2025-05-10T09:36:58+09:00
Likes    : 3
Views    : 796

Title    : 日本語プログラミング言語Mindの小技 「分ち書き」～形式言語としての日本語～
Author   : mylifewithviolin
PostedAt : 2025-05-03T12:11:00+09:00
Likes    : 3
Views    : 794

Title    : 日本語プログラミング言語Mindの小技 「回数指定」～指定回数くりかえすループ～
Author   : mylifewithviolin
PostedAt : 2025-04-26T15:33:12+09:00
Likes    : 3
Views    : 820

Title    : 日本語プログラミング言語Mindの小技 「関数」～戻り値を複数返せる～
Author   : mylifewithviolin
PostedAt : 2025-04-20T00:51:21+09:00
Likes    : 6
Views    : 7663

Title    : 日本語プログラミング言語Mindの小技 「選択」～処理も選択できる～
Author   : mylifewithviolin
PostedAt : 2025-04-12T09:30:29+09:00
Likes    : 5
Views    : 2026

Title    : 日本語プログラミング言語Mindの小技 「もう一度」～ループの先頭からもう一度やりなおす～
Author   : mylifewithviolin
PostedAt : 2025-04-05T22:46:52+09:00
Likes    : 4
Views    : 3072

Title    : 日本語プログラミング言語Mindの小技 「逆転介入」～計算式日本語表現の語順への逆転介入～
Author   : mylifewithviolin
PostedAt : 2025-03-30T19:57:38+09:00
Likes    : 3
Views    : 545

Title    : 日本語プログラミング言語Mindの小技 「空白を満たす」～文字列に右寄せで空白を満たす？～
Author   : mylifewithviolin
PostedAt : 2025-03-24T00:05:45+09:00
Likes    : 3
Views    : 273

Title    : 日本語プログラミング言語Mindの小技 「つぎに」～条件分岐の終端～
Author   : mylifewithviolin
PostedAt : 2025-03-20T00:37:50+09:00
Likes    : 5
Views    : 4061

Title    : 日本語プログラミング言語Mindの小技 「型紙」～構造体～
Author   : mylifewithviolin
PostedAt : 2025-03-15T22:00:09+09:00
Likes    : 3
Views    : 549

Title    : 日本語プログラミング言語Mindの小技 「局所処理単語」～クロージャっぽい～
Author   : mylifewithviolin
PostedAt : 2025-03-11T22:33:25+09:00
Likes    : 5
Views    : 3576

Title    : 日本語プログラミング言語Mindの小技 「等価」
Author   : mylifewithviolin
PostedAt : 2025-03-09T13:42:08+09:00
Likes    : 6
Views    : 6469
```



# おわりに
いかがでしたか？結果はなまのテキストでわかりにくくてすみません。なにかの参考になれば幸いです。

以下はほぼ自分用の備忘録ですが、PowerShellでQiitaAPI入門の過去記事リストです。
[PowerShellでQiitaAPI入門（ステップ７複数タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/e704fdfdbc151eda4c62)
[PowerShellでQiitaAPI入門（ステップ６複数タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/1d75a3cf5cd65a01b5f0)
[PowerShellでQiitaAPI入門（ステップ５指定タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/8a73f565625c09c69d41)
[PowerShellでQiitaAPI入門（ステップ４ 指定タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/83a0d74f7586950cfa65)
[PowerShellでQiitaAPI入門（ステップ３ 指定タグ全記事取得後の集計）](https://qiita.com/mylifewithviolin/items/6e9bfaa64477daa7b1ab)
[PowerShellでQiitaAPI入門（ステップ２ 指定タグ全記事取得）](https://qiita.com/mylifewithviolin/items/fd7a4ef9de1fa9809b15)
[PowerShellでQiitaAPI入門（ステップ１ 単純記事取得）](https://qiita.com/mylifewithviolin/items/7f38beacb069ade3db8e)



## 記事シリーズのご紹介
記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできますよ。


面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
