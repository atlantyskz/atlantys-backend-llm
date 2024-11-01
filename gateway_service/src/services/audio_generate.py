import os
import tempfile
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from configs.enums import SPEAKER_VOICE_ENUM
from pydub import AudioSegment
from shortuuid import uuid


class AudioGenerateService:
    def __init__(self):
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv('XI_API_KEY'))

    async def generate(self, text:str, voice_id:str)-> bytes:
        emotion_settings = {
            'happy': VoiceSettings(stability=0.3, similarity_boost=0.6, style=0.4),
            'sad': VoiceSettings(stability=0.4, similarity_boost=0.5, style=-0.5),
            'angry': VoiceSettings(stability=0.4, similarity_boost=0.6, style=0.3),
            'neutral': VoiceSettings(stability=0.4, similarity_boost=0.5, style=0.0)
        }
        res = self.elevenlabs_client.generate(text=text, voice=voice_id, model="eleven_turbo_v2_5",voice_settings=emotion_settings['happy'])
        return res

    async def process_audio(self, podcast_data: dict):
        audio:AudioSegment = await self.create_audio(podcast_data) 
        temp_file_path = f"/tmp/{uuid()}.mp3"
        audio.export(temp_file_path, format="mp3")
        return temp_file_path


    async def create_audio(self, podcast_data: dict):
        audio_segments = []
        for idx, entry in enumerate(podcast_data.get('dialogue')):
            speaker = entry.get('speaker')
            message = entry.get('message')

            voice_id = (
                SPEAKER_VOICE_ENUM.FemaleSpeakerVoiceID.value
                if speaker == "FemaleSpeaker"
                else SPEAKER_VOICE_ENUM.MaleSpeakerVoiceID.value
            )
            audio_generator = await self.generate(message, voice_id)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                for chunk in audio_generator:
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            audio_segment = AudioSegment.from_mp3(temp_file_path)
            audio_segments.append(audio_segment)

        return sum(audio_segments)

async def get_service():
    return AudioGenerateService()
    

