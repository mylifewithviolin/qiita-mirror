# はじめに
日本語の文章を元にAIがソースコードを書いてくれるサービス「AI Programmer」がプロトタイプとして無償公開されています。対応するプログラミング言語にC#がありましたので、さっそく日本語プログラミング言語Mind DNCL なでしこ プロデル Re:Mind各言語の構文を与えて、結果がどうなるか確認してみました。まずは、If..else if文。

## この記事内容の作業目的
自作言語Re:Mindの構文仕様策定の参考情報としてAIによる構文認識度を検討します。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（というよりまだ企画段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# 各日本語プログラミング言語の構文によるC#への変換結果
## Mind 
```mind:Mind
    Iが　0より　大きい
        ならば
            Jが　0に　等しい
                ならば　※todo
                さもなければ　※todo
                つぎへ
                ※todo
        さもなければ
            Iが　0より　小さい
                ならば　※todo
                さもなければ　※todo
                つぎへ
        つぎへ
```
```cs:C#変換結果
    if (I > 0)
    {
        if (J == 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
    else
    {
        if (I < 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
```
Mindはif..else if文がなさそうなのでelse側の入れ子で対応しましたが、その点も忠実に変換されました。※todoがコメント文として変換されたのは、驚きでした。しかいし、こまかい点ですが、最初のif文の入れ子のif文の後のdoコメントtodoは無視されました。
## DNCL 
```mind:DNCL
    もし　I > 0　ならば
        もし　J ＝ 0　ならば
            //todo
        を実行し，そうでなければ
            //todo
        実行する
        //todo
    を実行し，そうでなくもし I < 0 ならば
        //todo
    を実行し，そうでなければ
        //todo
    実行する
```
```cs:C#変換結果
    if(i>0)
    {
        if(j==0)
        {
           //todo
        }
        else
        {
           //todo
        }
       //todo
    }
    else if(i<0)
    {
        //todo
    }
    else
    {
        //todo
    }
```
DNCLはif..else if文も含めて忠実に変換されました。こまかい点ですが、最初のif文の入れ子のif文の後のtodoも評価されました。

## なでしこ 
```mind:なでしこ
    もし、I > ０　ならば
        もし、J ＝ ０ ならば
        　　 //todo
        違えば
        　　 //todo
        ここまで
    　　 //todo
    違えば、もし、I < ０ ならば
    　　 //todo
    違えば
    　　 //todo
    ここまで
```
```cs:C#変換結果
    if (I > 0)
    {
        if (J = 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
    else
    {
        if (I < 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
```
なでしこはif..else if文のelse ifが認識されない場合があるようでif文の入れ子で変化されました。念のため数回リトライしている。こまかい点ですが、最初のif文の入れ子のif文の後のtodoは無視されました。
## プロデル 
```mind:プロデル
    もし i ＞ 0 なら
        もし j ＝ 0 なら
        　　//todo
        そうでなければ
        　　//todo
        もし終わり
    　　//todo
    他でもし i ＜ 0 なら
    　　//todo
    そうでなければ
    　　//todo
    もし終わり
```
```cs:C#変換結果
    if (i > 0)
    {
        if (j == 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
    else if (i < 0)
    {
        //todo
    }
    else
    {
        //todo
    }
```

プロデルはif..else if文も含めて忠実に変換されました。こまかい点ですが、最初のif文の入れ子のif文の後のtodoは無視されました。
## Re:Mind
* Re:Mind
```mind:Re:Mind
    ◇i > 0 の場合
        ◇j == 0 の場合
            //todo
        ◇他に
            //todo
        ◇ここまで
        //todo
    ◇他に i < 0 の場合
        //todo
    ◇他に
        //todo
    ◇ここまで
```
```cs:C#変換結果
    if (i > 0)
    {
        if (j == 0)
        {
            //todo
        }
        else
        {
            //todo
        }
    }
    else
    {
        //todo
    }
```
Re:Mindはelse ifが認識されずカットされました。ifに相当するキーワードを用いず対人的に直感性を意図した◇だけというのがあだとなっているようです。もう少し学習してもらえれば、いけるようになるのぁもしれません。こまかい点ですが、最初のif文の入れ子のif文の後のtodoも無視されました。
## まとめ
優劣を競うものではありませんが、DNCL構文が「AI Programmer」にとって一番認識しやすいというのは意外でした。
Re:Mindは記号表現を含むのである程度結果を予想していました。

# おわりに
ChatGPTで同じような企画を考えていたのですが、よりプログラミング言語に特化した日本発のサービス（有限会社ASRealが提供している日本語対応のAIサービス）を発見したので、そちらでやってみました。
わたしの方向性としてはAIとの共存です。いつも仕事ではQiitaにあがった事例もたいへん参考にしておりますし、参考情報の選択肢が広がるのは助かります。

[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク
https://aiprogrammer.hashlab.jp/

[Mind プログラミングマニュアル ３ 制御構文](http://www.scripts-lab.co.jp/mind/ver8/doc/03-Control-syntax.html#naraba)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[目次－プロデルで始める日本語プログラミング言語入門](https://wp.utopiat.net/produirefirststep/)

[日本語プログラミング言語「なでしこ」 制御構文](https://nadesi.com/doc/reference/syntax/1-6-koubun.htm)

https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c

https://qiita.com/mylifewithviolin/items/d1283d75f1984ddde8ec

https://qiita.com/HitoshiKubo/items/44d4bb36e8a6f8ac3d2e
