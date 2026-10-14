# はじめに
Java C# Ts GoといったC言語を由来とする新旧の言語とMind DNCLなどの日本語プログラミング言語の制御構文を比較して自作言語Re:Mindの構文を定めます。
今回は変数宣言・実行文・関数宣言。

自作言語Re:Mindの詳しい利用シーンのイメージは[こちらへ](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)。すみません、企画段階です。日本語プログラミング言語です。

## この記事内容の作業目的
今回は各言語の変数宣言・実行文・関数宣言の構文を比較検討します。

## この記事内容の保証
※この記事には実装的な情報が含まれます。各言語で書かれた引用ソースの妥当性は保証されません。また、自作言語は開発中（というよりまだ企画段階）のため、本記事に開示された仕様は予告なく変更される場合があります。

# Java C# Ts Goの新旧C言語系の構文イメージ

なるべく長くならずイメージが比較しやすいよう、変数の型は整数、文字列、真偽の3つとします。関数は値を返すものと返さないもの2つとします。変数宣言、関数実行、関数宣言の3セットで比較します。初期化のリテラルの内容で型を決定する宣言とか、とりあえず今回は対象外です。


## Java
```java:Java
    /** 年齢 */
    int nenrei = 34;
    /** 名前 */
    String namae = "花子";
    /** 特待区分 */
    Bool tokutaiKubun = true; 

    nenrei= getMembersAge(namae,tokutaiKubun);
    memberNenreiSettei(namae,tokutaiKubun);

    /**
    * メンバーの年齢を取得する
    * @param name 名前
    * @param kubun 特待区分
    * @return 年齢
    */
    public int getMembersAge(string name,bool kubun)
    {
         //todo
        return year;
    }
    /**
    * メンバーの年齢を設定する
    * @param name 名前
    * @param kubun 特待区分
    */
    private void memberNenreiSettei(string name,bool kubun)
    {
         //todo
    }

```
のちに説明する理由のため、一般的なjava docのコメント付きとしています。
## C#
```cs:C#
    /// <summary>年齢</summary>
    int nenrei = 34;
    /// <summary>名前</summary>
    string namae = "花子";
    /// <summary>特待区分</summary>
    bool tokutaiKubun = true; 

    nenrei= GetMembersAge(namae,tokutaiKubun);
    MemberNenreiSettei(namae,tokutaiKubun);

 
    /// <summary>メンバーの年齢を取得する</summary>
    /// <param name="name">名前</param>
    /// <param name="kubun">特待区分</param>
    /// <returns>年齢</returns>
    public int getMembersAge(string name,bool kubun)
    {
         //todo
        return year;
    }

    /// <summary>メンバーの年齢を設定する</summary>
    /// <param name="name">名前</param>
    /// <param name="kubun">特待区分</param>
    private void memberNenreiSettei(string name,bool kubun)
    {
         //todo
    }
```
のちに説明する理由のため、一般的なC# documentのコメント付きとしています。
## TypeScript
```ts:TypeScript
    /** 年齢 */
    let nenrei:number = 34;
    /** 名前 */
    let namae:string  = "花子";
    /** 特待区分 */
    let tokutaiKubun:boolean  = true; 

    nenrei= getMembersAge(namae,tokutaiKubun)
    memberNenreiSettei(namae,tokutaiKubun)

    /**
    * メンバーの年齢を取得する
    * @param name 名前
    * @param kubun 特待区分
    * @return 年齢
    */
    getMembersAge(name:string ,kubun:boolean): number
    {
         //todo
        return year
    }
    /**
    * メンバーの年齢を設定する
    * @param name 名前
    * @param kubun 特待区分
    */
    memberNenreiSettei(name:string ,kubun:boolean)
    {
         //todo
    }
```
のちに説明する理由のため、Tsも採用した一般的なjava docのコメント付きとしています。

## Go
```go:Go
    //nenrei  年齢 
    var nenrei int = 34;
    //namae 名前 
    var namae string = "花子";
    // tokutaiKubun 特待区分 
    var tokutaiKubun Boolean = true; 

    nenrei= getMembersAge(namae,tokutaiKubun)
    memberNenreiSettei(namae,tokutaiKubun)

    // メンバーの年齢を取得する
    // name 名前
    // kubun 特待区分
    //return 年齢
    func getMembersAge(name string, kubun bool) int
    {
         //todo
        return year
    }

    // メンバーの年齢を設定する
    // name 名前
    // kubun 特待区分
    func memberNenreiSettei(name string, kubun bool)
    {
         //todo
    }
```
Go docの仕様はよくわかっていませんが、比較イメージとして記載。

