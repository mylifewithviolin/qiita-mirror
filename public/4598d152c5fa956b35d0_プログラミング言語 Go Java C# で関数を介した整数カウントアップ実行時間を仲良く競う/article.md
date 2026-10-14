# はじめに
プログラミング言語 Go ととJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。

## この記事内容の作業環境
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.78.2
java Eclipse Adoptium jdk-20.0.2.9-hotspot
C# 10 dotnet-sdk-6.0.404-win-x64
go version go1.19.5 windows/amd64
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

#### Go
```go:count.go
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

// メイン
func main() {

	countMax := 0
	count := 0

	if len(os.Args) <= 1 {
		countMax = 0
	} else {
		var err error
		countMax, err = strconv.Atoi(os.Args[1])
		if err != nil {
			countMax = 0
		}
	}
	//開始時間（ナノ秒）
	startTime := time.Now()

	for count < countMax {
		count = countup(count)
	}

	//終了時間（ナノ秒）
	stopTime := time.Now()
	spanTime := stopTime.Sub(startTime)
	fmt.Println("処理回数: ", count, "回")
	fmt.Println("処理時間: ", int64(spanTime/time.Millisecond), "ミリ秒")

}

func countup(c int) int {
	return c + 1
}
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

#### Go
```:
C:\developments\go1\Callfunc>Callfunc.exe 40
処理回数:  40 回
処理時間:  0 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 400
処理回数:  400 回
処理時間:  0 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 4000
処理回数:  4000 回
処理時間:  0 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 40000
処理回数:  40000 回
処理時間:  0 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 400000
処理回数:  400000 回
処理時間:  0 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 4000000
処理回数:  4000000 回
処理時間:  1 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 40000000
処理回数:  40000000 回
処理時間:  21 ミリ秒

C:\developments\go1\Callfunc>Callfunc.exe 400000000
処理回数:  400000000 回
処理時間:  205 ミリ秒

C:\developments\go1\Callfunc>
```

# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | Go |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 0  |
| 40,000  | 0  | 6  | 0  |
| 400,000  | 2  | 11 | 0  |
| 4,000,000  | 3  | 62  | 1  |
| 40,000,000  | 5  | 538  | 21  |
| 400,000,000  | 6  | 5,304  | 205  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
Goはcount++でカウントアップするより、関数を介してカウントアップした方が格段に速くなりました。
