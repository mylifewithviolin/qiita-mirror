# はじめに

Java C# Ts(TypeScrpt) GoといったC言語を由来とする新旧の言語とMind DNCLなどの日本語プログラミング言語の制御構文を比較して自作言語Re:Mindの構文を定めます。今回はwhile文。

自作言語Re:Mindの詳しい利用シーンのイメージは[こちらへ](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)。すみません、[設計段階です。](https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad)日本語プログラミング言語で、C言語を由来とする新旧言語へのトランスコンパイラ言語です。

## この記事内容の作業目的
今回は各言語のwhile文の構文を比較検討します。プログラミング言語によっては、ループの処理文を一度実行した後に継続条件式を評価する、後判定繰り返し構文をサポートする場合がありますので、トランスパイラ言語としてはこのあたりをどうさばくかが問題となります。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（というよりまだ設計段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# Java C# Ts Goの新旧C言語系の構文イメージ
## Java
```java:Java
    int i=0;
    while (i<10) {
        //todo
        反復処理;
        i++;
    }
```
```java:Java
    int i=0;
    do {
        //todo
        反復処理;
        i++;
    } while (i<10);
```
Javaは後判定繰り返し構文do-while文をサポートします。
```java:Java
    int i=0;
    int j=0;
    int k=0;
    while (i<10) {
        //todo
        反復処理;
        k++;
        j++;
        if(j>8) break;
        if(k<4) continue;
        i++;
    }
```
ループ本体内に条件分岐式を記述して、while文の判定が成立する前にループを脱出したり(break)、ループの先頭に復帰(continue)してループ本体の処理をスキップさせることができます。
## C#
```cs:C#
    int i=0;
    while (i<10) {
        //todo
        反復処理;
        i++;
    }
```
```cs:C#
    int i=0;
    do {
        //todo
        反復処理;
        i++;
    } while (i<10);
```
C#は後判定繰り返し構文do-while文をサポートします。
```cs:C#
    int i=0;
    int j=0;
    int k=0;
    while (i<10) {
        //todo
        反復処理;
        k++;
        j++;
        if(j>8) break;
        if(k<4) continue;
        i++;
    }
```
ループ本体内に条件分岐式を記述して、while文の判定が成立する前にループを脱出したり(break)、ループの先頭に復帰(continue)してループ本体の処理をスキップさせることができます。
## TypeScript
```ts:TypeScript
    let i: number=0
    while (i<10) {
        //todo
        反復処理
        i++
    }
```
```ts:TypeScript
    let i: number=0
    do {
        //todo
        反復処理
        i++
    } while (i<10)
```
Tsは後判定繰り返し構文do-while文をサポートします。
```ts:TypeScript
    let i: number=0
    let j: number=0
    let k: number=0
    while (i<10) {
        //todo
        反復処理
        k++
        j++
        if(j>8) break
        if(k<4) continue
        i++
    }
```
ループ本体内に条件分岐式を記述して、while文の判定が成立する前にループを脱出したり(break)、ループの先頭に復帰して(continue)ループ本体の処理をスキップさせることができます。
## Go
```go:Go
    i:=0
    for i<10 {
        //todo
        反復処理
        i++
    }
```
```go:Go
    i:=0
    for {
        //todo
        反復処理
        i++
        if i<10 break
    }
```
Goにはwhile文はないので、等価なfor文を出力します。前判定の場合はfor文に判定条件式だけを書くことで等価となります。後判定の場合は条件式とbreak文を末尾に記述します。
```go:Go
    i:=0
    j:=0
    k:=0
    for i<10 {
        //todo
        反復処理
        k++
        j++
        if j>8 {
            break
            }
        if k<4 {
            continue
            }
        i++
    }
```
for文の判定が成立する前にループを脱出したり(break)、ループの先頭に復帰して(continue)ループ本体の処理をスキップさせることができます。

# 自作言語の構文イメージ
ここですぐに自作言語の構文の開示です。日本語トランスコンパイラ言語 Re:Mindは、制御構文の開始シンボルとして、◇、〇、・、□などの全角記号を用い、箇条書きされた日本文としての体裁を日本語ロジック記述言語 Re:Mindの構文とも共有しています。◇は分岐構文、〇はループ構文の開始と終了を表し、冗長な日本語表記がなくてもフロー図の表現に慣れている方が直感的に認識できることを考慮しています。
## Re:Mind
```mind:Re:Mind
    ・int i=0
    〇(i<10) の間は繰り返す
        //todo
        □反復処理
        □i++
    〇ここまで
```
Re:Mindの前判定繰り返し構文は、最初の〇の後に　「(条件式) の間は繰り返す」を記述し、末尾の〇に「ここまで」を記述します。

