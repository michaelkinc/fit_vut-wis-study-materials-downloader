from bs4 import BeautifulSoup


class Parser:
    def __init__(self, content):
        self.content = BeautifulSoup(content, "html5lib")


class SubjectAbbreviationsParser(Parser):
    def get_subject_abbreviations(self):
        abbreviations = []
        tbody = self.content.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['stbl'])[0].tbody
        for tr in tbody.select("tr[valign='middle']"):
            abbrev = tr.find_all('td')[3]
            abbreviations.append(abbrev.text)
        return abbreviations
