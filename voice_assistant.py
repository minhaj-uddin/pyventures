import webbrowser
import pyttsx3
import speech_recognition as sr
import wikipedia

# init pyttsx
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say('Happy Fathers Day!')
    engine.runAndWait()

engine.setProperty('voice', voices[1].id)  # 1:female, 0:male voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-pk')
        print("User said: " + query + "\n")
    except Exception as e:
        print(e)
        speak("I didnt understand")
        return "None"
    return query


if __name__ == '__main__':

    speak("Amigo assistance activated ")
    speak("How can i help you?")
    while True:
        query = take_command().lower()
        if 'wikipedia' in query:
            speak("Searching Wikipedia ...")
            query = query.replace("wikipedia", '')
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(results)
        elif 'who are you' in query:
            speak("I am amigo voice assistant")
        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")
        elif 'open github' in query:
            speak("opening github")
            webbrowser.open("github.com")
        elif 'open stackoverflow' in query:
            speak("opening stackoverflow")
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query:
            speak("opening music")
            webbrowser.open("spotify.com")
        elif 'file explorer' in query:
            speak("opening local disk C")
            webbrowser.open("C://")
        elif 'goodbye' in query:
            exit(0)
