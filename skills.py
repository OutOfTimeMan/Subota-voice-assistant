import os, webbrowser, sys, requests, subprocess, pyttsx3

engine = pyttsx3.init()

# Скорость речи
engine.setProperty('rate', 180)


def speaker(text):
    """Активация речи"""
    engine.say(text)
    engine.runAndWait()


def passive():
    pass


def game():
    """Открывает фортнайт и закрывает хром"""
    subprocess.Popen('Q:/Fortnite/FortniteGame/Binaries/Win64/FortniteClient-Win64-Shipping.exe')
    os.system("TASKKILL /F /IM chrome.exe")


def game_with_friends():
    """Открывает фортнайт, дискорд, закрывает браузер"""
    subprocess.Popen('Q:/Fortnite/FortniteGame/Binaries/Win64/FortniteClient-Win64-Shipping.exe')
    subprocess.Popen("C:/Users/teret/AppData/Local/Discord/app-1.0.9005/Discord.exe")
    os.system("TASKKILL /F /IM chrome.exe")


def weather():
    '''Берёт данные о погоде с сайта openweather '''
    try:
        params = {'q': 'Kyiv', 'units': 'metric', 'lang': 'ru', 'appid': 'api-token'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')


def reload_pc():
    '''Перезагрузка пк'''
    os.system('shutdown /r')


def off_bot():
    '''Остановка работы программы'''
    sys.exit()


def off_pc():
    '''Выключение компьютера'''
    os.system('shutdown /s')


def browser():
    '''Открыть браузер'''
    webbrowser.open('https://www.youtube.com/', new=2)
