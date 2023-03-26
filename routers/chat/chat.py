from fastapi import APIRouter, UploadFile, File
from datetime import datetime
from pydub import AudioSegment
from io import BytesIO
import boto3
import openai

router = APIRouter()
openai.api_key = "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"

messages = []

def build_system_message():
    instructions = [
        "Your role will be an English teacher.",
        "I will provide you with text that was obtained using speech-to-text technology.",
        "Your task is to correct every grammar mistake, but keep in mind that the text is from spoken English, so be concise and natural in your corrections.",
        "Please focus on correcting the verb tense, and ignore any capitalization errors.",
        "You will receive the text from a speech-to-text software. When correcting, explain the error and provide the corrected version, but avoid congratulating the student. Treat them like a native Spanish-speaking student learning English.",
        "After you provide the correction, ask the student a related question, after that ask the student if he/shee wants to repeat the corrected phrase to confirm their understanding.",
        "Ignore the capitalization.",
        "Always speak English."
    ]

    return " ".join(instructions)

def add_text_to_messages(text, role):
    new_message = {"role": role, "content": text}
    messages.append(new_message)
    return messages

system_message = build_system_message()
add_text_to_messages(system_message , "system")


secret_access_key = 'qpthZJhz8cc+rqwI+lAJOgIbjPuAJatIfLuaunS7'
access_key_id = 'AKIA6KFYBI3X6RIV22WV'
polly = boto3.client('polly', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name="us-east-1")
s3 = boto3.resource("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
bucket_name = "smart-languages"

def convert_text_to_audio(text, output_format = "mp3", voice_id='Joanna'):
    response = polly.synthesize_speech(VoiceId=voice_id, Text=text, OutputFormat=output_format)
    audio_bytes = response['AudioStream'].read()
    return audio_bytes

def save_audio_to_s3(bucket_name, audio_bytes, format="mp3"):
    bucket = s3.Bucket(bucket_name)
    key = datetime.now().strftime("%Y_%m_%d %H_%M_%S"+ "."+format)
    bucket.put_object(Key=key, Body=audio_bytes)
    audio_path = f"https://{bucket_name}.s3.amazonaws.com/{key}"
    return audio_path

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
    user_text = transcript.text

    add_text_to_messages(user_text, "user")

    gpt_model ="gpt-3.5-turbo"
    openai_response = openai.ChatCompletion.create(
        model=gpt_model,
        messages= messages,
        temperature=0.2,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0.2,
        stop=[" Human:", " AI:"]
    )
    openai_text = openai_response.choices[0].message.content
    audio_bytes = convert_text_to_audio(openai_text)
    user_audio_url = save_audio_to_s3(bucket_name, mp3_file)
    openai_audio_url = save_audio_to_s3(bucket_name, audio_bytes)

    return {"user": {"text": user_text, "audio": user_audio_url }, "assistant": {"text" :openai_text, "audio": openai_audio_url}}
