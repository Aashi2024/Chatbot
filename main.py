
from api import get_weather
#from flowerapi import get_flower_info


def chatbot():
    print("ChatBot: Hello! Which of these do you want to know about!\n 1.WEATHER\n 2. FLOWER")
    
    while True:
        user_input = input("You: ").lower()

        if "weather" in user_input:
            city = input("Which city? ")
            print("Chatbot:", get_weather(city))
        elif user_input in ["hi","hii", "hello", "hey"]:
            print("ChatBot: Hello! Please type 'WEATHER' or 'FLOWER' only.")
        elif user_input in ["bye", "exit", "quit"]:
            print("ChatBot: Goodbye! Stay safe.")
            break
        else:
            print("ChatBot: Incorrect input.")
    
    

# Run the chatbot
chatbot()

'''elif user_input in ["flower"]:
             flower_name = input("Which flower? ")
             print("Chatbot:", get_flower_info(flower_name))'''