# はじめに
VSCodeでMind 8 for WindowsのKernelを[デバッグ実行開始できました](https://qiita.com/mylifewithviolin/items/1d01b250ef2d0a175d0c)ので、今回はそのデバッグ途中のご様子のレポートです。※注 デバッグの言い回しですが、もちろんデバッグが目的ではなく、学習目的でステップ実行しているだけです。

# 前提条件
Windows11 Pro 22H2
VSCode(Visual Studo Code)　1.86.1
Microsoft Visual C++ 2008 Express Edition
Mind Version 8.0.08 for Windows

## VSCodeの拡張機能
C/C++ for Visual Studio Code 1.18.5 Microsoft 
C/C++ Extension Pack 1.3.0 Microsoft 
C/C++ Extension UI Themes 2.0.0 Microsoft 
VS Code Makefile Tools 0.8.22 Microsoft 

# デバッグ実行の前提条件
Mind開発者の@killyさんからの前回記事コメントでの情報共有で、今回デバッグ対象のmindexec.exeは通常Mindコンパイラによりターゲットソースの主ファイル名でリネームされて（同名のMコードファイルといっしょにランタイム的に）実行されるとのことでしたので、今回はmindexec.exe状態でしかデバッグ実行できないため、通常とは異なりますがMコードファイル側をmindexec.mcoにリネームしておきデバッグ実行します。
とりあえずなにかよいMコードファイルないかなということで、とっさにはMindコンパイラ自体のmind.mcoをリネームしてみることとします。

```
C:\developments\vscode\mind8\kernel>dir mindexec.*

 C:\developments\vscode\mind8\kernel のディレクトリ

2023/01/22  16:36             2,130 mindexec.c
2024/02/17  10:12           169,472 mindexec.exe
2024/02/17  10:12           747,528 mindexec.ilk
2023/01/22  16:36           151,454 mindexec.mco
2024/02/17  10:12            34,727 mindexec.obj
2024/02/17  10:12         1,272,832 mindexec.pdb
               6 個のファイル           2,378,143 バイト
```
mindexec.mcoがほんとはmind.mcoだったやつです。


# デバッグ実行中のご様子
最初から下図の状態までウォッチ式を追加したわけではありませんが、どうもこの状態の場合、ランタイムファイルmrunt060.exeがないため、下図のtry_multpath_exec.cのループを失敗で抜けて

![vscodec14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/37d5773a-b99b-32cb-f1b6-16f8392c1f70.png)

mindex.cの下記のヶ所に入ってしまうようです。

```c:mindex.c
	/* ---------------------- */
	/* やっぱり起動できず     */
	/* ---------------------- */
	emgcyHeaderOutput();
	printf( "Mind runtime not found\n" );
	emgcyExit();
 ```

 Mind runtime not foundをコンソール出力して終了。

 # デバッグ実行の前提条件2
 mrunt060.exeをkernelフォルダに置かせていただきます。
```
C:\developments\vscode\mind8\kernel>dir mrunt*.exe

 C:\developments\vscode\mind8\kernel のディレクトリ

2023/01/22  16:36           181,760 mrunt060.exe
               1 個のファイル             181,760 バイト
```

# デバッグ実行中のご様子2

mindex.cの下記のヶ所exit_program(retcode);に入ってしまうようです。

```c:mindex.c
	retcode = spawnv( P_WAIT, FullpathRuntname, &(Argv[0]) );
	if ( retcode != -1 )
	{
		exit_program(retcode); /* 子の終了コードを上に返す */
	}
```
下記のエラーをコンソール出力して終了します。
```
  コンパイルエラー：ファイル名の指定が誤りです。
```

これはつまりMindコンパイラがコンパイル対象のソースファイルを要求していることのような（気もします。プロセス実行は成功したような気がします）。いきなりMindコンパイラのMコードを指定したのは大それ過ぎていたかもしれません。

# おわりに
ちょっとタイムアウトしてしまいましたが、次回は引数を要求しない簡単なMコードファイルで様子見します。