各言語の関数宣言の間に挟まれているtodoは各言語のコメントアウト符号によるコメントです。なにか実行文が書けますの意。returnは戻り値指定型の変数を返している想定で宣言は省略。


# 自作言語の構文イメージ
ここですぐに自作言語の構文の開示です。

## Re:Mind
```mind:Re:Mind
    /** nenrei */
    ・int 年齢 = 34;
    /** namae */
    ・string 名前 = "花子";
    /** tokutaiKubun */
    ・bool 特待区分 = true; 

    □年齢 = メンバーの年齢を取得する(名前,特待区分)
    □(名前,特待区分)で メンバーの年齢を設定する
    
    /**
    * getMembersAge
    * @param 名前 name
    * @param 特待区分 kubun
    * @return 年齢
    */
    ▽public int メンバーの年齢を取得する(string 名前,bool 区分)
         //todo
        齢を　返す
    △
    /**
    * memberNenreiSettei
    * @param 名前 name
    * @param 特待区分 kubu
    */
    ▽private メンバーの年齢を設定する(string 名前,bool 区分)
         //todo
    △
```
ご覧になっていただくとすぐわかるかと思いますが、日本語プログラミング言語というよりは、関数形を手続きの記述形式としている前記言語に寄せた構文となっています。変数の型は変換対象言語の物理型名をそのままかけるとします。ここでは記述していませんが、エイリアス指定して日本語型名を使うこともできるようにします。

分岐やループを直感的に表す全角記号「◇」や「〇」を積極的にトークンとして活用しようと考えているのが、「Re:Mind」（自作言語リマインド）の特徴ですが、日本語のまま記述すると、書くのが手間になりそうな構文はある程度の半角文字の記号表現（慣れれば直感的にわかりそうな範囲）を許容しようかなと考えております。カッコ内の記法は変換対象言語の構文に準拠します。

また、コンパイラとして実装することを退けるものではありませんが、当面はソースコードトランスコンパイラとして実装する想定から、基本となる自然言語が英語系の言語への変換となるため、通常の英語系プログラミング言語のコメントとして書く内容の逆を書く想定としています。英語の変数名、関数名に日本語の説明ではなく、日本語の変数名、関数名に英語またはローマ字の想定語句を記述し、コンパイラに指示します。はしょった場合はユニコードの日本語が変数名、関数名になることも許容します。

# Mind DNCLの日本語プログラミング言語の構文イメージ
では、続いて日本語プログラミング言語のグループです。
VBAは日本語ではありませんが、中かっこ「{}」を使って区切ることはなく、構文の表現も自然言語の英語に近いので、こっちの方に寄せました。

## VBA（Excel用）
```vb:VisualBasic for Application
    '年齢 
    Dim nenrei As Integer : nenrei = 34
    '名前 
    Dim namae As String : namae = "花子"
    '特待区分 
    Dim tokutaiKubun AS Boolean : tokutaiKubun= True 

    nenrei= getMembersAge(namae,tokutaiKubun)
    memberNenreiSettei namae,tokutaiKubun

    'メンバーの年齢を取得する
    'name 名前
    'kubun 特待区分
    'return 年齢
     Function GetMembersAge(string name,bool kubun) As Integer
         'todo
        GetMembersAge = year
    End Function

    'メンバーの年齢を設定する
    'name 名前
    'kubun 特待区分
    Sub MemberNenreiSettei(string name,bool kubun)
         'todo
    End Sub
```
## Mind
```mind:Mind
年齢は	変数。
名前は　文字列実体　長さ　１０桁。
特待区分は	変数。

名前と　特待区分で　メンバーの年齢を取得し　年齢に　入れる。
名前と　特待区分で　メンバーの年齢を設定する。

変数初期化とは
　　　　年齢に　34を　入れ
　　　　名前に　「花子」を　入れ
　　　　特待区分に　1を　入れ。

メンバーの年齢を取得するとは
            （名前、区分　→　整数）※コメントなので動作としては意味が無い
       ※todo
　　　　齢をつむこと。

メンバーの年齢を設定するとは 　処理単語
            （名前、区分　→　・）
       ※todo
　　　　・・・・・すること。
```
※2023/02/20訂正　正しくは「数値」でなく「変数」。Mindの整数型の変数宣言シンボルは「変数」。
## DNCL
```mind:DNCL
    nenrei　← メンバーの年齢を取得する(namae,tokutaiKubun)
    メンバーの年齢を設定する(namae,tokutaiKubun)
```
DNCLは変数の宣言構文や関数手続きの宣言方法は定義されていない模様。存在するならば、確認でき次第追記訂正します。



