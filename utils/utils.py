from .constants import TOKEN_IDS

def get_token_name(token_id: int) -> str:
    for token_name, token_id_ in TOKEN_IDS.items():
        if token_id == token_id_:
            return token_name

    return None

def get_token_id(token_name: str) -> int:
    return TOKEN_IDS[token_name]