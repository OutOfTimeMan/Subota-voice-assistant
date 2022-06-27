import queue
import sounddevice as sd
import vosk
import json
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from skills import *

q = queue.Queue()

model = vosk.Model('vosk_model')

# Выбор микрофона и динамиков (сейчас по умолчанию)
device = sd.default.device

#Получение частоты микрофона
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def recognize(data, vectorizer, clf):
    '''Анализ распознаной речи'''

    # Произнесено ли имя бота
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    # Перевод полученого текста в вектор, сравнение с вариантами
    data.replace(list(trg)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # Получение имени функции с data_set
    func_name = answer.split()[0]

    #Озвучка
    speaker(answer.replace(func_name, ''))
    exec(func_name + '()')


def callback(indata):
    '''Добавляет в очередь семплы из потока.
    вызывается каждый раз при наполнении blocksize
    в sd.RawInputStream'''
    q.put(bytes(indata))


def main():
    '''
        Обучаем матрицу ИИ
        и постоянно слушаем микрофон
    '''

    #Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    # постоянная прослушка микрофона
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype='int16',
                                channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)


if __name__ == '__main__':
    main()