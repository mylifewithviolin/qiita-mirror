# はじめに
Windows11上のVSCode統合のUbuntuターミナル(bash)は.profileを読み込んで、文字コードはEucJPになっているっぽい（コードエディタの文字コードもVSCodeのsettings.jsonでEucJPに設定済でこちらは問題ない）けど、統合ターミナル(bash)はUTF-8のままうんともすんともいわない。（UTF-8でものもうしている。）
統合ターミナル(bash)の文字コード設定方法が確定するまでのつなぎとして、TeraTermで接続できるよう構成する。

## この記事内容の作業目的
VSCode [WSL2:Ubuntu] をTeraTermで接続できるよう構成する。
EucJPネイティブアプリの文字出力をVSCode [WSL2:Ubuntu] で確認するため。

## この記事内容の作業環境
Windows11
Windows11WSL2（Ubuntu 22.04.1 LTS）
VSCode(Visual Studo Code)　VSCodeUserSetup-x64-1.67.2
TeraTerm teraterm-4.106

## この記事内容の保証
※この記事には環境構築の手順的な情報が含まれます。本記事に書かれた手順の妥当性は保証されません

# sshdのインストール
実行環境はVSCode [WSL2:Ubuntu] です。
VSCodeが起動してWSL2:Ubuntu22.04.1 LTSが起動している状態です。

TeraTermで接続できるようになるまでは統合ターミナル(bash)で作業します。

sshdをインストールします。
WSL2:Ubuntu22.04.1 LTSには/etc/sshフォルダにssh.confはあってもsshd.confがなかったため、sshdをインストールしました。
```bash:
$ sudo apt install ssh
```

こちらの記事を参考にしました。
[How to Enable SSH Service in Ubuntu 22.04 LTS](https://ubuntuhandbook.org/index.php/2022/04/enable-ssh-ubuntu-22-04/)

# sshd構成・起動

あとはこちらにまとめていただいている手順とまったくいっしょです。この当時のWSL:Ubuntuにはsshdが入っているけど起動はしていないという想定で書かれているようです。
[WSL:【Teraterm接続】する方法（Ubuntu）](https://broaden-your-horizons.com/ai-ss/wsl/teraterm/)

```bash:
$ ps -ef|grep ssh|grep -v grep
```
上記コマンドのエコーの返りがないことが起動していないことを意味します。
```bash:
$ sudo ssh-keygen -A
ssh-keygen: generating new host keys: RSA DSA ECDSA ED25519 
$ cd /etc/ssh
$ sudo cp -p sshd_config sshd_config.bk
```
VSCodeのコードエディタは/etc/sshを開けないので古典エディタで編集します。
```bash:
$ sudo vi sshd_config
```
差分が下記のように出るよう編集します。詳しくは参考リンクに書かれています。
```bash:
$ diff sshd_config.bk sshd_config
33c33
< #PermitRootLogin prohibit-password
---
> PermitRootLogin no
57c57
< #PasswordAuthentication yes
---
> PasswordAuthentication yes
```
sshdを起動して、冒頭のコマンドで起動状態を確認します。
```bash:
$ sudo service ssh start
 * Starting OpenBSD Secure Shell server sshd 
$ ps -ef|grep ssh|grep -v grep
root      2244  1282  0 23:20 pts/4    00:00:00 sudo vi sshd_config
root      2245  2244  0 23:20 pts/5    00:00:00 sudo vi sshd_config
root      2246  2245  0 23:20 pts/5    00:00:00 vi sshd_config
root      3818   874  0 23:28 ?        00:00:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
```

# TeraTermでssh接続

 TeraTermを起動してSSHポート22のlocalhostで接続します。
パスワードの設定が求められるので設定しましょう。

![teratermmind.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9de59375-c632-9138-dd7b-2c82fe3b1d0e.png)

無事に接続できました！

# 参考リンク

[How to Enable SSH Service in Ubuntu 22.04 LTS](https://ubuntuhandbook.org/index.php/2022/04/enable-ssh-ubuntu-22-04/)

[WSL:【Teraterm接続】する方法（Ubuntu）](https://broaden-your-horizons.com/ai-ss/wsl/teraterm/)
