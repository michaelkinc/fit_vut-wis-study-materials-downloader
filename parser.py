from bs4 import BeautifulSoup


class Parser:
    def __init__(self, content):
        self.content = BeautifulSoup(content, "html5lib")

    def get_column_values(self, column):
        values = []
        rows = self.get_rows()
        if rows is None:
            return None
        for tr in rows:
            values.append(tr.find_all('td')[column].text)
        return values

    def get_rows(self):
        try:
            tbody = self.content.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['stbl'])[0].tbody
            return tbody.select("tr[valign='middle']")
        except IndexError:
            return None

    def get_material_types(self):
        types = []
        rows = self.get_rows()
        if rows is None:
            return None
        for row in rows:
            type_td = row.find_all('td')[2]
            material_type = type_td.find('a')
            if row.find_all('td')[4].text != "0.":
                types.append(material_type.text)
        return types

    def get_img_src(self, row):
        icon = row.find_all('td')[2]
        icon_img = icon.find('img')
        return icon_img['src']

    def get_subject_materials_folder_dictionary(self):
        dictionary = {}
        rows = self.get_rows()
        if rows is None:
            return None
        for row in rows:
            icon = self.get_img_src(row)
            name = row.find_all('td')[3]
            if icon == "/images/dir.gif":
                dictionary[name.text] = "yes"
            else:
                dictionary[name.text] = "no"
        return dictionary



