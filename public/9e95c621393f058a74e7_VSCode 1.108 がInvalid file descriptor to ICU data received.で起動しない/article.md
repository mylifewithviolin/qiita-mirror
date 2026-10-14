# はじめに
VSCode 1.108がショートカットやコマンドプロンプトでカレントフォルダからのcode .で突然起動しなくなった。2026年1月12日の午後2時ごろ。その直前は普通に３つくらい起動していた。１つなんか閉じてしまったので開きなおそうとしたらまったく応答せず、タスクマネージャにも出現せず。OS再起動しても変わらず。

# 環境
Windows11 Pro 22H2 22621.4317
VSCode　1.108.0　2026年1月8日にアップデート更新


# Invalid file descriptor to ICU data received.というエラー
ただし、コマンドラインからのcodeでは下記のエラーが出たので、これを使って検索したところ

```cmd:
C:\developments\vscode>code .
[0112/144938.163:ERROR:base\i18n\icu_util.cc:223] Invalid file descriptor to ICU data received.
```
下記のイッシューが該当するようだった。


https://github.com/microsoft/vscode/issues/282920


ショートカット先でパスが通っている下記のフォルダのCode.exeを起動すると、同じエラーで起動しない。

```cmd:
C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code>code

C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code>
[0112/143039.857:ERROR:base\i18n\icu_util.cc:223] Invalid file descriptor to ICU data received.
```

しかし、icudtl.datが存在する下記のフォルダのCode.exeはエクスプローラからダブルクリックすると起動したので、下記のようにコマンドから起動すると、また異なるエラーを吐き出しながらも起動はしていることが判明。

```cmd:
C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code>cd _

C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\_>code

C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\_>
[13084:0112/143059.480:ERROR:ui\base\resource\resource_bundle.cc:1102] Failed to load C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\_\chrome_100_percent.pak
Some features may not be available.
[0112/143059.667:ERROR:ui\base\resource\resource_bundle.cc:1102] Failed to load C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\_\chrome_100_percent.pak
Some features may not be available.
[main 2026-01-12T05:31:00.290Z] update#setState idle
[main 2026-01-12T05:31:02.375Z] vscode-file: Refused to load resource c:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\resources\app\extensions\theme-seti\icons\seti.woff from vscode-file: protocol (original URL: vscode-file://vscode-app/c:/Users/mylifewithviolin/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/extensions/theme-seti/icons/seti.woff)
[main 2026-01-12T05:31:30.335Z] update#setState checking for updates
[main 2026-01-12T05:31:30.924Z] update#setState idle

C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code\_>
```

プロンプトはEnterキーを押したら戻ってきた。

# Microsoft VS Code\\_フォルダのCode.exeをMicrosoft VS Codeフォルダにコピーしてみる

変化なし。
```cmd:
C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code>code

C:\Users\mylifewithviolin\AppData\Local\Programs\Microsoft VS Code>
[0112/143039.857:ERROR:base\i18n\icu_util.cc:223] Invalid file descriptor to ICU data received.
```
# おわりに
イッシューに記載のとおり、このバージョンでは再インストールで直すしかない模様。VSCodeUserSetup-x64-1.108.0.exeをダウンロードし、再インストールで回復した。

# 参考
icudtl.datはMicrosoft VS Code\\_フォルダには存在していてMicrosoft VS Codeフォルダにはなかったようだが、再インストールでMicrosoft VS Codeフォルダにも存在するようになった気がする。

いまとなってはエビデンスがないが、再発した場合はMicrosoft VS Code\\_フォルダのicudtl.datをMicrosoft VS Codeフォルダにコピーしてみることとする。
