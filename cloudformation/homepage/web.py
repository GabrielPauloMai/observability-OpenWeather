import os
from flask import Flask, render_template, request, redirect
from api import OpenWeatherAPI

app = Flask(__name__)

api_key = 'c8323e14011f5f3b51fd1235520f0517'

if not api_key:
    raise ValueError("A chave da API da OpenWeather não foi configurada.")

weather_api = OpenWeatherAPI(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    cidade = request.form['city']
    try:
        dados_clima = weather_api.get_weather_by_city(cidade)
    except TypeError as e:
        return render_template('error.html', error=e)


    if dados_clima:
        info_clima = {
            'cidade': cidade,
            'temperatura': dados_clima['main']['temp'],
            'descricao': dados_clima['weather'][0]['description'],
        }
        return render_template('weather.html', weather=info_clima)
    else:
        return render_template('error.html', error=f"Falha ao obter dados de clima para {cidade}")

if __name__ == '__main__':
    app.run(debug=False)
