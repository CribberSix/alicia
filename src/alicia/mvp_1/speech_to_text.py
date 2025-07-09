import logging
import pyttsx3
import speech_recognition as sr
import os
from openai import OpenAI


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Adjusting for ambient noise... Please wait.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("You can start speaking now.")
        # timeout=5 : Maximum time to wait for speech to start.
        # phrase_time_limit=10 : Maximum time to record after speech starts, even if no silence is detected.
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    print("Processing your speech...")

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; check your internet connection. Error: {e}")


def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Change index to try other voices
    engine.say(text)
    engine.runAndWait()


def ask_chatgpt(question, model="gpt-4o"):
    client = OpenAI(
        # This is the default and can be omitted
        # api_key=os.getenv("OPENAI_API_KEY"),
        api_key="sk-proj-D9Ka3tML39v_7U99sbwQIJnLcEttLIKzFYLmX8zN_v5mSEN7wH0OenDbz0HxixcEYzHeSdeaDUT3BlbkF"
                "J6r1aHiVm26_-0FjX4LCmdN1FZdtpcs5V4F_FD6TdW3H2sBsNqn-AikX1BFoM-EVAWjS5XnFI8A"
    )
    response = client.responses.create(
        model=model,
        instructions="You are an assistant that gives very short and precise answers.",
        input=question,
    )
    print(response)
    print(response.output_text)
    return response.output_text

if __name__ == "__main__":
    text = listen_and_transcribe()
    answer = ask_chatgpt(text)
    speak_text(answer)
