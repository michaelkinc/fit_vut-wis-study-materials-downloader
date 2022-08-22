from parser import SubjectAbbreviationsParser
from connection import Connection


class Downloader:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.abbreviations = self._get_subject_abbreviations()

    def _get_subject_abbreviations(self):
        content = self.connection.get_contents("https://wis.fit.vutbr.cz/FIT/st/cfs.php.cs?file=/course/")
        abbrev_parser = SubjectAbbreviationsParser(content)
        return abbrev_parser.get_subject_abbreviations()
