import requests

def test_crawler():
    # クラウドフレアなどの遮断の影響を受けない Hacker News の公式公開APIをつかって
    # 「インターネットから最新の求人情報をJSONで取得する」コア部分の実証を行います
    url_stories = "https://hacker-news.firebaseio.com/v0/jobstories.json"
    print(f"🔍 情報取得先URL: {url_stories}")
    print("--------------------------------------------------")

    try:
        # 最新の求人IDリストを取得
        res_stories = requests.get(url_stories, timeout=10)
        
        if res_stories.status_code == 200:
            job_ids = res_stories.json()
            
            if not job_ids:
                print("⚠️ 情報が見つかりませんでした。")
                return
                
            print(f"✅ 求人IDリストを取得しました。上位3件の詳細をフェッチします！\n")
            
            for i, job_id in enumerate(job_ids[:3], 1):
                detail_url = f"https://hacker-news.firebaseio.com/v0/item/{job_id}.json"
                res_detail = requests.get(detail_url, timeout=10).json()
                
                title = res_detail.get('title', 'No title')
                link = res_detail.get('url', f"https://news.ycombinator.com/item?id={job_id}")
                
                print(f"[{i}] {title}")
                print(f"    リンク: {link}\n")
        else:
            print(f"⚠️ ステータスコードエラー: {res_stories.status_code}")
            
    except Exception as e:
        print(f"❌ Web情報の取得エラー: {e}")

if __name__ == "__main__":
    print("🚀 Web情報取得テスト（情報収集コアモデルのテスト）を開始します...")
    test_crawler()
    print("✅ テスト完了")
