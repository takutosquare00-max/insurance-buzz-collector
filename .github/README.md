# GitHub Actions 定期実行の設定

## 概要

`buzz_collector.yml` により、**毎日 9:00 JST** にタイ保険バズ投稿収集が自動実行されます。
PC を起動していなくても、GitHub のサーバー上で実行されます。

ツール本体は `buzz_collector/` フォルダに格納されています。

## レポートの取得方法

- 実行後、**Actions** タブ → 該当の実行 → **Artifacts** から `buzz-reports-xxx` をダウンロード
- レポートは 30 日間保持されます

## 手動実行

- **Actions** タブ → 「タイ保険バズ投稿収集」→ **Run workflow** で任意のタイミングで実行可能
