from flask import Flask, render_template, request
import requests

# --- ตั้งค่า ---
# !!! วาง API Key ของคุณจาก OpenWeatherMap ตรงนี้ !!!
API_KEY = "1b1be55659e5d213070e7b25e4ded324" 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form['city_name']
        
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'th'
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") == 200:
            weather_data = {
                "city": data["name"],
                "description": data["weather"][0]["description"].capitalize(),
                "temperature": int(data["main"]["temp"]),
                "icon": data["weather"][0]["icon"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        else:
            error = data.get("message", "ไม่สามารถค้นหาข้อมูลได้")

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)