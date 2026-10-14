# はじめに
ElectronでHello World!してみました。[Quick-start](https://www.electronjs.org/ja/docs/latest/tutorial/quick-start)では、「Hello World!」はindex.htmlのHタグのリテラル文字列だったので、そのあたりだけちょいとアプリケーション的な感じに書き換えてみました。

# Electronとはとかインストールとか

すべて割愛します。Qiita上にたくさん親切に記述された記事がありますので、それらからなるべく新し目の情報を参照するとよいかと思います。

# 配置
```cmd
C:\electron>dir /B
index.html
main.js
node_modules
package-lock.json
package.json
preload.js
```

# index.html
Quick-start記載のindex.htmlを下記のように変更しました。
従来は\<h1>タグの中にリテラルで書かれていましたが、\<span>タグにしました。

```diff_html:index.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
-    <title>Hello World!</title>
+    <title>evalute electron</title>
  </head>
  <body>
-    <h1>Hello World!</h1>
+    <h1><span id="message"></h1>
    We are using Node.js <span id="node-version"></span>,
    Chromium <span id="chrome-version"></span>,
    and Electron <span id="electron-version"></span>.
  </body>
</html>
```

\<span>タグを動的に置換するのはtymeleafを連想しました。

# preload.js
Quick-start記載のpreload.jsを下記のように変更しました。
```diff_javascript:preload.js
// preload.js

window.addEventListener('DOMContentLoaded', () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector)
    if (element) element.innerText = text
  }

  for (const dependency of ['chrome', 'node', 'electron']) {
    replaceText(`${dependency}-version`, process.versions[dependency])
  }
+  replaceText(`message`, `Hello World!`)
})
```


# main.js
基本的にはロジック的なことはなにも修正していませんが、開発者ツールの展開が無効化されていましたので、コメントアウト解除しました。
```diff_javascript:main.js
const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  })

  mainWindow.loadFile('index.html')
-  // mainWindow.webContents.openDevTools()
+  mainWindow.webContents.openDevTools()
}
```

 # 実行結果
 それでは実行してみます。
 
```cmd
C:\electron>C:\electron\node_modules\.bin\electron .
```
環境変数がセットアップされていませんので、フルパスで指定しています。

![electron.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/9dde46f8-4fdd-e66d-7834-f3ff1a8b8f5b.jpeg)

開発者ツールも同時に展開しました。\<span id="message">タグに「Hello World!」が無事に挿入されました。

# おわりに
Electronなかなか楽しいです。
