# проверить name,link,text по базе данных

import telebot
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
bot = telebot.TeleBot("7012423411:AAHcaFjCf30Ls9StwaQu5fRQcx3ouEOWDh4")
knowledge_base = pd.read_csv('max.csv')  # Загрузка базы данных знаний

@bot.message_handler(func=lambda message: True)
def prob(message):
    problem = message.text.strip()
    clear_problem = create_new_proposal(problem)
    bot.send_message(message.chat.id, "Принято, я работаю над этим. Ожидайте")
    answer = find_relevant_document_and_text(clear_problem)
    if answer[0]>0.00099:
        total_answer = f"<b>Название:</b> {answer[1]}\n<b>Ссылка:</b> {answer[2]}\n<b>Ответ:</b> {answer[3]}\n"
        bot.send_message(message.chat.id, total_answer, parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Попробуйте переформулировать вопрос")

# обработка текста и его преобразование
def create_new_proposal(text):
    stemmer = PorterStemmer()

    stop_words = set(stopwords.words('russian'))
    text = text.lower()

    tokens = word_tokenize(text)  # по словам
    tokens = [word for word in tokens if word not in stop_words]  # убрать мусор
    tokens = [stemmer.stem(word) for word in tokens]  # убрать знаки препинания

    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stop_words]

    sentence = " ".join(tokens)
    return(sentence)

# Функция для предобработки текста
def preprocess(text):
    tokens = word_tokenize(text.lower())
    return ' '.join(tokens)

# Предобработка каждого абзаца
knowledge_base['processed'] = knowledge_base['text'].apply(preprocess)

# Инициализация Vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(knowledge_base['processed'])

# Функция поиска наиболее подходящего документа и его содержимого
def find_relevant_document_and_text(question):
    processed_question = preprocess(question) # Предобработка вопроса
    question_vector = vectorizer.transform([processed_question]) # Векторизация вопроса
    texts_vector = vectorizer.transform(knowledge_base['processed']) # Векторизация текстов
    similarities = cosine_similarity(question_vector, texts_vector) # Вычисление косинусного сходства
    average = np.mean(similarities)  # точность по среднему арифметическому
    print(average)

    most_relevant_idx = similarities.argmax() # Нахождение индекса текста с максимальным сходством

    # Возвращение наиболее релевантного названия документа и текста
    return average,knowledge_base.iloc[most_relevant_idx]['name'], knowledge_base.iloc[most_relevant_idx]['link'], knowledge_base.iloc[most_relevant_idx]['text']


bot.polling(none_stop=True)
