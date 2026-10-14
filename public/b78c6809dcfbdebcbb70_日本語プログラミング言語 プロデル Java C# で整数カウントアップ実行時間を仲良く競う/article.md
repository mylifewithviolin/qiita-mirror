# はじめに
日本語プログラミング言語 プロデル とJava C# とで整数カウントアップの反復実行時間を仲良く競い合わせてみます。コンソール出力は意外と重い処理のようで、いったん素の処理でどんなものなのかなと。

https://qiita.com/advent-calendar/2023/produire

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
Produire Version 2.0.1197 for Windows
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

            count+=1;
        }
        //終了時間（ナノ秒）
        long stopTime = System.nanoTime();
        long spanTime = stopTime - startTime;
        System.out.println("処理回数: " + count + "回");
        System.out.println("処理時間: " + (spanTime / 1000000) + "ミリ秒");

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

            count+=1;
        }
        //終了時間（ミリ秒）
        stopTime = DateTime.Now;
        TimeSpan st =stopTime-startTime;
        Console.WriteLine("処理回数: " + count + "回");
        Console.WriteLine("処理時間: " + st.TotalMilliseconds + "ミリ秒");

    }
}
```

#### プロデル
```mind:main.rdr
※コンソール
    【count:整数】は、0
    【countMax:整数】は、0
    
    もしプログラムのコマンドライン引数が無なら
    　　countMax=0
    そうでなければ
       例外監視
    　　  countMax=プログラムのコマンドライン引数(1)
    　　発生した場合
     　　 countMax=0
        監視終わり
    もし終わり
    
    開始日時は、今日
    count < countMaxの間、繰り返す
    
    	count =count +1
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する
    
```
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（ランタイム環境）」で行っています。2023/12/07追記

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
C:\developments\cs6\HelloWorld\bin\Debug\net6.0>Count.exe 4000000
処理回数: 4000000回
処理時間: 23.1618ミリ秒

C:\developments\cs6\HelloWorld\bin\Debug\net6.0>
```

#### プロデル
```:
C:\produire\sample>count 4000000
処理回数：4000000回
処理時間：3969.1469ミリ秒

C:\produire\sample>
```

# 実行結果まとめ
表2　整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | プロデル |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  15 |
| 400  | 0  | 6  | 31 |
| 4,000  | 0  | 7  | 31  |
| 40,000  | 0  | 6  | 70  |
| 400,000  | 3  | 7  | 437  |
| 4,000,000  | 3  | 23  | 3,969  |
| 40,000,000  | 3  | 139  | 39,575 |
| 400,000,000  | 3  | 1,341  | 435,196  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
プロデルは.NET Framework 4.8のCLRで動いているのでC#との差異は.NET Core 6.0との差異なのかもしれません。スミレで要検証。
Javaは回数の桁数の増加の影響をほぼ受けないという結果で、他の言語が40万回を超えると線形に処理時間が増えていくのと対照的でした。
