import aiml
import wikipedia
import os
from search import search_answers

SESSION_ID = 1234


if __name__ == '__main__':
    kernel = aiml.Kernel()

    # Check for existing "brain", meaning existing kernel progress saved
    # If there is, load it, if not, learn from existing AIML file
    if os.path.isfile('bot_brain.brn'):
        kernel.bootstrap(brainFile='bot_brain.brn')
    else:
        kernel.bootstrap(learnFiles='std-startup.xml', commands='load aiml b')
        kernel.saveBrain('bot_brain.brn')

    # Begin conversation loop
    while True:
        # Get user text input
        message = input('User> ')

        # In case of 'quit' or 'exit', stop conversation and exit program
        if message == 'quit' or message == 'exit':
            print("Debug Assistant> See ya next time!")
            exit()
        # In case if 'save', save kernel progress in a "brain" file
        elif message == 'save':
            print('Debug Assistant> Saved conversation!')
            kernel.saveBrain('bot_brain.brn')
        # Carry on conversation according to AIML file categories
        else:
            bot_response = kernel.respond(message, SESSION_ID)
            message = message.lower()

            # If the user text starts with "what is a...", get the rest of the sentence
            # and use it as input for searching StackOverflow for an answer, then send it
            if message.startswith('i have a question'):
                theme = kernel.getPredicate('query', SESSION_ID)
                answers = search_answers(theme, 1)
                print('Debug Assistant> This was the original question:',
                      answers[0][0])
                print('Debug Assistant>', answers[0][1])
                print('Debug Assistant> For more details, please check',
                      answers[0][2])
            # Still working on this
            elif message.startswith('tell me more about'):
                theme = kernel.getPredicate('factual', SESSION_ID)
                summary = wikipedia.summary(theme)
                print('Debug Assistant>', summary)
                # print('Debug Assistant> For more, please head to', )
            else:
                # Plain responses, used for testing
                print('Debug Assistant>', bot_response)
