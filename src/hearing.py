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
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions,Microphone
from dotenv import load_dotenv

import asyncio #非同期処理用ライブラリ
import pyaudio #音声入出力ライブラリ



# class HearingProcess(Process):
#     """音声認識プロセスクラス"""
    
#     def __init__(self, text_queue: Queue):
        
        
#         """ 
#         Args:
#             text_queue: 認識したテキストを格納するキュー
#         音声認識するよー
#         """        

#         super().__init__() #親クラスの初期化
#         load_dotenv()#load.env()というAPIキーなどの一般の人に見られたくない情報を.envファイルに保存しておき、環境変数として読み込むためのライブラリ
#         self.text_queue = text_queue
#         self.api_key = os.getenv("DEEPGRAM_API_KEY")
#         if not self.api_key:
#             raise ValueError("DEEPGRAM_API_KEY is not set in environment variables.")

        
#         # Deepgramクライアントの初期化

#         # TODO: Deepgramクライアントの実装

#         self.dg_connection = None #後で初期化する

    
#     def on_error(self, error):
#         """
#         エラーハンドリング
        
#         Args:
#             error: エラー情報
#         """
#         # TODO: エラーログの出力
#         print(f"Error: {error}")
    
#     def run(self):
#         """音声認識プロセスの開始"""
#         # HearingProcess.start()が呼ばれたときに非同期で実行される
#         # TODO: 音声ストリームの開始
#         # TODO: Deepgram接続の開始
#         # TODO: 継続的な音声認識ループ

#         # self.start_microphone() # マイクの初期化とストリーム開始
#         # self.contact_deepgram() # Deepgramと接続する関数
#         # while True:
#         #       # プレースホルダー
#         #     data = self.read_audio_chunk()  # マイクから音声データを読み取る
#         #     self.send_to_deepgram(data)  # Deepgramに音声データを送信
#         #     result = self.receive_result() # Deepgramから認識結果を受信
#         #     print(f"認識結果: {result}")
#         dg_client = DeepgramClient(api_key=self.api_key)

#         with dg_client.listen.v2.connect(
#             model="flux-general-en",
#             encoding="linear16",
#             sample_rate="16000"
#         ) as connection:
#             def on_message(message):
#                 print(f"Received {message.type} event")

#             connection.on(EventType.OPEN, lambda _: print("Connection opened"))
#             connection.on(EventType.MESSAGE, on_message)
#             connection.on(EventType.CLOSE, lambda _: print("Connection closed"))
#             connection.on(EventType.ERROR, lambda error: print(f"Error: {error}"))

#             # Start listening and send audio data
#             connection.start_listening()
    
#     def stop(self):
#         """音声認識プロセスの停止"""
#         # TODO: ストリームのクローズ
#         # TODO: 接続のクローズ
#         if self.dg_connection:
#             self.dg_connection.close()


class HearingProcess:
    def __init__(self, text_queue: Queue):
        """ 
        Args:
            text_queue: 認識したテキストを格納するキュー
        音声認識するよー
        """        

        super().__init__() #親クラスの初期化
        load_dotenv()#load.env()というAPIキーなどの一般の人に見られたくない情報を.envファイルに保存しておき、環境変数として読み込むためのライブラリ
        self.text_queue = text_queue
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY is not set in environment variables.")
        
        self.message_queue = Queue()

        
    def start(self):
        """音声認識プロセスの開始"""
        self.process = Process(target=self.run, args=(self.text_queue,self.api_key, self.message_queue))
        self.process.start()


    @staticmethod
    def run(text_queue: Queue,api_key:str, message_queue:Queue):
        dg_client = DeepgramClient(api_key=api_key) 
        
        dg_connection = dg_client.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            if result.is_final:
                print(f"Final result: {sentence}")
                text_queue.put(sentence)
            else:
                print(f"Interim result: {sentence}")

        # def on_metadata(self, metadata, **kwargs):
        #     print(f"\n\n{metadata}\n\n")

        # def on_speech_started(self, speech_started, **kwargs):
        #     print(f"\n\n{speech_started}\n\n")

        def on_utterance_end(self, utterance_end, **kwargs):
            text_queue.put("<utterance_end>")
        # def on_error(self, error, **kwargs):
        #     print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        # dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
        # dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
        dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
        # dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options: LiveOptions = LiveOptions(
            # model="nova-2",
            # language="ja",
            model = "nova-3",
            language="multi",
            punctuate=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # To get UtteranceEnd, the following must be set:
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
        )
        dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        while True:
            try:
                message = message_queue.get_nowait()
                if message == "stop":
                    # Wait for the microphone to close
                    microphone.finish()

                    # Indicate that we've finished
                    dg_connection.finish()
                    break

            except:
                pass


    def stop(self):
        """音声認識プロセスの停止"""
        self.message_queue.put("stop")
        self.process.join()



if __name__ == "__main__":
    import time
    # テスト用コード
    text_queue = Queue()
    hearing_process = HearingProcess(text_queue)
    hearing_process.start()
    time.sleep(20)
    hearing_process.stop()
    # hearing_process = Process(target=HearingProcess)