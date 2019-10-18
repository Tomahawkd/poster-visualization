from time import sleep

import requests
import json
import os

session: requests.Session = requests.Session()
ua = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0"}
session.headers.update(ua)
session.get("https://movie.douban.com")

base_url: str = "https://movie.douban.com/j/new_search_subjects?" \
                "sort=U&range=0,10" \
                "&tags=%E7%94%B5%E5%BD%B1" \
                "&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86"

count: int = 20


def crawl(starting: int = 0, year: int = 2018) -> int:
    url = f"{base_url}&year_range={year},{year}&start={starting}"
    content = session.get(url).text
    j = json.loads(content)["data"]

    if len(j) == 0:
        return 0

    for i in j:
        try:
            if len(i['directors']) == 0:
                continue
            for dire in i['directors']:
                if str(dire).__contains__("·"):
                    raise StopIteration
        except StopIteration:
            continue
        print(i)
        save_to_file(i['cover'], year, i['id'])

    return len(j)


def save_to_file(url: str, year: int, id: str):
    try:
        url.index('/f/movie/30c6263b6db26d055cbbe73fe653e29014142ea3/pics/movie/')
        print("No picture, skipping")
        return
    except ValueError:
        pass

    if url.endswith('/movie_default_large.png'):
        print("No picture, skipping")
        return
    binary = requests.get(url).content
    if not os.path.exists(f"./data/{year}"):
        os.mkdir(f"./data/{year}")
    print(f"Saving file as .{year}/{id}.jpg")
    with open(f'./data/{year}/{id}.jpg', mode='wb') as f:
        f.write(binary)
        f.flush()


if __name__ == '__main__':
    for i in range(0, 60):
        if crawl(starting=i * count, year=2013) == 0:
            break

    for i in range(0, 60):
        if crawl(starting=i * count, year=2012) == 0:
            break
