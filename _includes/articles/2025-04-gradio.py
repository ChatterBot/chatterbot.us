import gradio as gr
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


chatbot = ChatBot(
    "Chatbot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.TimeLogicAdapter"
    ],
    database_uri="sqlite:///database.sqlite3",
    read_only=True
)

def train_chatbot():
    """
    Train the chatbot with a small amount of simple data
    """

    # Skip training if the chatbot has already has data
    if chatbot.storage.count() > 0:
        return

    trainer = ListTrainer(chatbot)

    trainer.train([
        "Hello, how are you?",
        "I am good, thank you!",
        "You're welcome!",
    ])

    trainer.train([
        "Who are you?",
        "I am a chatbot built using ChatterBot and Gradio.",
        "It's nice to meet you!",
        "Nice to meet you too!",
    ])

    trainer.train([
        "Tell me a joke.",
        "Why did the chicken cross the road? To get to the other side!",
        "So funny!",
        "I know, right?",
    ])


def response_function(message, history):
    return chatbot.get_response(message).text


train_chatbot()

interface = gr.ChatInterface(
    fn=response_function, 
    type="messages",
    title="ChatterBot with Gradio",
    description="Enter your message and get a response from the chatbot.",
)


interface.launch(server_port=9000)
