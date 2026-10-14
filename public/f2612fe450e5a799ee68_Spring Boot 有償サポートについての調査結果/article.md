# はじめに

Spring Boot 2.7.5のOSSサポートの終了が2023年11月18日に迫る中、VMware社が提供する有償サポートとはどんなものなのかを調査してみた結果のお話ですが、期待はしないでください。決定的に有用な情報は得られていません。私個人の備忘録のようなもの。

# 有償サポート提供ベンダー

[VMware Tanzu - VMware Spring Runtime](https://tanzu.vmware.com/jp/spring-runtime)

[Microsoft - Azure Spring Apps](https://azure.microsoft.com/ja-jp/products/spring-apps/)

# VMware Spring Runtime

[Spring Boot日本語サイトのサポート期間](https://spring.pleiades.io/projects/spring-boot#support)の[有償サポートについて (*)]の但し書きみたいなところからVMware社が提供する有償サポートの日本語紹介ページへジャンプできます。

VMware社のTanzu製品・サービスは正直認識がありませんでした。Kubernetesはdockerの管理ツールといった程度。

https://frontier.networld.co.jp/knowhow-vmwaretanzu/tanzu-intro3-overview/

上記サイトからの引用
>Tanzuは、VMwareが提供するKubernetes関連製品群の総称で、Kubernetesに対応したソフトウエアの開発を支援するための一連のソフトウエアやサービスなどを含んでいます。

VMware Spring Runtimeサイトのよくある質問（FAQ)からの引用
>他のTanzu製品やサブスクリプションを購入せずに、VMware Spring Runtimeだけを購入することはできますか？
はい。VMware Spring Runtimeはあらゆる企業でご利用いただけます。

Spring Boot 有償サポートだけを別契約できそうということがわかっただけです。

下記はBingのCoPilotに問い合わせしてみた結果です。（「Spring Boot 有償サポート 価格例」 ）
>Spring Boot の提供元は、VMware です。VMware は Spring Boot および Spring Framework に対してサポートを提供しています。Spring Boot には、無料のコミュニティサポートと有償のプレミアムサポートがあります。有償サポートの価格は公式サイトに掲載されていませんが、お問い合わせフォームから問い合わせることができます。

価格を知るには問い合わせフォームからお問い合わせする必要がありそうです。

# Microsoft Azure Spring Apps

こちらはMicrosoft Azure上で利用することが前提そうです。（VMware Tanzu をAzureに乗っけたイメージ？）Azureの価格シミュレータで、想定スペック上の月額利用費などは見積もりできそう。「Microsoft と VMware のフル マネージド サービス」とありますので、実際のサポート提供主体はVMwareのようです。

https://azure.microsoft.com/ja-jp/pricing/calculator/?service=spring-apps


参考値ですが、下記の条件の仮想マシンスペックで下記のような結果がでました。
Azure Spring Apps
リージョン 東日本
Standard レベル、6 vCPU、12 GB メモリ、730 時間
複製削除
前払い: $0.00
月払い: $613.78

これに加えて、（上記のサポートオプションは[無償]）

サポート 標準
$100.00

サポートオプションが無償の場合はどのようなサポートなのかはちょっと調べきれませんでした。
標準サポートのご説明
>Standard サポートは、Azure の利用がビジネス上最低限必要な小規模または中規模の企業を対象としています。

# おわりに

あくまで参考情報です。有益な情報をご存じの方はコメント欄にてご教授いただければ幸いです。
