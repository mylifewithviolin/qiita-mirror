# はじめに
日本語プログラミング言語 Mind とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。前回の単純な整数カウントアップで驚異的？な結果をたたき出したJavaの結果が気になります。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Mind Version 8.07 for Windows
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

#### Mind
```mind:main.src
    カウントアップとは　（c　→　c）
    	cは　変数
     
    	cに　入れ
        cを　一つ増加し
    	cを　返すこと。
 
    メインとは
        countMaxは　変数
        countは　変数
        合否は　変数

        startTimeは　変数
        stopTimeは　変数
        spanTimeは　変数
        
        起動引数個数が　ゼロ？
        ならば　countMaxに　0を　入れ
        つぎに
        起動引数（1）を　数値変換し　countMaxと　合否に　入れ
        合否が　偽？
        ならば　countMaxに　0を　入れ
        つぎに

        ※開始時間（秒）
        日時を値で得る　startTimeに　入れる
        countに　0を　入れ
        ここから
        　　countが　countMax　以上　ならば　打ち切り
        　　　　　　　　つぎに
            countを　カウントアップし　countに　入れ
        繰り返し
        
        ※終了時間（秒）
        日時を値で得る　stopTimeに　入れる
        stopTimeから　startTimeを　引き　1000を　掛け　spanTimeに　入れる
        「処理回数: 」と　countを　文字列変換し　合成し 「回」を　合成し
        一行表示し
        「処理時間: 」と　spanTimeを　文字列変換し　合成し 「ミリ秒」を　合成し
        一行表示すること。

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

#### Mind

```:
C:\pmind\sample>count2 4000000
処理回数: 4000000回
処理時間: 562ミリ秒

C:\pmind\sample>
```
# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | Mind |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 0  |
| 40,000  | 0  | 6  | 15  |
| 400,000  | 2  | 11 | 62  |
| 4,000,000  | 3  | 62  | 562  |
| 40,000,000  | 5  | 538  | 5,516  |
| 400,000,000  | 6  | 5,304  | 53,165  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
今回の条件ではJavaもやたら速いという結果です。回数の桁数の増加の影響を若干うけるようになり40万回を超えると微増しました。
Mindの関数相当の処理単語では通常のスタックに引数countがあるとして、それをローカル変数に代入して1つ増加したローカル変数をスタックに返してメイン側で再度countに入れていますのでスタック操作回数はかなり増えている書き方となっています。その影響は受けているようですね。
