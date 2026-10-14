# はじめに
要求仕様記述段階での使用が主に想定されている数学的形式手法VDM(Vienna Development Method)[^1]のオブジェクト指向拡張言語VDM++の検証ツールWindows版[^2]を公式サイト[^3]からダウンロードしてインストールしました。Windows11で起動してみましたところ、「MSVCR100.dllが見つからない」的なエラーメッセージがループして起動できませんでした。

# 「MSVCR100.dllが見つからない」の解決策
これは **M**icrosoft **V**isual **C**++ **R**untime version **100** が存在しないことによるエラーです。dllは **D**ynamic **L**ink **L**ibraryの略で実行時に動的にリンクされる言語ライブラリのことです。ランタイムライブラリ、または略してランタイムと呼ばれるファイルです。

VDM++の検証ツールWindows版はMSVC++で実装されていることがわかります。MSVC++の内部バージョン100はMSVC++2010です。WindowsOSが新しくなると古いバージョンのMSVC++ランタイムライブラリが格納されていない場合があります。

そのため、「Microsoft Visual C++ 2010 Service Pack 1 再頒布可能パッケージ」をダウンロードしてインストールしようとしたのですが、ダウンロードサイトの情報が更新されて意外と発見しづらかったため、備忘録として残しておきます。

## 古いランタイムが存在しないときに起こりうる問題
この件はVDM++の検証ツールに関わらず、古いランタイムで実装されたアプリケーションを新しめのWindowsで起動しようとした際に、古いランタイムが存在しないときに起こりうる問題として応用可能です。

# 2023/10/21時点 「Microsoft Visual C++ 2010 Service Pack 1 再頒布可能パッケージ」ダウンロードリンク

[Microsoft Visual C++ 2010 Service Pack 1 再頒布可能パッケージ MFC のセキュリティ更新プログラム](
https://www.microsoft.com/ja-JP/download/details.aspx?id=26999)

## ３つのWindowsOSアーキテクチャ
ここから下記の３つのWindowsOSアーキテクチャに対応したランタイムがダウンロードできます。
vcredist_ia64.exe Itanium
vcredist_x64.exe
vcredist_x86.exe

CPUがItaniumのパソコンは今日ほぼ見受けられませんが、パソコンのシステム情報からCPUがx64なのかx86なのかを確認して対応するインストーラをダウンロードしましょう。

[^1]: IBMのウィーン研究所で1960年代から70年代にかけて開発された形式手法。その実装には1996年にISO標準（ISO_IEC_13817-1）となったVDM-SLと、そのオブジェクト指向拡張のVDM++がある。
[^2]: FMVDM　[VDMTools VDMTools](http://fmvdm.org/vdmtools/index-ja.html)
[^3]: FMVDM　[VDMTools リリース版 (9.0.7) Windows VDM++](http://fmvdm.org/VDMTools/Windows/setuppp-9.0.7-vs10-x64.exe)
