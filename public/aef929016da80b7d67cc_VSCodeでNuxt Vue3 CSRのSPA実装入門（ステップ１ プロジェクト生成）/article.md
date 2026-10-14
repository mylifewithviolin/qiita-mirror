# はじめに
VSCode(Visual Studio Code)でNuxtのVue3でCSRのSPAを実装してみる入門のステップ１です。まずはとっかかりとしてプロジェクトのテンプレートを生成してみます。環境はVSCodeExtensionの実装用に導入した状態ですので最新ではないです。

 # 前提条件
Windows11 Pro 22H2 22621.4169
VSCode(Visual Studo Code)　1.95.1
node 20.10.0 -> 22.12.0
npm 10.9.0


# Nuxtアプリケーションプロジェクトの作成

## create-nuxt-appのインストール
最初に create-nuxt-appをインストールします。
まず、コマンドプロンプトを起動して、下記のようにコマンドをタイプします。
(最初のはどんなnodeとnpmが入っているかの念のための確認です。入っていることに確信のある人は実行不要です。）

```cmd:
C:\developments\vscode>node -v
v20.10.0
C:\developments\vscode>npm -version
10.9.0
C:\developments\vscode>npm install -g create-nuxt-app@latest
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
\^Cバッチ ジョブを終了しますか (Y/N)? Y
```

最初の警告は、inflightというパッケージが古くなっており、メモリリークの問題があるため推奨されないことを示しています。深刻度は低くないようなのでいったん中断しました。

```cmd:
C:\developments\vscode>node -v
v22.12.0
```
インストール手順は割愛しましたが、nodeのバージョンをあげました。この状態でcreate-nuxt-appをインストールします。

```cmd:
C:\developments\vscode>npm install -g create-nuxt-app@latest
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated

changed 380 packages in 10m

15 packages are looking for funding
  run `npm fund` for details
```

警告の出具合は変化ありませんでしたが、評価検証用の環境のためこのまま続行します。

## create-nuxt-appの実行
件名にあるVue3 CSRのSPAをTypeScriptで実装するプロジェクトを作成します。この目的に沿うため、いくつかの質問に適切に応答する必要があります。

```cmd:
C:\developments\vscode>create-nuxt-app vue3csr

create-nuxt-app v5.0.0
✨  Generating Nuxt.js project in vue3csr
? Project name: vue3csr
? Programming language: TypeScript
? Package manager: Npm
? UI framework: (Use arrow keys)
? UI framework: Bootstrap Vue
? Template engine: HTML
? Nuxt.js modules: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Linting tools: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Testing framework: None
? Rendering mode: Single Page App
? Deployment target: Server (Node.js hosting)
? Development tools: Dependabot (For auto-updating dependencies, GitHub only)
? What is your GitHub username? mylifewithviolin
? Version control system: Git
```
最後の質問に応答すると、インストール時よりも大量の警告が出力された後、取り合えずプロジェクト作成は成功します。

```cmd:
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated @babel/plugin-proposal-private-methods@7.18.6: This proposal has been merged to the ECMAScript stan
dard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated @babel/plugin-proposal-private-methods@7.18.6: This proposal has been merged to the ECMAScript stan
dard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.
npm warn deprecated @babel/plugin-proposal-class-properties@7.18.6: This proposal has been merged to the ECMAScript sta
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated @babel/plugin-proposal-private-methods@7.18.6: This proposal has been merged to the ECMAScript stan
dard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.
npm warn deprecated @babel/plugin-proposal-class-properties@7.18.6: This proposal has been merged to the ECMAScript sta
ndard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-class-properties instead.
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated @babel/plugin-proposal-private-methods@7.18.6: This proposal has been merged to the ECMAScript stan
dard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.
npm warn deprecated @babel/plugin-proposal-class-properties@7.18.6: This proposal has been merged to the ECMAScript sta
ndard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-class-properties instead.
npm warn deprecated @babel/plugin-proposal-nullish-coalescing-operator@7.18.6: This proposal has been merged to the ECM
AScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-nullish-coalescing-op
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache
if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and power
ful.
npm warn deprecated source-map-url@0.4.1: See https://github.com/lydell/source-map-url#deprecated
npm warn deprecated rimraf@2.7.1: Rimraf versions prior to v4 are no longer supported
npm warn deprecated move-concurrently@1.0.1: This package is no longer supported.
npm warn deprecated figgy-pudding@3.5.2: This module is no longer supported.
npm warn deprecated urix@0.1.0: Please see https://github.com/lydell/urix#deprecated
npm warn deprecated stable@0.1.8: Modern JS already guarantees Array#sort() is a stable sort, so this library is deprec
ated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Obje
cts/Array/sort#browser_compatibility
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated glob@8.1.0: Glob versions prior to v9 are no longer supported
npm warn deprecated copy-concurrently@1.0.5: This package is no longer supported.
npm warn deprecated source-map-resolve@0.5.3: See https://github.com/lydell/source-map-resolve#deprecated
npm warn deprecated resolve-url@0.2.1: https://github.com/lydell/resolve-url#deprecated
npm warn deprecated consolidate@0.15.1: Please upgrade to consolidate v1.0.0+ as it has been modernized with several lo
ng-awaited fixes implemented. Maintenance is supported by Forward Email at https://forwardemail.net ; follow/watch http
s://github.com/ladjs/consolidate for updates and release changelog
npm warn deprecated @npmcli/move-file@1.1.2: This functionality has been moved to @npmcli/fs
npm warn deprecated fs-write-stream-atomic@1.0.10: This package is no longer supported.
npm warn deprecated @babel/plugin-proposal-private-methods@7.18.6: This proposal has been merged to the ECMAScript stan
dard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.
npm warn deprecated @babel/plugin-proposal-class-properties@7.18.6: This proposal has been merged to the ECMAScript sta
ndard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-class-properties instead.
npm warn deprecated @babel/plugin-proposal-nullish-coalescing-operator@7.18.6: This proposal has been merged to the ECM
AScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-nullish-coalescing-op
erator instead.
npm warn deprecated @babel/plugin-proposal-private-property-in-object@7.21.11: This proposal has been merged to the ECM
AScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-property-in-o
bject instead.
npm warn deprecated @babel/plugin-proposal-optional-chaining@7.21.0: This proposal has been merged to the ECMAScript st
andard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-optional-chaining instead.
npm warn deprecated nuxt@2.18.1: Nuxt 2 has reached EOL and is no longer actively maintained. See https://nuxt.com/blog
/nuxt2-eol for more details.
npm warn deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm warn deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm warn deprecated popper.js@1.16.1: You can find the new Popper v2 at @popperjs/core, this package is dedicated to th
e legacy v1
npm warn deprecated vue@2.7.16: Vue 2 has reached EOL and is no longer actively maintained. See https://v2.vuejs.org/eo
l/ for more details.


added 1303 packages, and audited 1304 packages in 3m

🎉  Successfully created project vue3csr

  To get started:

        cd vue3csr
        npm run dev

  To build & start for production:

        cd vue3csr
        npm run build
        npm run start


  For TypeScript users.

  See : https://typescript.nuxtjs.org/cookbook/components/
```

## プロジェクトのフォルダ構成

下記のようなフォルダ構成でプロジェクトが生成されています。nodeとvueで開発したことがあるひとならなんとなくわかりそうな構成。

```cmd:
C:\developments\vscode>cd vue3csr

C:\developments\vscode\vue3csr>dir
 C:\developments\vscode\vue3csr のディレクトリ

2024/12/30  12:57    <DIR>          .
2024/12/30  12:54    <DIR>          ..
2024/12/30  12:54               207 .editorconfig
2024/12/30  12:54    <DIR>          .github
2024/12/30  12:54             1,253 .gitignore
2024/12/30  12:54    <DIR>          components
2024/12/30  12:57    <DIR>          node_modules
2024/12/30  12:54             1,213 nuxt.config.js
2024/12/30  12:57           644,411 package-lock.json
2024/12/30  12:54               518 package.json
2024/12/30  12:54    <DIR>          pages
2024/12/30  12:54             2,792 README.md
2024/12/30  12:54    <DIR>          static
2024/12/30  12:54    <DIR>          store
2024/12/30  12:54               581 tsconfig.json
               7 個のファイル             650,975 バイト
               8 個のディレクトリ   4,749,250,560 バイトの空き領域
```

大量のサブフォルダのあるnode_modulesフォルダの配下は割愛してTREEを構成すると下記のような感じとなります。

```cmd:
C:.
│  .editorconfig
│  .gitignore
│  nuxt.config.js
│  package-lock.json
│  package.json
│  README.md
│  tree.txt
│  tsconfig.json
│  
├─.github
│      dependabot.yml
│      
├─components
│      NuxtLogo.vue
│      Tutorial.vue
│      
├─node_modules
│  │  .package-lock.json
│
├─pages
│      index.vue
│
├─static
│      favicon.ico
│
└─store
        README.md

```


# VSCodeを起動
vue3csrフォルダをカレントにしてVSCodeを起動します。

```cmd:
C:\developments\vscode\vue3csr>code .
```

VSCodeが起動しましても、拡張機能の推奨事項がウィンドウ右下に表示されませんでした。とりあえずこのままとします。

![vue3csr1.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/cb0d308e-0ea0-983e-b771-ad6e40f11db3.png)

nuxt.config.jsを開いてみますとssrオプションはfalseとなっていますので、CSRで生成されたことが確認できます。

taskやlaunchをまだ構成できていませんが、とりあえずコマンドプロンプトのターミナルを開いてプロジェクトをビルドします。npm run buildとタイプ。

![vue3csr2.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/c5348d02-7de0-ae12-4ea8-3cbf1915b8d6.png)

いちおう成功したみたいなので起動してみます。npm run startとタイプ。
> Listening: http:\/\/localhost:3000/

がターミナルにエコーされたのでアクセスしてみます。


![vue3csr3.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3118036/cb60ff2e-a8a6-f9c2-cb36-1b053858ac1b.png)

無事にNuxtアプリケーションのご挨拶vueが展開しました。


次回はtaskやlaunchを構成し、index.vueになにかサンプル実装してデバッグ実行してみます。

# おわりに
いかがでしたでしょうか？なにかの参考になれば幸いです。
