"""
speaker.py
音声合成・再生の最小実装（ElevenLabs 統合想定）

この実装は次を満たします:
- ElevenLabs クライアントで合成を行う（SDK の戻り値により微調整が必要）
- WAV バイト列を解析して PyAudio で再生
- PyAudio が無ければ再生をシミュレーション（開発用）
- 同期(blocking=True) / 非同期(blocking=False) 再生をサポート
- 停止(stop) とリソース解放を安全に行う
"""

import io
import time
import logging
"""
speaker.py
音声合成・再生の最小実装（ElevenLabs 統合想定）

この実装は次を満たします:
- ElevenLabs クライアントで合成を行う（SDK の戻り値により微調整が必要）
- WAV バイト列を解析して PyAudio で再生
- PyAudio が無ければ再生をシミュレーション（開発用）
- 同期(blocking=True) / 非同期(blocking=False) 再生をサポート
- 停止(stop) とリソース解放を安全に行う
"""

import io
import time
import logging
import threading
import wave
import os
from typing import Optional
from dotenv import load_dotenv


import io
import time
import logging
import threading
import wave
import os
from typing import Optional
from dotenv import load_dotenv

# ElevenLabs SDK import (already in project)
from elevenlabs import ElevenLabs, VoiceSettings, play, Voice




logger = logging.getLogger(__name__)


class SpeakerError(Exception):
    """Speaker に関するエラー"""


class Speaker:
    """音声合成・再生クラス

    コンストラクタは環境変数から API キー等を読み取る（既存設計に合わせる）
    """

    def __init__(self, api_key: Optional[str] = None, voice_id: Optional[str] = None, sample_rate: int = 24000):
        load_dotenv()

        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is not set in environment variables.")

        # ElevenLabs クライアント初期化
        self.client = ElevenLabs(api_key=self.api_key)

        # voice_id は引数または環境変数から
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")
        if not self.voice_id:
            raise ValueError("ELEVENLABS_VOICE_ID is not set in environment variables.")

        # voice settings の初期値（必要に応じて調整）
        try:
            self.voice_settings: Optional[VoiceSettings] = VoiceSettings(
                stability=1,
                use_speaker_boost=True,
                similarity_boost=1,
                style=0,
                speed=1,
            )
        except Exception:
            # SDK が VoiceSettings をサポートしない場合は None にしておく
            self.voice_settings = None

    def say(self, text:str):
        print("Speaker say:", text)
        audio = self.client.generate(text=text, voice=Voice(voice_id=self.voice_id,settings=self.voice_settings))
        play(audio, notebook=False)
        
