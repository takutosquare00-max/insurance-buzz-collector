# タイ保険バズ投稿収集ツール

DuckDuckGo検索でタイ保険関連のSNS投稿（X / Threads / Facebook）を収集するツール。

## 特徴

- **API不要**: DuckDuckGo検索のみで動作
- **優先順位**: 今日 > 直近1週間
- **定期実行**: GitHub Actions で毎日 9:00 JST に自動実行

## ローカル実行

```bash
cd buzz_collector
pip install -r requirements.txt
python buzz_collector.py
```

レポートは `buzz_collector/reports/` に保存されます。

## GitHub Actions 定期実行

- **スケジュール**: 毎日 9:00 JST
- **レポート取得**: Actions タブ → 該当の実行 → Artifacts からダウンロード
- **手動実行**: Actions タブ → 「タイ保険バズ投稿収集」→ Run workflow
