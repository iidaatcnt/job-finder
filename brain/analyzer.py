import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env を読み込む
load_dotenv(override=True)

# Gemini API の設定
gemini_api_key = os.environ.get("GEMINI_API_KEY")
gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")

if not gemini_api_key:
    print("❌ エラー: .env ファイルに GEMINI_API_KEY が設定されていません。")
    exit(1)

genai.configure(api_key=gemini_api_key)

def analyze_job(job_title, job_description):
    """
    案件のタイトルと説明を読み込み、飯田さんの経歴とマッチするか判定して、
    A〜Eのランクと、その理由、パーソナライズされた応募文を作成する
    """
    
    # 飯田さんの経歴（プロンプト用）
    iida_profile = """
    【飯田さんの経歴・スキル】
    - ITエンジニア歴30年。C, Python, PHP, VBA, Linuxなどに精通。
    - 最近の実績：神戸のクラブチーム向けDX支援ポータル『コベカツ』の開発・運用。Discordを使った自動化botシステムの開発。
    - 動画や映像制作のスキル（Premiere Pro等）の実務経験あり。
    - WordPress（Tutor LMS, WooCommerce等）の構築・保守が得意。
    - ITリテラシーが高く、マニュアルがなくても自走可能。業務改善のコンサルティングが可能。
    - 求める条件：業務委託、完全フルリモート（常駐や派遣はNG）。
    """

    prompt = f"""
    あなたは優秀なIT案件のマッチングコンサルタントです。
    以下の【飯田さんの経歴・スキル】と、【求人案件情報】を比較し、以下の3点を出力してください。

    {iida_profile}

    【求人案件情報】
    案件名: {job_title}
    業務内容・詳細: {job_description}

    ---
    【出力形式】
    1. マッチ度ランク (A, B, C, D, Eのいずれか。Aが最高。派遣や常駐必須なら即Eにしてください)
    2. 判定理由 (なぜそのランクにしたのか、強みがどう活きるかを100文字程度で)
    3. 応募メッセージ草案 (もしこの案件に応募する場合、「飯田さんの実績（コベカツなど）」を自然にアピールする丁寧な応募文を200文字程度で)
    """

    print(f"🧠 Gemini ({gemini_model_name}) で案件の分析を開始します...")
    
    try:
        model = genai.GenerativeModel(gemini_model_name)
        response = model.generate_content(prompt)
        
        print("\n================ 分析結果 ================\n")
        print(response.text)
        print("\n==========================================\n")
    except Exception as e:
        print(f"❌ Geminiの解析中にエラーが発生しました: {e}")

if __name__ == "__main__":
    # テスト用の架空の案件データ
    sample_title = "【フルリモート/業務委託】Pythonエンジニア（業務改善bot・ツール開発）"
    sample_description = "社内の業務効率化のためのPythonスクリプト開発やDiscord botの運用をお願いします。要件定義から一人称で動けるITリテラシーの高い方を求めています。完全リモート稼働で、週3日〜OKです。"
    
    analyze_job(sample_title, sample_description)
