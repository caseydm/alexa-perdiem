import logging

from flask import Flask, render_template
from flask_ask import Ask, question, statement
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


app = Flask('__name__')
ask = Ask(app, '/')


@ask.launch
def launch():
    speech_text = render_template('welcome_text')
    reprompt_text = render_template('welcome_reprompt')
    return question(speech_text).reprompt(reprompt_text)


@ask.intent('GetPerDiemRate')
def get_per_diem():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask for Per Diem rates'
    return question(speech_text). \
        reprompt(speech_text). \
        simple_card('GetPerDiemRate', speech_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
