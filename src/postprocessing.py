from bs4 import BeautifulSoup as bs
from konlpy.tag import Okt
import glob
import os
import re

remove = ["서울신문", "페이스북", "글로벌세상", "동영상뉴스", "전체보기", "포토뉴스", "아시아투데이", "기자", "한국일보",
          "무단 전재 및 재배포 금지", "서울신문사 무단 전재 및 재배포 금지"]


def tokenize(year, month):
    if month < 10:
        month = "0" + str(month)

    okt = Okt()

    if not os.path.exists(f"./newspaper/txt/newspaper{year}/{year}.{month}"):
        os.makedirs(f"./newspaper/txt/newspaper{year}/{year}.{month}")

    for file in os.listdir(f"./newspaper/newspaper{year}/{year}.{month}/"):
        with open(f"./newspaper/newspaper{year}/{year}.{month}/" + file, encoding="euc-kr") as f:
            soup = bs(f, 'html.parser')
            article = soup.find("p").get_text()
            result = []

            for r in remove:
                article.replace(r, "")

            article = re.sub('[^ \nㄱ-ㅣ가-힣]+', "", article)

            token = okt.pos(article, stem=True, norm=True)
            temp = []
            for word in token:
                if len(word[0]) > 1:
                    temp.append(word[0])
            result.extend(temp)

            article_to_txt = f"./newspaper/txt/newspaper{year}/{year}.{month}/" + file.rstrip(".html") + ".txt"

            txt = open(article_to_txt, "w")
            for noun in result:
                txt.write(noun + ",")
            txt.close()
