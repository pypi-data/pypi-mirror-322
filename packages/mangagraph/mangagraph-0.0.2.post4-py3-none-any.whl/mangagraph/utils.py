
import re
from urllib.parse import urlparse
from .exceptions import InvalidURLException


class MangaLibUrl:
    MANGALIB_URL_PATTERNS = [
        r"^https://mangalib\.me/ru/manga/[\w\-]+(\?.+)?$",
        r"^https://mangalib\.me/ru/\d+--[\w\-]+/read/v\d+/c\d+(\?.+)?$"
    ]
    
    def __init__(self, url: str):
        self.url = url
        self._validate_url()

    def _validate_url(self):
        parsed_url = urlparse(self.url)
        if not (parsed_url.scheme == "https" and parsed_url.netloc == "mangalib.me"):
            raise ValueError("Неверный адресс. Только 'https://mangalib.me' доступен.")
        
        if not any(re.compile(pattern).match(self.url) for pattern in self.MANGALIB_URL_PATTERNS):
            raise ValueError(
                "Неверный URL. Ссылка должна быть одного из типов:\n"
                "- 'https://mangalib.me/ru/manga/{slug_url}'\n"
                "- 'https://mangalib.me/ru/{slug_url}/read/v{volume}/c{chapter}'"
            )

    def __str__(self):
        return self.url

def estimate_remaining_time(remaining_chapters: int, chapters_per_minute: int = 12) -> str:
    estimated_minutes = (remaining_chapters / chapters_per_minute) * 1.1
    
    if estimated_minutes < 1:
        return "меньше минуты"
        
    hours = int(estimated_minutes // 60)
    minutes = int(estimated_minutes % 60)
    
    if hours > 0:
        return f"{hours} ч {minutes} мин"
    return f"{minutes} мин"

def extract_slug(url: str) -> str:
    pattern = r'/manga/(\d+--[^?]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise InvalidURLException(url, "Invalid MangaLib URL format.")