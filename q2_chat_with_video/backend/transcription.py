# transcription.py
import whisper

def transcribe_audio(audio_path: str):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=False)
    return result['segments']  # [{"start": float, "end": float, "text": str}, ...]