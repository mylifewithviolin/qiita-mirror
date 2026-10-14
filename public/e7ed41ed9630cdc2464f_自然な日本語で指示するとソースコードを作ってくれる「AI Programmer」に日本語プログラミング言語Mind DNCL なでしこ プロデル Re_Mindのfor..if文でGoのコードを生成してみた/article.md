# はじめに

日本語の文章を元にAIがソースコードを書いてくれるサービス「AI Programmer」がプロトタイプとして無償公開されています。対応するプログラミング言語にGoがありましたので、さっそく日本語プログラミング言語Mind DNCL なでしこ プロデル Re:Mind各言語の構文を与えて、結果がどうなるか確認してみました。今回はfor文内にif文の脱出がある構文。

## この記事内容の作業目的
自作言語Re:Mindの構文仕様策定の参考情報としてAIによる構文認識度を検討します。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（というよりまだ企画段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# 各日本語プログラミング言語の構文によるGoへの変換結果
## Mind 
```mind:Mind
    １０を　回数指定して
       ※todo
        Jが　0に　等しい
            ならば　打ち切り
            つぎへ
       ※todo
    繰り返す
```
```go:go変換結果
    for i := 0; i < 10; i++ {
    	if i == 0 {
    		break
    	}
    	fmt.Println(i)
    }
```
Mindの「10を回数して」が、for i := 0; i < 10; i++に変換されました。※todoがコメント文として変換されませんでした。また、if文の後のdoコメントtodoは無視され？カウンタのコンソール文が意図せず変換されました。
## DNCL 
```mind:DNCL
    i を 1 から 10 まで 1 ずつ増やしながら，
        //todo
        もし　j = 0　ならば
            //脱出文は未定義？
        実行する
        //todo
    を繰り返す
```
```go:go変換結果
    for i := 1; i <= 10; i++ {
        if j == 0 {
            //todo
        }
        //todo
    }
```
DNCLは「i を 1 から 10 まで 1 ずつ増やし」が忠実に変換されました。こまかい点ですが、if文の後のtodoコメントも評価されました。しかし、if文の前のは無視され、脱出文未定義のコメントがtodoコメントに置換されました。

## なでしこ 
```mind:なでしこ
    カウンタで０から９まで繰り返す
        //todo
        もし、Jが０ならば、抜ける
        //todo
    ここまで
```
```go:go変換結果
    for i := 0; i < 10; i++ {
        if j == 0 {
            break
        }
    }
```
なでしこは「カウンタで０から９まで繰り返す」がfor i := 0; i < 10; i++ に変換されました。i := 0; i <= 9;としなかったのはなぜか？やや謎。こまかい点ですが、if文の前後のtodoコメントは無視されました。
## プロデル 
```mind:プロデル
    Iを0から1ずつ増やしながら9まで繰り返す
        //todo
        もしJが0なら、繰り返しから抜け出す
        //todo
    繰り返し終わり
```
```go:go変換結果
    for i := 0; i <= 9; i++ {
        if j == 0 {
            break
        }
    }
```

プロデルは「Iを0から1ずつ増やしながら9まで繰り返す」がfor i := 0; i <= 9; i++ に忠実に変換されました。こまかい点ですが、if文の前後のtodoコメントは無視されました。
## Re:Mind
```mind:Re:Mind
    〇i=0,i<10,i++ 繰り返す
        //todo
        ◇j==0 の場合 やめる
        //todo
    〇ここまで
```
```go:go変換結果
    for i := 0; i < 10; i++ {
      if j == 0 {
        break
      }
    }
```
Re:Mindは日本語として不自然な「i=0,i<10,i++」がfor i := 0; i < 10; i++ に忠実に変換されました。こまかい点ですが、if文の前後のtodoコメントは無視されました。
## まとめ
脱出文未定義のDNCLを除き、各言語ともbreak文への変換は正常に行えました。
Re:Mindの日本語として不自然な「i=0,i<10,i++」が「AI Programmer」によってどのように変換されるか注目していましたが、思いのほか素直に解釈してもらえたという結果となりました。


# おわりに
ChatGPTで同じような企画を考えていたのですが、よりプログラミング言語に特化した日本発のサービスを発見したので、[If..else if文をC#に変換](https://qiita.com/mylifewithviolin/items/9beb1e7f2267a91c7edc)に続いてやってみました。
わたしの方向性としてはAIとの共存です。いつも仕事ではQiitaにあがった事例もたいへん参考にしておりますし、参考情報の選択肢が広がるのは助かります。目指すところは微妙に似ていて違うのですが、自然言語を入力ソースとするトランスコンパイラ言語の領域はAIによる実装は増えていきそうですね。プログラミング言語同士のAIによる変換もすでにあるようです。

[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク
https://aiprogrammer.hashlab.jp/

https://qiita.com/HitoshiKubo/items/44d4bb36e8a6f8ac3d2e

[Mind プログラミングマニュアル ３ 制御構文](http://www.scripts-lab.co.jp/mind/ver8/doc/03-Control-syntax.html#naraba)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[目次－プロデルで始める日本語プログラミング言語入門](https://wp.utopiat.net/produirefirststep/)

[日本語プログラミング言語「なでしこ」 制御構文](https://nadesi.com/doc/reference/syntax/1-6-koubun.htm)

https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c

https://qiita.com/mylifewithviolin/items/d1283d75f1984ddde8ec
