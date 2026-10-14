# はじめに
SpringBootに依存した話ではないですが、JasperReportsのデザイナ環境でよく使われる各要素の「Print When Expression」プロパティについての備忘録です。

## この記事内容の作業目的
小一時間浪費したので備忘録。「Print When Expression」プロパティに言及した日本語情報はいくつかありますが、Javaを常用しているひとには既定のお話でとくに強調はされない、Java以降のC#やTypeScriptとか使っているとつい忘れてしまいがちな点。

## この記事内容の作業環境
Windows10 21H2
VSCode(Visual Studo Code)
java 11
SpringBoot
JasperReports 6.12
jusperStudio 6.12
## この記事内容の保証
※この記事には設定的な情報が含まれます。あらゆる条件下でも書かれた内容の妥当性を保証するものではありません。

# 設定のポイント

各要素の「Print When Expression」プロパティに設定する条件式はJavaで動いている。そのため、文字列同士A,Bの比較では

 A == B や A != B では常に不成立となる。こう書いてもコンパイル時にエラーにはならず実行時に意図した動作にはならない。

A.equals(B) や !A.equals(B)　で正常判定される。

# 参考リンク

https://stackoverflow.com/questions/294989/how-to-use-printwhenexpression-in-jasperreports
