# タイ保険バズ投稿収集ツール

DuckDuckGo検索でタイ保険関連のSNS投稿（X / Threads / Facebook）を収集するツール一式。

## フォルダ構成

```
buzz_collector_tool/
├── buzz_collector/      # メインスクリプト
├── .github/             # GitHub Actions 定期実行
├── .cursor/             # Cursor 設定
├── requirements.txt
├── .gitignore
└── README.md
```

## ローカル実行

```bash
cd buzz_collector
pip install -r requirements.txt
python buzz_collector.py
```

## GitHub Actions

- 毎日 9:00 JST に自動実行
- レポートは Actions → Artifacts からダウンロード
