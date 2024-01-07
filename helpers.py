import requests

from flask import redirect, render_template, session
from functools import wraps

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def getWeather():
    url = f'http://api.weatherapi.com/v1/current.json?key=80a40b56457941e8adc15509233012&q=Cuiaba&aqi=no'

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados_clima = resposta.json()
        return dados_clima
    except requests.exceptions.RequestException:
        return None


