from fastrtc import ReplyOnPause, Stream, get_tts_model
from fastrtc_whisper_cpp import get_stt_model
from talkingagent import agent_ollama

stt_model = get_stt_model()  # moonshine/base
tts_model = get_tts_model()  # kokoro


def echo(audio):
    transcript = stt_model.stt(audio)
    print("🎙️ Audio Transcrito: "+transcript)
    response_text = agent_ollama().llm.invoke(input=transcript)
    print("🤖 Respuesta Ollama: "+str(response_text.content))
    print("=================================================================")
    for audio_chunk in tts_model.stream_tts_sync(response_text.content):
        yield audio_chunk


stream = Stream(ReplyOnPause(echo), modality="audio", mode="send-receive")
stream.ui.launch()