# はじめに

Mind作者の @killyさんにご提案というよりも、完成するかどうかはわかりませんがとりあえず自分で実装してみます的な内容５選です。


# １．データベース接続
Mind7やMind9のTcl機能でもODBCライブラリのデータベース接続が書けることがわかっていますが、わたしの場合はCで書いた方が書きやすいみたいで、Mind9の場合はGUIライブラリの一部になってしまうので、やっぱりCのDLLインターフェースでMind単語を用意かなという感じです。

## このテーマの今年の最終状態

https://qiita.com/mylifewithviolin/items/5c8a440c18ebda0bde1a

https://qiita.com/mylifewithviolin/items/9a1bd4c75a2a3be543f0

https://qiita.com/mylifewithviolin/items/77dafdc556568a5a8ddc

２にも関係しますがMindがバックエンドのロジック実装に勝機を見だすならばDB接続はマスト要件と思っています。

# ２．WebAPIが実装できるようにしたい
Webアプリケーションのフロントエンドは現状百科繚乱のレッドオーシャンなので、MindのCGIをWebAPIコントローラっぽい感じに対応させたい。

## このテーマの今年の最終状態

今年というより昨年のアドベントカレンダーの記事が最後でした。

https://qiita.com/mylifewithviolin/items/bd97e56fdfef2b293828

https://qiita.com/mylifewithviolin/items/f8730d2ff1ed61828a87


# ３．httpクライアントが実装できるようにしたい
２にも関係しますが、Mindをバックエンドのコントローラとした場合、やはりほしいのが別の外部APIとの連携機能です。cURLとかを別プロセスで起動するとかはてっとり早いかもしれませんが、やはり当該言語でのhttpクライアントがほしい。

## このテーマの今年の最終状態

とりあえずMindでのMindレベル単語でのソケット通信の確認にとどまっています。

https://qiita.com/mylifewithviolin/items/f0da45977955cf5f2b3d

# ４．.NET互換ランタイムがほしい

Mindの単語拡張としてはC言語とTclがありますが、どちらもいろいろたいへんなので、.NET言語、具体的にはC#でMind単語が書けるようになるといろいろラクかなという願望があります。
Mindのランタイム中間コードは非常に実装言語と疎のつくりになっているので原理的には実現可能と考えています。

## このテーマの今年の最終状態

今年というより昨年の記事が最後でした。今年はなにもやっていません(^-^;

https://qiita.com/mylifewithviolin/items/151517f7a57b5b8b97f5

https://qiita.com/mylifewithviolin/items/b2895eaaadd41a9395e9


# ５．JavaVM互換ランタイムがほしい

４と同じような話ですが、C#と同じようにCディスパッチャをJavaに書き換えたい願望があります。@killyさんはAndroid版でこれに近いことを既にやっていて、Cランタイムもそのまま使ってしまうという凄ワザでご対応されていらっしゃいますが、わたしは４と同じく中間コードディスパッチャをCからJavaに書き換えたいなと。

## このテーマの今年の最終状態

今年はといいますか、まだなにもやっていません(^-^;来年は着手できるかな？
