# はじめに
日本語プログラミング言語 プロデル とJava C# とで関数呼び出しを介した整数カウントアップの反復実行時間を仲良く競い合わせてみます。いわゆるファンクションコールのオーバーヘッドとはどんなものなのかを切り分けます。プロデルはコンパイル済中間コードでの実行を再計測してみます。

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
プロデルのコンパイルはプロデルデザイナで「実行ファイルの作成する（コンパイル済）」で行っています。ランタイム環境で動作したソースは実行ファイル作成は通過しましたが、実行時にランタイム例外が発生しましたので、少し調整しています。

```mind:callfunc2.rdr
※コンソール
【count:整数】は、0
【countMax:整数】は、0
【引数:文字列】
コンソールから受け取って引数に入れる
引数をcountMaxに入れる

開始日時は、起動時間
count < countMaxの間、繰り返す
	countをカウントアップしたものをcountに入れる
	//count = カウントアップする(count)
繰り返し終わり
終了日時は、起動時間
経過時間＝終了日時-開始日時

「処理回数：」＆ count＆ 「回」をコンソールへ表示して改行する
「処理時間：」＆ 経過時間＆ 「ミリ秒」をコンソールへ表示して改行する。

【c:整数】をカウントアップする手順
     c = c +1
     cを返す
終わり

```
ランタイム環境で動作して少し速かった方の「count = カウントアップする(count)」は上記のコードの状態では動きませんでした。（余談参照）

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
「countをカウントアップしたものをcountに入れる」での結果
コマンドライン引数は読み込めなかったので、コンソールからの入力としています。

```:
C:\produire\sample2>callfunc2.exe
40
処理回数：40回
処理時間：0ミリ秒

C:\produire\sample2>callfunc2.exe
400
処理回数：400回
処理時間：16ミリ秒

C:\produire\sample2>callfunc2.exe
4000
処理回数：4000回
処理時間：16ミリ秒

C:\produire\sample2>callfunc2.exe
40000
処理回数：40000回
処理時間：16ミリ秒

C:\produire\sample2>callfunc2.exe
400000
処理回数：400000回
処理時間：125ミリ秒

C:\produire\sample2>callfunc2.exe
4000000
処理回数：4000000回
処理時間：1078ミリ秒

C:\produire\sample2>callfunc2.exe
40000000
処理回数：40000000回
処理時間：10890ミリ秒

C:\produire\sample2>callfunc2.exe
400000000
処理回数：400000000回
処理時間：106047ミリ秒

C:\produire\sample2>
```


# 実行結果まとめ
表3　関数経由の整数カウントアップの反復実行時間（ミリ秒）
| 実行回数 | Java | C# | プロデル |
|-:|-:|-:|-:|
|  40 |  0 | 6  |  0 |
| 400  | 0  | 6  | 0 |
| 4,000  | 0  | 6  | 16 |
| 40,000  | 0  | 6  | 16  |
| 400,000  | 2  | 11 | 125  |
| 4,000,000  | 3  | 62  | 1,078  |
| 40,000,000  | 5  | 538  | 10,890  |
| 400,000,000  | 6  | 5,304  | 106,047  |

※Java C#ナノ秒台は切り捨て

# おわりに
いかがでしたでしょうか？整数カウントアップの関数呼び出しを単純にループさせているだけですので、各言語、実装によってはいろいろな差異がでるものと思われますので、この件はあくまで参考情報です。

# 余談
<details><summary>余談です。</summary>
ランタイム環境で動作した「count = カウントアップする(count)」の関数呼び出し風の記述の場合、実行時に下図の例外がスローされました。
```
C:\produire\sample2>callfunc2.exe
40
------------------------------------------------------------------------------------------------------------------------
エラーが発生しました。
予期しないエラーが発生しました。申し訳ありません。
原因:Exception
動詞「カウントアップ」の適切な手順が決定できません。
【c:整数】をカウントアップする@広域種類


場所 Produire.ConstructScopeIL.Invoke(Object targetObject, String shortVerbName, String[] names, String[] particles, Object[] arguments, Boolean acceptReturnValue, Boolean isPartial, Object lastValue)
場所 Produire.ConstructScopeIL.GetDynamicObjectAccessValue(Object caller, String memberName, Object nounValue)
場所 callfunc2.広域種類.MainCode()
場所 callfunc2.メイン種類.Main()

ハンドルされていない例外: System.Exception: 動詞「カウントアップ」の適切な手順が決定できません。
【c:整数】をカウントアップする@広域種類
   場所 Produire.ConstructScopeIL.Invoke(Object targetObject, String shortVerbName, String[] names, String[] particles, Object[] arguments, Boolean acceptReturnValue, Boolean isPartial, Object lastValue)
   場所 Produire.ConstructScopeIL.GetDynamicObjectAccessValue(Object caller, String memberName, Object nounValue)
   場所 callfunc2.広域種類.MainCode()
   場所 callfunc2.メイン種類.Main()

C:\produire\sample2>
```
</details>
