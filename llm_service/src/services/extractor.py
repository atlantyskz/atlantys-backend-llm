from goose3 import Goose


class UrlExtractorService:

    def __init__(self,):
        self.goose_client = Goose()

    async def extract_content_from_url(self, url: str | None):
        if url is None:
            return None
        article = self.goose_client.extract(url=url)
        return {
            "title": article.title,
            "cleaned_text": article.cleaned_text[:30],
        }
    
async def get_service():
    return UrlExtractorService()