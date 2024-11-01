from pydantic import BaseModel


class PodcastRequestDTO(BaseModel):
    topic: str
    url: str = None

    class Config:
        from_attributes = True