import requests
from prometheus_client import Counter, Gauge, Histogram
import logging
from pygelf import GelfTcpHandler

class OpenWeatherAPI:
    
    def __init__(self, api_key):
        self.base_url_geo = 'http://api.openweathermap.org/geo/1.0/direct'
        self.base_url_weather = 'https://api.openweathermap.org/data/2.5/weather'
        self.api_key = api_key

        # Inicializando as métricas para monitorar solicitações bem-sucedidas e malsucedidas
        self.successful_requests_counter = Counter('api_successful_requests_total', 'OpenWeatherAPI Successful Requests', ["instance", "status_code"])
        self.failed_requests_counter = Counter('api_failed_requests_total', 'OpenWeatherAPI Failed Requests', ["instance"])

        # Inicializando métricas para monitorar status da resposta e tamanho do payload
        self.response_status_gauge = Gauge('api_response_status', 'OpenWeatherAPI Response Status', ["instance"])
        self.response_payload_size_histogram = Histogram('api_response_payload_size_bytes', 'OpenWeatherAPI Response Payload Size', ["instance"])
        self.request_duration_histogram = Histogram('api_request_duration_seconds', 'OpenWeatherAPI Request Duration', ["method", "instance"])

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(GelfTcpHandler(host='root_graylog_1', port=12201))

    def log_request(self, method, instance, payload=None,status_code=None, duration=None):
        self.logger.info(f"method={method} instance={instance} payload={payload} status_code={status_code} duration={duration}")
        

    def get_city(self, name):
        params = {'q': name, 'limit': 1, 'appid': self.api_key}
        response = requests.get(self.base_url_geo, params=params)

        if response.status_code == 200:
            # Incrementando a métrica de solicitações bem-sucedidas
            self.successful_requests_counter.labels(instance='homepage', status_code=response.status_code).inc()
            self.log_request(method='get_city', instance='homepage',status_code=response.status_code, payload=response.text, duration=response.elapsed.total_seconds())
            return response.json()
        else:
            # Incrementando a métrica de solicitações malsucedidas
            self.failed_requests_counter.labels(instance='homepage').inc()
            self.log_request(method='get_city', instance='homepage',status_code=500, payload=response.text, duration=response.elapsed.total_seconds())
            raise Exception(f"Localidade {name} não encontrada", response.status_code, response.text)
        
    def get_weather(self, lat, lon):
        params = {'lat': lat, 'lon': lon, 'lang': 'pt_br','units': 'metric', 'exclude': 'minutely,hourly', 'appid': self.api_key}
        response = requests.get(self.base_url_weather, params=params)
        
        # Incrementando a métrica de status da resposta
        self.response_status_gauge.labels(instance='homepage').set(response.status_code)

        # Incrementando a métrica de tamanho do payload
        self.response_payload_size_histogram.labels(instance='homepage').observe(len(response.text))
        
        if response.status_code == 200:
            # Incrementando a métrica de solicitações bem-sucedidas
            self.log_request(method='get_weather', instance='homepage',status_code=response.status_code, payload=response.text, duration=response.elapsed.total_seconds())
            return response.json()
        else:
            # Incrementando a métrica de solicitações malsucedidas
            self.log_request(method='get_weather', instance='homepage',status_code=500, payload=response.text, duration=response.elapsed.total_seconds())
            self.failed_requests_counter.labels(instance='homepage').inc()
            return None
        
    def get_weather_by_city(self, name):
        city_info = self.get_city(name)
        if city_info is None or len(city_info) == 0:
            self.log_request(method='get_weather_by_city', instance='homepage',status_code=404, payload="Localidade {name} não encontrada", duration=None)
            raise TypeError(f"Localidade {name} não encontrada")
        else:
            print(city_info[0]['lat'], city_info[0]['lon'])
            self.log_request(method='get_weather_by_city', instance='homepage',status_code=200, payload=city_info[0], duration=None)
            return self.get_weather(city_info[0]['lat'], city_info[0]['lon'])