```mind:Re:Mind
    ・int i=0
    〇ここから
        //todo
        □反復処理
        □i++
    〇(i<10) の間は繰り返す
```
Re:Mindは後判定繰り返し構文をサポートします。その場合、最初の〇の後に「ここから」を記述し、末尾の〇に判定文　「(条件式) の間は繰り返す」を記述します。

```mind:Re:Mind
    ・int i=0
    ・int j=0
    ・int k=0
    〇(i<10) の間は繰り返す
        //todo
        □反復処理
        □k++
        □j++
        ◇j>8 の場合
            □脱出する
        ◇ここまで
        ◇k<4 の場合
            □ループ先頭へ
        ◇ここまで
        □i++
    〇ここまで
```
ループ本体内に条件分岐式を記述して、ループ続行の判定が成立する前にループを脱出したり(□脱出する)、ループの先頭に復帰して(□ループ先頭へ)ループ本体の処理をスキップさせることができます。

# Mind DNCLの日本語プログラミング言語の構文イメージ
では、続いて日本語プログラミング言語のグループです。

## Mind
```mind:Mind
    iは 整数。
    i:= 0
    ここから
            iが10以上？
                ならば　打ち切り
                つぎに
            反復処理 ※todo
            iを 1つ増加
    繰り返すこと。
```
```mind:Mind
    iは 整数。
    i:= 0
    ここから
            反復処理 ※todo
            iが10以上？
                ならば　打ち切り
                つぎに
            iを 1つ増加
    繰り返すこと。
```
Mindにはwhile文に相当する構文はない ~~？~~ ので、ここから～繰り返すのループ構文内に条件式と「打ち切り」文を記述します。条件式と「打ち切り」文の記述と、本体の反復処理の前後関係で、前判定か後判定かとなります。
```mind:Mind
    iは 整数。
    jは 整数。
    kは 整数。
    i:= 0
    j:= 0
    k:= 0
    ここから
            iが10以上？
                ならば　打ち切り
                つぎに
            反復処理 ※todo
            jを 1つ増加
            kを 1つ増加
            jが 8より 大きい
                ならば　打ち切り
                つぎに
            kが 4より 小さい
                ならば　もう一度
                つぎに
            iを 1つ増加
    繰り返すこと。
```
また、Mindのループの先頭に復帰させるcontinue文に相当する構文は ~~ない模様。（あったらごめんなさい、訂正します。）~~ 条件式と「もう一度」文を記述します。

## DNCL
```mind:DNCL
    I ← 0
    I＜10 の間，
        //todo   反復処理
        I ← I + 1
    を繰り返す
```
```mind:DNCL
    I ← 0
    繰り返し，
        //todo   反復処理
        I ← I + 1
    を， I＜10 になるまで実行する
```
DNCLは前判定繰り返し構文、後判定繰り返し構文の両方をサポートしています。
ループ続行の判定が成立する前にループを脱出したり(break文相当)、ループの先頭に復帰してループ本体の処理をスキップさせる構文(continue文相当)は定義されていないようです。

VBAは日本語ではありませんが、中かっこ「{}」を使って区切ることはなく、構文の表現も自然言語の英語に近いので、こっちの方に寄せました。

## VBA（Excel用）
```vb:VisualBasic for Application
    Dim i As Long
    i = 0
    Do While i < 10 
      'todo 反復処理      
       i = i + 1
    Loop
```
```vb:VisualBasic for Application
    Dim i As Long
    i = 0
    Do 
      'todo 反復処理      
      i = i + 1
    Loop While i < 10 
```
VBAは後判定繰り返し構文do-loop-while文をサポートします。

```vb:VisualBasic for Application
    Dim i As Long
    Dim j As Long
    Dim k As Long
    i = 0
    j = 0
    k = 0
    Do While i < 10 
      'todo  反復処理
       j = j + 1
       k = k + 1
       If j > 8 Then Exit Do
       If K < 4 Then GoTo continue     
      i = i + 1
continue:
    Loop
```
また、VBAにはループ本体内に条件分岐式を記述して、while文の判定が成立する前にループを脱出させる(Exit Do)構文はありますが、ループの先頭に復帰させるcontinue文に相当する構文はないため、上記のようにGoTo文でループ文末尾の直前のラベルにジャンプさせることで等価な処理とすることができます。Re:Mindとしてジャンプ構文をサポートするかは未定です。


