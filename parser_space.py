import json
import requests
from bs4 import BeautifulSoup


def get_first_news_space():
    url = "https://www.unian.ua/tag/kosmos"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards_space = soup.find_all("div", class_='list-thumbs__item')
    news_dict = {}

    for card in articles_cards_space:
        title_space = card.find('a', class_='list-thumbs__title').text.strip()
        link_space = card.find('a', class_='list-thumbs__title').get('href')
        time_space = card.find('div', class_='list-thumbs__time time').text

        article_id_space = link_space.split('/')[-1]
        id_space = article_id_space.split('-')[-1]
        id__ = id_space.split('.')[0]

        news_dict[id__] = {
            'time': time_space,
            'title': title_space,
            'link': link_space,
        }

    with open('news_dict_space.json', 'w') as f:
        json.dump(news_dict, f, indent=4, ensure_ascii=False)


def check_news_update_space():
    fresh_news_space = {}
    with open("news_dict_space.json") as file:
        news_dict_space = json.load(file)
        url_space = 'https://www.unian.ua/tag/kosmos'
        r = requests.get(url_space)
        soup_space = BeautifulSoup(r.text, 'lxml')
        articles_cards_space = soup_space.find_all('div', class_='list-thumbs__item')

        for card in articles_cards_space:
            link_space = card.find('a', class_='list-thumbs__title').get('href')
            article_id = link_space.split('/')[-1]
            id_ = article_id.split('-')[-1]
            id__ = id_.split('.')[0]
            if id__ in news_dict_space:
                continue
            else:
                title_space = card.find('a', class_='list-thumbs__title').text.strip()
                link_space = card.find('a', class_='list-thumbs__title').get('href')
                time_space = card.find('div', class_='list-thumbs__time time').text

                news_dict_space[id__] = {
                    'time': time_space,
                    'title': title_space,
                    'link': link_space,
                }

                fresh_news_space[id_] = {
                    'time': time_space,
                    'title': title_space,
                    'link': link_space,
                }

            with open('news_dict_space.json', 'w') as f:
                json.dump(news_dict_space, f, indent=4, ensure_ascii=False)

        return fresh_news_space


def main():
    # get_first_news_space()
    check_news_update_space()


if __name__ == '__main__':
    main()
