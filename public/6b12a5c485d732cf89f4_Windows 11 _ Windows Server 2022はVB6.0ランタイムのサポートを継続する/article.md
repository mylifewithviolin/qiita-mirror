# はじめに

Qiitaの記事で[Windows 11はVB6.0アプリのサポートを継続するか](https://qiita.com/yaju/items/1ba0fd5466230c963052)というのを発見した。
確定情報は追記されてないようなので、記事にしておきました。

## この記事内容の作業目的
自作言語Re:Mindのターゲット言語としてVisualBasic6.0を含めるか検討します。（開発環境はEOSしてるのを知らないとか勘違いしているとかではないです。）
## この記事内容の作業環境
Windows 11 22H2
## この記事内容の保証
※この記事にはMicrosoft社の公表情報が含まれます。引用ソース情報の妥当性は保証されません。
# Windows 11/ Windows Server 2022はVB6.0ランタイムのサポートを継続する

参考リンクからの引用
The Visual Basic team is committed to "It Just Works" compatibility for Visual Basic 6.0 applications on the following supported Windows operating systems:

Windows 11
Windows Server 2022

**2026/01/01追記**
Windows operating system versions that support VB6
Windows Server 2025

## Windows 11 22H2に格納されているバージョン
msvbvm60.dll
6.00.98.48
2022/05/07 14:20:00

## Windows 11 22H2に格納されているフォルダ
C:\Windows\SysWOW64
C:\Windows\WinSxS\wow64_microsoft-windows-msvbvm60_31bf3856ad364e35_10.0.22621.1_none_2e6e3ad979d8cfb7

# おわりに
マイクロソフト社による長期サポートには頭の下がる思いです。
わたしはVisual Basic6.0の直前バージョンVisual Basic5.0/Visual Studio 97を自費購入しました。けっこう高かったです。Let's Noteがまだ銀色でなく30万円強した時代でした。VisualC++で書くよりGUIやデータベースがシンプルに書けるのに驚いた記憶があります。
.NETではないクロスコンパイラのVisual Basicって見てみたいな。
# 参考リンク

https://learn.microsoft.com/ja-jp/previous-versions/visualstudio/visual-basic-6/visual-basic-6-support-policy


https://qiita.com/yaju/items/1ba0fd5466230c963052
