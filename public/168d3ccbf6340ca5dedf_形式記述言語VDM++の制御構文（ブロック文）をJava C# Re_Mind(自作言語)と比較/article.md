# はじめに

要求仕様記述段階での使用が主に想定されている数学的形式手法VDM(Vienna Development Method)[^1]のオブジェクト指向拡張言語VDM++ですが、ロジックの実装も記述できる構文が用意されています。本記事ではVDM++の制御構文（ブロック文）をJavaとC#そして自作言語のRe:Mind[^2] と比較してみます。

## この記事内容の作業目的
VDM++の下記の制御構文[^3][^4]についていくつかの記事に分割して比較検討します。

・**ブロック文**　←本記事対象
・コメント文
・代入文
・条件文
・ループ文
・call文
・return文
・例外処理

VDM++はオブジェクト指向言語的な言語要素を持ち、数学的形式手法言語の中では一般のプログラミング言語のオブジェクト指向言語に近い面があります。また、Re:MindはJavaやC#の経験者向けに設計された日本語プログラミング言語の一種で、自然言語の日本語で記述するよりは厳密な構造的な記述が可能です。クラスの定義構文の比較についてはこちらの記事[^5]を参照することができます。


## この記事内容の保証
各言語で書かれた引用ソースの妥当性は保証されません。また、本記事に開示された自作言語の仕様は、開発中の仕様のため予告なく変更される場合があります。

# 構文比較
## VDM++
```vdm:VDM++
    doAnything: () ==> ()
    doAnything() ==
    (
       --todo1
       --todo2
    )
```
VDM++のブロック文は()で囲われた範囲となります。
## Java
```java:Java
    void doAnything()
    {
       //todo1
       //todo2
    }
```
Javaのブロック文は{}で囲われた範囲となります。
## C#
```cs:C#
    void doAnything()
    {
       //todo1
       //todo2
    }
```
C#のブロック文は{}で囲われた範囲となります。
```mind:Re:Mind
    ▽void doAnything()
        //todo1
        //todo2
    △
```
Re:Mindのブロック文は▽の定義行の末尾から△で囲われた範囲となります

# おわりに
VDMのような数学的形式手法を使わない場合は、一般的に自然言語の日本語で要求仕様が記述されているものと推察されます。本記事では数学的形式手法と自然言語の日本語記述とのはざまで、構造化された日本語が要求仕様記述に使えないか模索しています。

[^1]: IBMのウィーン研究所で1960年代から70年代にかけて開発された形式手法。その実装には1996年にISO標準（ISO_IEC_13817-1）となったVDM-SLと、そのオブジェクト指向拡張のVDM++がある。
[^2]: Qiita [オープンな設計言語仕様 日本語ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94) 参照
[^3]: FMVDM　[VDMTools 付属文書](http://fmvdm.org/doc/index-ja.h
[^4]: FMVDM-> github [[PDF] VDMTools VDM 言語マニュアル VDM++](https://github.com/vdmtools/vdmtools/raw/stable/doc-jp/lang-man/langmanpp_a4J.pdf)
[^5]: Qiita [要求仕様 形式記述言語VDM++ との構文比較 ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/2a8c6dc66cead04536a8)
