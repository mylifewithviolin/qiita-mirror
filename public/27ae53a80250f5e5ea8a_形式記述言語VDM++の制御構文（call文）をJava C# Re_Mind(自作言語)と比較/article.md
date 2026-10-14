# はじめに

要求仕様記述段階での使用が主に想定されている数学的形式手法VDM(Vienna Development Method)[^1]のオブジェクト指向拡張言語VDM++ですが、ロジックの実装も記述できる構文が用意されています。本記事ではVDM++の制御構文（call文）をJavaとC#そして自作言語のRe:Mind[^2] と比較してみます。

## この記事内容の作業目的
VDM++の下記の制御構文[^3][^4]についていくつかの記事に分割して比較検討します。クラスの定義構文についてはこちらの記事[^5]を参照することができます。

・ブロック文
・コメント文
・代入文
・条件文
・ループ文
・**call文**　←本記事対象
・return文
・例外

VDM++はオブジェクト指向言語的な言語要素を持ち、数学的形式手法言語の中では一般のプログラミング言語のオブジェクト指向言語に近い面があります。また、VDMのような数学的形式手法を使わない場合は、一般的に自然言語の日本語で要求仕様が記述されているものと推察されます。本記事では数学的形式手法と自然言語の日本語記述とのはざまで、構造化された日本語が要求仕様記述に使えないか模索しています。


## この記事内容の保証
各言語で書かれた引用ソースの妥当性は保証されません。また、本記事に開示された自作言語の仕様は、開発中の仕様のため予告なく変更される場合があります。

# 構文比較
## VDM++
```vdm:VDM++
    doAnything: () ==> int
    doAnything() ==
    (
       i:int := 1;
       --todo1
       return i
    );
    doAnythingNoReturn: () ==> ()
    doAnythingNoReturn() ==
    (
       --todo1
       return
    );
    doAny: () ==> ()
    doAny() ==
    (
       j:int;
       --todo1
       j := doAnything();
       doAnythingNoReturn();  --call文
       return
    );
```
VDM++のcall文は戻り値のない操作を実行する際の構文でJavaやC#と同じです。上記例は引数がないパターン。戻り値のある関数を同様に記述して変数に代入しない場合どうなるかは未確認。
## Java
```java:Java
    int doAnything()
    {
       int i = 1;
       //todo1
       return i;
    }
    void doAnythingNoReturn()
    {
       //todo1
       return;
    }
    void doAny()
    {
       int i = 1;
       //todo1
       j = doAnything();
       doAnythingNoReturn();  //call文
       return;
    }
```
Javaのcall文は戻り値のない関数の関数名と実引数を記述します。戻り値のある関数を同様に記述して変数に代入しなくてもエラーになりません。
## C#
```cs:C#
    int doAnything()
    {
       int i = 1;
       //todo1
       return i;
    }
    void doAnythingNoReturn()
    {
       //todo1
       return;
    }
    void doAny()
    {
       int j;
       //todo1
       j = doAnything();
       doAnythingNoReturn();  //call文
       return;
    }
```
C#のcall文は戻り値のない関数の関数名と実引数を記述します。戻り値のある関数を同様に記述して変数に代入しなくてもエラーになりません。
## Re:Mind

```mind:Re:Mind
    ▽int doAnything()
        ・int i = 1
        //todo1
        □返す i
    △
    ▽void doAnythingNoReturn()
        //todo1
        □返す
    △
    ▽void doAny()
        ・int j
        //todo1
        □j = doAnything()
        □doAnythingNoReturn()  //call文
        □返す
    △
```
Re:Mindのcall文は戻り値のない関数の関数名と実引数を記述します。戻り値のある関数を同様に記述して変数に代入しなくてもエラーになりません。

# おわりに
VDM++はC/C++やJavaに近くプログラマに馴染みやすいとされていますが、いかがでしたでしょうか？
Re:MindはJavaやC#の経験者向けに設計された日本語プログラミング言語の一種で、ロジック仕様記述言語とトランスコンパイラ言語とで言語仕様を共有しています。ロジック仕様記述言語は疑似言語みたいなものですから、コンパイラを通さないことを前提にするならば未定義の関数を要件表記として使うこともできます。自然言語の日本語で記述するよりは厳密な構造的な記述が可能です。



[^1]: IBMのウィーン研究所で1960年代から70年代にかけて開発された形式手法。その実装には1996年にISO標準（ISO_IEC_13817-1）となったVDM-SLと、そのオブジェクト指向拡張のVDM++がある。
[^2]: Qiita [オープンな設計言語仕様 日本語ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/52f806777e6ea031de94) 参照
[^3]: FMVDM　[VDMTools 付属文書](http://fmvdm.org/doc/index-ja.h
[^4]: FMVDM-> github [[PDF] VDMTools VDM 言語マニュアル VDM++](https://github.com/vdmtools/vdmtools/raw/stable/doc-jp/lang-man/langmanpp_a4J.pdf)
[^5]: Qiita [要求仕様 形式記述言語VDM++ との構文比較 ロジック仕様記述言語 Re:Mind（リマインド）](https://qiita.com/mylifewithviolin/items/2a8c6dc66cead04536a8)
