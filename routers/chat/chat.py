from fastapi import APIRouter, UploadFile, File
#from datetime import datetime
from pydub import AudioSegment
import soundfile as sf
from io import BytesIO
import openai
import tempfile
import os
import pydub
import wave

router = APIRouter()
openai.api_key = "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"

@router.post("/chat/exchange")
async def add_exchange(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()

    # Determine the audio format from the file extension
    file_ext = audio.filename.split(".")[-1].lower()
    if file_ext == "mp3":
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
    elif file_ext == "wav":
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="wav")
    elif file_ext == "ogg":
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="ogg")
    else:
        return {"error": "Unsupported audio format"}

    # Export the audio to WAV format
    wav_bytes = BytesIO()
    output_format = "wav"
    audio_segment.export(wav_bytes, format=output_format)

    # Transcribe the audio
    model = "whisper-1"
    wav_file = BytesIO(wav_bytes.getvalue())
    wav_file.name = audio.filename
    transcript = openai.Audio.transcribe(
        model=model,
        file=wav_file,
        content_type="audio/wav"
    )

    return {"response": transcript.text}