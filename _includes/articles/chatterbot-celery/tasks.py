from celery import Celery
from chatterbot import ChatBot


app = Celery('tasks', broker='pyamqp://guest@rabbitmq//')


@app.task
def solve(message_id: int, message: str):
    """
    Create a simple chatbot that can solve math problems.
    """
    chatbot = ChatBot(
        'Example Bot',
        logic_adapters=[
            'chatterbot.logic.MathematicalEvaluation'
        ]
    )

    response = chatbot.get_response(message)

    # Save the response to a file in the data directory
    with open(f'/data/{message_id}-response.txt', 'w+') as f:
        f.write(response.text)

    return response
