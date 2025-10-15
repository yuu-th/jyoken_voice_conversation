"""
speaker.py
音声合成を担当
ElevenLabs APIを使用してテキストを音声に変換して再生
"""

import os
from typing import Optional
from elevenlabs import ElevenLabs, VoiceSettings
import pyaudio
from dotenv import load_dotenv


class Speaker:
    """音声合成・再生クラス"""
    
    def __init__(self):
        """初期化"""
        load_dotenv()
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        
        # ElevenLabsクライアントの初期化
        # TODO: ElevenLabsクライアントの実装
        
        # PyAudioの初期化
        # TODO: PyAudioの実装
        
        # 音声設定
        self.voice_id: Optional[str] = None
        self.voice_settings: Optional[VoiceSettings] = None
        
    def say(self, text: str):
        """
        テキストを音声に変換して再生
        
        Args:
            text: 音声に変換するテキスト
        """
        # TODO: ElevenLabs APIでテキストを音声に変換
        # TODO: 音声データの取得
        # TODO: 音声の再生
        pass
    

    def stop(self):
        """音声再生の停止とリソースの解放"""
        # TODO: ストリームのクローズ
        # TODO: PyAudioの終了
        pass
