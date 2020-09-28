from typing import Dict
from urllib.parse import parse_qs


def parse_params(params_str: str) -> Dict[str, str]:
    params = parse_qs(params_str)
    params = {k: v[0] for k, v in params.items()}
    return params
