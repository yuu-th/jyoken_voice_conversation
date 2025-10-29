# 情研 会話AI プロジェクト

## 概要
音声での会話を可能にするAIシステムの開発を目指しています。
このプロジェクトでは、音声認識、自然言語処理、音声合成の各技術を組み合わせて、ユーザーと自然な対話ができるAIを構築します。


## 主要技術
- **音声認識**: ユーザーの音声入力をテキストに変換します。利用するapiはdeepgram です。
- **自然言語処理**: テキストデータを解析し、適切な応答を生成します。利用するapiはGemini です。
- **音声合成**: テキスト応答を音声に変換し、ユーザーに返します。利用するapiはElevenLabs です。

## システム構成
システムは以下の主要コンポーネントで構成されています。
- **hearing**: 音声認識を担当するプロセス。ユーザーの音声をリアルタイムでテキストに変換します。
- **main**: 自然言語処理を担当するプロセス。hearingからのテキストを受け取り、適切な応答を生成します。
- **Speaker**: 音声合成を担当するプロセス。mainからのテキスト応答を音声に変換し、再生します。

## 環境
- Python 3.12
- パッケージ管理: uv
- OS: Windows 11

## uvのインストール方法

uvは、Pythonのパッケージ管理ツールです。このプロジェクトでは、uvを使用してライブラリなどの依存関係の管理とスクリプトの実行を行います。

Windowsの場合、以下のコマンドをPowerShellで実行します。
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## FFmpegのインストール（Windows）

このプロジェクトでは音声処理やフォーマット変換のためにFFmpegが必要になることがあります。WindowsではMicrosoft Storeではなく、winget（Windows Package Manager）を使って簡単にインストールできます。PowerShellまたは管理者権限のあるコマンドプロンプトで以下を実行してください：

```powershell
winget install --id=FFmpeg.FFmpeg -e --source=winget
```

インストール後、パスが通っているか確認するために以下を実行してください：

```powershell
ffmpeg -version
```


## プロジェクト構造
```
jyoken_voice_conversation/
├── src/
│   ├── __init__.py
│   ├── main.py          # メインプロセス
│   ├── hearing.py       # 音声認識プロセス
│   ├── llm.py          # LLM（Gemini）クラス
│   └── speaker.py      # 音声合成クラス
├── .env.example        # 環境変数のテンプレート
├── .gitignore
├── pyproject.toml      # uvプロジェクト設定
└── README.md
```

## 使用ライブラリ
- **deepgram-sdk** (5.0.0): Deepgram音声認識API
- **google-generativeai** (0.8.5): Google Gemini LLM API
- **elevenlabs** (2.18.0): ElevenLabs音声合成API
- **pyaudio** (0.2.14): 音声入出力
- **python-dotenv** (1.1.1): 環境変数管理
- **websockets** (15.0.1): WebSocket通信（Deepgramで使用）

## インストール手順

### 前提条件
- Python 3.12以上
- uv（Pythonパッケージマネージャー）
- マイクとスピーカー

### 1. リポジトリをクローン
```bash
git clone <repository-url>
cd jyoken_voice_conversation
```

### 2. uvで依存関係をインストール
```bash
uv sync
```

### 3. APIキーの設定
以下のサービスからAPIキーを取得してください：
- [Deepgram](https://deepgram.com/): 音声認識
- [Google AI Studio](https://aistudio.google.com/): Gemini API
- [ElevenLabs](https://elevenlabs.io/): 音声合成

`.env.example`をコピーして`.env`ファイルを作成し、取得したAPIキーを設定します：
```bash
copy .env.example .env
```

`.env`ファイルを編集：
```plaintext
DEEPGRAM_API_KEY=your_deepgram_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 4. プロジェクトを実行
```bash
uv run src/main.py
```

## フロー

1. hearingプロセスが、継続的に音声を認識し、テキストに変換します。
2. 変換されたテキストが、キューに保存されます。キューはhearingプロセスとmainプロセスで共有されます。
3. chatプロセスがキューからテキストを取得し、LLM.call()を呼び出し、Gemini APIを使用して応答を生成します。
4. 生成された応答テキストをSpeaker.say()に渡します。
5. Speaker.say()がElevenLabs APIを使用して応答テキストを音声に変換し、再生します。