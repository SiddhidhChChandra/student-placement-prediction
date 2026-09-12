from pathlib import Path
from urllib.request import urlopen

URL = 'https://huggingface.co/spaces/Datatrooper/boston_housing/resolve/main/Housing.csv?download=true'
OUTPUT = Path('Housing.csv')

with urlopen(URL) as response:
    OUTPUT.write_bytes(response.read())

print(f'Dataset saved to {OUTPUT.resolve()}')
