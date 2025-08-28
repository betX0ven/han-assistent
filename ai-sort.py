# Импортируем необходимые библиотеки
from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd

import pymorphy3

morph = pymorphy3.MorphAnalyzer()

model = SentenceTransformer("gmunkhtur/paraphrase-multilingual-minilm-l12-v3-mn")

all_answers = ['погода', 'время', 'стим', 'браузер', 'музыка']

banword = ["как, он, мы, его, вы, вам, вас, ее, что, который, их, все, они, я, весь, мне, меня, таким, для, на, по, со, из, от, до, без, над, под, за, при, после, во, же, то, бы, всего, итого, даже, да, нет, ой, ого, эх, браво, здравствуйте, спасибо, извините, пожалуйста".replace(",","").split()][0]
def text_clear(query:str):
    ignorechars = r''',:\—=/|'%*"?<>!-_'''
    query = str(query).lower()
    queryC = ""
    for i in query:
        if i not in ignorechars:
            queryC += i

    banwordC = ""
    for i in queryC.split():
        if i not in banword:
            banwordC += i+" "
    return banwordC

tags = [text_clear(i) for i in all_answers]

text_embeddings = model.encode(tags, convert_to_tensor=True)

def semantic_search(query, embeddings, top_n=3):
    # Векторизуем запрос
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Вычисляем косинусное сходство между запросом и каждым текстом
    similarities = util.pytorch_cos_sim(query_embedding, embeddings)[0]

    # Получаем индексы наиболее похожих текстов
    top_results = np.argsort(similarities.cpu().numpy())[-top_n:][::-1]
    
    return all_answers[top_results[0]]


def start_ai(query):
    response = semantic_search(query, text_embeddings)
    return text_clear(preparing_query(response))

# query = text_clear("Какая сейчас погода")

def preparing_query(query):
    total_query = ''
    for word in query.split():
        word = morph.parse(word)[0]
        total_query+=word.normal_form+" "
    return total_query

# while True:
#   query = input("Введите запрос: ")
#   print(text_clear(preparing_query(query)))
#   print(start_ai(text_clear(preparing_query(query))))
