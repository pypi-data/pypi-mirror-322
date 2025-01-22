class NetworkError(Exception):
    pass


try:
    import requests
except ImportError:
    raise NetworkError("Requests module not installed")


def connection_check():
    error = NetworkError("Подключение к интернету отсутствует")
    try:
        response = requests.get("https://google.com", timeout=5)
        if response.status_code != 200:
            raise error
        return True
    except requests.ConnectionError:
        raise error


def is_connected() -> bool:
    try:
        connection_check()
    except NetworkError:
        return False
    else:
        return True


def connect_to_site(url: str, **kwargs) -> bool:
    if is_connected():
        response = requests.get(url, **kwargs)
        return response.status_code == 200
    else:
        return False


def translate_text(text: str, input_language: str = 'auto', output_language: str = 'en', server: str = 'google') -> str:
    from translators import translate_text as translate
    MAX = 3900
    length = text.__len__()
    if length < MAX:
        return translate(text, )
    else:
        output = ''
        l = length if length % MAX == 0 else length + MAX
        for i in range(0, l, MAX):
            output += translate(text[i:i + MAX], server, input_language, output_language)
        return output


class TestResponse:
    def __init__(self, response: requests.Response):
        self.response = response

    def __call__(self, *args, **kwargs):
        if self.response.status_code == 200:
            self.success(*args, **kwargs)
        else:
            self.error(*args, **kwargs)

    def success(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass
