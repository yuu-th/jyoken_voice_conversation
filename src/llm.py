"""
llm.py
LLM（大規模言語モデル）との対話を担当
Google Gemini APIを使用して応答を生成
"""

from ast import Pass
import os
import json
from typing import Optional, List
import google.generativeai as genai
from dotenv import load_dotenv


class LLM:
    """LLMクラス - Gemini APIとの対話を管理"""

    def __init__(self):
        """初期化"""
        # Gemini APIの設定
        # TODO: genai.configureの実装
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key = self.api_key)

        # モデルの初期化
        # TODO: モデルの選択と初期化
        self.model_name = os.getenv("MODEL_NAME")
        self.chat = genai.GenerativeModel(self.model_name).start_chat(
            history = [
                {"role": "user", "parts": [""]}
            ]
        )

        # 会話履歴
        self.conversation_history: List[dict] = []

        self.initialization()

    def initialization(self):
        self.json_path = r"C:\Users\owner\Documents\Programming\情報工学研究部\jyoken_voice_conversation\data\data.json"
        self.initial_data = {
            "name": "",
            "nickname": "",
            "birthday": "" 
        }

        self.field_labels = {
            "name": "名前",
            "nickname": "ニックネーム",
            "birthday": "誕生日"
        }

        if not os.path.exists(self.json_path) or os.path.getsize(self.json_path) == 0:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.initial_data, f, ensure_ascii=False, indent=2)

   
    def call(self, user_input: str) -> str:
        prompt = ""
        empty_fields = []

        with open(self.json_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        for key, value in user_data.items():
            if value == "":
                empty_fields.append(key)

        if empty_fields:
            labels = [self.field_labels.get(field, field) for field in empty_fields]
            joined = "と".join(labels)

            response = self.chat.send_message(f"""開発者です。あなたは今お話ししているユーザーの{joined}を知っていますか？
                                              全て知っていなければ、「No」と
                                              もし一つでも知っていれば、{joined}のうち、知っているものをラベルとして
                                               「｛
                                                 "名前": "太郎",
                                                 "出身地": "東京",
                                                 "住んでいるところ": "大阪"
                                                ｝」
                                              のようにjson形式で返してください""")
            print(f"⭐⭐{joined}に対する質問\n{response.text}")
            print(f"⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐\n\n\n{response.text}\n\n\n")

            if response.text == "No":
                prompt = f"""
                        {joined}を会話の中でしれっと聞いてください。
                        「わかりました、質問をすればいいですね」といったこの文章に対する返答をいりません。
                        """
            else:
                print(f"AIはしってたよ")
            print(f"{joined}が未入力です。")
        else:
            prompt = ""

        # prompt = ""
        response = self.chat.send_message(f"{prompt}{user_input}")
        
        return response.text  # プレースホルダー
    
    def memory(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
        
        user_data["name"] = input("名前を入力してください: ")
        user_data["nickname"] = input("ニックネームを入力してください: ")
        user_data["birthday"] = input("誕生日を入力してください（例: 2000-01-01）: ")

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        print("\n保存された情報:")
        print(f"名前: {user_data['name']}")
        print(f"ニックネーム: {user_data['nickname']}")
        print(f"誕生日: {user_data['birthday']}")
    
    def reset_conversation(self):
        """会話履歴をリセット"""
        # TODO: 会話履歴のクリア
        pass
    
    def get_conversation_history(self) -> List[dict]:
        """
        会話履歴を取得
        
        Returns:
            会話履歴のリスト
        """
        return self.conversation_history

class Test:
    def __init__(self):
        self.json_path = r"C:\Users\owner\Documents\Programming\情報工学研究部\jyoken_voice_conversation\data\data.json"
        self.initial_data = {
            "name": "",
            "nickname": "",
            "birthday": "" 
        }

    def main(self):
        if not os.path.exists(self.json_path) or os.path.getsize(self.json_path) == 0:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.initial_data, f, ensure_ascii=False, indent=2)
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)
        
        user_data["name"] = input("名前を入力してください: ")
        user_data["nickname"] = input("ニックネームを入力してください: ")
        user_data["birthday"] = input("誕生日を入力してください（例: 2000-01-01）: ")

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        print("\n保存された情報:")
        print(f"名前: {user_data['name']}")
        print(f"ニックネーム: {user_data['nickname']}")
        print(f"誕生日: {user_data['birthday']}")


if __name__ == "__main__":
    # test = Test()
    # test.main()

    """デバック用コード"""
    llm = LLM()
    while True:
        user_input = input("あなた： ")

        if user_input.lower() in ["exit", "quit", "終了", "やめる"]:
            print("会話を終了します。")
            break
        
        response = llm.call(user_input)
        print(f"AI： {response}")