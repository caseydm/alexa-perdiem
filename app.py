import logging
import datetime
import requests
from flask import Flask, render_template
from flask_ask import Ask, question, statement
from config import STATES


logging.getLogger('flask_ask').setLevel(logging.DEBUG)


app = Flask('__name__')
ask = Ask(app, '/')


@ask.launch
def launch():
    speech_text = render_template('welcome_text')
    help_text = render_template('help_text')
    return question(speech_text).reprompt(help_text)


@ask.intent('GetPerDiemRate')
def get_per_diem(city, state):
    rate = parse_api(city, state)
    speech_text = 'The per diem rate for {} is {} for loding and {} for meals.'.format(city, rate['lodging'], rate['meals'])
    return statement(speech_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    return "", 200


def parse_api(city, state):
    url = 'https://inventory.data.gov/api/action/datastore_search?' \
        'resource_id=8ea44bc4-22ba-4386-b84c-1494ab28964b&' \
        'filters={"City":"' + city + '","State":"' + STATES[state] + '"}'

    resp = requests.get(url=url)
    data = resp.json()

    month = datetime.datetime.now().strftime('%b')

    if data['success'] is True:
        success = True
        lodging = data['result']['records'][0][month]
        meals = data['result']['records'][0]['Meals']
    else:
        success = False
        lodging = None
        meals = None

    return {'lodging': lodging, 'meals': meals, 'success': success}


if __name__ == '__main__':
    app.run(debug=True)
