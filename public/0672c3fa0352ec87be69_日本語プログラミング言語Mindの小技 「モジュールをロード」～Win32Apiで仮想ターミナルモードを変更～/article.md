# はじめに
日本語プログラミング言語Mindの小技「モジュールをロード」について説明したいと思います。

# 対象読者
日本語プログラミング言語Mindのユーザー、または日本語プログラミング言語に興味のある方

# この小技に関連するMind言語マニュアル

この小技に関連するMind言語仕様の記述はMind8プログラミングマニュアルに記載がありません。

Mind7の付属の上級者向けドキュメントmind7\doc\file.docmに記載があります。

Ｆ８．　ＡＰＩ呼出し
￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
>　任意の Windows API を呼出す機能です。任意のDLL内関数を呼出すのにも使えます。（WindowsAPIはDLLの一つに過ぎません）

>■モジュールをロード
－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
　＜モジュール名＞で　モジュールをロード　→　モジュールハンドル
－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
　モジュールを名前で指定し（モジュール名とは物理的なDLLファイル名のこと）を
ロードしてそのハンドルを返します。ハンドルは32ビット長の数値です。


本機能（本記事）は、下記のバージョンに対応しています。Mind８のLinux版は対応していません。本記事では特に検証を行っておりません。

# 対応バージョン
■Mind７　■Mind８　■Mind９
■Windows版　□Linux版

# 小技の解説
Mindの小技「モジュールをロード」は任意の Windows API を呼出す機能のベーシックな単語です。任意のDLL内関数を呼出すのにも使えます。
「モジュールをロード」自体はDLLのパスを指定しますが、システムAPIの場合はDLL名だけでOKです。

DLLからエクスポートされた関数のアドレスを取得する単語として「モジュールの関数アドレスを得る」があります。「モジュールをロード」で取得したハンドラを指定して関数アドレスを取得します。

関数アドレスを取得した後は、引数の数に応じて「アドレス指定でＡＰＩ呼出し１」などを使ってAPIを実行します。「１」のヶ所が引数の数に応じて異なる単語を使用します。「アドレス指定でＡＰＩ呼出しｎ」（ｎ＝０～８）

この３つのステップを１つの処理単語にまとめた「ＡＰＩ呼出しｎ」（ｎ＝０～８）があります。単一のモジュールから異なる関数を呼び出す場合は、「モジュールをロード」が毎回内部で呼ばれますので、前記３ステップで記述することが推奨されています。

 以下のサンプルプログラムでは、Win32Apiで仮想ターミナルモードを変更する処理を題材に、前記３ステップで記述して説明します。

# Mindプログラムソース
## ライブラリ
```mind:"win32consoleapi.src
ローカル。

モジュール名は             文字列定数　「kernel32」。
VTモード関数名１は         文字列定数　「GetStdHandle」。
VTモード関数名２は         文字列定数　「GetConsoleMode」。
VTモード関数名３は         文字列定数　「SetConsoleMode」。
STD_OUTPUT_HANDLEは 　　　数値　　　　　-11。
ENABLE_VIRTUAL_TERMINAL_PROCESSINGは　数値 04H。

モジュールロード失敗表示とは　 （・　→　・）
    「APIモジュールのロードに失敗しました。」を　一行表示し　改行すること。
関数アドレス取得失敗表示とは　 （・　→　・）
    「関数アドレス取得に失敗しました。」を　一行表示し　改行すること。
VTモードを有効化失敗表示とは　 （・　→　・）
    「VTモードを有効化に失敗しました。」を　一行表示し　改行すること。
VTモードを無効化失敗表示とは　 （・　→　・）
    「VTモードを無効化に失敗しました。」を　一行表示し　改行すること。
VTモード取得失敗表示とは　 （・　→　・）
    「VTモードの取得に失敗しました。」を　一行表示し　改行すること。

ANDNOTとは　（変数　変数　→　変数）
        変数１は　変数
        変数２は　変数
    変数２に　入れ
    変数１に　入れ
    変数２と　0FFFFFFFFHで　XORし　変数２に　入れ
    変数１と　変数２で　ANDすること。    

VTモードを変更するとは　 （１/０：有効/無効　→　１/０：成功/失敗）
        有効化フラグは　　　　変数
        モジュールハンドラは　変数
        関数アドレス１は　　　変数
        関数アドレス２は　　　変数
        関数アドレス３は　　　変数
        失敗フラグは        　変数
        hConsoleは　　　　　　変数
        currentModeは　　　　変数

    有効化フラグに　入れ
    hConsoleを　クリアし
    currentModeを　クリアし
    失敗フラグを　クリアし
    モジュール名を　モジュールをロードし　モジュールハンドラに　入れ
    エラー？
    ならば　モジュールロード失敗表示し　０をかえす
    つぎに

    モジュールハンドラと　VTモード関数名１で
　　　　　　　　　モジュールの関数アドレスを得て　関数アドレス１に　入れる
    エラー？
    ならば　関数アドレス取得失敗表示し　失敗フラグを　セットする
    つぎに
    モジュールハンドラと　VTモード関数名２で
　　　　　　　　　モジュールの関数アドレスを得て　関数アドレス２に　入れる
    エラー？
    ならば　関数アドレス取得失敗表示し　失敗フラグを　セットする
    つぎに
    モジュールハンドラと　VTモード関数名３で
　　　　　　　　　モジュールの関数アドレスを得て　関数アドレス３に　入れる
    エラー？
    ならば　関数アドレス取得失敗表示し　失敗フラグを　セットする
    つぎに

    失敗フラグが　偽？
    ならば
        ※「モード取得実行」を　一行表示し
        ※GetStdHandle(STD_OUTPUT_HANDLE)
        STD_OUTPUT_HANDLEと　関数アドレス１で　アドレス指定でＡＰＩ呼出し１して
        hConsoleに　入れ
        ※hConsoleを　数値表示し　改行し
        ※GetConsoleMode(hConsole, currentMode)
        hConsoleと  currentModeの　アドレスと　関数アドレス２で　アドレス指定でＡＰＩ呼出し２して
        ゼロ？
        ならば　VTモード取得失敗表示し　０をかえし
        さもなければ
            ※「currentMode:」を　表示し　currentModeを　数値表示し　改行し
            有効化フラグが　１に　等しい
            ならば
                ※「有効化実行」を　一行表示し
                hConsoleと 
                currentModeと　ENABLE_VIRTUAL_TERMINAL_PROCESSINGで　ORして
                ※SetConsoleMode(hConsole, currentMode Or ENABLE_VIRTUAL_TERMINAL_PROCESSING)
                関数アドレス３で　アドレス指定でＡＰＩ呼出し２して
            さもなければ
                ※「無効化実行」を　一行表示し
                hConsoleと
                currentModeと　ENABLE_VIRTUAL_TERMINAL_PROCESSINGで　ANDNOTして
                ※SetConsoleMode(hConsole, currentMode And Not ENABLE_VIRTUAL_TERMINAL_PROCESSING)
                関数アドレス３で　アドレス指定でＡＰＩ呼出し２して
            つぎに
            ゼロ？
            ならば　
                有効化フラグが　真？
                ならば  　　　VTモードを有効化失敗を表示し
                さもなければ  VTモードを無効化失敗を表示し　
                つぎに
                ０をかえし
            さもなければ　１をかえし
            つぎに
        つぎに
    つぎに
　　モジュールハンドラで　モジュールを解放すること。

    グローバル。

VTモードを有効化するとは　 （・　→　１/０：成功/失敗）
    １で　VTモードを変更すること。

VTモードを無効化するとは　 （・　→　１/０：成功/失敗）
    ０で　VTモードを変更すること。

ローカル語を捨てる。
```

