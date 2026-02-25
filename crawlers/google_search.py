import os
import requests
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def run_google_search(query, num_results=3):
    """
    Google Custom Search APIを使ってウェブ全体から求人を検索します。
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id = os.environ.get("GOOGLE_CSE_ID")

    if not api_key or not cse_id:
        print("❌ エラー: .env ファイルに GOOGLE_API_KEY または GOOGLE_CSE_ID が設定されていません。")
        return

    url = "https://www.googleapis.com/customsearch/v1"
    
    # APIに渡すパラメータ
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results,
        "gl": "jp", # 日本の検索結果
        "lr": "lang_ja", # 日本語
    }

    print(f"🔍 検索キーワード: {query}")
    print("--------------------------------------------------")

    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                print("⚠️ 検索結果が見つかりませんでした。")
                print("※もし全く結果が出ない場合は、Googleの設定画面で「ウェブ全体を検索」がONになっているか確認してください。")
                return
                
            print(f"✅ {len(items)} 件の検索結果を取得しました！\n")
            
            for i, item in enumerate(items, 1):
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                snippet = item.get("snippet", "No description")
                
                snippet_text = snippet.replace('\n', '')
                print(f"[{i}] {title}")
                print(f"    リンク: {link}")
                print(f"    抜粋: {snippet_text[:100]}...\n")
                
        else:
            print(f"⚠️ ステータスコードエラー: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Web情報の取得エラー: {e}")

if __name__ == "__main__":
    print("🚀 Google Custom Search テストを開始します...")
    # 検索キーワード（派遣以外、Python、フルリモート、業務委託）
    sample_query = "Python 業務委託 フルリモート -派遣"
    run_google_search(sample_query)
    print("✅ テスト完了")
