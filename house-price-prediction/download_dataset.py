from pathlib import Path
from urllib.request import urlopen

URL = 'https://raw.githubusercontent.com/Datatrooper/boston_housing/main/Housing.csv'
OUTPUT = Path('Housing.csv')

with urlopen(URL) as response:
    OUTPUT.write_bytes(response.read())

print(f'Dataset saved to {OUTPUT.resolve()}')
