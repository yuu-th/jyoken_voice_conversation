"""
llm.py
LLM（大規模言語モデル）との対話を担当
Google Gemini APIを使用して応答を生成
"""

import os
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
                {"role": "user", "parts": ["あなたは高専生です。ユーザーからの随時に与えられる音声入力のテキストに対して、短い文で返答します。高専生らしく、語尾は「わらわら」など言ってください。"]},
                {"role": "user", "parts": [""]}
            ]
        )

        # 会話履歴
        self.conversation_history: List[dict] = []
        

    
    def call(self, user_input: str) -> str:
        """
        LLMを呼び出して応答を生成
        
        Args:
            user_input: ユーザーからの入力テキスト
            
        Returns:
            LLMからの応答テキスト
        """
        # TODO: 会話履歴への追加
        # TODO: Gemini APIの呼び出し
        # TODO: 応答の取得と整形
        # TODO: 会話履歴の更新
        print("LLM call with input:", user_input)
        prompt = ""
        response = self.chat.send_message(f"{prompt}{user_input}")

        print("LLM response:", response.text)
        return response.text  # プレースホルダー
    
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
    
if __name__ == "__main__":
    """デバック用コード"""
    llm = LLM()
    while True:
        user_input = input("あなた： ")

        if user_input.lower() in ["exit", "quit", "終了", "やめる"]:
            print("会話を終了します。")
            break
        
        response = llm.call(user_input)
        print(f"AI： {response}")