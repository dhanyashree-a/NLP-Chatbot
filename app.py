from flask import Flask, request, jsonify, render_template
import random
import spacy

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Default chatbot name
chatbot_name = "ChatBot"

# Define chatbot responses
responses = {
    "greeting": ["Hi there!", "Hello!", "Hey! 😊"],
    "how_are_you": ["I'm just a bot, but I'm doing great! How about you?", "I'm here and ready to chat!"],
    "name": ["I'm {name}, your friendly chatbot!", "You can call me {name}!", "I'm your virtual assistant!"],
    "rename": ["Alright! You can call me {name} now! 😊"],
    "goodbye": ["Goodbye! Have a great day!", "See you soon!", "Take care! 😊"],
    "see_you": ["See you soon! 😊", "Cya! Take care!", "Looking forward to our next chat!"],
    "presence": ["Yes, I'm here! How can I assist you? 😊"],
    "positive": ["Glad to hear that! 😊", "That's awesome!", "Great! Keep smiling! 😃"],
    "joke": [
        "Why don’t skeletons fight each other? Because they don’t have the guts! 😂",
        "Why did the math book look sad? Because it had too many problems! 🤣",
        "Parallel lines have so much in common. It’s a shame they’ll never meet! 😆"
    ],
    "kindness_response": [
    "Because I like chatting with you! 😊",
    "You're awesome, so you deserve kindness! ❤️",
    "That's just who I am! 😃"
    ],

    "laugh": ["Haha! 😆", "LOL! 😂", "Glad you liked it! 😃"],
    "appreciation": ["Thank you! 😊", "Aww, that means a lot! ❤️", "Glad to hear that!"],
    "you_too": ["You too! 😊", "Thanks! You take care as well!", "Same to you! 😊"],
    "whats_up": ["Not much, just hanging around! What about you? 😊", "Just here to chat! What's up with you?"],
    "compliment": ["Aww, thank you! 😊", "You're too kind! ❤️", "That means a lot! 😃"],
    "sorry": ["No worries! 😊", "It's okay! We all make mistakes!", "All good! Don't worry about it!"],
    "welcome": ["Anytime! 😊", "You're welcome!", "Happy to help!"],
    "chat_topics": [
        "I can chat about jokes, greetings, casual talks, and even fun topics! 😊",
        "I can tell you jokes, chat about your day, or just have a fun talk!"
    ],
    "take_care": ["Take care too! 😊", "Stay safe! See you soon!"],
}

def classify_intent(user_input):
    """Classify the intent of user input using NLP"""
    doc = nlp(user_input.lower().strip())

    if any(token.text in ["hello", "hi", "hii", "hey"] for token in doc):
        return "greeting"
    
    if "name" in user_input:
        return "name"
    
    if any(phrase in user_input for phrase in ["how are you", "how you doing", "how's it going", "how have you been"]):
        return "how_are_you"

    if any(token.text in ["bye", "goodbye", "see you", "take care"] for token in doc):
        return "goodbye"

    if any(phrase in user_input for phrase in ["bot", "are you there", "you there", "bot u there"]):
        return "presence"

    if user_input in ["good", "fine", "great", "awesome", "okay", "not bad"]:
        return "positive"

    if "joke" in user_input or "tell me a joke" in user_input:
        return "joke"

    if user_input in ["haha", "lol", "lmao", "rofl"]:
        return "laugh"

    if user_input in ["wow", "amazing", "awesome", "nice", "cool", "great"]:
        return "appreciation"

    if any(phrase in user_input for phrase in ["you too", "u too", "same to you", "tc too", "take care too"]):
        return "you_too"

    if any(phrase in user_input for phrase in ["what's up", "whats up", "sup"]):
        return "whats_up"

    if any(phrase in user_input for phrase in ["you are great", "you're amazing", "you are awesome", "you're the best"]):
        return "compliment"

    if any(phrase in user_input for phrase in ["can I call you", "can I rename you", "can I give you a new name"]):
        return "rename"

    if any(phrase in user_input for phrase in ["sorry", "my bad", "forgive me"]):
        return "sorry"

    if any(phrase in user_input for phrase in ["see you", "cya", "c ya", "see ya", "catch you later"]):
        return "see_you"

    if any(phrase in user_input for phrase in ["you're welcome", "your welcome", "no problem"]):
        return "welcome"

    if any(phrase in user_input for phrase in ["what can you chat", "what can you talk about", "what do you chat"]):
        return "chat_topics"
    
    if any(phrase in user_input for phrase in ["why are you so good to me", "why are you so nice to me"]):
        return "kindness_response"

    if "take care" in user_input:
        return "take_care"

    return "unknown"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chatbot_name
    user_input = request.json["message"].strip()

    if "call you" in user_input or "rename you" in user_input:
        new_name = user_input.split("call you")[-1].strip().capitalize()
        if new_name:
            chatbot_name = new_name
            return jsonify({"response": f"Alright! You can call me {chatbot_name} now! 😊"})
    
    response = get_response(user_input)
    return jsonify({"response": response.replace("{name}", chatbot_name)})

def get_response(user_input):
    """Get the chatbot response based on classified intent"""
    intent = classify_intent(user_input)
    if intent in responses:
        return random.choice(responses[intent]).replace("{name}", chatbot_name)
    return "I'm not sure how to respond to that. Can you try rephrasing?"

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
