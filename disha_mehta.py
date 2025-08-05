from time import strftime
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyjokes
import datetime

# Initialize recognizer and engine once (faster performance)
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Faster speech speed

def listen():
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Reduced calibration time
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)  # Timeout after 3s, max 5s speech
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("[No speech detected]")
            return ""
        except sr.UnknownValueError:
            print("[Could not understand audio]")
            return ""
        except sr.RequestError:
            print("[API unavailable]")
            return ""

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def handle_command(command):
    if not command:
        return True
    
    # Faster response checks (using dictionary)
    responses = {
        "time": f"It's {strftime('%I:%M %p')}. Don't forget to take breaks!",
        "date": f"Today is {strftime('%A, %B %d')}. Plan your day well!",
        "joke": pyjokes.get_joke(),
        "exit": "Goodbye! Jai Shree Krishna!"
    }

    websites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "spotify": "https://open.spotify.com"
    }

    # Check for matches
    for key in responses:
        if key in command:
            speak(responses[key])
            return key != "exit"  # Continue unless "exit"

    for site in websites:
        if site in command:
            speak(f"Opening {site}...")
            webbrowser.open(websites[site])
            return True

    speak("I didn't catch that. Try saying 'time', 'joke', or 'open YouTube'.")
    return True

def main():
    speak("Hello! How can I help you today?")
    while True:
        command = listen()
        if not handle_command(command):
            break

if __name__ == "__main__":
    main()