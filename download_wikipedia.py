import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

def download_wikipedia_article(title, filename):
    url = f'https://he.wikipedia.org/wiki/{quote(title)}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find(id='mw-content-text').get_text()

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def create_directory_structure():
    base_dir = "wikipedia_articles"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    for letter in "אבגדהוזחטיכלמנסעפצקרשת":
        letter_dir = os.path.join(base_dir, letter)
        if not os.path.exists(letter_dir):
            os.mkdir(letter_dir)
    return base_dir

def get_all_article_titles():
    S = requests.Session()

    URL = "https://he.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "aplimit": "max"
    }

    article_titles = []
    while True:
        R = S.get(url=URL, params=PARAMS)
        if R.status_code == 200:
            try:
                DATA = R.json()
            except ValueError as e:
                print(f"Failed to parse JSON: {e}")
                break

            for page in DATA['query']['allpages']:
                article_titles.append(page['title'])

            if 'continue' not in DATA:
                break

            PARAMS['apcontinue'] = DATA['continue']['apcontinue']
        else:
            print(f"Request failed with status code {R.status_code}")
            break

        time.sleep(1)  # Sleep to avoid overloading the server

    return article_titles

def main():
    base_dir = create_directory_structure()
    article_titles = get_all_article_titles()

    for title in article_titles:
        first_letter = title[0]
        if first_letter not in "אבגדהוזחטיכלמנסעפצקרשת":
            first_letter = "א"
        target_dir = os.path.join(base_dir, first_letter)
        filename = os.path.join(target_dir, f"{title}.txt")
        print(f"Downloading {title}...")
        try:
            download_wikipedia_article(title, filename)
            print(f"Saved {title} to {filename}")
        except Exception as e:
            print(f"Failed to download {title}: {e}")

if __name__ == "__main__":
    main()
