from flask import Flask
from flask_assistant import Assistant, ask, tell

app = Flask(__name__)
assist = Assistant(app, route='/')


@assist.action('greeting')
def greet_and_start():
    speech = "What would you like to search?"
    return ask(speech)

if __name__ == '__main__':
    app.run(debug=True)


@assist.action("give-choice")
def ask_for_vehiclechoice(choice):
    if choice == 'Car selection':
        choice_msg = 'Here are the available cars:!'
    else:
        choice_msg = 'That is not a valid option'

    speech = choice_msg
    return ask(speech)