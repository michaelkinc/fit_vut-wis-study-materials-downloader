import re
from requests import Session, Response
from requests.auth import HTTPBasicAuth


class Connection:
    def __init__(self, username, password):
        self.session = Session()
        self.session.auth = HTTPBasicAuth(username, password)

    def _get(self, url):
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def get_contents(self, url):
        return self._get(url).content.decode('iso-8859-2')

    def _get_file_name(self, url):
        return re.search(r"([^\/]+$)", url).group(0)

    def download_file(self, url, path):
        response = self._get(url)
        file_name = self._get_file_name(url)
        path = path + "/" + file_name
        with open(path, 'wb') as fd:
            for chunk in response.iter_content(2000):
                fd.write(chunk)

    def __del__(self):
        self.session.close()
