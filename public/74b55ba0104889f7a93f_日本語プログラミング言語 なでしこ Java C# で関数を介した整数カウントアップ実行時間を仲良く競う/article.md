# はじめに
日本語プログラミング言語 なでしこ とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。
なでしこワンはレガシーかもしれませんのでなでしこ３の検証を急ぎ来ます。本記事筆者のあくまで興味本位の調査で、各言語の優劣を評価するものではありませんので念のため。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
nadesiko version 1.588 for Windows
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz


## この記事内容の保証
※この記事の実行結果は参考情報です。実行環境に大きく依存します。

# お題のソースコード
#### Java
```Java:main.java
import java.lang.System;
/**
* プログラム型
*/
class Program
{
    /**
    * メイン
    * @param args 引数
    */
    public static void main(String[] args) throws Exception
    {
        int countMax=0;
        int count=0;
        if (args.length != 1) {
            countMax=0;
        }
        try
        {
            countMax=Integer.parseInt(args[0]);
        }
        catch (Exception e)
        {
            countMax=0;
        }
        //開始時間（ナノ秒）
        long startTime = System.nanoTime();

        while(count < countMax){
            count = countup(count);
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

    }
	
	/**
    * カウントアップ関数
    * @param c count
    */
	private int countup(int c){
		return c+=1;
	}
}
```
#### C#
```cs:main.cs
using System;

/// <summary>プログラム型</summary>
class Program
{

    /// <summary>メイン</summary>
    /// <param name="args">引数</param>
    static void Main(string[] args)
    {
        int countMax=0;
        int count=0;
        if (args.Length != 1) {
            countMax=0;
        }else{
            try
            {
                countMax=int.Parse(args[0]);
            }
            catch (FormatException)
            {
                countMax=0;
            }
        }
 
        //開始時間（ミリ秒）
        DateTime startTime= new DateTime();
        DateTime stopTime = new DateTime();
        startTime = DateTime.Now;

        while(count < countMax){
            count = Countup(count);
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
    /// <summary>カウントアップ関数</summary>
    /// <param name="c">count</param>
    private static int Countup(int c){
		return c+=1;
	}
 }
```


#### なでしこ
```mind:helloworld.nako
※【なでしこ実行モード】cnako

countとは整数
countMaxとは整数

count=0
countMax=0

もし コマンドラインの配列要素数 < 2 ならば
　　countMax=0
違えば
   エラー監視
　    countMax=コマンドライン[1]を整数変換
　　エラーならば
 　　 countMax=0
    ここまで
ここまで

開始日時は、システム時間

（count < countMax）の間
	//countをカウントアップし、countに代入する
	count = カウントアップする(count)
ここまで

終了日時は、システム時間
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する

●カウントアップする(cを)
     c = c +1
     cで戻る
```
※なでしこ(v1)のコンソールアプリケーション[^1]


なでしこには戻り値のある関数の呼びだし方としては、日本語構文の
```
countをカウントアップし、countに代入する
```
の他に、代入文形式の
```
count = カウントアップする(count)
```
も書けます。
両者に実行時間の有意差はなさそうでした。他言語との比較結果では代入文形式の実行結果を使用しています。

関数宣言の際の仮引数の型情報の指定方法は発見できませんでした。（戻り値型の指定方法もよくわかっていません。動的型付けシステムなのかもしれません。）
```
●カウントアップする(cを)
```

# 実行結果
#### Java
```:
C:\developments\java20>java -cp . Program 4000000
処理回数: 4000000回
処理時間: 3ミリ秒

C:\developments\java20>
```

#### C#

```:
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Count2.exe 4000000
処理回数: 4000000回
処理時間: 62.3866ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```


#### なでしこ
```:
C:\nadesiko\sample1>callfunc.exe 4000000
処理回数：4000000回
処理時間：20361ミリ秒
```
上記は代入文形式の実行結果です。次節の表はこの条件での結果です。
下記は日本語構文での実行結果です。代入文形式との有意差はなさそうです。
```:
C:\nadesiko\sample1>callfunc.exe 4000000
処理回数：4000000回
処理時間：20614ミリ秒

C:\nadesiko\sample1>callfunc.exe 4000000
処理回数：4000000回
処理時間：20488ミリ秒

C:\nadesiko\sample1>callfunc.exe 40000000
処理回数：40000000回
処理時間：202355ミリ秒
```

# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# |なでしこ |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 16  |
| 40,000  | 0  | 6  | 205  |
| 400,000  | 2  | 11 | 2,047  |
| 4,000,000  | 3  | 62  | 20,361  |
| 40,000,000  | 5  | 538  | 208,327  |
| 400,000,000  | 6  | 5,304  | 2,022,358  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
今回の条件でもJavaは驚異的に速いという結果です。400万回を超えると微増しましたが有意差かは疑問が残ります。コンソール出力の場合はそれなりに値が増加していますので、計測方法の不具合はないはずです。


[^1]: なでしこ(v1)の上記のソースコードにウィンドウ版とコンソール版の違いはなく、なでしこパッドで一度コンソールアプリケーションの実行モードで実行してから、実行ファイルを作成するとコンソールアプリケーションとなりました。今回は「現在の実行モードをカーソル位置に挿入」を最初の行で行っています。
