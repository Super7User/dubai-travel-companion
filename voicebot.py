import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Speech service is down.")
            return None

def get_ai_response(prompt):
    # Initialize the OpenAI client with your API key
    client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )
    # Create a chat completion
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a travel guide. Provide responses in 200 characters or less."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50  
    )

    # Extract and return the assistant's reply
    return response.choices[0].message.content.strip()

def main():
    speak("Hello! I'm your Dubai travel guide. How can I assist you today?")
    exit_phrases = ['exit', 'thank you', 'thanks']
    while True:
        user_input = listen()
        if user_input:
            # Convert user input to lowercase for case-insensitive comparison
            user_input_lower = user_input.lower()
            # Check if any exit phrase is in the user input
            if any(phrase in user_input_lower for phrase in exit_phrases):
                speak("Goodbye! Have a great time in Dubai.")
                break
            response = get_ai_response(user_input)
            speak(response)


if __name__ == "__main__":
    main()
