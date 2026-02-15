# GitHub Actions 定期実行の設定

## 概要

`buzz_collector.yml` により、**毎日 9:00 JST** にタイ保険バズ投稿収集が自動実行されます。
PC を起動していなくても、GitHub のサーバー上で実行されます。

## セットアップ手順

1. **GitHub リポジトリを作成**
   - GitHub で新規リポジトリを作成
   - リポジトリのルートに `buzz_collector.py`、`requirements.txt`、`.github/workflows/` がある状態にする

2. **コードを push**
   ```bash
   cd /path/to/insurance
   git init
   git add buzz_collector.py requirements.txt .github/
   git commit -m "Add buzz collector and GitHub Actions"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Actions を有効化**
   - リポジトリの「Actions」タブでワークフローが有効になっていることを確認

## レポートの取得方法

- 実行後、**Actions** タブ → 該当の実行 → **Artifacts** から `buzz-reports-xxx` をダウンロード
- レポートは 30 日間保持されます

## 手動実行

- **Actions** タブ → 「タイ保険バズ投稿収集」→ **Run workflow** で任意のタイミングで実行可能