# プロデル なでしこ 第2世代日本語プログラミング言語の構文イメージ（参考）
あまりと言いますかかなり詳しくはないのですが、参考にわたしの心の中での第2世代日本語プログラミング言語「プロデル」と「なでしこ」の構文も比較してみました。よくわかっていないので、間違っていたらごめんなさい。訂正します。
## プロデル
```mind:プロデル
【年齢:整数】
【名前:文字列】
【特待区分:真偽値】

年齢 = メンバーの年齢を取得する(名前と特待区分の)
名前と特待区分でメンバーの年齢を設定する

【名前】を、【特待区分】で、メンバーの年齢を取得する手順
        //todo
    齢を返す
終わり

【名前】を、【特待区分】で、メンバーの年齢を設定する手順
        //todo
終わり

```

## なでしこ
```mind:なでしこ
年齢とは整数。
名前とは文字列。
特待区分とは整数。

年齢 = メンバーの年齢を取得する(名前と特待区分の)
名前と特待区分でメンバーの年齢を設定する

●メンバーの年齢を取得する(名前と特待区分の)
        //todo　　v1はかっこ後方
    それは歳
ここまで

●(名前と特待区分で)メンバーの年齢を設定するとは
        //todo  v3はかっこ前方
ここまで

```
2言語とも独特の助詞などのルールを覚えるのに少々抵抗を感じるところがありました。ただ、この点はどのようなプログラミング言語でもついてまわる話で、単に筆者がC言語系慣れしているせいで、そうでない場合や新手の記号記法とかはとまどうのはいっしょかと思います。

Re:Mindは結局のところ慣れている人が多い現場で利用度の高い言語構文に寄せているので、これらの言語に慣れていれば直感的にわかりやすく、余分な構文ルールを覚えなくてよいという記述環境を構築していきます。

# おわりに


[日本語トランスコンパイラ言語](https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde)という企画を実現・設計・実装していくには、スキル上の課題や未獲得の知見など多数あることが予想されます。Qiita様の場をお借りして、獲得したスキルや知見の共有、いたらない点のご支援をいただければと考えています。

# 参考リンク

[Mind プログラミングマニュアル ３ 制御構文](http://www.scripts-lab.co.jp/mind/ver8/doc/03-Control-syntax.html#naraba)

[共通テスト手順記述標準言語 (DNCL) の説明](https://www.dnc.ac.jp/albums/abm.php?d=88&f=abm00001247.pdf&n=%E4%BB%A4%E5%92%8C%EF%BC%93%E5%B9%B4%E5%BA%A6%E8%A9%A6%E9%A8%93%E5%85%B1%E9%80%9A%E3%83%86%E3%82%B9%E3%83%88%E6%89%8B%E9%A0%86%E8%A8%98%E8%BF%B0%E6%A8%99%E6%BA%96%E8%A8%80%E8%AA%9E%EF%BC%88DNCL%EF%BC%89%E3%81%AE%E8%AA%AC%E6%98%8E.pdf)

[目次－プロデルで始める日本語プログラミング言語入門](https://wp.utopiat.net/produirefirststep/)

[日本語プログラミング言語「なでしこ」 制御構文](https://nadesi.com/doc/reference/syntax/1-6-koubun.htm)

https://qiita.com/mylifewithviolin/items/9d58db8a101807c19bde

https://qiita.com/mylifewithviolin/items/ebb406bf5ea7a4eea24c

https://qiita.com/jpl_produire/items/0aed0a6699e89a794211

https://qiita.com/kujirahand/items/03d506d71472c2361de2
