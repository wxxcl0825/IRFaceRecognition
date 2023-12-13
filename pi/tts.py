import asyncio
import edge_tts
from pydub import AudioSegment
import simpleaudio as sa

VOICE = "zh-CN-YunxiNeural"
OUTPUT_FILE = "test.mp3"
TMP_FILE = "test.wav"


def trans_mp3_to_wav(fp):
    song = AudioSegment.from_mp3(fp)
    song.export(TMP_FILE, format="wav")


async def amain(content) -> None:
    communicate = edge_tts.Communicate(content, VOICE)
    await communicate.save(OUTPUT_FILE)


async def generate(content):
    await amain(content)


def speak(content):
    asyncio.run(generate(content))
    trans_mp3_to_wav(OUTPUT_FILE)
    wave_obj = sa.WaveObject.from_wave_file(TMP_FILE)
    play_obj = wave_obj.play()
    play_obj.wait_done()
