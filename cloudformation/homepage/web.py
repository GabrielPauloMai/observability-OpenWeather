import os
from flask import Flask, render_template, request, redirect
from api import OpenWeatherAPI
from prometheus_client import start_http_server, Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from time import time
import logging
from pygelf import GelfTcpHandler

app = Flask(__name__)

# Configurando o sistema de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(GelfTcpHandler(host='root_graylog_1', port=12201))


# Métricas para monitorar as requisições HTTP
request_counter = Counter('http_requests_total', 'Total HTTP Requests', ["status_code", "instance"])
request_duration_histogram = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ["endpoint", "status_code", "instance"])

# Métricas para monitorar erros na API da OpenWeather
api_key_error_counter = Counter('api_key_errors_total', 'OpenWeather API Key Errors', ["instance"])

# Métricas para monitorar a duração das chamadas da OpenWeatherAPI
weather_api_request_duration_histogram = Histogram('openweatherapi_request_duration_seconds', 'OpenWeatherAPI Request Duration', ["method", "instance"])

api_key = 'c8323e14011f5f3b51fd1235520f0517'

if not api_key:
    api_key_error_counter.labels(instance='homepage').inc()
    raise ValueError("A chave da API da OpenWeather não foi configurada.")

weather_api = OpenWeatherAPI(api_key)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/')
def index():
    start_time = time()
    request_counter.labels(status_code='200', instance='homepage').inc()
    request_duration = time() - start_time
    request_duration_histogram.labels(endpoint='index', status_code='200', instance='homepage').observe(request_duration)
    
    # Log de informações
    logger.info(f"Successful request to /index with status code 200 in {request_duration:.4f} seconds.")
    
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    start_time = time()
    cidade = request.form['city']
    try:
        dados_clima = weather_api.get_weather_by_city(cidade)
    except TypeError as e:
        request_counter.labels(instance='homepage', status_code='404').inc()
        
        # Log de erro
        logger.error(f"Error: {e}")
        
        return render_template('error.html', error=e)

    if dados_clima:
        info_clima = {
            'cidade': cidade,
            'temperatura': dados_clima['main']['temp'],
            'sensacao_termica': dados_clima['main']['feels_like'],
            'umidade': dados_clima['main']['humidity'],
            'velocidade_vento': dados_clima['wind']['speed'],
            'descricao': dados_clima['weather'][0]['description'],
            'icon_code': dados_clima['weather'][0]['icon'],
        }
        request_counter.labels(instance='homepage', status_code='200').inc()
        weather_api_request_duration = time() - start_time
        weather_api_request_duration_histogram.labels(method='get_weather_by_city', instance='homepage').observe(weather_api_request_duration)
        
        # Log de informações
        logger.info(f"Successful request to /weather with status code 200 in {weather_api_request_duration:.4f} seconds.")
        
        return render_template('weather.html', weather=info_clima)
    else:
        request_counter.labels(instance='homepage', status_code='404').inc()
        
        # Log de erro
        logger.error(f"Falha ao obter dados de clima para {cidade}")
        
        return render_template('error.html', error=f"Falha ao obter dados de clima para {cidade}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
