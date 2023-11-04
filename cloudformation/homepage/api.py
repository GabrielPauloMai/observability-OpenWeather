import requests

class OpenWeatherAPI:
    
    def __init__(self, api_key):
        self.base_url_geo = 'http://api.openweathermap.org/geo/1.0/direct'
        self.base_url_weather = 'https://api.openweathermap.org/data/2.5/weather'
        self.api_key = api_key
    
    def get_city(self, name):
        params = {'q': name, 'limit': 1, 'appid': self.api_key}
        response = requests.get(self.base_url_geo, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Localidade {name} não encontrada", response.status_code, response.text)
        
    def get_weather(self, lat, lon):
        params = {'lat': lat, 'lon': lon, 'lang': 'pt_br','units': 'metric', 'exclude': 'minutely,hourly', 'appid': self.api_key}
        response = requests.get(self.base_url_weather, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_weather_by_city(self, name):
        city_info = self.get_city(name)
        if city_info is None or len(city_info) == 0:
            raise TypeError(f"Localidade {name} não encontrada")
        else:
            print(city_info[0]['lat'], city_info[0]['lon'])
            return self.get_weather(city_info[0]['lat'], city_info[0]['lon'])



if __name__ == '__main__':
    run = OpenWeatherAPI('c8323e14011f5f3b51fd1235520f0517')
    print(run.get_weather_by_city('saffasdass'))