# はじめに
PowerShellでQiitaAPI入門のステップ９です。今回は特定タグを指定して記事タイトルから特定ワードを条件に記事タイトル、投稿日、いいね数、View数をリスト化して集計した上でView数で並べ替えてみます。

具体的にはmindタグの件名「日本語プログラミング言語Mindの小技」に対して行ってみます。


# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ９）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 特定タグの特定件名の記事取得（ページネーション指定してループ ループ内集計　件名の特定ワードでフィルター 一覧出力 並べ替え）

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
$totalItems = 0
$totalLikes = 0
$totalViews = 0
$matchedItems = @()

do {
    $url = "https://qiita.com/api/v2/tags/$tagId/items?page=$page&per_page=$perPage"
    $response = Invoke-RestMethod -Uri $url -Headers $headers

    foreach ($item in $response) {
        if ($item.title -like "*$keyword*") {
            $matchedItems += $item
            $totalItems+=1
            $totalLikes += $item.likes_count
            $totalViews += $item.page_views_count

        }
    }

    $page++
} while ($response.Count -eq $perPage)

# View数で降順に並べ替え
$sortedItems = $matchedItems | Sort-Object -Property page_views_count -Descending

# 表示
foreach ($item in $sortedItems) {
    $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
    Write-Output "$formattedDate $($item.title) $($item.likes_count) $($item.page_views_count)  $($item.user.id)"
}

