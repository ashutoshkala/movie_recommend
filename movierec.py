import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')
columns = ["User_id", "item_id", "rating", "timestamp"]
df = pd.read_csv('u.data', sep="\t", names=columns)
movies_title = pd.read_csv(
    'u.item', sep="\|", header=None, encoding="ISO-8859-1")
movies_title = movies_title[[0, 1]]
movies_title.columns = ['item_id', 'title']
fdf = pd.merge(df, movies_title, on='item_id')
rating = pd.DataFrame(fdf.groupby('title').mean()['rating'])
rating['no of rating'] = pd.DataFrame(fdf.groupby('title').count()['rating'])
moviemat = fdf.pivot_table(index="User_id", columns="title", values='rating')


def pred_movies(movie_name):
    movuserr = moviemat[movie_name]
    x = moviemat.corrwith(movuserr)
    corrsw = pd.DataFrame(x, columns=['corr'])
    corrsw.dropna(inplace=True)

    data = corrsw.join(rating['no of rating'])
    pred = data[data['no of rating'] > 100].sort_values(
        by='corr', ascending=False)
    return pred


mov_name = input('Enter Full Movie name ')
p = pred_movies(mov_name)
p.drop('corr', inplace=True, axis=1)
# p.drop('no of rating', inplace=True, axis=1)
# print(p.head())
print("\n")

print("Suggestion 1")
print(p.iloc[1])
print("\n")

print("Suggestion 2")
print(p.iloc[2])
