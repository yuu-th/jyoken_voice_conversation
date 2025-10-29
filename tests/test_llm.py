"""
LLMクラスのテスト
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from src.llm import LLM


class TestLLM:
    """LLMクラスのテストケース"""

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key", "MODEL_NAME": "test_model"})
    def test_initialization(self):
        """LLMの初期化テスト"""
        # TODO: 実装
        llm_instance = LLM()
        assert llm_instance.api_key == "test_api_key"
        assert llm_instance.model_name == "test_model"
        assert llm_instance.conversation_history == []

    @patch('google.generativeai.GenerativeModel')   
    def test_call(self, mock_generative_model):
        """LLMのcallメソッドテスト"""
        # TODO: 実装
        # モックの設定
        mock_chat_instance = MagicMock()
        mock_chat_instance.send_message.return_value.text = "こんにちは！"
        mock_generative_model.return_value.start_chat.return_value = mock_chat_instance

        llm_instance = LLM()
        
        user_input = "こんにちは"
        response = llm_instance.call(user_input)

        assert response == "こんにちは！"
        mock_chat_instance.send_message.assert_called_once_with(user_input)
    
    def test_reset_conversation(self):
        """会話履歴のリセットテスト"""
        # TODO: 実装
        pass