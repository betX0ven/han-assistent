# Импортируем необходимые библиотеки
from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd

import pymorphy3

morph = pymorphy3.MorphAnalyzer()

model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")

all_answers = ['погода', 'время', 'стим', 'браузер', 'музыка']

banword = ["как, он, мы, его, вы, вам, вас, ее, что, который, их, все, они, я, весь, мне, меня, таким, для, на, по, со, из, от, до, без, над, под, за, при, после, во, же, то, бы, всего, итого, даже, да, нет, ой, ого, эх, браво, здравствуйте, спасибо, извините, пожалуйста".replace(",","").split()][0]

tags = [i for i in all_answers]

text_embeddings = model.encode(tags, convert_to_tensor=True)

def semantic_search(query, embeddings, top_n=3):
    # Векторизуем запрос
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Вычисляем косинусное сходство между запросом и каждым текстом
    similarities = util.pytorch_cos_sim(query_embedding, embeddings)[0]

    # Получаем индексы наиболее похожих текстов
    top_results = np.argsort(similarities.cpu().numpy())[-top_n:][::-1]
    
    for i in range(len(top_results)):
        print(similarities[top_results[i]], tags[top_results[i]])
    if float(similarities[top_results[0]]) > 0.53:
        return all_answers[top_results[0]]
    else:
        return "for_ai"

def start_ai(query):
    response = semantic_search(query, text_embeddings)
    return response

def preparing_query(query):
    total_query = ''
    for word in query.split():
        word = morph.parse(word)[0]
        total_query+=word.normal_form+" "
    return total_query

def final_query_handler(query):
    print('Запрос ' + query)
    return start_ai(preparing_query(query))
