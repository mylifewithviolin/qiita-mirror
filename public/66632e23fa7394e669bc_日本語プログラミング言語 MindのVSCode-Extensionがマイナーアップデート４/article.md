# はじめに
日本語プログラミング言語Mind（マインド）のシンタックスハイライトとスニペットが使用可能なVSCode拡張機能（の非公式プレビュー版）をマイナーバージョンアップしました！

# 前提条件
Windows11 Pro 22H2 22621.4317
VSCode(Visual Studo Code)　1.107.1

## VSCodeの拡張機能
mind-extension-preview 0.0.4

# 今回のアップデートのハイライト
今回のバージョンアップでは、コードスニペットをMindの二項演算と単項演算に対応しました。

Mind8公式プログラミングマニュアルの「６ 数値演算」の下記の範囲に対応しています。

「整数変数に副作用を与えるもの」　複数変数を一括処理する場合を除く
「１つの値を受け取り、１つの値を返すもの」　ビット操作を除く
「２つの値を受け取り、１つの値を返すもの」
「２つの値を受け取り、検査結果を返すもの」
「１つの値を受け取り、検査結果を返すもの」

# 「日本語プログラミング言語MindのVSCode拡張（非公式）」0.0.4のインストール

VSCodeの拡張機能の検索で、「mindv」くらいまでタイプすると下図のような検索結果が表示されます。スクショはアッパーキャメル風になっていますが、全部小文字でもだいじょうぶです。

![vscode-mind-syntax7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/678d701f-6f07-e555-2242-9ec76505f941.png)


検索結果ペインで「MindVsCodeExtension」の「インストール」をクリックするとインストールされてエディタウィンドウにドキュメントが展開します。

![vscode-mind-syntax8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/fa14a098-0a40-aab4-dbf6-d761530ce7ed.png)

既に以前のバージョンをインストールしていただいている環境では下図のような状態になります。アップデートが検出されてエクステンションの再起動が促された状態です。（図は前回アップデートの状態です。）

![mind-vscode-extentsion-0.0.3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/a7216036-0919-40b6-b295-99386dabdd8d.png)


[拡張機能の再起動]をクリックしてください。VSCodeが再起動されるというわけではなく、当該エクステンションがそのまま再ロードされてアップデートします。


# コードスニペット
コードスニペットはキーワードをタイプした時点で選択肢として表示されます。

## コードスニペットの出し方

下図は「ku」を入力した状態。今回追加された「加え」の他に、以前からある「回数指定して」の構文も選択肢に展開されました。

「k*u」みたいな感じでマッチするようです。自動展開された「condition」というプレースホルダをタブで移動すると置換モードでハイライトされますのでそこに本来の変数や値を入力する流れとなります。

![mindvscodeextentionsnipet1.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/aeb82808-bc44-4676-879f-4e9b8bc276af.jpeg)

コードスニペットの選択肢のサンプル表示でも助詞のシンタックスハイライトが対応するようです。

日本語プログラミングユーザーは日本語入力変換モードで入力しているため全角ひらがなのキーワードにも対応しています。半角英字のキーワードはおおむねこの全角ひらがなのローマ字に対応しています。

下図は「く」を入力した状態。**ひらがな状態でいったん変換確定する**とコードスニペット選択が展開します。
![mindvscodeextentionsnipet2.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/08c0abaf-ef8c-4cbc-ac03-e57db4d6da1c.jpeg)

下図は「ひ」を入力した状態。右側の英語の説明はVSCodeExtentionのコードスニペット設定のjsonのキー値となっているので、一般言語のサンプルどおり英語で記述しています。日本語プログラミング言語ユーザーで英語が苦手な方にはちょっとわかりづらいですが、カンタンな英語ですので慣れてくれば模様として認識はできるかと思います。

![mindvscodeextentionsnipet3.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/4553ffaf-918c-4f28-a6ea-57e6d5ce627f.jpeg)

選択肢を矢印キーで移動すれば日本語の説明とコードスニペットの展開された状態が表示されます。作成者の趣味で若干「はしょり語」となっている場合があります。
「ひとくわ」→「一つ加え」のこと。「ひとぞ」→「一つ増加」のこと

下図は「ふ」を入力した状態。もちろんMindの処理単語名の先頭数文字をひらがなで確定すれば選択肢を絞ることができます。

![mindvscodeextentionsnipet4.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/6f8982c3-00c1-4f79-898d-1fff4a4c8d8a.jpeg)

下図は各コードスニペットの3つ目のキーワードを入力した状態です。（つまり、１つ目が半角英字、２つ目がひらがな全角文字）これはカテゴリ的に同一の選択肢を一発表示する際に便利です。「binaope」は「binary operation」（二項演算）の略です。

![mindvscodeextentionsnipet5.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/0bbcf54c-498c-4a45-891b-a6059c36b248.jpeg)

下図も各コードスニペットの3つ目のキーワードを入力した状態。これはカテゴリ的に同一の選択肢を一発表示する際に便利です。「unaope」は「unary operation」（単項演算）の略です。

![mindvscodeextentionsnipet6.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c009a541-ccbc-44b8-a97d-f737f5e00cc7.jpeg)

下図も各コードスニペットの3つ目のキーワードを入力した状態でこれは以前からサポートしている分岐構文のリストとなります。

![mindvscodeextentionsnipet7.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/41b8b539-298a-430d-a6e0-385dd2c3091f.jpeg)

直感的にはなっていると思いますので、コードスニペットとキーワードの対応表は今回割愛いたします。


# シンタックスハイライト

今回のバージョンアップでは対象外です。[前回の記事](https://qiita.com/mylifewithviolin/items/0970dd5f2ded8c8c3824)をご参照ください。


# MindソースコードをVSCodeでビルドする方法
Mind7とMind8とMind9βのソースコードをVSCodeでビルドする環境を構築する方法はこちらもご参照ください。

https://qiita.com/mylifewithviolin/items/cf8b531bc98a518e3710

# おわりに
いかがでしたでしょうか？なにかのお役に立てればと思います。引き続きバージョンアップしてまいります:relaxed:まだまだ粗削りの状態ですが、引き続きみなさまのご意見ちょうだいいただきたく、よろしくお願いいたします。:bow:

2025年は日本語プログラミング言語Mind生誕４０周年でした。当Extension機能は「日本語プログラミング言語Mind生誕４０周年記念プロジェクト」の第３弾となりました。
謹んで日本語プログラミング言語Mind生誕４０周年をお祝い申し上げます。
