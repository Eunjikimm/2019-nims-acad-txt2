from bs4 import BeautifulSoup as bs
from konlpy.tag import Kkma
import glob
import os


def html_2_txt(year, month):
    if month < 10:
        month = "0" + str(month)
    if not os.path.exists(f"./newspaper/txt/newspaper{year}/{year}.{month}"):
        os.makedirs(f"./newspaper/txt/newspaper{year}/{year}.{month}")

    for file in glob.glob(f"./newspaper/newspaper{year}/{year}.{month}/*.html"):
        with open(file, encoding="euc-kr") as f:
            soup = bs(f, 'html.parser')
            article = soup.find("p").get_text()
            if len(article) == 0:
                break
            file = file.rstrip(".html")
            article_to_txt = f"./newspaper/txt/newspaper" + file.lstrip("./newspaper/") + ".txt"
            for k, s in enumerate(article):
                if "ⓒ" == s:
                    article = article[:k]
                    break
            txt = open(article_to_txt, "w")
            txt.write(article)
            txt.close()


def tokenize(year, month):
    if month < 10:
        month = "0" + str(month)
    kkma = Kkma()
    result = []
    for file in glob.glob(f"./newspaper/txt/newspaper{year}/{year}.{month}/*.txt"):
        f = open(file, "r")
        result.extend(kkma.nouns(f.readline()))
        f.close()
    return result
