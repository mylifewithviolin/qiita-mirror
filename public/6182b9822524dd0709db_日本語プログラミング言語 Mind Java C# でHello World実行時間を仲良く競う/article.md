# はじめに
日本語プログラミング言語 Mind とJava C# とで「Hello World」コンソール出力の反復実行時間を仲良く競い合わせてみます。

https://qiita.com/advent-calendar/2023/mind

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Mind Version 8.07 for Windows
CPU Intel(R) Core(TM) i3-5005U 2.00 GHz

## この記事内容の保証
※この記事の実行結果は参考情報です。実行環境に大きく依存します。Mindは現状秒単位で計測していますので誤差があります。

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
            System.out.println("Hello World!");
            count+=1;
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

    }
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
            Console.WriteLine("Hello World!");
            count+=1;
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
```

#### Mind
```mind:main.src
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
            「Hello World!」を　一行表示する
            countを　一つ増加し
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
C:\developments\java20>java -cp . Program 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 4565ミリ秒

C:\developments\java20>
```

#### C#

```:
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Helloworld 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 4206.8631ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```

#### Mind

```:
C:\pmind\sample>hello2.exe 40000
Hello World!
・・・
Hello World!
Hello World!
Hello World!
処理回数: 40000回
処理時間: 7000ミリ秒

C:\pmind\sample>
```
# 実行結果まとめ
表1　「Hello World」コンソール出力の反復実行時間（ミリ秒）
| 実行回数 | Java | C# | Mind |
|-:|-:|-:|-:|
|  40 |  8 | 16  |  0*1 |
| 400  | 72  | 57  | 0*1  |
| 4,000  | 563  | 468  | 1,000  |
| 40,000  | 4,565  | 4,206  | 7,000  |
| 400,000  | 42,618  | 40,075  | 67,000  |

*1 Mindは秒単位計測のため1秒未満計測不能

# おわりに
いかがでしたでしょうか？コンソール出力を単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。Mindはすみません、もう少しシステム記述よりの単語を探せばミリ秒単位で計測できたかもしれません。

備忘録 Mindは局所変数は実行記述単語より手前、単語定義の冒頭に集めないと怒られます。例えば、spanTimeは　変数　をコメント文※開始時間（秒）の上に持っていきますと．．．
```
17 行目でエラー。行内容は、
        spanTimeは　変数
      要因１：この位置では局所変数や局所処理単語は定義できません。
      要因２：この位置では局所変数などは定義できません。
```
みなさん、気を付けましょう。知らなかったのはわたしだけ:sweat_smile:

この記事は[日本語プログラミング言語 Mind（マインド） Advent Calendar 2023](https://qiita.com/advent-calendar/2023/mind)のために投稿しましたが、私の中ではQiita投稿100記事目:confetti_ball:となりました。Mindの記事で100投稿目:tada:を迎えられたことを光栄に思います。
