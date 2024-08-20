import json
import requests
from bs4 import BeautifulSoup


def get_first_news_it():
    #  url сайта
    url = "https://speka.media/news-it?utm_source=google&utm_medium=cpc&utm_campaign=21107681931&gad_source=1"
    r = requests.get(url=url)
    #  збираемо всі новини із сайту
    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="post-wrapper")  #
    news_dict = {}
    #  пробігаюсь циклом за статтями
    for article in articles_cards:
        #  title статьи с тегом h3 в класі news-item__title
        article_title = article.find("h3", class_="news-item__title").text.strip()
        #  decs с тегом div в класі w-8/12 hidden sm:flex px-3
        #  методом strip обрізаємо зайве
        article_decs = article.find("div", class_="w-8/12 hidden sm:flex px-3").text.strip()
        #  забираємо url через href
        article_url = article.find("a")["href"]
        #  published в класі mr-4
        published = (article.find(class_="mr-4")).text.strip()

        #  split прибираємо символи / і беремо id щоб надалі за ними визначати наявність новини
        article_id = article_url.split("/")[-1]
        id_ = article_id.split("-")[-1]

        #  створюємо словник статей
        news_dict[id_] = {
            "published": published,
            "article_title": article_title,
            "article_decs": article_decs,
            "article_url": article_url,

        }

    #  зберігаємо в json файл, 'w'- для запису в json файл
    with open("news_dict_it.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

#  функція для перевірки новин на оновлення


def check_news_update_it():
    fresh_news = {}
    #  читаємо та зберігаємо словник у змінну
    with open("news_dict_it.json") as file:
        news_dict = json.load(file)
        url = "https://speka.media/news-it?utm_source=google&utm_medium=cpc&utm_campaign=21107681931&gad_source=1"
        r = requests.get(url)
        #  збираємо всі новини із сайту
        soup = BeautifulSoup(r.text, "lxml")
        articles_cards = soup.find_all("div", class_="post-wrapper")
        #  створюю новий словник з новими новинами

    #  пробігаюсь циклом за статтями
        for article in articles_cards:
            article_url = article.find("a")["href"]  # забираем url через href
            #  відокремлюю id від зайвих символів
            article_id = article_url.split("/")[-1]
            id_ = article_id.split("-")[-1]
            #  якщо id вже є у словнику
            if id_ in news_dict:
                continue
            #  якщо збігів не знайдено
            else:
                #  збираю всі дані на новини
                article_title = article.find("h3", class_="news-item__title").text.strip()
                article_decs = article.find("div", class_="w-8/12 hidden sm:flex px-3").text.strip()
                published = (article.find(class_="mr-4")).text.strip()
                #  додаю новину до словника
                news_dict[id_] = {
                    "published": published,
                    "article_title": article_title,
                    "article_decs": article_decs,
                    "article_url": article_url,
                }
                #  додаю новинку до нового словника
                fresh_news[id_] = {
                    "published": published,
                    "article_title": article_title,
                    "article_decs": article_decs,
                    "article_url": article_url,
                    }

            with open("news_dict_it.json", "w") as f:
                json.dump(news_dict, f, indent=4, ensure_ascii=False)
            #  повертаю новини у новому словнику
        return fresh_news


def main():
    #  вызываем функцию по сбору статей вызывается один раз что бы собрать новости
    # get_first_news_it()
    #  вызываем функцию с новыми новостями
    check_news_update_it()


if __name__ == "__main__":
    main()
