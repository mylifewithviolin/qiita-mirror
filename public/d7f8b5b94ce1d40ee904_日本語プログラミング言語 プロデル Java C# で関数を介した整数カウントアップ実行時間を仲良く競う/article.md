# はじめに
日本語プログラミング言語 プロデル とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。と、軽い感じでやってみましたところ、プロデルの２つの手順呼び出しの構文の違いで有意差があることを発見しました。

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


#### プロデル
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（ランタイム環境）」で行っています。2023/12/07追記
```mind:callfunc.rdr
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
    
       	//countをカウントアップしたものをcountに代入する
    	count =　countをカウントアップする
    繰り返し終わり
    終了日時は、今日
    時間差は、終了日時-開始日時
    
    「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
    「処理時間：」＆ 時間差の合計ミリ秒数＆ 「ミリ秒」をコンソールへ表示して改行する

【c:整数】をカウントアップする手順
     c = c +1
     cを返す
終わり

```
プロデルには戻り値のある手順の呼びだし方としては、日本語構文の
```
countをカウントアップしたものをcountに代入する
```
の他に、代入文形式の
```
count =　countをカウントアップする
```
も書けます。
原因はわかりませんが、実行時間に有意差がありそうでしたので、他言語との比較値はより速そうであった後者による結果としています。
また、当初
```
【c:整数】をカウントアップする手順
```
の手順宣言部での仮引数の宣言を下記のように型名を明示せずに書いていましたが、動的型変換が起きるともしかすると遅くなってしまうかもと推察して、型明記としてあります。（この点は実際に検証したわけではありません。）
```
【c】をカウントアップする手順
```
また、上記の場合は問題なく実行されますが、下記のように書いても実行ファイル作成（コンパイル）時はエラーとならず
```
cをカウントアップする手順
```
実行時に下記の実行エラーとなりました。
```
[エラー番号119] [はじめ:18行目]
説明: https://docs.utopiat.net/rdr/manual/verbs/kauntoappusuru.html
---------------------------------------------------------------------------------
エラー(119):「カウントアップする」の中身が、無です。作るか変数に値を代入してください。
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

#### プロデル
「count =　countをカウントアップする」での結果
```:
C:\produire\sample>callfunc 4000000
処理回数：4000000回
処理時間：13462.839300000001ミリ秒

C:\produire\sample>
```
参考に
「countをカウントアップしたものをcountに代入する」
で実行した場合は下記の結果でした。
```:
C:\produire\sample>callfunc 4000000
処理回数：4000000回
処理時間：37255.7392ミリ秒

C:\produire\sample>
```

# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | プロデル |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  46 |
| 400  | 0  | 6  | 46 |
| 4,000  | 0  | 6  | 62  |
| 40,000  | 0  | 6  | 171  |
| 400,000  | 2  | 11 | 1,328  |
| 4,000,000  | 3  | 62  | 13,462  |
| 40,000,000  | 5  | 538  | 137,991  |
| 400,000,000  | 6  | 5,304  | 1,807,584  |

※ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。
今回の条件でもJavaは驚異的に速いという結果です。回数の桁数の増加の影響を若干うけるようにはなりまして40万回を超えると微増しました。有意差かは疑問が残ります。
