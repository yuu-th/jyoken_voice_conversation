from speaker import Speaker

if __name__ == '__main__':
    s = Speaker()
    print('Calling Speaker.play_audio() — this will synthesize and play audio (blocking)')
    try:
        s.play_audio('こんにちは。テスト音声です。')
        print('Playback finished')
    except Exception as e:
        print('Speaker failed:', repr(e))

