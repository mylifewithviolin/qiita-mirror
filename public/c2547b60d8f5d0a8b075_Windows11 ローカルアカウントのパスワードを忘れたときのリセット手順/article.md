# はじめに
最近、Windows11のローカルアカウントのパスワードを忘れた友だちの支援をしたので、その備忘録です。ネット上ではUbuntuで起動してユーティリティマネージャの実行ファイルをコマンドプロンプトの実行ファイルに書き換えるという説がありますが、セーフモードで起動するときなどのオプション詳細のコマンドプロンプトでもできたので、その手順メモです。

# 前提条件
Windows11 Pro 22H2
USBメモリにはリセットキーが退避されていない
セキュリティの質問の答えも忘れた場合

# Windows Utility managerの実行ファイル
これはwindows\system32フォルダ内に格納されているutilman.exeというファイルです。このファイルはWindowsログイン画面で、ログイン前に実行できるファイルということからターゲットになります。

※Windowsログイン画面の右下の電源アイコンの左となりの大の字になっているひとのアイコンをクリックすると表示されるメニューがutilman.exeによる動作です。

# コマンドプロンプトの実行ファイルをWindows Utility managerの実行ファイル名にする

これによって、Windowsログイン画面で、ログイン前にコマンドプロンプトを実行できるようにしてしまおうということです。

## トラブルシューティング用のコマンドプロンプトを起動する

まず、そのためにはトラブルシューティング用のコマンドプロンプトを起動します。シフトキーを押しながら起動、または再鼓動してブルースクリーンの「オプションの選択」を起動します。
「オプションの選択」からは下記の選択でコマンドプロンプトを起動します。

「オプションの選択」→「トラブルシューティング」→「オプション詳細」→「コマンドプロンプト」

管理者権限でコマンドプロンプトが起動します。
```:管理者:X:\Windows\System32\cmd.exe
Microsoft Windows [Version 10.0.22621.525]
(c) Microsoft Corporation. All rights reserved.

X:\Windows\System32>
```

X:\Windows\System32フォルダにはutilman.exeは存在しませんし、ログイン画面で起動されるのはシステムドライブのWindows\System32フォルダのutilman.exeなので、システムドライブのWindows\System32フォルダに移動しておくとよいでしょう。

```:管理者:X:\Windows\System32\cmd.exe
X:\Windows\System32>C:
C:\>

C:\>cd \Windows\System32
C:\Windows\System32>
```
## コマンドプロンプトcmd.exeをutilman.exeとしてコピーします。
このフォルダ上でutilman.exeをバックアップしてコマンドプロンプトcmd.exeをutilman.exeとしてコピーします。
```:管理者:X:\Windows\System32\cmd.exe
C:\Windows\System32>ren utilman.exe utilman.org

C:\Windows\System32>copy cmd.exe utilman.exe
        1 個のファイルをコピーしました。
```

これで準備OKです。トラブルシューティング用のコマンドプロンプトを抜けて、オプションの選択に戻ってWindows11の通常実行に進行します。

# windowsログイン画面でコマンドプロンプトutilman.exeを起動

Windowsログイン画面の右下の電源アイコンの左となりの大の字になっているひとのアイコンをクリックするとコマンドプロンプトが起動します。

```:C:\Windows\System32\utilman.exe
メッセージ番号 0x2350 のメッセージ文が Application のメッセージ ファイルに見つかりません。
(c) Microsoft Corporation. All rights reserved.
このコマンドを処理するにはメモリ リソースが足りません。
C:\Windows\System32>

```
この状態で下記のnet userコマンドでパスワードをリセットします。
userの次のuserはデフォルトのuserアカウントです。（Administratorグループ）ログイン画面には別名で表示されている場合があります。新規に追加したアカウントでフルネームと物理名がわかっている場合は物理名を指定してください。
*****は新しいパスワードをタイプします。下図は伏字になっていますが実際はそのままエコーされます。

```:C:\Windows\System32\utilman.exe
C:\Windows\System32>net user user *****
コマンドは正常に終了しました。
C:\Windows\System32>
```

# おわりに
ほとんど自分用の備忘録ですが、なにかのお役に立てれば幸いです。現時点ではこの手順でリセットできましたが、のちのセキュリティアップデートでこの手順は無効化されるかもしれません。
