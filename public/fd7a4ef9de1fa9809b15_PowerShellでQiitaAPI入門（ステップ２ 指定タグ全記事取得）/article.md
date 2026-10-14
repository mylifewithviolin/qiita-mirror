# はじめに
PowerShellでQiitaAPI入門のステップ２です。今回は指定タグの全記事取得です。既に高度に使いこなされている方にはあたりまえすぎる話ですが、公式解説はチームに関連した機能が詳しく解説されていて、基本的な使用例とかはすっとばされている感じがしたので、このあたりわかりにくくて手が出せにくかった方を対象にしつつ自分用のメモを兼ねます。

https://qiita.com/api/v2/docs

# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ２）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

https://learn.microsoft.com/ja-jp/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-5.1


## 指定タグの基本情報取得
タグの基本情報取得です。

### コマンド文
```powershell:
Invoke-RestMethod "https://qiita.com/api/v2/tags/(タグ名)"
```

### 実行結果

例として筆者がよく投稿しているmindタグに対して実行します。
```powershell:
PS C:\pmind> Invoke-RestMethod "https://qiita.com/api/v2/tags/mind"

followers_count icon_url
--------------- --------
             19 https://s3-ap-northeast-1.amazonaws.com/qiita-tag-image/4d747b01209ee0bbead2d9fc33274fe065fcd38a/med...
```

フォロワー数とイメージのURLが返ります。

## 指定タグの記事取得（ページネーション指定無）
記事取得をデフォルトの件数で取得すると大量の記事テキストが受信されますので、いったん変数に結果を格納するとします。のちにこの変数を使っていろいろ操作します。

### コマンド文
```powershell:
$res = Invoke-RestMethod "https://qiita.com/api/v2/tags/(タグ名)/items"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/tags/mind/items"
PS C:\pmind> $rest.count
20
```
20記事返っています。$restを出力すると大量のテキストでコンソールが流れます。ここでは割愛します。

## 記事取得（記事ID指定）
特定の記事の内容を取得するには記事IDを指定します。（ステップ１と重複します。）

### コマンド文
```powershell:
$res = Invoke-RestMethod "https://qiita.com/api/v2/items/(記事ID)"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/items/bd97e56fdfef2b293828"
```

### 実行結果（取得内容）
テキスト量が多いため割愛しますが、出力イメージを確認したい方は[ステップ１](https://qiita.com/mylifewithviolin/items/7f38beacb069ade3db8e)を参照してください。

## 指定タグの記事取得（ページネーション指定有）
### コマンド文
```powershell:
$rest =Invoke-RestMethod "https://qiita.com/api/v2/tags/(タグ名)/items?page=(ページ位置)&per_page=(1ページあたりの記事数)"
```

### 実行結果
```powershell:
PS C:\pmind> $rest = Invoke-RestMethod "https://qiita.com/api/v2/users/mylifewithviolin/items?page=1&per_page=10"
PS C:\pmind> $rest.count
10
```

10記事返っています。$restを出力すると大量のテキストでコンソールが流れます。ここでは割愛します。


## 指定タグの記事取得（ページネーション指定してループ）

### コマンド文
```powershell:
# 特定のタグ名 
$tag_name = (タグ名)
# ページネーション設定 
$page = (ページ位置初期値)
$per_page = (1ページあたりの記事数)
$all_articles = @() 

# 〇ループ開始
# APIエンドポイントのURL(ページネーションのページ位置変化)
# APIリクエストを送信 
# レスポンスを配列に追加 
# 次のページへ (ページネーションのページ位置カウントアップ)
# 〇ループ終端◇最後のページに到達したかを確認 

do { 
$apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page" 
$res = Invoke-RestMethod -Uri $apiUrl -Method Get 
$all_articles += $res 
$page++ 
} while($res.Count -eq $per_page)
```

### 実行結果
```powershell:
PS C:\pmind> $tag_name = "mind"
PS C:\pmind> $page = 1
PS C:\pmind> $per_page = 100
PS C:\pmind> $all_articles = @()
PS C:\pmind> do {
>> $apiUrl = "https://qiita.com/api/v2/tags/$tag_name/items?page=$page&per_page=$per_page"
>> $res = Invoke-RestMethod -Uri $apiUrl -Method Get
>> $all_articles += $res
>> $page++ 
>> } while ($res.Count -eq $per_page)
PS C:\pmind>
PS C:\pmind> $all_articles.count
299
```
mindタグのページに公開されている記事数より＋１となってしまいましたが、近い数字にはなっています。

# おわりに
いかがでしたか？参考になれば幸いです。
