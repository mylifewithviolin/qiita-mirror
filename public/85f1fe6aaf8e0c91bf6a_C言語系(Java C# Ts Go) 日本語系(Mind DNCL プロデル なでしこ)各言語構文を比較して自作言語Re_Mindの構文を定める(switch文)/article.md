# はじめに

Java C# Ts(TypeScript) GoといったC言語を由来とする新旧の言語とMind DNCLなどの日本語プログラミング言語の制御構文を比較して自作言語Re:Mindの構文を定めます。今回はswitch文。

自作言語Re:Mindの詳しい利用シーンのイメージは[こちらへ](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)。すみません、[設計段階です。](https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad)日本語プログラミング言語で、C言語を由来とする新旧言語へのトランスコンパイラ言語です。

## この記事内容の作業目的
今回は各言語のswitch文の構文を比較検討します。条件構文自体に分岐を抜けさせる働きがないことをフォークスルーといいます。言語によってはこのフォールスルーがあったり、なかったりする場合だったりしますので、トランスコンパイラ言語としてはこのあたりをどうさばくかは悩ましいところです。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（というよりまだ設計段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# Java C# Ts Goの新旧C言語系の構文イメージ
## Java
```java:Java
    switch(val){
        case const1:
            //todo1
            処理1;
            break;
        case const2:
            //todo2
            処理2;
            break;
        default:
            //todo3
            処理3;
            break;
    }

```
JavaはC/C++の構文を継承し、caseブロック内にbreakを書かないと次の合致するcase内に処理が移るフォールスルー動作ありの言語となります。Re:Mindはブレーク文に相当する構文を用意して、Javaをターゲット言語とする場合はフォールスルー動作もできるようにします。
valで使用できる変数の型、constで使用できる定数の型はJavaの仕様に準じます。

## C#
```cs:C#
    switch(val){
        case const1:
            //todo1
            処理1;
            break;
        case const2:
            //todo2
            処理2;
            break;
        default:
            //todo3
            処理3;
            break;
    }
```
C#はC/C++の構文を継承していますが、caseブロック内にbreakを書かないとエラーとなるフォールスルー動作なしの言語となります。Re:Mindはブレーク文に相当する構文を用意します。C＃をターゲット言語とする場合はブレーク相当構文が必須となります。
valで使用できる変数の型、constで使用できる定数の型はC#の仕様に準じます。

## TypeScript
```ts:TypeScript
    switch(val){
        case const1:
            //todo1
            処理1
            break
        case const2:
            //todo2
            処理2
            break
        default:
            //todo3
            処理3
            break
    }
```
TypeScriptは既定ではフォールスルー動作ありとなります。ただし、コンパイラオプションnoFallthroughCasesInSwitchをtrueとすることでcaseブロック内にbreakを書かないと警告がでるようになりますので、Re:Mindはブレーク文に相当する構文を用意して、TypeScriptをターゲット言語とする場合はTypeScriptコンパイラの挙動に準ずるとします。

## Go
```go:Go
    switch val{
        case const1:
            //todo1
            処理1
        case const2:
            //todo2
            処理2
        default:
            //todo3
            処理3
    }
```
Goは既定ではフォールスルー動作なしとなります。caseブロック内にbreakを書かなくてもフォールスルーは動作しません。Re:Mindはブレーク文に相当する構文を用意して、Goをターゲット言語とする場合はブレーク文に相当する構文を書いてもbreakを出力しないとします。

# 自作言語の構文イメージ
ここで自作言語の構文イメージの開示です。日本語トランスコンパイラ言語 Re:Mindは、制御構文の開始シンボルとして、◇、〇、・、□などの全角記号を用い、箇条書きされた日本文としての体裁を日本語ロジック記述言語 Re:Mindの構文とも共有しています。◇は分岐構文、〇はループ構文の開始と終了を表し、冗長な日本語表記がなくてもフロー図の表現に慣れている方が直感的に認識できることを考慮しています。
## Re:Mind
```mind:Re:Mind
        ◇値　で分岐する
        ◇定数1
            //todo1
            □処理する1
            □脱出する
        ◇定数2
            //todo2
            □処理する2
            □脱出する
        ◇既定
            //todo3
            □処理する3
            □脱出する
        ◇ここまで
```
◇定数1　がCase文に相当する構文で、ここでは実行文を書く場合改行必須です。「◇既定」がdefalut文相当です。
□脱出するがbreak文に相当します。ターゲット言語がフォークスルー動作しない言語の場合は書いても無視されます。
値は半角かっこ()で囲っても囲わなくても可です。

# Mind DNCLの日本語プログラミング言語の構文イメージ
では、続いて日本語プログラミング言語のグループです。

## Mind
```mind:Mind
    値で
    事例をとる
        定数１　処理する１ ※todo1
        定数２　処理する２ ※todo2
        例外なら　処理する３ ※todo3
    事例終り
```
```mind:Mind
    値で
    文字列事例をとる
        定数１　処理する１ ※todo1
        定数２　処理する２ ※todo2
        例外なら　処理する３ ※todo3
    事例終り
```
Mindはフォールスルー動作なしとなります。または値の型が文字列型の場合は「文字列事例をとる」となります。
「例外なら」がdefalut文相当です。

## DNCL
```mind:DNCL
    もし　値 = 定数１　ならば
        //todo1
        処理する１
    を実行し，そうでなくもし値 = 定数２ ならば
        //todo2
        処理する２
    を実行し，そうでなければ
        //todo3
        処理する３
    実行する
```
DNCLはswitch文に相当する構文がないようでした。If文の組み合わせで等価な構文を書くことができます。

VBAは日本語ではありませんが、中かっこ「{}」を使って区切ることはなく、構文の表現も自然言語の英語に近いので、こっちの方に寄せました。VBAにswitch関数がありますが、構文としてはSelect Case文のがswitch文に近いです。

## VBA（Excel用）
```vb:VisualBasic for Application
    Select Case val
        Case const1
            'todo1
            処理1
        Case const2
            'todo2
            処理2
        Case Else
            'todo3
            処理3
    End Select
```
VBAはフォールスルー動作なしとなります。Case Elseがdefalut文相当です。


# プロデル なでしこ 第2世代日本語プログラミング言語の構文イメージ（参考）
あまりと言いますかかなり詳しくはないのですが、参考にわたしの心の中での第2世代日本語プログラミング言語「プロデル」と「なでしこ」の構文も比較してみました。よくわかっていないので、間違っていたらごめんなさい。訂正します。
## プロデル
```mind:プロデル
    値について分岐
    定数１の場合
    　　　処理する１ //todo1
    定数２の場合
    　　　処理する２ //todo2
    他の場合
    　　　処理する３ //todo3
    分岐終わり

```
プロデルはフォールスルー動作なしのようです。「他の場合」がdefalut文相当です。

## なでしこV1
```mind:なでしこ
    値で条件分岐
        定数１ならば、処理する１。 //todo1
        定数２ならば、処理する２。 //todo2
        違えば、処理する３。 //todo3

```
なでしこV1はフォールスルー動作なしのようです。「違えば」がdefalut文相当です。
注意点としては、「条件分岐」と書いた後に改行してインデントで条件を字下げする必要があるそうです。


# おわりに


[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク

[Mind プログラミングマニュアル ３ 制御構文](http://www.scripts-lab.co.jp/mind/ver8/doc/03-Control-syntax.html#naraba)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[目次－プロデルで始める日本語プログラミング言語入門](https://wp.utopiat.net/produirefirststep/)

[日本語プログラミング言語「なでしこ」 制御構文](https://nadesi.com/doc/reference/syntax/1-6-koubun.htm)

https://qiita.com/mylifewithviolin/items/9214582528edcbd606ad
