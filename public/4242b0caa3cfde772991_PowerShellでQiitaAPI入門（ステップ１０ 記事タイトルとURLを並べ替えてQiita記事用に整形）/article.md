# はじめに
PowerShellでQiitaAPI入門のステップ１０です。今回は特定タグを指定して記事タイトルから特定ワードを条件に記事タイトル、記事URL、投稿日をリスト化して記事数、View数、いいね数を集計した上で投稿日降順で並べ替えながら、出力内容をQiita記事用に整形してみます。

具体的にはmindタグの件名「日本語プログラミング言語Mindの小技」に対して行ってみます。


# 前提条件
Windows11 Pro 22H2 22621.4169
PowerShell psversion 5.1.22621.4249
QiitaAPI 2.0

# 実行例（ステップ１０）
PowerShellではInvoke-RestMethodを使ってQiitaAPIにアクセスします。

## 特定タグの特定件名の記事取得（ページネーション指定してループ ループ内集計　件名の特定ワードでフィルター 一覧出力 並べ替え　出力整形）ステップ９を基本的に継承

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

# 投稿日で降順に並べ替え
$sortedItems = $matchedItems | Sort-Object -Property created_at -Descending

# リスト表示（Qiita記事用に整形）
foreach ($item in $sortedItems) {
    $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
    Write-Output "**$($item.title)** $formattedDate $($item.user.id) `n [$($item.url)]`($($item.url)`) `n"

}

Write-Output "`n========= 集計結果の表示 ========="
Write-Output "Total Items: $totalItems"
Write-Output "Total Likes: $totalLikes"
Write-Output "Total Views: $totalViews"

```
実質ステップ１０は下記のヶ所がお題です。
```powershell:
    Write-Output "**$($item.title)** $formattedDate $($item.user.id) `n [$($item.url)]`($($item.url)`) `n"

