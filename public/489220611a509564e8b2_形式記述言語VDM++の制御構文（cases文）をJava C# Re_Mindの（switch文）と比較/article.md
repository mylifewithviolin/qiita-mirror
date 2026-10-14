# はじめに

要求仕様記述段階での使用が主に想定されている数学的形式手法VDM(Vienna Development Method)[^1]のオブジェクト指向拡張言語VDM++ですが、ロジックの実装も記述できる構文が用意されています。本記事ではVDM++の制御構文（cases文）をJavaとC#そして自作言語のRe:Mind[^2] （switch文）と比較してみます。

## この記事内容の作業目的
VDM++の下記の制御構文[^3][^4]についていくつかの記事に分割して比較検討します。

・ブロック文
・代入文
・**条件文**　←本記事対象
・ループ文
・call文
・return文
・コメント文
・例外

VDM++はオブジェクト指向言語的な言語要素を持ち、数学的形式手法言語の中では一般のプログラミング言語のオブジェクト指向言語に近い面がありますが、かなり別物という面もあります。また、VDMのような数学的形式手法を使わない場合は、一般的に自然言語の日本語で要求仕様が記述されているものと推察されます。本記事では数学的形式手法と自然言語の日本語記述とのはざまで、構造化された日本語が要求仕様記述に使えないか模索しています。

クラスの定義構文についてはこちらの記事[^5]を参照することができます。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、本記事に開示された自作言語の仕様は、開発中の仕様のため予告なく変更される場合があります。

# 構文比較
## VDM++
```vdm:VDM++
    cases val:
        const1 -> (
            //todo1
        ),
        const2 -> (
            //todo2
        ),
        others -> (
             //todo3
        )
    end
```
VDM++のcases文はプログラミング言語のswitch文と大枠の構造は似ていますが、分岐先の選択肢には予約語的なトークン（switchに対するcase句のようなもの）はなく、選択肢の値からアロー演算子で選択先が記述されるというのが特徴的です。
```vdm:VDM++
    cases val:
        const11, const12 -> (
            //todo1
        ),
        const21, const21 -> (
            //todo2
        ),
        others -> (
             //todo3
        )
    end
```
分岐先の選択肢には値を列挙して、複数条件に合致させることができます。

## Java
```java:Java
    switch(val){
        case const1:
            //todo1
            break;
        case const2:
            //todo2
            break;
        default:
            //todo3
            break;
    }
```
JavaはC/C++の構文を継承し、caseブロック内にbreakを書かないと次の合致するcase内に処理が移るフォールスルー動作ありの言語となります。
## C#
```cs:C#
    switch(val){
        case const1:
            //todo1
            break;
        case const2:
            //todo2
            break;
        default:
            //todo3
            break;
    }
```
C#はC/C++の構文を継承していますが、caseブロック内にbreakを書かないとエラーとなるフォールスルー動作なしの言語となります。
## Re:Mind
```mind:Re:Mind
        ◇値　で分岐する
        ◇定数1
            //todo1
            □脱出する
        ◇定数2
            //todo2
            □脱出する
        ◇既定
            //todo3
            □脱出する
        ◇ここまで
```
値は半角かっこ()で囲っても囲わなくても可です。
◇定数1　がCase文に相当する構文で、ここでは実行文を書く場合改行必須です。「◇既定」がdefalut文相当です。
□脱出するがbreak文に相当します。

Re:MindはJavaやC#の経験者向けに設計された日本語プログラミング言語の一種で、ロジック仕様記述言語とトランスコンパイラ言語とで言語仕様を共有しています。自然言語の日本語で記述するよりは厳密な構造的な記述が可能です。どちらかというと箇条書きを想定していて、箇条書きの冒頭記号□◇〇▽が制御トークンになっています。


# おわりに
いかがでしたでしょうか？VDM++のcases文にアロー演算子が記法として採用されているのが興味深いです。


[^1]: IBMのウィーン研究所で1960年代から70年代にかけて開発された形式手法。その実装には1996年にISO標準（ISO_IEC_13817-1）となったVDM-SLと、そのオブジェクト指向拡張のVDM++がある。
[^2]: Qiita [オープンな設計言語仕様 日本語ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94) 参照
[^3]: FMVDM　[VDMTools 付属文書](http://fmvdm.org/doc/index-ja.h
[^4]: FMVDM-> github [[PDF] VDMTools VDM 言語マニュアル VDM++](https://github.com/vdmtools/vdmtools/raw/stable/doc-jp/lang-man/langmanpp_a4J.pdf)
[^5]: Qiita [要求仕様 形式記述言語VDM++ との構文比較 ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/2a8c6dc66cead04536a8)
