"""
main.py
メインプロセス
hearingからのテキストを受け取り、LLMで応答を生成し、Speakerで音声化
"""

import os
import time
from multiprocessing import Process, Queue
from typing import Optional
from dotenv import load_dotenv

from hearing import HearingProcess
from llm import LLM
from speaker import Speaker


class MainProcess:
    """メインプロセスクラス"""
    
    def __init__(self):
        """初期化"""
        load_dotenv()
        
        # プロセス間通信用のキュー
        self.text_queue = Queue()
        
        # LLMとSpeakerの初期化
        self.llm = LLM()
        
        self.speaker = Speaker()

        # hearingプロセス
        self.hearing_process: Optional[HearingProcess] = None
        
    def setup(self):
        """セットアップ"""
        print("Setting up Main Process...")

        self.hearing_process = HearingProcess(self.text_queue)

        self.hearing_process.start()

    def process_text(self, text: str):
        """
        テキストを処理して応答を生成・発話
        
        Args:
            text: 処理するテキスト
        """
        print(f"Received text: {text}")
        
        response = self.llm.call(text)
        
        self.speaker.say(response)
        
    def run(self):
        """メインループ"""
        print("Main Process started")

        try:
            while True:

                if not self.text_queue.empty():
                    text = self.text_queue.get()
                    if text:
                        self.process_text(text)
                
                # プレースホルダー
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nMain Process stopped by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """クリーンアップ処理"""
        print("Cleaning up...")
        
        
        if self.hearing_process and self.hearing_process.is_alive():
            self.hearing_process.terminate()
            self.hearing_process.join()

        if self.text_queue:
            self.text_queue.close()
            self.text_queue.join_thread()

def main():
    """エントリーポイント"""
    print("=== 情研 会話AI システム ===")
    
    main_process = MainProcess()
    main_process.setup()
    main_process.run()


if __name__ == "__main__":
    main()
