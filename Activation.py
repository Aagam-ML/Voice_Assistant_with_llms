import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv
import speech_recognition as sr
load_dotenv()
# Initialize Porcupine with your AccessKey and wake words
access_key = os.getenv("pvporcupine_APi_KEY")
keywords = ["jarvis", "computer"]
handle = pvporcupine.create(access_key=access_key, keywords=keywords)

# Set up audio stream from microphone
pa = pyaudio.PyAudio()
def toggle_stream_on():
    """Open and return the audio stream."""

    print("entered")
    audio_stream = pa.open(rate=handle.sample_rate, channels=1, format=pyaudio.paInt16,
                           input=True, frames_per_buffer=handle.frame_length)
    return pa, audio_stream  # R

def toggle_stream_off(pa, audio_stream):
    """Close the audio stream."""
    audio_stream.stop_stream()
    audio_stream.close()


def process_audio_from_active_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text = ""
        print("Microphone is active. Speak now!")
        while True:  # Infinite loop to keep the microphone on
            try:
                print("Listening...")

                audio = recognizer.listen(source)  # Continuously listen
                print("Recognizing...")
                new_text = recognizer.recognize_google(audio)
                text =text + " "+ new_text  # Convert speech to text
                print(f"You said: {text}")
                if new_text == "stop":
                    break
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print(f"Speech service error: {e}")
        wake_up()

def wake_up():
    pa, audio_stream = toggle_stream_on()
    while True:
        # Read audio frame from microphone


        pcm = audio_stream.read(handle.frame_length)
        pcm = struct.unpack_from("h" * handle.frame_length, pcm)

        # Process audio frame with Porcupine
        keyword_index = handle.process(pcm)

        if keyword_index >= 0:
            print("detected")
            toggle_stream_off(pa,audio_stream)
            process_audio_from_active_mic()

wake_up()
