# はじめに
数学的形式手法VDM(Vienna Development Method)[^1] のオブジェクト指向拡張言語VDM++の検証ツールWindows版[^2][^3] をお試し的に使ってみています。

## この記事の概要
[前回の記事](https://qiita.com/mylifewithviolin/items/1ab2471444b141fbb12d)では、九州大学さんが作成されたVDM++開発手法ガイドライン1.0[^4] にある事前条件、事後条件がどのようなソースコードになるのかツールのJavaコード生成機能で確認してみたのですが、思いのほかコード生成量が多かったため、今回は少し課題をシンプル化してみます。例題モチーフの概要、細かい詳細は前回記事と重複しますので、そちらをご参照ください。

## この記事内容の作業環境
Windows11 Pro 22H2  ※msvcr100SP1インストール済[^5]
The VDM++ Toolbox v9.0.7


# 化学プラントアラームシステムのクラス定義
## 化学プラントアラームシステムの3つのクラス
VDM++開発手法ガイドラインでは化学プラントの簡単なアラームシステムの適用事例が説明されていて、「プラント」「専門家」「アラーム」の３つのクラスからなる構成が例示されています。

それら3つのクラスのうち「専門家」のVDM++によるクラス定義構文を確認します。クラス名の「クラス」装飾はそのままとしています。
### 「専門家」のVDM++のクラス定義
```mind:VDM++
class 専門家クラス
types
    public 資格型= <機械> | <化学> | <生物> | <電気>;
instance variables
operations
    資格を得る:()==>  set of 資格型
    資格を得る()==
        is not yet specified;
end 専門家クラス
```

### VDM++クラス定義をVDM++検証ツールに読み込ませる
最終的にJavaコード生成可能な状態となったクラス定義を以下に示します。
```mind:plant.vpp
\section{専門家クラス}

\begin{vdm_al}
class 専門家クラス
types
    public 資格型 = <機械> | <化学> | <生物> | <電気>;
instance variables
operations
    public 資格を得る:()==>  set of 資格型
    資格を得る()==
        is not yet specified;

end 専門家クラス

\end{vdm_al}
```

# VDM++検証ツールに読み込ませたファイルとフォルダの構成
```
examples\test\plant.vpp
examples\test\test.opt
examples\test\test.prj
examples\test\test.wgm
```
今回は１つのフォルダtestにtestプロジェクトとして「専門家」のクラス定義ファイル.vppを格納しています。

## Javaコード生成後のファイルとフォルダの構成
上記のソースコードファイルとプロジェクトファイルを除くと下記のようなファイルとサブフォルダが生成されました。
```
examples\test\専門家クラス.java
examples\test\external_専門家クラス.java
examples\test\quotes
examples\test\quotes\化学.java
examples\test\quotes\生物.java
examples\test\quotes\電気.java
```

# 生成されたJavaコード
本記事の本題はクラス定義の中身をJavaコード出力で確認することにありますので、生成されたjavaのコード内容をそれぞれ見てみます。quotesフォルダ生成のクラスは化学.javaを代表例とします。またツールが出力する決まり文句のコメントは削除してあります。
## quotes\化学.java
```java:化学クラス.java
package quotes;

public class 化学 {

  static private int hc = 0;
  public 化学 () {
    if (hc == 0) 
      hc = super.hashCode();
  }

  public int hashCode () {
    return hc;
  }
  public boolean equals (Object obj) {
    return obj instanceof 化学;
  }
  public String toString () {
    return "<化学>";
  }
}
```
コンストラクタ内のsuper.hashCode()はObjectクラスのhashCodeが呼ばれます。インスタンス化されたときにハッシュ値を保持して、equalsメソッドが実装されています。化学、生物、電気で異なるハッシュ値を保持するオブジェクト型変数として実装されているようです。VDM++クラス定義では専門家クラス内で型定義されていました。

## external_専門家クラス.java
```java:external_専門家クラス.java
import java.util.Set;
import java.util.HashSet;
import jp.vdmtools.VDM.UTIL;
import jp.vdmtools.VDM.Sentinel;
import jp.vdmtools.VDM.EvaluatePP;
import jp.vdmtools.VDM.CGException;


public class external_専門家クラス {
  専門家クラス parent = null;

  public external_専門家クラス (専門家クラス parent専門家クラス) {
    parent = parent専門家クラス;
  }

  public external_専門家クラス () {}

  public Set impl_資格を得る () throws CGException {
    UTIL.RunTime("Preliminary Operation 資格を得る has been called");
    return new HashSet();
  }
}
;
```
external_専門家クラス.javaは内部で保持している専門家クラス型のparent変数に、コンストラクタのオーバーロードで専門家クラス型のインスタンスをセットします。
専門家クラス.javaは継承可能なexternal_専門家クラス型のchild変数を保持して、自身をchild変数の初期化でセットします。


## 専門家クラス.java
```java:専門家クラス.java
import java.util.Set;
import java.util.HashSet;
import jp.vdmtools.VDM.UTIL;
import jp.vdmtools.VDM.Sentinel;
import jp.vdmtools.VDM.EvaluatePP;
import jp.vdmtools.VDM.CGException;

public class 専門家クラス implements EvaluatePP {

  volatile 専門家クラスSentinel sentinel;

  class 専門家クラスSentinel extends Sentinel {
    public final int 資格を得る = 0;
    public final int nr_functions = 1;
    public 専門家クラスSentinel () throws CGException {}
        public 専門家クラスSentinel (EvaluatePP instance) throws CGException {
      init(nr_functions, instance);
    }
  }

  public Boolean evaluatePP (int fnr) throws CGException {
    return Boolean.TRUE;
  }

  public void setSentinel () {
    try {
      sentinel = new 専門家クラスSentinel(this);
    }
    catch (Exception e) {
      System.out.println(e.getMessage());
    }
  }

  protected external_専門家クラス child = new external_専門家クラス(this);

  private void vdm_init_専門家クラス () {
    try {
      setSentinel();
    }
    catch (Exception e) {
      e.printStackTrace(System.out);
      System.out.println(e.getMessage());
    }
  }

  public 専門家クラス () throws CGException {
    this.vdm_init_専門家クラス();
  }

  public Set 資格を得る () throws CGException {
    sentinel.entering(sentinel.資格を得る);
    try {
      return child.impl_資格を得る();
    }
    finally {
      sentinel.leaving(sentinel.資格を得る);
    }
  }
  
}
```
また、専門家クラス.javaはsentinelの派生型の専門家クラスSentinel型をクラス内で宣言し、スレッドセーフにvolatile装飾されたSentinel変数を保持します。Sentinel変数は専門家クラスのsetSentinel ()メソッド内で初期化されます。vdm_init_専門家クラス ()がsetSentinel ()メソッドを呼び出していて、専門家クラスのコンストラクタがvdm_init_専門家クラス ()を呼び出すことで、Sentinel変数がインスタンス化されます。

VDM++クラス定義で定義された操作（実装は未定義）が
```
operations
    public 資格を得る:()==>  set of 資格型
    資格を得る()==
        is not yet specified;
```
下記のように実装されています。

```java:
  public Set 資格を得る () throws CGException {
    sentinel.entering(sentinel.資格を得る);
    try {
      return child.impl_資格を得る();
    }
    finally {
      sentinel.leaving(sentinel.資格を得る);
    }
  }
```
ここではsentinel.資格を得る（ = 0）がsentinel.enteringとsentinel.leavingの引数に渡され、それぞれ関数の冒頭と終了処理に呼ばれます。
child.impl_資格を得るが、処理本体として呼ばれますが、実際は未定義なので external_専門家クラスで実装されているimpl_資格を得るがハッシュセットを返します。前回記事により、事前条件を実装している関数はtryブロックの中でchild.impl_同名関数の直前に呼ばれることがわかっています。

      
# おわりに
なぜこういう構造になっているのかという目的的な意味の解釈まで進行しませんでしたが、クラス定義が出力するJavaコードのクラスの実装が、かなり複雑な多重構造をなしていることが明らかになりました。また、時間があればjp.vdmtools.VDM.Sentinelの実装やjp.vdmtools.VDM.EvaluatePPインターフェースの謎に迫ってみたいと思います。


一般的に条件式を満たすときに特定の処理を実行するプログラムの類をJavaセンチネルと言っているようです。jp.vdmtools.VDM.SentinelはVDM++で宣言的に書かれた条件式に対して実際の実行内容を実装しているものと推察されます。そういえば番兵法の末尾のデータがセンチネル。Sentinelは監視員や見張りを意味する英単語。

[^1]: IBMのウィーン研究所で1960年代から70年代にかけて開発された形式手法。その実装には1996年にISO標準（ISO_IEC_13817-1）となったVDM-SLと、そのオブジェクト指向拡張のVDM++がある。
[^2]: FMVDM　[VDMTools VDMTools](http://fmvdm.org/vdmtools/index-ja.html)
[^3]: FMVDM　[VDMTools リリース版 (9.0.7) Windows VDM++](http://fmvdm.org/VDMTools/Windows/setuppp-9.0.7-vs10-x64.exe)
[^4]: FMVDM-> github [[PDF] VDMTools VDM++開発手法ガイドライン1.0 2016](https://github.com/vdmtools/vdmtools/raw/stable/doc-jp/guidelines/guidelines_a4J.pdf)
[^5]: Qiita [「MSVCR100.dllが見つからない」の解決策](https://qiita.com/mylifewithviolin/items/7c9a6f39b73bdd9235af) 参照
[^6]: FMVDM-> github [VDMTools ユーザマニュアル VDM++](https://github.com/vdmtools/vdmtools/raw/stable/doc-jp/user-man/usermanpp_a4J.pdf)
