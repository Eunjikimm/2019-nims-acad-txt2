from bs4 import BeautifulSoup as bs
import glob
import os


def article_2_txt(year, month):
    if month < 10:
        month = "0" + str(month)
    os.chdir(f"./data/newspaper/newspaper{year}/{year}.{month}")
    os.makedirs("../txt")
    for file in glob.glob("*.html"):
        with open(file, encoding="euc-kr") as f:
            soup = bs(f, 'html.parser')
            article = soup.find("p").get_text()
            article_to_txt = "../txt/" + file.rstrip(".html") + ".txt"
            for k, s in enumerate(article):
                if "ⓒ" == s:
                    article = article[:k]
                    break
            print(article_to_txt)
            txt = open(article_to_txt, "w")
            txt.write(article)
            txt.close()
