# openai_helper.py
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from openai import OpenAI

api_key = os.environ['OPENAI_API_KEY']

# OpenAIクライアントの初期化
client = OpenAI(api_key=api_key)

def analyze_image(url: str) -> str:
    try:
        print(f"画像URL: {url}")
        # ユーザ提供のサンプルコードと同様の形式でAPIコール
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "この落書きが何を描いているか推測し、一単語で表してください。"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ],
                }
            ],
            max_tokens=300,
        )
        
        # レスポンスから回答テキストを取得
        print(f"画像URL: {response.choices[0].message.content.strip()}")
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "不明"

def check_answer_via_chat(answer: str, topic: str) -> bool:
    """
    Chat APIを用いて、answerがtopicと同一対象か判定。
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that determines if two answers refer to the same well-known entity."},
                {"role": "user", "content": f"Correct answer: '{topic}'\nUser answer: '{answer}'\nAre they essentially the same thing? Reply ONLY 'YES' or 'NO'."}
            ],
            temperature=0
        )
        response = completion.choices[0].message.content
        if response.upper() == "YES":
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in check_answer_via_chat: {e}")
        return False

def pick_human_final_answer_via_chat(answers: list[str]) -> str:
    """
    Chat APIを用いて、与えられた人間の回答一覧から
    最も頻出と思われる1つの回答をAIに選んでもらう関数。

    answers: ["answer1", "answer2", ...] といった文字列のリスト。
    AIには「これらは複数の人が回答したもの。最も多い回答を選んで一つだけ返して」と依頼する。
    同数トップがあればAIが適当に1つ選ぶ。
    """
    joined_answers = "\n".join([f"- {a}" for a in answers])
    prompt = f"Here are the human team answers:\n{joined_answers}\nPlease identify which single answer was given by the largest number of humans. If multiple answers have the same highest frequency, choose one arbitrarily. Just return that single answer."
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that chooses the single most frequent answer from a provided list of answers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        final_answer = completion.choices[0].message.content
        # AIが返した答えがそのまま最終人間回答
        return final_answer
    except Exception as e:
        print(f"Error in pick_human_final_answer_via_chat: {e}")
        # エラー時は一番目の回答を返すなどfallback
        return answers[0] if answers else "(no answer)"