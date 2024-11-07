import os

class Settings:

    def __init__(self):
        self.llm_service_url = os.getenv("LLM_SERVICE_URL", "http://llm-service:8001")

    
settings = Settings()