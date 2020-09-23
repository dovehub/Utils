def parse_cookie_str(cookie_str: str) -> dict:
    cookie_list = cookie_str.split(';')
    cookies = {}
    for cookie in cookie_list:
        cookie = cookie.strip()
        key, value = cookie.split('=', maxsplit=1)
        cookies[key] = value
    return cookies
