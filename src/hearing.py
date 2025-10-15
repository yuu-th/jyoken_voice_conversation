"""
hearing.py
音声認識を担当するプロセス
Deepgram APIを使用してリアルタイムで音声をテキストに変換
"""

from http.client import PROCESSING
import os
from multiprocessing import Process, Queue
from typing import Optional
import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from dotenv import load_dotenv


class HearingProcess(Process):
    """音声認識プロセスクラス"""
    
    def __init__(self, text_queue: Queue):
        """
        初期化
        
        Args:
            text_queue: 認識したテキストを格納するキュー
        """
        load_dotenv()
        self.text_queue = text_queue
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        
        # Deepgramクライアントの初期化

        # TODO: Deepgramクライアントの実装
    
    def on_error(self, error):
        """
        エラーハンドリング
        
        Args:
            error: エラー情報
        """
        # TODO: エラーログの出力
        pass
    
    def run(self):
        """音声認識プロセスの開始"""
        # HearingProcess.start()が呼ばれたときに非同期で実行される
        # TODO: 音声ストリームの開始
        # TODO: Deepgram接続の開始
        # TODO: 継続的な音声認識ループ
        while True:
            pass  # プレースホルダー
    
    def stop(self):
        """音声認識プロセスの停止"""
        # TODO: ストリームのクローズ
        # TODO: 接続のクローズ
        pass
