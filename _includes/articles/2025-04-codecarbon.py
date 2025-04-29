from codecarbon import EmissionsTracker
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


with EmissionsTracker() as tracker:

    chatbot = ChatBot(
        "Chatbot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.BestMatch",
            "chatterbot.logic.TimeLogicAdapter"
        ],
        database_uri="sqlite:///database.sqlite3"
    )

    # Train the chatbot with a small amount of simple data

    trainer = ListTrainer(chatbot)

    trainer.train([
        "Hello, how are you?",
        "I am good, thank you!",
        "You're welcome!",
    ])

    trainer.train([
        "Who are you?",
        "I am a chatbot built using ChatterBot.",
        "It's nice to meet you!",
        "Thanks, it's nice to meet you too!",
    ])

    message = "Hello, how are you?"

    response = chatbot.get_response(message)

    print(f"Chatbot response: {response.text}")

# Display the tracked emissions data

print(f"Carbon emissions from computation: {tracker.final_emissions * 1000:.4f} g CO2eq")
print("Detailed emissions data:", tracker.final_emissions_data)