```
```powershell:
**$($item.title)**
```
ダブルアスタリスクを挟むことでQiita記事の太字に対応しています。

`nは改行です。
```powershell:
[$($item.url)]`($($item.url)`)
```
かぎカッコで挟むことでURLを表示文字列として
かつリンクにしています。`(　はかっこをエスケープしています。閉じる方も同様。
そのままURLをQiita原稿にした場合、直上に空改行で空白行がなければそのままリンクになりますが、ここでは機械出力なので冗長な出力としています。


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
PS C:\developments\vscode\mind9> # 投稿日で降順に並べ替え
PS C:\developments\vscode\mind9> $sortedItems = $matchedItems | Sort-Object -Property created_at -Descending
PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> # リスト表示（Qiita記事用に整形）
PS C:\developments\vscode\mind9> foreach ($item in $sortedItems) {
>>     $formattedDate = ([DateTime]::Parse($item.created_at)).ToString("yyyy/MM/dd")
>>     Write-Output "**$($item.title)** $formattedDate $($item.user.id) `n [$($item.url)]`($($item.url)`) `n"
>> }
**Mind生誕４０周年プロジェクト「日本語プログラミング言語Mindの小技」リンク集** 2025/11/22 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71](https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71)

**日本語プログラミング言語Mindの小技 「ａｃｃｅｐｔ」～ソケット１対多の接続待機ループ～** 2025/11/01 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/0a97d92ff69abe7cb473](https://qiita.com/mylifewithviolin/items/0a97d92ff69abe7cb473)

**日本語プログラミング言語Mindの小技 「ハンドルとサイズ指定で構造体に読み出し」～ソケット１対多の双方向通信～** 2025/10/25 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/f0da45977955cf5f2b3d](https://qiita.com/mylifewithviolin/items/f0da45977955cf5f2b3d)

**日本語プログラミング言語Mindの小技 「ハンドル指定で書き込み」～ソケットへのブロック書き込み～** 2025/10/25 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/36308ec310df9401c2c1](https://qiita.com/mylifewithviolin/items/36308ec310df9401c2c1)

**日本語プログラミング言語Mindの小技 「入力可能？」～ソケットからの受信状態チェック～** 2025/10/19 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/3d2f0abd485074f45eee](https://qiita.com/mylifewithviolin/items/3d2f0abd485074f45eee)

**日本語プログラミング言語Mindの小技 「ｌｉｓｔｅｎ」～Mindのソケット通信ライブラリ～** 2025/10/18 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/7e7ed77138ec5ea33cc0](https://qiita.com/mylifewithviolin/items/7e7ed77138ec5ea33cc0)

**日本語プログラミング言語Mindの小技 「コネクション確立」～Mind7のソケット通信ライブラリ～** 2025/10/18 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/9b86e1cf38e6a381cbdf](https://qiita.com/mylifewithviolin/items/9b86e1cf38e6a381cbdf)

**日本語プログラミング言語Mindの小技 「論理ファイルをクローズ」～論理ファイル動的確保した場合のクローズ** 2025/10/12 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/2415ac4f824ccc3dcdda](https://qiita.com/mylifewithviolin/items/2415ac4f824ccc3dcdda)

**日本語プログラミング言語Mindの小技 「論理ファイルの新規オープン」～論理ファイル動的確保して書き込みオープン～** 2025/10/12 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/97b65b1cf7309dcf3ab7](https://qiita.com/mylifewithviolin/items/97b65b1cf7309dcf3ab7)

**日本語プログラミング言語Mindの小技 「論理ファイルをオープン」～論理ファイル動的確保してオープン～** 2025/10/11 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/d69db38d1f6976fa87dd](https://qiita.com/mylifewithviolin/items/d69db38d1f6976fa87dd)

**日本語プログラミング言語Mindの小技 「論理ファイルを獲得」～ファイル管理構造体の動的確保～** 2025/10/11 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/e6c4bf65cbe88ef81b4d](https://qiita.com/mylifewithviolin/items/e6c4bf65cbe88ef81b4d)

**日本語プログラミング言語Mindの小技 「処理単語 YVとWO」～読出バッファ任意使用と特定送り仮名指定～** 2025/10/05 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/5953cfa4215983d525dc](https://qiita.com/mylifewithviolin/items/5953cfa4215983d525dc)

**日本語プログラミング言語Mindの小技 「処理単語 .V」～（論理ファイルの）構造体情報を得る～** 2025/10/05 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/7cae30f30cf3f1c8a3ca](https://qiita.com/mylifewithviolin/items/7cae30f30cf3f1c8a3ca)

**日本語プログラミング言語Mindの小技 「ファイル情報」～読み出し用論理ファイルのローカル変数～** 2025/10/04 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/a941fddb20acacbe58e6](https://qiita.com/mylifewithviolin/items/a941fddb20acacbe58e6)

**日本語プログラミング言語Mindの小技 「データ終り？」～EOFの安全な判定～** 2025/10/04 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/57a5bf3e7a643fff932e](https://qiita.com/mylifewithviolin/items/57a5bf3e7a643fff932e)

**日本語プログラミング言語Mindの小技 「ダンプ・バイト」～文字列をダンプして表示～** 2025/10/01 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/886313e5613c11571451](https://qiita.com/mylifewithviolin/items/886313e5613c11571451)

**日本語プログラミング言語Mindの小技 「ダブルクオートで囲んで表示」～特殊な文字列表示～** 2025/10/01 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/d9f9f8acb692aa3141ed](https://qiita.com/mylifewithviolin/items/d9f9f8acb692aa3141ed)

**日本語プログラミング言語Mindの小技 「追加書き込み」～シーケンシャルファイル追加書き込み～** 2025/09/28 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/ae9cf701adc4e7cd94e4](https://qiita.com/mylifewithviolin/items/ae9cf701adc4e7cd94e4)

**日本語プログラミング言語Mindの小技 「一行書き込み」～シーケンシャルファイル書き込み～** 2025/09/28 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/ebbe8a3c86931b3556f4](https://qiita.com/mylifewithviolin/items/ebbe8a3c86931b3556f4)

**日本語プログラミング言語Mindの小技 「ファイルの新規オープン」～ファイルを書き込みモードでオープン～** 2025/09/28 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/f7f67381a4ee281b8d44](https://qiita.com/mylifewithviolin/items/f7f67381a4ee281b8d44)

**日本語プログラミング言語Mindの小技 「逆方向に一行読み出し」～シーケンシャルファイル逆方向読み出し～** 2025/09/27 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/76a9302e362ad3fc308d](https://qiita.com/mylifewithviolin/items/76a9302e362ad3fc308d)

**日本語プログラミング言語Mindの小技 「一行読み出し」～シーケンシャルファイル正方向読み出し～** 2025/09/27 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/400bd2153d1b9bf85182](https://qiita.com/mylifewithviolin/items/400bd2153d1b9bf85182)

**日本語プログラミング言語Mindの小技 「ファイルのオープンとクローズ」～ファイルを読み取りモードでオープン～** 2025/09/27 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/dcf7f32217f9fe6b21d9](https://qiita.com/mylifewithviolin/items/dcf7f32217f9fe6b21d9)

**日本語プログラミング言語Mindの小技 「文字列変数の配列」～文字列情報または文字列実体変数の配列～** 2025/09/21 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/6aead1c1d8323ac3559e](https://qiita.com/mylifewithviolin/items/6aead1c1d8323ac3559e)

**日本語プログラミング言語Mindの小技 「数値変数の配列」～整数または小数変数の配列～** 2025/09/21 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/bef2955799df2fcecfdb](https://qiita.com/mylifewithviolin/items/bef2955799df2fcecfdb)

**日本語プログラミング言語Mindの小技 「文字列の定数配列」～文字列定数の配列～** 2025/09/20 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/e0dc3dc913a41018b5ba](https://qiita.com/mylifewithviolin/items/e0dc3dc913a41018b5ba)

**日本語プログラミング言語Mindの小技 「数値の定数配列」～整数または小数定数の配列～** 2025/09/20 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/63bb5b8530b738c8e4c8](https://qiita.com/mylifewithviolin/items/63bb5b8530b738c8e4c8)

**日本語プログラミング言語Mindの小技 「カーソル位置設定」～PureMind5.2互換仮想ターミナルコマンド２～** 2025/09/14 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/0ed43e577884d116e281](https://qiita.com/mylifewithviolin/items/0ed43e577884d116e281)

**日本語プログラミング言語Mindの小技 「一文字直接入力」～Win32ApiのReadConsoleWで復活～** 2025/09/14 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/86b23a6e64d8fd39464b](https://qiita.com/mylifewithviolin/items/86b23a6e64d8fd39464b)

**日本語プログラミング言語Mindの小技 「コンソール制御」～PureMind5.2互換仮想ターミナルコマンド～** 2025/09/13 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/5fb0229a336487cd8715](https://qiita.com/mylifewithviolin/items/5fb0229a336487cd8715)

**日本語プログラミング言語Mindの小技 「論理演算」～AND(論理積) OR(論理和) XOR(排他的論理和) NOT(否定)～** 2025/09/13 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/2a4c1b4c0b07be0aaac8](https://qiita.com/mylifewithviolin/items/2a4c1b4c0b07be0aaac8)

**日本語プログラミング言語Mindの小技 「モジュールをロード」～Win32Apiで仮想ターミナルモードを変更～** 2025/09/08 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/0672c3fa0352ec87be69](https://qiita.com/mylifewithviolin/items/0672c3fa0352ec87be69)

**日本語プログラミング言語Mindの小技 「スタック検査」～クリアされていないスタック状態の検出～** 2025/09/06 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/01ee2714fdb57b16791a](https://qiita.com/mylifewithviolin/items/01ee2714fdb57b16791a)

**日本語プログラミング言語Mindの小技 「起動引数をモニタ」～コンソールアプリの起動パラメータをモニタ～** 2025/08/30 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/b37e52e6c8c177191a83](https://qiita.com/mylifewithviolin/items/b37e52e6c8c177191a83)

**日本語プログラミング言語Mindの小技 「文字列入力」～コンソールからの入力～** 2025/08/23 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/b592b20d7c138013e1b5](https://qiita.com/mylifewithviolin/items/b592b20d7c138013e1b5)

**日本語プログラミング言語Mindの小技 「子プロセス終了？」～非同期実行と終了検知２～** 2025/08/16 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/e1fbced1889fe8330d48](https://qiita.com/mylifewithviolin/items/e1fbced1889fe8330d48)

**日本語プログラミング言語Mindの小技 「子プロセス起動」～非同期実行と終了検知～** 2025/08/09 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/ec6ebdc84400e5c8673f](https://qiita.com/mylifewithviolin/items/ec6ebdc84400e5c8673f)

**日本語プログラミング言語Mindの小技 「プログラム実行」～２つの終了パラメータ～** 2025/08/02 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/224ba20676b56f96fa34](https://qiita.com/mylifewithviolin/items/224ba20676b56f96fa34)

**日本語プログラミング言語Mindの小技 「コメント（注釈）」～インラインとブロックとスタック仕様～** 2025/07/26 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/5cc12f90dd792616db8f](https://qiita.com/mylifewithviolin/items/5cc12f90dd792616db8f)

**日本語プログラミング言語Mindの小技 「実体変数と情報変数の使い分け」～文字列の変数型２種徹底解説～** 2025/07/21 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/8c01b01353b10d63fc3f](https://qiita.com/mylifewithviolin/items/8c01b01353b10d63fc3f)

**日本語プログラミング言語Mindの小技 「処理単語 .J」～文字列実体情報を得る～** 2025/07/12 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/8180b6b3c27bddbfadf2](https://qiita.com/mylifewithviolin/items/8180b6b3c27bddbfadf2)

**日本語プログラミング言語Mindの小技 「文字列を分断する」～分割位置の文字を消してくれる～** 2025/07/12 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/d3e84f3c61f7fe7b663f](https://qiita.com/mylifewithviolin/items/d3e84f3c61f7fe7b663f)

**日本語プログラミング言語Mindの小技 「送り仮名」～形式言語としての日本語２～** 2025/07/05 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/0599e8c85cc366a7bc06](https://qiita.com/mylifewithviolin/items/0599e8c85cc366a7bc06)

**日本語プログラミング言語Mindの小技 「数値定数を単語定義」～数値定数を表す単語～** 2025/06/28 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/c603b8b4cefea50e1890](https://qiita.com/mylifewithviolin/items/c603b8b4cefea50e1890)

**日本語プログラミング言語Mindの小技 「空白？」～文字コードを調べる単語～** 2025/06/21 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/4ce004fa4db8c683d0f2](https://qiita.com/mylifewithviolin/items/4ce004fa4db8c683d0f2)

**日本語プログラミング言語Mindの小技 「単語を切り出す」～元文字列も切り出された状態になる～** 2025/06/14 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/ef2e0aa8c239bdee84fa](https://qiita.com/mylifewithviolin/items/ef2e0aa8c239bdee84fa)

**日本語プログラミング言語Mindの小技 「処理単語の属性指定」～スタック上の変数の数や型チェック～** 2025/06/07 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/4b858baae3bb24aa122c](https://qiita.com/mylifewithviolin/items/4b858baae3bb24aa122c)

**日本語プログラミング言語Mindの小技 「処理単語」～複数の戻り値をスタックに置ける～** 2025/05/31 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/d84639178e12519a3dca](https://qiita.com/mylifewithviolin/items/d84639178e12519a3dca)

**日本語プログラミング言語Mindの小技 「小数」～構造体の多次元配列内の小数変数～** 2025/05/28 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/502d0a531c59e1d13065](https://qiita.com/mylifewithviolin/items/502d0a531c59e1d13065)

**日本語プログラミング言語Mindの小技 「二番目を捨てる」～スタックツートップのNo.1を生かしてNo.2を捨てる～** 2025/05/24 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/73f55ed78880d9c1c15d](https://qiita.com/mylifewithviolin/items/73f55ed78880d9c1c15d)

**日本語プログラミング言語Mindの小技 「多次元配列」～構造体の多次元配列～** 2025/05/17 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/05bd513cee3be9a5a6f0](https://qiita.com/mylifewithviolin/items/05bd513cee3be9a5a6f0)

**日本語プログラミング言語Mindの小技 「複写」～スタックトップの値を２つにする～** 2025/05/10 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/e92b0e613c1d02ffcd0a](https://qiita.com/mylifewithviolin/items/e92b0e613c1d02ffcd0a)

**日本語プログラミング言語Mindの小技 「分ち書き」～形式言語としての日本語～** 2025/05/03 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/227041b012a4f07ba5ec](https://qiita.com/mylifewithviolin/items/227041b012a4f07ba5ec)

**日本語プログラミング言語Mindの小技 「回数指定」～指定回数くりかえすループ～** 2025/04/26 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/1a5a4fdef27e0e88f3ba](https://qiita.com/mylifewithviolin/items/1a5a4fdef27e0e88f3ba)

**日本語プログラミング言語Mindの小技 「関数」～戻り値を複数返せる～** 2025/04/20 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/86bfe9e74b10bde81088](https://qiita.com/mylifewithviolin/items/86bfe9e74b10bde81088)

**日本語プログラミング言語Mindの小技 「選択」～処理も選択できる～** 2025/04/12 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/4bb9c6375ed9c673b901](https://qiita.com/mylifewithviolin/items/4bb9c6375ed9c673b901)

**日本語プログラミング言語Mindの小技 「もう一度」～ループの先頭からもう一度やりなおす～** 2025/04/05 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/c8bff9eb12b034da6204](https://qiita.com/mylifewithviolin/items/c8bff9eb12b034da6204)

**日本語プログラミング言語Mindの小技 「逆転介入」～計算式日本語表現の語順への逆転介入～** 2025/03/30 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/85eac9eb6b9393afee64](https://qiita.com/mylifewithviolin/items/85eac9eb6b9393afee64)

**日本語プログラミング言語Mindの小技 「空白を満たす」～文字列に右寄せで空白を満たす？～** 2025/03/24 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/219fb2edf4d474484e47](https://qiita.com/mylifewithviolin/items/219fb2edf4d474484e47)

**日本語プログラミング言語Mindの小技 「リカーシブコール」たらい回し関数** 2025/03/20 ITvision
 [https://qiita.com/ITvision/items/c0bf3789a59df83d2d70](https://qiita.com/ITvision/items/c0bf3789a59df83d2d70)

**日本語プログラミング言語Mindの小技 「つぎに」～条件分岐の終端～** 2025/03/20 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/aa3eda2236ab1777a9ea](https://qiita.com/mylifewithviolin/items/aa3eda2236ab1777a9ea)

**日本語プログラミング言語Mindの小技 「型紙」～構造体～** 2025/03/15 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/17ab9a1c960d6a29c345](https://qiita.com/mylifewithviolin/items/17ab9a1c960d6a29c345)

**日本語プログラミング言語Mindの小技 「局所処理単語」～クロージャっぽい～** 2025/03/11 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/0a6f45635bf36bdd9111](https://qiita.com/mylifewithviolin/items/0a6f45635bf36bdd9111)

**日本語プログラミング言語Mindの小技 「等価」** 2025/03/09 mylifewithviolin
 [https://qiita.com/mylifewithviolin/items/51e1522621cd4a4d5ab2](https://qiita.com/mylifewithviolin/items/51e1522621cd4a4d5ab2)

PS C:\developments\vscode\mind9>
PS C:\developments\vscode\mind9> Write-Output "`n========= 集計結果の表示 ========="

========= 集計結果の表示 =========
PS C:\developments\vscode\mind9> Write-Output "Total Items: $totalItems"
Total Items: 64
PS C:\developments\vscode\mind9> Write-Output "Total Likes: $totalLikes"
Total Likes: 188
PS C:\developments\vscode\mind9> Write-Output "Total Views: $totalViews"
Total Views: 92998
PS C:\developments\vscode\mind9>
```
結果はなまのテキストでわかりにくくてすみません。この出力をつかって書いたQiitaの記事がこちらです。

[Mind生誕４０周年プロジェクト「日本語プログラミング言語Mindの小技」リンク集
](https://qiita.com/mylifewithviolin/items/6e7ca404684fe37ecb71)

# おわりに
いかがでしたか？なにかの参考になれば幸いです。

以下はほぼ自分用の備忘録ですが、PowerShellでQiitaAPI入門の過去記事リストです。
[PowerShellでQiitaAPI入門（ステップ９ 記事タイトルの特定ワードのいいね数とView数を集計し並べ替え）](https://qiita.com/mylifewithviolin/items/cdf896c9a88ccc8ab5f3)
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
