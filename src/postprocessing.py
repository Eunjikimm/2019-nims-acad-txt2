from bs4 import BeautifulSoup as bs
from konlpy.tag import Okt
import glob
import os
import re

remove = ["서울신문", "페이스북", "글로벌세상", "동영상뉴스", "전체보기", "포토뉴스", "아시아투데이", "기자", "한국일보",
          "무단 전재 및 재배포 금지", "서울신문사 무단 전재 및 재배포 금지"]


def html_2_txt(year, month):
    if month < 10:
        month = "0" + str(month)

    if not os.path.exists(f"./newspaper/txt/newspaper{year}/{year}.{month}"):
        os.makedirs(f"./newspaper/txt/newspaper{year}/{year}.{month}")

    for file in os.listdir(f"./newspaper/newspaper{year}/{year}.{month}/"):
        with open(f"./newspaper/newspaper{year}/{year}.{month}/" + file, encoding="euc-kr") as f:
            soup = bs(f, 'html.parser')
            article = soup.find("p").get_text()

            for r in remove:
                article.replace(r, "")

            article = re.sub('[^ \nㄱ-ㅣ가-힣]+', "", article)

            article_to_txt = f"./newspaper/txt/newspaper{year}/{year}.{month}/" + file.rstrip(".html") + ".txt"

            txt = open(article_to_txt, "w")
            txt.write(article)
            txt.close()


def tokenize(year, month):
    if month < 10:
        month = "0" + str(month)
    okt = Okt()
    result = []
    i = 0
    for file in glob.glob(f"./newspaper/txt/newspaper{year}/{year}.{month}/*.txt"):
        print(i)
        print(file)
        i += 1
        f = open(file, "r")
        token = okt.pos(f.readline(), stem=True, norm=True)
        temp = []
        for word in token:
            if (word[1] == "Noun") and (len(word[0]) > 1):
                temp.append(word[0])
        result.append(temp)
        f.close()
    return result