# プロデル なでしこ 第2世代日本語プログラミング言語の構文イメージ（参考）
あまりと言いますかかなり詳しくはないのですが、参考にわたしの心の中での第2世代日本語プログラミング言語「プロデル」と「なでしこ」の構文も比較してみました。よくわかっていないので、間違っていたらごめんなさい。訂正します。
## プロデル
```mind:プロデル
    【i:整数】
    i = 0
    繰り返す
    　　もしiが10以上なら、繰り返しから抜け出す
        //todo
       反復処理
        i = i + 1
    繰り返し終わり
```
```mind:プロデル
    【i:整数】
    i = 0
    繰り返す
        //todo
       反復処理
        i = i + 1
    　　もしiが10以上なら、繰り返しから抜け出す
    繰り返し終わり

```
プロデルにはwhile文に相当する構文はない？ので、繰り返す～繰り返し終わりのループ構文内に条件式と「繰り返しから抜け出す」文を記述します。条件式と「抜け出す」文の記述と、本体の反復処理の前後関係で、前判定か後判定かとなります。
また、プロデルにはループの先頭に復帰させるcontinue文に相当する構文はない模様。（あったらごめんなさい、訂正します。）ジャンプ文があればVBAのような等価構文を出力させれます。

## なでしこ
```mind:なでしこ
    iとは整数。
    i = 0
    (i < 10)の間
        反復処理
        i = i + 1
    ここまで
```
```mind:なでしこ
    iとは整数。
    i = 0
    (0 < 1)の間
        反復処理
        i = i + 1
        もし、iが10以上ならば、抜ける
    ここまで
```
なでしこは前判定繰り返し文はサポートしているようですが、後判定繰り返し文はなさそうでした。（あったらごめんなさい、訂正します。）そのため、前判定繰り返し文の判定式を常に成立するダミー式として無限ループにして、反復処理とカウント増分の後に条件分岐で脱出させます。
また、なでしこV1にはループの先頭に復帰させるcontinue文に相当する構文はない模様。（あったらごめんなさい、訂正します。）ジャンプ文があればVBAのような等価構文を出力させれます。

# おわりに


[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク

[Mind プログラミングマニュアル ３ 制御構文](http://www.scripts-lab.co.jp/mind/ver8/doc/03-Control-syntax.html#naraba)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[目次－プロデルで始める日本語プログラミング言語入門](https://wp.utopiat.net/produirefirststep/)

[日本語プログラミング言語「なでしこ」 制御構文](https://nadesi.com/doc/reference/syntax/1-6-koubun.htm)

https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad

[日本語トランスコンパイラ言語 Re:Mind （自作言語）と他言語との構文比較（IF文）](https://qiita.com/mylifewithviolin/items/579e6c9b77dcd2adda0f)
[日本語トランスコンパイラ言語 Re:Mind （自作言語）と他言語との構文比較（FOR文）](https://qiita.com/mylifewithviolin/items/b669e02ecc8595e72b8f)
[Java C# Ts GoのC系言語 Mind DNCLの日本語系言語の制御構文を比較して自作言語Re:Mindの構文を定める(if..else if..else文)](https://qiita.com/mylifewithviolin/items/d1283d75f1984ddde8ec)
[Java C# Ts GoのC系言語 Mind DNCLの日本語系言語の制御構文を比較して自作言語Re:Mindの構文を定める(for..if文)](https://qiita.com/mylifewithviolin/items/deffa0aea063fc06fe60)
[C言語系(Java C# Ts Go) 日本語系(Mind DNCL)各言語構文を比較して自作言語Re:Mindの構文を定める(変数宣言・実行文・関数宣言)](https://qiita.com/mylifewithviolin/items/89ac25290d2c684dd5cc)
[C言語系(Java C# Ts Go) 日本語系(Mind DNCL プロデル なでしこ)各言語構文を比較して自作言語Re:Mindの構文を定める(switch文)](https://qiita.com/mylifewithviolin/items/85f1fe6aaf8e0c91bf6a)
