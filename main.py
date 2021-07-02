import re
import rocksdb

from slugify import slugify


db = rocksdb.DB("./dbreverse.db", rocksdb.Options(create_if_missing=True))
WEB = 'web'
LINKEDIN = 'lnkd'
NAME = 'name'


class ReverseIndex:
    @staticmethod
    def _to_bytes(key):
        return str.encode(str(key))

    @staticmethod
    def set(key, value):
        db.put(ReverseIndex._to_bytes(key), ReverseIndex._to_bytes(value))

    @staticmethod
    def get(key):
        value = db.get(ReverseIndex._to_bytes(key))
        if value:
            return value.decode()
        return value


def clean_url(url):
    if url.startswith('http'):
        url = re.sub(r'https?:\\', '', url)
    if url.startswith('www.'):
        url = re.sub(r'www.', '', url)
    return url


def clean_name(name):
    names = name.split(' ')
    len_names = len(names)
    return [slugify('-'.join(names[:i + 1])) for i in range(len_names)]


def process(id, name, website=None, linkedin=None, *args, **kwargs):
    website_value = ReverseIndex.get(f'{WEB}:{website}')
    linkedin_value = ReverseIndex.get(f'{LINKEDIN}:{linkedin}')
    found = ''
    possibly_names = clean_name(name)
    if website_value and str(id) != website_value:
        print(f'[Company {name} repeated] Same website id:', website_value)
        found = WEB
    elif linkedin_value and str(id) != linkedin_value:
        print(f'[Company {name} repeated] Same linkedin id:', linkedin_value)
        found = LINKEDIN
    else:
        for sub_name in possibly_names:
            name_value = ReverseIndex.get(f'{NAME}:{sub_name}')
            if name_value and str(id) != name_value:
                print(
                    '[Possibly repeated]',
                    'name_company:', name,
                    'found_name:', sub_name,
                    id, name_value,
                )
                found = NAME
                break
    new_id = id
    if found == WEB:
        new_id = website_value
    elif found == LINKEDIN:
        new_id = linkedin_value
    elif found == NAME:
        new_id = name_value
    if website:
        ReverseIndex.set(f'{WEB}:{website}', new_id)
    if linkedin:
        ReverseIndex.set(f'{LINKEDIN}:{linkedin}', new_id)
    for sub_name in possibly_names:
        ReverseIndex.set(f'{NAME}:{sub_name}', new_id)


# This is a mock database, the idea is to get the data from a real database.
companies_db = (
    (1, 'Facebook', 'facebook.com', 'https://www.linkedin.com/company/facebook/', '2020-02-02'),
    (2, 'SaleMove', 'salemove.com', 'linkedin.com/company/salemove', '2019-03-01'),
    (3, 'Glia', 'glia.com', 'linkedin.com/company/salemove', '2021-02-01'),
    (4, 'Snapchat', None, None, '2017-01-01'),
    (5, 'Snapchat, LLC', None, None, '2017-02-01'),
)


if __name__ == '__main__':
    for company in companies_db:
        process(*company)
