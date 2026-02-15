#!/usr/bin/env python3
"""タイ保険バズ投稿収集ツール
API不要・DuckDuckGo検索でSNS投稿を収集。
X / Threads / Facebook を site: フィルタで検索。
優先順位: 今日 > 直近3日 > それ以前（DDGの timelimit: d=今日, w=1週間 で取得）
※エンゲージメントは取得不可のため、検索結果の上位表示を注目度の指標として利用。
"""

import os
import time
from datetime import datetime

from ddgs import DDGS

# --- パス設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# --- 検索キーワード ---
KEYWORDS = [
    "タイ 保険 日本人",
    "タイ 生命保険",
    "タイ 貯蓄型保険",
    "海外保険 タイ",
    "タイ在住 保険",
]

MAX_RESULTS_PER_QUERY = 25

# 除外URLパターン（検索ノイズを除去）
EXCLUDED_URL_PATTERNS = [
    "help.x.com", "about.x.com", "blog.x.com", "analytics.twitter.com",
    "help.twitter.com", "about.twitter.com",
    "help.instagram.com", "about.facebook.com", "help.facebook.com",
    "/adsct?", "/mob_idsync",
]


def is_relevant_url(url: str) -> bool:
    """除外パターンに該当しないURLか"""
    return not any(pattern in url for pattern in EXCLUDED_URL_PATTERNS)


def search_ddg(query: str, region: str = "jp-jp", timelimit: str | None = None) -> list[dict]:
    """DuckDuckGoでテキスト検索（APIキー不要）
    timelimit: d=今日, w=直近1週間, m=1ヶ月, y=1年
    """
    try:
        results = DDGS().text(
            query,
            region=region,
            safesearch="moderate",
            timelimit=timelimit,
            max_results=MAX_RESULTS_PER_QUERY,
        )
        return list(results) if results else []
    except Exception as e:
        print(f"  [エラー] DuckDuckGo検索失敗: {query} -> {e}")
        return []


def _search_by_site(site_filters: list[str], platform_name: str) -> list[dict]:
    """site: フィルタでプラットフォーム別に検索
    優先順位: 今日(d) > 直近1週間(w、今日を除く)
    """
    today_results = []
    week_results = []
    today_urls = set()

    for keyword in KEYWORDS:
        for site_filter in site_filters:
            query = f"{keyword} {site_filter}"

            # 1. 今日の結果を最優先で取得
            print(f"  検索（今日）: {query}")
            raw_today = search_ddg(query, timelimit="d")
            for r in raw_today:
                url = r.get("href", "")
                if not url or not is_relevant_url(url):
                    continue
                if url not in today_urls:
                    today_urls.add(url)
                    today_results.append({
                        "keyword": keyword,
                        "title": r.get("title", "(タイトルなし)"),
                        "url": url,
                        "snippet": r.get("body", "(スニペットなし)"),
                        "recency": "今日",
                    })
            time.sleep(2)

            # 2. 直近1週間の結果（今日と重複しないもの＝直近3日程度をカバー）
            print(f"  検索（直近1週間）: {query}")
            raw_week = search_ddg(query, timelimit="w")
            for r in raw_week:
                url = r.get("href", "")
                if not url or not is_relevant_url(url):
                    continue
                if url not in today_urls:
                    today_urls.add(url)  # 重複防止
                    week_results.append({
                        "keyword": keyword,
                        "title": r.get("title", "(タイトルなし)"),
                        "url": url,
                        "snippet": r.get("body", "(スニペットなし)"),
                        "recency": "直近1週間",
                    })
            time.sleep(2)

    # 今日を先に、次に直近1週間
    return today_results + week_results


def collect_results() -> dict:
    """DuckDuckGo検索でSNSから投稿を収集（API不要、毎回新規検索）"""
    all_results = {}

    # --- X (Twitter) ---
    print(f"\n{'='*60}")
    print(" Twitter/X を検索中（DuckDuckGo）...")
    print(f"{'='*60}")
    all_results["Twitter/X"] = _search_by_site(
        ["site:x.com", "site:twitter.com"],
        "Twitter/X",
    )
    print(f"  -> {len(all_results['Twitter/X'])} 件")

    # --- Threads ---
    print(f"\n{'='*60}")
    print(" Threads を検索中（DuckDuckGo）...")
    print(f"{'='*60}")
    all_results["Threads"] = _search_by_site(
        ["site:threads.net"],
        "Threads",
    )
    print(f"  -> {len(all_results['Threads'])} 件")

    # --- Facebook ---
    print(f"\n{'='*60}")
    print(" Facebook を検索中（DuckDuckGo）...")
    print(f"{'='*60}")
    all_results["Facebook"] = _search_by_site(
        ["site:facebook.com"],
        "Facebook",
    )
    print(f"  -> {len(all_results['Facebook'])} 件")

    return all_results


def format_report(results: dict) -> str:
    now = datetime.now()
    lines = [
        "=" * 70,
        "タイ保険 バズ投稿収集レポート",
        f"生成日時: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"対象: タイ在住日本人向け保険関連",
        "取得方法: DuckDuckGo検索（API不要）",
        "優先順位: 今日 > 直近1週間（DDGの制限により直近3日は「直近1週間」に含む）",
        "※エンゲージメントは取得不可。検索上位表示を注目度の参考に。",
        "=" * 70,
    ]

    total = 0
    for platform, items in results.items():
        total += len(items)
        lines.append("")
        lines.append(f"{'─'*70}")
        lines.append(f"■ {platform} ({len(items)}件)")
        lines.append(f"{'─'*70}")

        if not items:
            lines.append("  (該当する投稿が見つかりませんでした)")
            continue

        for i, item in enumerate(items, 1):
            lines.append(f"\n  [{i}] {item['title']}")
            lines.append(f"      URL: {item['url']}")
            lines.append(f"      キーワード: {item['keyword']}")
            if item.get("recency"):
                lines.append(f"      新しさ: {item['recency']}")
            lines.append(f"      概要: {item['snippet']}")

    lines.extend([
        "",
        f"{'='*70}",
        f"合計: {total} 件",
        f"検索キーワード: {', '.join(KEYWORDS)}",
        f"{'='*70}",
    ])
    return "\n".join(lines)


def save_report(report: str) -> str:
    os.makedirs(REPORT_DIR, exist_ok=True)
    filename = f"buzz_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(REPORT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    return filepath


def main():
    print("タイ保険 バズ投稿収集ツール")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("（DuckDuckGo検索・API不要・常に最新の検索結果を取得）")

    results = collect_results()
    report = format_report(results)

    print("\n")
    print(report)

    filepath = save_report(report)
    print(f"\nレポート保存先: {filepath}")


if __name__ == "__main__":
    main()