Write-Output "`n========= 集計結果の表示 ========="
Write-Output "Total Items: $totalItems"
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
PS C:\developments\vscode\mind9> $totalItems = 0
PS C:\developments\vscode\mind9> $totalLikes = 0
PS C:\developments\vscode\mind9> $totalViews = 0
PS C:\developments\vscode\mind9> $matchedItems = @()
PS C:\developments\vscode\mind9> do {
>>     $url = "https://qiita.com/api/v2/tags/$tagId/items?page=$page&per_page=$perPage"
>>     $response = Invoke-RestMethod -Uri $url -Headers $headers
>>
>>     foreach ($item in $response) {
>>         if ($item.title -like "*$keyword*") {
>>             $matchedItems += $item
>>             $totalItems+=1
>>             $totalLikes += $item.likes_count
>>             $totalViews += $item.page_views_count
>>
>>         }
>>     }
>>
>>     $page++
>> } while ($response.Count -eq $perPage)
PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> # View数で降順に並べ替え
PS C:\developments\vscode\mind9> $sortedItems = $matchedItems | Sort-Object -Property page_views_count -Descending
PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> # 表示
PS C:\developments\vscode\mind9> foreach ($item in $sortedItems) {
>>     $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
>>     Write-Output "$formattedDate $($item.title) $($item.likes_count) $($item.page_views_count)  $($item.user.id)"
>> }
2025/04/20 日本語プログラミング言語Mindの小技 「関数」～戻り値を複数返せる～ 6 7851  mylifewithviolin
2025/03/09 日本語プログラミング言語Mindの小技 「等価」 6 6653  mylifewithviolin
2025/08/30 日本語プログラミング言語Mindの小技 「起動引数をモニタ」～コンソールアプリの起動パラメータをモニタ～ 3 5009  mylifewithviolin
2025/10/12 日本語プログラミング言語Mindの小技 「論理ファイルの新規オープン」～論理ファイル動的確保して書き込みオープン～ 6 4566  mylifewithviolin
2025/03/20 日本語プログラミング言語Mindの小技 「つぎに」～条件分岐の終端～ 5 4181  mylifewithviolin
2025/10/18 日本語プログラミング言語Mindの小技 「コネクション確立」～Mind7のソケット通信ライブラリ～ 4 4073  mylifewithviolin
2025/09/21 日本語プログラミング言語Mindの小技 「数値変数の配列」～整数または小数変数の配列～ 4 3955  mylifewithviolin
2025/10/12 日本語プログラミング言語Mindの小技 「論理ファイルをクローズ」～論理ファイル動的確保した場合のクローズ 5 3787  mylifewithviolin
2025/03/11 日本語プログラミング言語Mindの小技 「局所処理単語」～クロージャっぽい～ 5 3656  mylifewithviolin
2025/09/13 日本語プログラミング言語Mindの小技 「論理演算」～AND(論理積) OR(論理和) XOR(排他的論理和) NOT(否定)～ 5 3356  mylifewithviolin
2025/04/05 日本語プログラミング言語Mindの小技 「もう一度」～ループの先頭からもう一度やりなおす～ 4 3175  mylifewithviolin
2025/04/12 日本語プログラミング言語Mindの小技 「選択」～処理も選択できる～ 5 2137  mylifewithviolin
2025/09/14 日本語プログラミング言語Mindの小技 「一文字直接入力」～Win32ApiのReadConsoleWで復活～ 3 2086  mylifewithviolin
2025/06/07 日本語プログラミング言語Mindの小技 「処理単語の属性指定」～スタック上の変数の数や型チェック～ 4 2055  mylifewithviolin
2025/09/27 日本語プログラミング言語Mindの小技 「逆方向に一行読み出し」～シーケンシャルファイル逆方向読み出し～ 4 1795  mylifewithviolin
2025/08/16 日本語プログラミング言語Mindの小技 「子プロセス終了？」～非同期実行と終了検知２～ 3 1717  mylifewithviolin
2025/09/20 日本語プログラミング言語Mindの小技 「文字列の定数配列」～文字列定数の配列～ 2 1683  mylifewithviolin
2025/09/06 日本語プログラミング言語Mindの小技 「スタック検査」～クリアされていないスタック状態の検出～ 2 1664  mylifewithviolin
2025/05/31 日本語プログラミング言語Mindの小技 「処理単語」～複数の戻り値をスタックに置ける～ 5 1617  mylifewithviolin
2025/08/23 日本語プログラミング言語Mindの小技 「文字列入力」～コンソールからの入力～ 3 1603  mylifewithviolin
2025/10/11 日本語プログラミング言語Mindの小技 「論理ファイルをオープン」～論理ファイル動的確保してオープン～ 3 1601  mylifewithviolin
2025/09/20 日本語プログラミング言語Mindの小技 「数値の定数配列」～整数または小数定数の配列～ 2 1538  mylifewithviolin
2025/09/27 日本語プログラミング言語Mindの小技 「ファイルのオープンとクローズ」～ファイルを読み取りモードでオープン～ 3 1523  mylifewithviolin
2025/09/27 日本語プログラミング言語Mindの小技 「一行読み出し」～シーケンシャルファイル正方向読み出し～ 3 1490  mylifewithviolin
2025/10/04 日本語プログラミング言語Mindの小技 「ファイル情報」～読み出し用論理ファイルのローカル変数～ 4 1369  mylifewithviolin
2025/10/11 日本語プログラミング言語Mindの小技 「論理ファイルを獲得」～ファイル管理構造体の動的確保～ 2 1334  mylifewithviolin
2025/09/14 日本語プログラミング言語Mindの小技 「カーソル位置設定」～PureMind5.2互換仮想ターミナルコマンド２～ 2 1262  mylifewithviolin
2025/05/24 日本語プログラミング言語Mindの小技 「二番目を捨てる」～スタックツートップのNo.1を生かしてNo.2を捨てる～ 3 1132  mylifewithviolin
2025/10/18 日本語プログラミング言語Mindの小技 「ｌｉｓｔｅｎ」～Mindのソケット通信ライブラリ～ 3 1094  mylifewithviolin
2025/09/13 日本語プログラミング言語Mindの小技 「コンソール制御」～PureMind5.2互換仮想ターミナルコマンド～ 2 1091  mylifewithviolin
2025/08/09 日本語プログラミング言語Mindの小技 「子プロセス起動」～非同期実行と終了検知～ 2 942  mylifewithviolin
2025/05/03 日本語プログラミング言語Mindの小技 「分ち書き」～形式言語としての日本語～ 3 936  mylifewithviolin
2025/08/02 日本語プログラミング言語Mindの小技 「プログラム実行」～２つの終了パラメータ～ 3 921  mylifewithviolin
2025/04/26 日本語プログラミング言語Mindの小技 「回数指定」～指定回数くりかえすループ～ 3 915  mylifewithviolin
2025/05/10 日本語プログラミング言語Mindの小技 「複写」～スタックトップの値を２つにする～ 3 877  mylifewithviolin
2025/05/17 日本語プログラミング言語Mindの小技 「多次元配列」～構造体の多次元配列～ 4 764  mylifewithviolin
2025/07/12 日本語プログラミング言語Mindの小技 「文字列を分断する」～分割位置の文字を消してくれる～ 3 613  mylifewithviolin
2025/03/30 日本語プログラミング言語Mindの小技 「逆転介入」～計算式日本語表現の語順への逆転介入～ 3 606  mylifewithviolin
2025/03/15 日本語プログラミング言語Mindの小技 「型紙」～構造体～ 3 579  mylifewithviolin
2025/10/25 日本語プログラミング言語Mindの小技 「ハンドルとサイズ指定で構造体に読み出し」～ソケット１対多の双方向通信～ 2 400  mylifewithviolin
2025/03/24 日本語プログラミング言語Mindの小技 「空白を満たす」～文字列に右寄せで空白を満たす？～ 3 343  mylifewithviolin
2025/09/08 日本語プログラミング言語Mindの小技 「モジュールをロード」～Win32Apiで仮想ターミナルモードを変更～ 2 335  mylifewithviolin
2025/10/25 日本語プログラミング言語Mindの小技 「ハンドル指定で書き込み」～ソケットへのブロック書き込み～ 2 289  mylifewithviolin
2025/09/28 日本語プログラミング言語Mindの小技 「ファイルの新規オープン」～ファイルを書き込みモードでオープン～ 2 277  mylifewithviolin
2025/06/21 日本語プログラミング言語Mindの小技 「空白？」～文字コードを調べる単語～ 2 253  mylifewithviolin
2025/07/05 日本語プログラミング言語Mindの小技 「送り仮名」～形式言語としての日本語２～ 2 251  mylifewithviolin
2025/06/14 日本語プログラミング言語Mindの小技 「単語を切り出す」～元文字列も切り出された状態になる～ 2 242  mylifewithviolin
2025/09/28 日本語プログラミング言語Mindの小技 「追加書き込み」～シーケンシャルファイル追加書き込み～ 2 238  mylifewithviolin
2025/07/12 日本語プログラミング言語Mindの小技 「処理単語 .J」～文字列実体情報を得る～ 2 235  mylifewithviolin
2025/05/28 日本語プログラミング言語Mindの小技 「小数」～構造体の多次元配列内の小数変数～ 3 223  mylifewithviolin
2025/07/21 日本語プログラミング言語Mindの小技 「実体変数と情報変数の使い分け」～文字列の変数型２種徹底解説～ 2 222  mylifewithviolin
2025/06/28 日本語プログラミング言語Mindの小技 「数値定数を単語定義」～数値定数を表す単語～ 2 202  mylifewithviolin
2025/07/26 日本語プログラミング言語Mindの小技 「コメント（注釈）」～インラインとブロックとスタック仕様～ 2 197  mylifewithviolin
2025/10/19 日本語プログラミング言語Mindの小技 「入力可能？」～ソケットからの受信状態チェック～ 2 153  mylifewithviolin
2025/10/01 日本語プログラミング言語Mindの小技 「ダンプ・バイト」～文字列をダンプして表示～ 2 153  mylifewithviolin
2025/10/05 日本語プログラミング言語Mindの小技 「処理単語 YVとWO」～読出バッファ任意使用と特定送り仮名指定～ 2 137  mylifewithviolin
2025/10/01 日本語プログラミング言語Mindの小技 「ダブルクオートで囲んで表示」～特殊な文字列表示～ 2 125  mylifewithviolin
2025/09/21 日本語プログラミング言語Mindの小技 「文字列変数の配列」～文字列情報または文字列実体変数の配列～ 2 109  mylifewithviolin
2025/10/04 日本語プログラミング言語Mindの小技 「データ終り？」～EOFの安全な判定～ 2 107  mylifewithviolin
2025/10/05 日本語プログラミング言語Mindの小技 「処理単語 .V」～（論理ファイルの）構造体情報を得る～ 2 94  mylifewithviolin
2025/09/28 日本語プログラミング言語Mindの小技 「一行書き込み」～シーケンシャルファイル書き込み～ 2 77  mylifewithviolin
2025/11/01 日本語プログラミング言語Mindの小技 「ａｃｃｅｐｔ」～ソケット１対多の接続待機ループ～ 1 52  mylifewithviolin
2025/03/20 日本語プログラミング言語Mindの小技 「リカーシブコール」たらい回し関数 3   ITvision
PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> Write-Output "`n========= 集計結果の表示 ========="

