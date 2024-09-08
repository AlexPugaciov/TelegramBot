import requests
from datetime import datetime, timedelta
from config import WEATHER_API

WEATHER_API = WEATHER_API


def get_next_day(day, hour, minute):
    now = datetime.now()
    days_ahead = (day - now.weekday() + 7) % 7
    if days_ahead == 0 and (now.hour, now.minute) >= (hour, minute):
        days_ahead += 7
    next_occurrence = (now + timedelta(days=days_ahead)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    return next_occurrence


def get_wether(api_key, city, target_times):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dict_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        closest_forecasts = list()

        for target_time in target_times:
            closest_forecast = None
            min_diff = float('inf')

            for forecast in data['list']:
                forecast_time = datetime.fromtimestamp(forecast['dt'])
                diff = abs((forecast_time - target_time).total_seconds())

                if diff < min_diff:
                    min_diff = diff
                    closest_forecast = forecast

            if closest_forecast:
                temperature = closest_forecast['main']['temp']
                precipitation = closest_forecast.get('rain', {}).get('3h', 0) + closest_forecast.get('snow', {}).get(
                    '3h',
                    0)
                precipitation_probability = closest_forecast.get('pop', 0) * 100
                wind_speed = closest_forecast.get('wind').get('speed')
                closest_forecasts.append(
                    (target_time, temperature, precipitation, precipitation_probability, wind_speed))

        if closest_forecasts:
            closest_forecasts.sort(key=lambda x: x[0])
            nearest_forecast = closest_forecasts[0]
            day = nearest_forecast[0].weekday()
            return (f"🏐🏆Entry for {dict_days[day]}🏆🏐"
                    f"{nearest_forecast[0].strftime('\n\n📅 %Y-%m-%d......⏰ %H:%M')}"
                    f"\n\n🌡Temperature: {nearest_forecast[1]}°C"
                    f"\n🌧️Precipitation: {nearest_forecast[2]} mm probability: {nearest_forecast[3]}%"
                    f"\n 🌬Wind: {nearest_forecast[4]} m/s"
                    f"\n\n⚔️Will go:\n\n")
    else:
        return f'Error conection: status code {response.status_code}'


def get_weather_next_day():
    return get_wether(api_key, city, target_times)


api_key = WEATHER_API
city = 'your_city'

target_times = [
    get_next_day(day=1, hour=18, minute=30),
    get_next_day(day=3, hour=18, minute=30),
    get_next_day(day=5, hour=9, minute=0),
    get_next_day(day=6, hour=9, minute=0)]

if __name__ == '__main__':
    print(get_wether(api_key, city, target_times))
