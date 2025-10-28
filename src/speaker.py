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
import io
import wave


class Speaker:
    """音声合成・再生クラス"""
    
    def __init__(self):
        """初期化"""
        # .envファイルから環境変数をリロード
        load_dotenv() 
        
        # ElevenLabs APIキーの取得
        self.api_key = os.getenv("ELEVENLABS_API_KEY") 
        if(self.api_key is None):
            raise ValueError("ELEVENLABS_API_KEY is not set in environment variables.")

        # ElevenLabsクライアントの初期化
        self.client = ElevenLabs(api_key=self.api_key)   
        
        # 音声設定
        self.voice_id : Optional[str] = os.getenv("ELEVENLABS_VOICE_ID") # ElevenLabs Voice IDの取得
        if(self.voice_id is None):
            raise ValueError("ELEVENLABS_VOICE_ID is not set in environment variables.")
        
        self.voice_settings: Optional[VoiceSettings] = VoiceSettings(
            stability=1,
            use_speaker_boost=True,
            similarity_boost=1,
            style=0,
            speed=1
        )

        def _ensure_pyaudio(self):
            """PyAudio インスタンスを遅延初期化する"""

            if self._pyaudio is None:
                if pyaudio is None:
                    logger.debug("PyAudio not available; playback will be simulated")
                    return None
                self._pyaudio = pyaudio.PyAudio()
            return self._pyaudio

    def say(self, text: str, blocking : bool = True) -> bool:
        """
        テキストを音声に変換して再生
        
        Args:
            text: 音声に変換するテキスト
        """
        # TODO: ElevenLabs APIでテキストを音声に変換
        # TODO: 音声データの取得
        # TODO: 音声の再生

        self.stop() #音声の停止

        if not isinstance(text, str) or not text:
            raise ValueError("text must be a non-empty string.")
        
        p = self._ensure_pyaudio()

        # ElevenLabs APIでテキストを音声に変換
        audio = self.client.generate(text=text, voice_id=self.voice_id, voice_settings=self.voice_settings)



        

    

    def stop(self):
        """音声再生の停止とリソースの解放"""
        # TODO: ストリームのクローズ
        # TODO: PyAudioの終了
        pass
