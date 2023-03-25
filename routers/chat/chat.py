from fastapi import APIRouter, UploadFile, File
from datetime import datetime
from pydub import AudioSegment
from io import BytesIO
import openai

router = APIRouter()
openai.api_key = "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"

@router.post("/chat/exchange")
async def add_exchange(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    file_ext = file.filename.split(".")[-1].lower()
    audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format=file_ext)

    mp3_buffer = BytesIO()
    output_format = "mp3"
    audio_segment.export(mp3_buffer, format=output_format)

    mp3_file = BytesIO(mp3_buffer.getvalue())

    model = "whisper-1"
    mp3_file.name = datetime.now().strftime("%Y_%m_%d %H_%M_%S"+ "."+output_format)
    transcript = openai.Audio.transcribe(
        model=model,
        file=mp3_file,
        content_type="audio/mpeg"
    )

    return {"response": transcript.text}
