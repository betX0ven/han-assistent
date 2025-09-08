import requests
import webbrowser

def get_weather(city):
    api_key = '9c5258c859de394817b5b82cd64a0455' # получите ключ API на сайте OpenWeatherMap
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    
    try:
        response = requests.get(url)
        response.raise_for_status() # сгенерирует исключение для кода отличного от 200
        
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        return f'Погода в городе {city}: {weather_description}, Температура: {temperature}°C, Влажность: {humidity}%'
    
    except requests.exceptions.HTTPError as err:
        # обработка ошибки
        return f'Произошла ошибка: {err}'

city = 'Yuzhno-Sakhalinsk'


#Открытие гугла
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    
print(get_weather('Южно-Сахалинск'))