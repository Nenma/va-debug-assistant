from turtle import title
import aiml
import wikipedia
import os
from search import search_answers
from flask import Flask, jsonify, request, render_template
app = Flask(__name__)


SESSION_ID = 1234


@app.route("/")
def hello():
    return render_template('index.html', title='Debug Assistant')


@ app.route('/send', methods=['POST'])
def send():
    data = request.json
    message = data['message']
    bot_response = kernel.respond(message, SESSION_ID)
    message = message.lower()

    if message == 'quit' or message == 'exit' or message == 'bye':
        return jsonify({'answer': 'See ya next time!'})
    elif message == 'save':
        kernel.saveBrain('bot_brain.brn')
        return jsonify({'answer': 'Saved conversation!'})

    # If the user text starts with "what is a...", get the rest of the sentence
    # and use it as input for searching StackOverflow for an answer, then send it
    elif message.startswith('i have a question'):
        theme = kernel.getPredicate('query', SESSION_ID)
        answers = search_answers(theme, 1)
        print('Debug Assistant> This was the original question:',
              answers[0][0])
        print('Debug Assistant>', answers[0][1])
        print('Debug Assistant> For more details, please check',
              answers[0][2])
        return jsonify({
            'original_question': answers[0][0],
            'answer': answers[0][1],
            'question_link': answers[0][2]
        })
    elif message.startswith('tell me more about'):
        theme = kernel.getPredicate('factual', SESSION_ID)
        return jsonify({'answer': f'Testing, testing! Looking for stuff on {theme}...'})
    else:
        print('Debug Assistant>', bot_response)
        return jsonify({'answer': bot_response})


if __name__ == '__main__':
    kernel = aiml.Kernel()

    # Check for existing "brain", meaning existing kernel progress saved
    # If there is, load it, if not, learn from existing AIML file
    if os.path.isfile('bot_brain.brn'):
        kernel.bootstrap(brainFile='bot_brain.brn')
    else:
        kernel.bootstrap(learnFiles='std-startup.xml',
                         commands='load aiml b')
        kernel.saveBrain('bot_brain.brn')

    app.run(port=5000, debug=True)