========= 集計結果の表示 =========
PS C:\developments\vscode\mind9> Write-Output "Total Items: $totalItems"
Total Items: 63
PS C:\developments\vscode\mind9> Write-Output "Total Likes: $totalLikes"
Total Likes: 188
PS C:\developments\vscode\mind9> Write-Output "Total Views: $totalViews"
Total Views: 91920
PS C:\developments\vscode\mind9>
```

ちょっとタイトルが長すぎてわかりづらいですが、View数の降順で出力されていることがわかります。View数は認証トークンを設定して、自分が投稿した記事のみ取得できますので、他の方の記事はView数の出力ブランクで最後になります。

記事全体を配列にいったんすべて格納してから並べ替えていますので、メモリ消費量は大きくやパフォーマンスは低い状態です。


# おわりに
いかがでしたか？結果はなまのテキストでわかりにくくてすみません。なにかの参考になれば幸いです。

以下はほぼ自分用の備忘録ですが、PowerShellでQiitaAPI入門の過去記事リストです。
[PowerShellでQiitaAPI入門（ステップ８ 記事タイトルの特定ワードのいいね数とView数を集計）](
https://qiita.com/mylifewithviolin/items/9ee09fb43b7517ec55a9)
[PowerShellでQiitaAPI入門（ステップ７複数タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/e704fdfdbc151eda4c62)
[PowerShellでQiitaAPI入門（ステップ６複数タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/1d75a3cf5cd65a01b5f0)
[PowerShellでQiitaAPI入門（ステップ５指定タグ全記事取得中の複数キー集計）](https://qiita.com/mylifewithviolin/items/8a73f565625c09c69d41)
[PowerShellでQiitaAPI入門（ステップ４ 指定タグ全記事取得中の集計）](https://qiita.com/mylifewithviolin/items/83a0d74f7586950cfa65)
[PowerShellでQiitaAPI入門（ステップ３ 指定タグ全記事取得後の集計）](https://qiita.com/mylifewithviolin/items/6e9bfaa64477daa7b1ab)
[PowerShellでQiitaAPI入門（ステップ２ 指定タグ全記事取得）](https://qiita.com/mylifewithviolin/items/fd7a4ef9de1fa9809b15)
[PowerShellでQiitaAPI入門（ステップ１ 単純記事取得）](https://qiita.com/mylifewithviolin/items/7f38beacb069ade3db8e)



## 集計対象の記事シリーズのご紹介
記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできますよ。


面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
