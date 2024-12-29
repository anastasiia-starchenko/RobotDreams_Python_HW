# Реалізувати клас Url, який представлятиме URL
 # * Його параметрами мають бути параметри URL (scheme, authority, path, query, fragment). Їх має приймати конструктор (__init__)
  #* Перевизначити операцію == для Url. Якщо Url порівнюється з рядком, має повертатися True в разі, якщо рядок відповідає поданому Url
  #* Унаслідувати від Url клас HttpsUrl, де scheme за замовчуванням дорівнює https
  #* Унаслідувати від Url клас HttpUrl, де scheme за замовчуванням дорівнює http
  #* Реалізувати метод __str__, який формуватиме рядок з Url
  #* Унаслідувати від Url GoogleUrl та WikiUrl, для яких authority будуть google.com та wikipedia.org

from urllib.parse import urlencode

class Url:
    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        self.scheme = scheme
        self.authority = authority
        self.path = path if path else []
        self.query = query if query else {}
        self.fragment = fragment

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, Url):
            return str(self) == str(other)
        return False

    def __str__(self):
        # Формування рядка з URL
        url = ""
        if self.scheme:
            url += f"{self.scheme}://"
        if self.authority:
            url += self.authority
        if self.path:
            url += "/" + "/".join(self.path)
        if self.query:
            url += "?" + urlencode(self.query)
        if self.fragment:
            url += f"#{self.fragment}"
        return url

class HttpsUrl(Url):
    def __init__(self, authority=None, path=None, query=None, fragment=None):
        super().__init__(scheme="https", authority=authority, path=path, query=query, fragment=fragment)

class HttpUrl(Url):
    def __init__(self, authority=None, path=None, query=None, fragment=None):
        super().__init__(scheme="http", authority=authority, path=path, query=query, fragment=fragment)

class GoogleUrl(HttpsUrl):
    def __init__(self, path=None, query=None, fragment=None):
        super().__init__(authority="google.com", path=path, query=query, fragment=fragment)

class WikiUrl(HttpsUrl):
    def __init__(self, path=None, query=None, fragment=None):
        super().__init__(authority="wikipedia.org", path=path, query=query, fragment=fragment)

# Tests
assert GoogleUrl() == HttpsUrl(authority='google.com')
assert GoogleUrl() == Url(scheme='https', authority='google.com')
assert GoogleUrl() == 'https://google.com'
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'

#Реалізувати клас UrlCreator, з допомогою якого можна створювати Url
  #* Виклик методу _create має повертати Url
  #* Конструктор має приймати scheme та authority
  #* Методи __getattr__ та __call__ мають додавати нові параметри до url (див. приклад)
  #  * *args з __call__ мають додавати частини до path
  #  * **kwargs з __call__ мають додавати query params
  #  * __getattr__ має додавати одну частину до path

class UrlCreator:
    def __init__(self, scheme, authority):
        self.scheme = scheme
        self.authority = authority
        self._path_parts = []
        self._query_params = {}

    def __getattr__(self, name):
        self._path_parts.append(name)
        return self

    def __call__(self, *args, **kwargs):
        self._path_parts.extend(args)
        self._query_params.update(kwargs)
        return self

    def _create(self):
        path = '/'.join(self._path_parts)
        url = f"{self.scheme}://{self.authority}/{path}"
        if self._query_params:
            query = '&'.join(f"{key}={value}" for key, value in self._query_params.items())
            url = f"{url}?{query}"
        return url

# UrlCreator check
url_creator = UrlCreator(scheme='https', authority='docs.python.org')
assert url_creator.docs.v1.api.list == 'https://docs.python.org/docs/v1/api/list'
assert url_creator("api", "v1", "list") == 'https://docs.python.org/api/v1/list'
assert url_creator("api", "v1", "list", q='my_list') == 'https://docs.python.org/api/v1/list?q=my_list'
assert url_creator('3').search(q='getattr', check_keywords='yes', area='default')._create() == 'https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default'



