# はじめに
日本語プログラミング言語 なでしこ３ とJava C# とで整数カウントアップの反復実行時間を仲良く競い合わせてみます。関数呼び出しは意外と重い処理なので、いったん素の処理でどんなものなのか検証します。なでしこ３のコンソールアプリです。

https://qiita.com/advent-calendar/2023/nadesiko

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
nadesiko version 3.4.5 nadesiko3win32-3.4.5
Node.js v20.10.0.
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

#### なでしこ3
```mind:count3.nako
※【なでしこ実行モード】cnako3


count=0
countMax=0
sizeArgs=コマンドラインの配列要素数
もし (sizeArgs < 4) ならば
　　countMax=0
違えば
   エラー監視
　    countMax=コマンドライン[3] //を整数変換
　　エラーならば
 　　 countMax=0
    ここまで
ここまで

開始日時は、システム時間ミリ秒

（count < countMax）の間
	count = count + 1
ここまで

終了日時は、システム時間ミリ秒
経過時間は、終了日時-開始日時

「処理回数：{count}回」を表示する
「処理時間：{経過時間}ミリ秒」を表示する

```
#### なでしこ(v3)のコンソールアプリケーション
なでしこ(v1)のソースコードとは若干の非互換があり調整しています。
コマンドラインの配列要素数は直接定数と大小比較すると怒られていましたので、いったん変数に格納しました。
「システム時間」は秒単位となったので「システム時間ミリ秒」としています。
起動引数のindexはNode.jsで2つ、なでしこで1つ使われるので3が正解でした。

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

#### なでしこ3
```:
C:\nadesiko\sample1>count3.nako.bat 40
処理回数：40回
処理時間：0ミリ秒

C:\nadesiko\sample1>count3.nako.bat 400
処理回数：400回
処理時間：1ミリ秒

C:\nadesiko\sample1>count3.nako.bat 4000
処理回数：4000回
処理時間：1ミリ秒

C:\nadesiko\sample1>count3.nako.bat 40000
処理回数：40000回
処理時間：7ミリ秒

C:\nadesiko\sample1>count3.nako.bat 400000
処理回数：400000回
処理時間：13ミリ秒

C:\nadesiko\sample1>count3.nako.bat 4000000
処理回数：4000000回
処理時間：93ミリ秒

C:\nadesiko\sample1>count3.nako.bat 40000000
処理回数：40000000回
処理時間：4067ミリ秒

C:\nadesiko\sample1>count3.nako.bat 400000000
処理回数：400000000回
処理時間：42226ミリ秒

C:\nadesiko\sample1>
```
なでしこパッドからは「なでしこ実行モード:cnako3」で一度実行成功すると
上記count3.nako.batが生成されました。コマンドライン引数を受け取れるよう下記のように少し調整しています。

```bat
@ ECHO OFF
REM --- NADESIKO V3 ---
"C:\nadesiko\nodejs\node.exe" "C:\nadesiko\node_modules\nadesiko3\src\cnako3.mjs" "C:\nadesiko\sample1\count3.nako.bak" %1
rem ECHO ---
rem pause
```


# 実行結果まとめ
表2　整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | なでしこ |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 1 |
| 4,000  | 0  | 7  | 1  |
| 40,000  | 0  | 6  | 7  |
| 400,000  | 3  | 7  | 13  |
| 4,000,000  | 3  | 23  | 93  |
| 40,000,000  | 3  | 139  | 4,067 |
| 400,000,000  | 3  | 1,341  | 42,226  |

※Java C#ナノ秒台は切り捨て

# おわりに

いかがでしたでしょうか？整数カウントアップを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
