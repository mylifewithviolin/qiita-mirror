# はじめに
日本語プログラミング言語Mind（マインド）のシンタックスハイライトとスニペットが使用可能なVSCode拡張機能（の非公式プレビュー版）がついにリリース！まだまだ粗削りの状態ですが、みなさまのご意見ちょうだいいただきたく、よろしくお願いいたします。:bow:

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.95.1


## VSCodeの拡張機能
mind-extension-preview 0.0.1

# 「日本語プログラミング言語MindのVSCode拡張（非公式）」0.0.1のインストール

VSCodeの拡張機能の検索で、「mindv」くらいまでタイプすると下図のような検索結果が表示されます。スクショはアッパーキャメル風になっていますが、全部小文字でもだいじょうぶです。

![vscode-mind-syntax7.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/678d701f-6f07-e555-2242-9ec76505f941.png)


検索結果ペインで「MindVsCodeExtension」の「インストール」をクリックするとインストールされてエディタウィンドウにドキュメントが展開します。

![vscode-mind-syntax8.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/fa14a098-0a40-aab4-dbf6-d761530ce7ed.png)

# シンタックスハイライトの様子
下図は先日の雪っぽいのを降らせるMind9βのソースコードです。

![vscode-mind-syntax9.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/8e84d8aa-59aa-e8f1-4dca-979e8fefa23a.png)

下図はMind9β標準添付のサンプルソースコードの例です。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/15862dff-f36e-bd8c-a9f6-886a6e420b74.png)

こちらでは全角空白の強調表示に選択肢が提示されました。開発時に表示したサンプルソースコードでは全角空白が強調されていますが、これはextensionとしてはなにもやっていないので、VSCode全体の設定なのかなと思っていました。この選択肢は初めてみましたので、あとで深堀しておきます。

日本語プログラミング言語Mindユーザーとしては全角空白の強調はうるさいかなとも思っていたのですが、ユーザーさまのご意見を伺えればと思います。

# コードスニペットの様子
このバージョンではコードスニペットも一部の構文で対応しています。
詳しくは[こちらの記事](https://qiita.com/mylifewithviolin/items/5eec7787c1b76cd9fcea)をご参照ください。

# ソースコードをVSCodeでビルドする方法
Mind7とMind8のソースコードをVSCodeでビルドする環境を構築する方法はこちらもご参照ください。

https://qiita.com/mylifewithviolin/items/afe36d1fe26194e241ec

# おわりに
いかがでしたでしょうか？なにかのお役に立てればと思います。シンタックスハイライトの守備範囲はまだ不十分なので、追ってバージョンアップしていけたらと考えております:relaxed:
