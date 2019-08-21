from src import postprocessing
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import os


def draw_plot_tsne(model):
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rc('font', family='AppleGothic')
    vocab = list(model.wv.vocab)
    X = model[vocab]
    print(len(X))

    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=1000)
    X_tsne = tsne.fit_transform(X)

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(1, 1, 1)
    df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
    ax.scatter(df['x'], df['y'])

    for word, pos in df.iterrows():
        ax.annotate(word, pos)
    plt.show()


result = []
'''
for m in range(1, 13):
    postprocessing.html_2_txt(2014, m)
    result.extend(postprocessing.tokenize(2014, m))
'''

# for m in range(1, 2):
# postprocessing.html_2_txt(2014, m)

year = 2014
month = 1
postprocessing.tokenize(year, month)

for file in os.listdir(f"./newspaper/txt/newspaper{year}/{year}.{month}/"):
    with open(f"./newspaper/txt/newspaper{year}/{year}.{month}/" + file, encoding="euc-kr") as f:
        result.append(f.readline().split(","))

if os.path.exists(f"2019.model"):
    model = Word2Vec.load("2019.model")
else:
    model = Word2Vec(result, size=300, min_count=100, workers=4, sg=1)
    model.save("2019.model")

draw_plot_tsne(model)
