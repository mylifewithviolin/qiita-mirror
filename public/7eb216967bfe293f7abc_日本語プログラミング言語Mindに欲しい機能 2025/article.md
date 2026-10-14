# はじめに
Mindに欲しい機能を今年も議論したいと思います。このテーマは@ITvisionさんより移譲いただきました。アドベントカレンダーの主旨上、他の方による同様の記事のご投稿をさまたげるものではございません。

あると良い機能について優先度・実装方法などを検討し、ユーザーでできそうなものはユーザーで、できなさそうなのはMind作者の@killyさんにご検討を依頼していきたいと思いますので、よろしくお願いします。

# 過去のアドベントカレンダーにあがった要件

昨年のアドベントカレンダーの[日本語プログラミング言語Mindに欲しい機能 2024](https://qiita.com/ITvision/items/6935f4d3063e1b6b8d60)では、下記の要件があげられていました。
・文字列関係関数
・EXCEL対応
・jsonパーサ
・小技集
・データベース操作
・固定小数点型
・乱数
・正規表現エンジン。
・ソケット
・ActiveXを呼びたい。

# 各要件の対応状況

ここではこれらの計上済の要件についての対応状況、実現方法案もまとめておきます。

| 要件名 | 補足 |実現方法案 | 対応状況 | 参考リンク|
|:-|:-|:-|:-|:-|
| 文字列関係関数  |  先頭部分文字列(作業文字列１、３文字） |Mind単語で属性つけて関数化？| 未対応  |   |
| EXCEL対応  | Mindで実装した機能をExcelから使う  |Mind7のDLL機能でExcelからインポートDeclare文   |ユーザーで試作   |[C#からMind7で実装したDLLを実行する - Qiita](https://qiita.com/mylifewithviolin/items/62bbdeb584a20f881a5a)|
| jsonパーサ  |JSONシリアライズ・デシリアライズをMind構造体に適用 |  検討中 |ユーザーで実現方検討中   |   |
| 小技集  | いろいろなMind単語の使用例  |40周年記念プロジェクト |ユーザーで作成中   |[日本語プログラミング言語Mindの小技 「ａｃｃｅｐｔ」～ソケット１対多の接続待機ループ～ - Qiita](https://qiita.com/mylifewithviolin/items/0a97d92ff69abe7cb473) <br><br>[日本語プログラミング言語Mindの小技 「リカーシブコール」たらい回し関数 - Qiita](https://qiita.com/ITvision/items/c0bf3789a59df83d2d70)|
| データベース操作  | データベースをMind単語で操作  |C言語DLL拡張でMind単語化、Tclインタプリタ経由でMind単語化   |ユーザーで試作中   | [Mind7/8/9β odbcライブラリC言語DLL拡張単語のアップデート（結果セット取得の9βTcl互換調整） - Qiita](https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a) <br><br>[Mind９βでSQLServer、Mysql、PostgreSQLからのSELECT結果を構造体格納（SQLServer） - Qiita](https://qiita.com/mylifewithviolin/items/77dafdc556568a5a8ddc)  |
| 固定小数点型  |Mindの小数は浮動小数点型  |Mindカーネル拡張で64bit変数を固定小数点扱いする単語追加 |ユーザー試作中   |[Mind8で通貨型（64bit整数の4桁スケーリング固定小数点型）の四則演算を実装してみる（currency.src） - Qiita](https://qiita.com/mylifewithviolin/items/d5d65042ca02477a680c)|
| 乱数  |   | Mind単語で実装、Tclインタプリタ経由でMind単語化  |ユーザー作成事例有   | [Mind言語で 疑似乱数関数 を作ってみた - Qiita](https://qiita.com/ITvision/items/19b3749e015aabd0c331) <br><br>[日本語プログラミング言語Mindのバージョン９βでTcl乱数関数の定義を試みる３](https://qiita.com/mylifewithviolin/items/f5556e7673fb27456dcd)|
| 正規表現エンジン  |   | Tclインタプリタ経由でMind単語化  |未対応   |   |
| ソケット  | ソケットの高機能語が欲しい  |既存単語を組み合わせて構築|ユーザー作成事例有    | [日本語プログラミング言語Mindの小技 「ｌｉｓｔｅｎ」～Mindのソケット通信ライブラリ～ - Qiita](https://qiita.com/mylifewithviolin/items/7e7ed77138ec5ea33cc0)  |
| ActiveX  | MindからActiveX（COM実装）を呼び出したい  | COMをC言語から呼び出すラッパ実装しCのDLL経由呼び出し  |難度高のため未対応   |   |

# おわりに
いかがでしたでしょうか？筆者もこれらの欲しい機能の議論を受けて、その課題感でQiita上の記事を展開していますので、その状況の備忘録を兼ねています。
追加のご要望はコメント欄にお願いします。

2025年は日本語プログラミング言語Mind生誕４０周年です。

Mindをまだお使いでない方は　[Mind8 ダウンロードページ](https://www.scripts-lab.co.jp/mind8download/download.html)　から無料でダウンロードできます。[Mind8プログラミングマニュアル](https://www.scripts-lab.co.jp/mind/ver8/doc/index.html)　を参考にしてください。Qiitaユーザーでない方は[Mindサポート掲示板](https://www.scripts-lab.co.jp/support/public/html/mind.cgi?tframe+035+-s+F001)　にも投稿できたらと思います。
