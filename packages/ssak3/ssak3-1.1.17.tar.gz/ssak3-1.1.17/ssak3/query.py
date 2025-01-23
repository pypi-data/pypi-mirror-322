import hashlib
from .constants import *
from .utils import elapsed, prompt_template_yaml

# opt 종류
QUERY = 'query'
ENGINE = 'engine'
FIX = 'fix'
PROMPT = 'prompt'
KEYWORDS = 'keywords'
DESCRIPTION = 'description'

# --------------------------------------------------------------------------------------------------------------
def get_prompt(_domain, _name, _opt):
    if _domain == SX_DOMAIN_NEWS:
        query_domain = f'query_{SX_DOMAIN_NEWS}'
    elif _domain == SX_DOMAIN_COMPANY:
        query_domain = f'query_{SX_DOMAIN_COMPANY}'
    elif _domain == SX_DOMAIN_COIN:
        query_domain = f'query_{SX_DOMAIN_COIN}'
    else:
        return None

    datadict = prompt_template_yaml(query_domain)
    for entry in datadict:
        if entry.get('name') == _name:
            if _opt == FIX:
                return fix_query(_name.strip(), entry[QUERY].strip())
            return entry[_opt].strip()
    return None

# --------------------------------------------------------------------------------------------------------------
# domain 별로 이름은 유니크 해야 함
# 'Hello | World + 한글 - "Test"'
# --------------------------------------------------------------------------------------------------------------
def fix_query(_name, _query):
    combined_query = _name + _query
    hash_bytes = hashlib.sha256(combined_query.encode()).digest()
    out =  bytes(a ^ b ^ c ^ d for a, b, c, d in zip(hash_bytes[:8], hash_bytes[8:16], hash_bytes[16:24], hash_bytes[24:]))
    return out.hex()

# --------------------------------------------------------------------------------------------------------------
def get_config_path(_storage, install=SX_STORAGE_BASE):
    basic_path = f'{install}-{_storage}'
    news_path = f'{basic_path}-{AF_SCRAPER_NEWS}'
    return f'{news_path}-{AF_CONFIG}'

# eof