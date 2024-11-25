from enum import Enum

class SPEAKER_VOICE_ENUM(Enum):
    """
    Enum for speaker voices
    """
    FemaleSpeakerVoiceID = "cgSgspJ2msm6clMCkdW9"
    MaleSpeakerVoiceID  = "PGKcNbNFBvaNXUCi2fgx"


class LLM_ENDPOINT(Enum):
    """
    Enum for LLM Endpoints
    """

    WEB_CLIENT = 'http://llm_service:8001/chatbot/generate-chat-response'
    TELEGRAM_CLIENT = 'http://llm_service:8001/chatbot/generate-tg-chat-response'