from typing import Optional
from app.config import settings


def get_role_from_token(token: str) -> Optional[str]:
    """
    Map token → role using config.TOKENS
    """
    return settings.TOKENS.get(token)