GetConsoleMode(hConsole, currentMode)のcurrentModeはC言語のポインタ変数をわたしいますので、currentModeのアドレスをわたすことで、結果が格納されるようにしています。

## メインプログラム
```mind:conclear.src

"win32consoleapi"を　コンパイルする。
※以下の制御コードは定義済
※ＥＳＣは　　　　　　　　数値　　1BH。

画面クリアとは  （・　→　・）   
    「&ESC&[2J」を　表示すること。

メインとは  
    VTモードを有効化し
    ０に　等しい　ならば　実行終わり　つぎに
    
    画面クリアし
    VTモードを無効化。
```


# コンパイル結果
ではコンパイルしてみます。下位ライブラリはfileを指定します。


## Mind９
下図はMind９βです。
```cmd:
C:\developments\vscode\mind9>mind conclear file   

日本語プログラミング言語 Ｍｉｎｄ Version 8.11 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. C:\mind9-beta\mind9-beta\bin\mindex.exe --> conclear.exe
```
## Mind8
```cmd:
C:\developments\vscode\mind9>mind conclear file

日本語プログラミング言語 Ｍｉｎｄ Version 8.07 for Windows
          Copyright(C) 1985 Scripts Lab. Inc.
コンパイル中 .. 終了
Coping.. c:\pmind\bin\mindex.exe --> conclear.exe
```
## Mind7
```cmd:
C:\developments\vscode\mind9>mind conclear file
日本語プログラミング言語 Ｍｉｎｄ Version 7.5 for Windows
          Copyright(C) 1985-2004 Scripts Lab. Inc.
          Single user license.  Serial No:********
コンパイル中 - 終了
Coping.. C:\mind7\bin\mindexec.exe -> conclear.exe
```
# 実行結果
つづいて実行してみます。

Mind8の結果です。記述は割愛していますがMind7/9βも同じです。

```cmd:
C:\developments\vscode\mind9>conclear 












C:\developments\vscode\mind9>
```

この実行環境はVSCodeのターミナルのため、既定でVTモードは有効になっています。また無効化はできませんでした。

このサンプルでは画面クリアのエスケープシーケンスのみ記述していますが、VTモード有効化した後は、いろいろなエスケープシーケンスコマンドを実行できます。


# 参考情報
この小技「モジュールをロード」を使った記述例の記事はいくつかあります。下記はSQLServerODBCを独自のC言語DLLでラップしてMindから呼び出している事例です。

https://qiita.com/mylifewithviolin/items/21fa8a6e7531c7d67196

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。2025年は日本語プログラミング言語Mind生誕４０周年です。

## 本記事シリーズのご紹介
本記事シリーズ「日本語プログラミング言語Mindの小技」は「日本語プログラミング言語Mind生誕４０周年プロジェクト」の一環です。

興味を持たれた方は[日本語プログラミング言語Mind公式サイト](https://www.scripts-lab.co.jp/mind8download/download.html)にアクセスすると、Mindコンパイラをダウンロードできます。

面白い！、楽しい、カンタン、難しいのも書ける！みんなでやってみよう:relaxed:
