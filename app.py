import logging

from flask import Flask, render_template
from flask_ask import Ask, question, statement
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


app = Flask('__name__')
ask = Ask(app, '/')


@ask.launch
def launch():
    speech_text = render_template('welcome_text')
    help_text = render_template('help_text')
    return question(speech_text).reprompt(help_text)


@ask.intent('GetPerDiemRate')
def get_per_diem(city):
    speech_text = 'The per diem rate for {} is $320.'.format(city)
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


if __name__ == '__main__':
    app.run(debug=True)
