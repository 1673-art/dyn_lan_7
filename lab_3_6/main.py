from flask import Flask, render_template, request
import requests
from xml.etree import ElementTree as ET

app = Flask(__name__)

def load_cbr_rates():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)

    rates = {}

    root = ET.fromstring(response.content)
    items = root.findall('.//Valute')

    for item in items:
        code = item.find('CharCode').text
        curs = item.find('Value').text
        rates[code] = float(curs.replace(',', '.'))

    return rates

@app.route('/', methods=['GET', 'POST'])
def index():
    cbr_rates = load_cbr_rates()

    if request.method == 'POST':
        usd_amount = float(request.form['usd_amount'])
        eur_amount = float(request.form['eur_amount'])

        usd_rate = cbr_rates.get('USD')
        eur_rate = cbr_rates.get('EUR')
        total_rubles_USD = usd_amount * usd_rate
        total_rubles_EUR = eur_amount * eur_rate

        return render_template('index.html', usd_rate=usd_rate, eur_rate=eur_rate, total_rubles_USD=total_rubles_USD, total_rubles_EUR=total_rubles_EUR)

    return render_template('index.html', usd_rate=cbr_rates.get('USD', 0), eur_rate=cbr_rates.get('EUR', 0), total_rubles_USD=0, total_rubles_EUR=0)

if __name__ == '__main__':
    app.run(debug=True)
