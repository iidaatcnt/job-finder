import time
import os
import sys

# brainディレクトリとcrawlersディレクトリをモジュールとして読み込めるようにパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain.analyzer import analyze_job

def mock_get_jobs():
    """
    Google Custom Search APIが開通するまでの間、テスト用の求人データを提供するモック（代用）関数です。
    """
    return [
        {
            "title": "【フルリモート/業務委託】Pythonエンジニア（業務改善bot・ツール開発）",
            "snippet": "社内の業務効率化のためのPythonスクリプト開発やDiscord botの運用をお願いします。要件定義から一人称で動けるITリテラシーの高い方を求めています。完全リモート稼働で、週3日〜OKです。",
            "link": "https://example.com/job/1"
        },
        {
            "title": "週5日出社必須/客先常駐エンジニア【派遣社員】",
            "snippet": "都内オフィスへの常駐が必須のシステム開発案件です。レガシーシステムの保守がメインとなります。開発言語は特に問いません。",
            "link": "https://example.com/job/2"
        },
        {
            "title": "【業務委託/在宅】WordPress・WooCommerce特化のWeb開発",
            "snippet": "新規のEC・学習サイト構築プロジェクトで、WordPressおよびWooCommerce、TutorLMSに精通したエンジニアを探しています。フルリモートで、設計から実装までお任せします。",
            "link": "https://example.com/job/3"
        }
    ]

def main():
    print("🚀 Sojourner (Job Finder) メインシステムを起動します...\n")
    
    print("🔍 [STEP 1] インターネットから最新の求人情報を収集しています...")
    # ※Google APIが開通（403エラー解消）したら、ここを本物の google_search.py の関数に切り替えます
    jobs = mock_get_jobs()
    time.sleep(1) # モックなのであえて少し待つ演出
    print(f"✅ {len(jobs)} 件の求人候補が見つかりました（現在はテスト用ダミーデータ）。\n")
    
    print("🧠 [STEP 2] Gemini AI による適合度判定（Analayzer）を開始します...")
    print("-" * 60)
    
    for i, job in enumerate(jobs, 1):
        print(f"\n▼▼▼ ターゲット案件 {i} ▼▼▼")
        print(f"【タイトル】: {job['title']}")
        print(f"【URL】: {job['link']}")
        print(f"【概要】: {job['snippet']}")
        
        # Analyzer (AI) に案件情報を渡して判定させる
        analyze_job(job['title'], job['snippet'])
        
        # API制限（連投スパム判定）を防ぐため、1件分析するごとに3秒休憩する
        if i < len(jobs):
            print("⏳ 次の案件の分析準備中（3秒待機）...")
            time.sleep(3)

    print("\n🎉 全ての案件の分析が完了しました！")

if __name__ == "__main__":
    main()
