from typing import Optional, Dict, Any
from fake_useragent import UserAgent


def get_default(**kwargs: Any) -> Dict[str, str]:
    if not kwargs:
        kwargs = dict(platforms=["pc"])
    headers = {
        "User-Agent": UserAgent(**kwargs).random
    }
    return headers
