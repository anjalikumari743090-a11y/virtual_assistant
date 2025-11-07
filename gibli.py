import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import tkinter as tk
from tkinter import scrolledtext
import requests
import threading

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def wishMe():
    """Generate a greeting based on the current time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Hello, Good Morning!"
    elif hour < 18:
        greeting = "Hello, Good Afternoon!"
    else:
        greeting = "Hello, Good Evening!"
    
    speak(greeting)
    return greeting

def takeCommand():
    """Capture voice command from the microphone and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        safe_log("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            safe_log(f"User: {statement}")
            return statement.lower()
        except Exception:
            safe_log("Sorry, I didn't understand. Please try again.")
            speak("Sorry, I didn't understand. Please try again.")
            return "none"

def execute_command(statement):
    """Process user command and perform actions accordingly."""
    if statement == "none":
        return

    if any(exit_command in statement for exit_command in ["bye", "stop", "exit", "quit"]):
        safe_log("Assistant: Shutting down...")
        speak("Your personal assistant Anjali is shutting down. Goodbye!")
        root.quit()
        return

    if 'wikipedia' in statement:
        query = statement.replace("wikipedia", "").strip()
        if query:
            speak('Searching Wikipedia...')
            try:
                results = wikipedia.summary(query, sentences=2)
                safe_log(f"Wikipedia: {results}")
                speak(results)
            except wikipedia.exceptions.DisambiguationError:
                safe_log("Assistant: Multiple results found, please be more specific.")
                speak("Multiple results found, please be more specific.")
            except wikipedia.exceptions.PageError:
                safe_log("Assistant: No page found on Wikipedia.")
                speak("No page found on Wikipedia.")
        else:
            safe_log("Assistant: Please specify a topic for Wikipedia search.")
            speak("Please specify a topic.")

    elif 'open college website' in statement:
        webbrowser.open("https://www.cuchd.in/")
        safe_log("Assistant: Opening Chandigarh University website.")
        speak("Opening Chandigarh University website.")


    elif 'open youtube' in statement:
        webbrowser.open("https://www.youtube.com")
        safe_log("Assistant: Opening YouTube.")
        speak("Opening YouTube.")

    elif 'time' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        safe_log(f"Assistant: The time is {strTime}")
        speak(f"The time is {strTime}")

    elif "who made you" in statement:
        safe_log("Assistant: I was built by Anjali.")
        speak("I was built by Anjali.")

    elif "weather" in statement:
        speak("What's the city name?")
        safe_log("Assistant: Asking for city name...")
        city_name = takeCommand()

        if city_name == "none":
            return

        api_key = "8ef61edcf1c576d65d836254e11ea420"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"

        try:
            response = requests.get(complete_url, timeout=10)
            x = response.json()

            if str(x.get("cod")) == "200":  # ✅ Corrected check
                y = x["main"]
                temperature = y["temp"]
                humidity = y["humidity"]
                weather_description = x["weather"][0]["description"]

                weather_info = f"Temperature: {temperature}°C\nHumidity: {humidity}%\nDescription: {weather_description}"
                safe_log(f"Weather in {city_name}: {weather_info}")
                speak(f"The current temperature in {city_name} is {temperature} degrees Celsius with {weather_description} and {humidity} percent humidity.")
            elif str(x.get("cod")) == "404":
                safe_log(f"Assistant: City '{city_name}' not found.")
                speak(f"City {city_name} not found. Please try again.")
            else:
                safe_log(f"Assistant: Unable to fetch weather. API error: {x.get('message', 'Unknown error')}")
                speak("Sorry, I couldn't fetch the weather information right now.")
        except requests.exceptions.RequestException:
            safe_log("Assistant: Network error while fetching weather.")
            speak("Sorry, I couldn't connect to the weather service.")

    elif 'news' in statement:
        webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
        safe_log("Assistant: Here are some latest news headlines.")
        speak("Here are some headlines from the Times of India. Happy reading!")

    elif 'search' in statement:
        query = statement.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            safe_log(f"Assistant: Searching Google for {query}.")
            speak(f"Searching for {query} on Google.")
        else:
            safe_log("Assistant: Please specify what to search.")
            speak("Please specify what to search.")

def log_message(message):
    """Directly update the chat box."""
    chat_box.insert(tk.END, message + '\n')
    chat_box.yview(tk.END)

def safe_log(message):
    """Safely update the chat box using Tkinter's main thread."""
    chat_box.after(0, lambda: log_message(message))

# Background task functions
def voice_task():
    statement = takeCommand()
    execute_command(statement)

def text_task():
    statement = user_input.get()
    if statement:
        safe_log(f"User: {statement}")
        execute_command(statement)
        user_input.delete(0, tk.END)

def on_voice_input():
    threading.Thread(target=voice_task).start()

def on_text_input():
    threading.Thread(target=text_task).start()

# Initialize GUI
root = tk.Tk()
root.title("AI Assistant - Anjali")
root.geometry("500x500")
root.configure(bg='lightgray')

# Chat history display
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
chat_box.pack(pady=10)
chat_box.insert(tk.END, "Anjali: " + wishMe() + "\n")

# User input field
user_input = tk.Entry(root, width=50)
user_input.pack(pady=5)

# Buttons
text_button = tk.Button(root, text="Send", command=on_text_input)
text_button.pack(pady=5)

voice_button = tk.Button(root, text="🎤 Speak", command=on_voice_input)
voice_button.pack(pady=5)


# Run the GUI
root.mainloop()
