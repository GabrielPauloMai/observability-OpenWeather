import requests
from prometheus_client import Counter, Gauge, Histogram

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
    
    def get_city(self, name):
        params = {'q': name, 'limit': 1, 'appid': self.api_key}
        response = requests.get(self.base_url_geo, params=params)
        
        if response.status_code == 200:
            # Incrementando a métrica de solicitações bem-sucedidas
            self.successful_requests_counter.labels(instance='homepage', status_code=response.status_code).inc()
            return response.json()
        else:
            # Incrementando a métrica de solicitações malsucedidas
            self.failed_requests_counter.labels(instance='homepage').inc()
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
            return response.json()
        else:
            # Incrementando a métrica de solicitações malsucedidas
            self.failed_requests_counter.labels(instance='homepage').inc()
            return None
        
    def get_weather_by_city(self, name):
        city_info = self.get_city(name)
        if city_info is None or len(city_info) == 0:
            raise TypeError(f"Localidade {name} não encontrada")
        else:
            print(city_info[0]['lat'], city_info[0]['lon'])
            return self.get_weather(city_info[0]['lat'], city_info[0]['lon'])
