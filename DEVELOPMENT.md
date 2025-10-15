# 開発ガイド

## 開発環境のセットアップ

### 1. 依存関係のインストール
```bash
# 本番用とdev用の全依存関係をインストール
uv sync --all-groups
```

### 2. 環境変数の設定
`.env.example`を`.env`にコピーして、APIキーを設定してください。


## プロジェクト構造の詳細

### src/hearing.py
- **役割**: 音声認識を担当するプロセス
- **主要クラス**: `HearingProcess`
- **使用API**: Deepgram (WebSocket経由でリアルタイム音声認識)
- **実装予定**:
  - マイクからの音声入力
  - Deepgramへのストリーミング送信
  - 認識結果のキューへの追加

### src/llm.py
- **役割**: LLM（Gemini）との対話
- **主要クラス**: `LLM`
- **使用API**: Google Generative AI (Gemini)
- **実装予定**:
  - 会話履歴の管理
  - Gemini APIへのリクエスト送信
  - 応答の生成と返却

### src/speaker.py
- **役割**: 音声合成と再生
- **主要クラス**: `Speaker`
- **使用API**: ElevenLabs
- **実装予定**:
  - テキストから音声への変換
  - 音声の再生
  - 音声ファイルの保存（オプション）

### src/main.py
- **役割**: メインプロセス、全体の制御
- **主要クラス**: `MainProcess`
- **機能**:
  - hearingプロセスの起動・管理
  - キューからのテキスト取得
  - LLMとSpeakerの統合

## トラブルシューティング

### PyAudioのインストールエラー
Windowsでは、事前にビルド済みのwheelが必要な場合があります。
```bash
# pipでインストールする場合
pip install pipwin
pipwin install pyaudio
```

### APIキーが読み込まれない
- `.env`ファイルがプロジェクトルートにあることを確認
- `.env`ファイルの形式が正しいことを確認（`KEY=value`、引用符なし）

### マイクが認識されない
- システムのマイク設定を確認
- PyAudioのデバイス一覧を確認するスクリプトを実行

## 参考リンク

- [Deepgram Python SDK Documentation](https://developers.deepgram.com/docs/python-sdk)
- [Google Generative AI Python Documentation](https://ai.google.dev/tutorials/python_quickstart)
- [ElevenLabs Python Documentation](https://elevenlabs.io/docs/api-reference/python)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
