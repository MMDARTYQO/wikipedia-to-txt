import requests
from bs4 import BeautifulSoup

def download_wikipedia_article(title, filename):
    url = f'https://he.wikipedia.org/wiki/{title}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find(id='mw-content-text').get_text()

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    article_title = "פייתון_(שפת_תכנות)"  # ערך קבוע
    output_filename = "python_article.txt"  # שם קובץ קבוע בתוך ספריית הפרויקט
    download_wikipedia_article(article_title, output_filename)
    print(f"הערך '{article_title}' נשמר בהצלחה בקובץ '{output_filename}'")