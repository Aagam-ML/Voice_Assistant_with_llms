import pvporcupine
import pyaudio
import struct
import streamlit as st
import os
from dotenv import load_dotenv
import speech_recognition as sr
import streamlit as st

load_dotenv()
# Initialize Porcupine with your AccessKey and wake words
access_key = os.getenv("pvporcupine_APi_KEY")
keywords = ["jarvis", "computer"]
handle = pvporcupine.create(access_key=access_key, keywords=keywords)


class VoiceAssistant():
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.Mic = False
        self.audio_stream = self.pa.open(rate=handle.sample_rate, channels=1, format=pyaudio.paInt16,
                                   input=True, frames_per_buffer=handle.frame_length)

    def audio_stream_on(self):

        return

    def audio_stream_off(self):
        self.audio_stream.stop_stream()
        self.pa.close(self.audio_stream)
        print("Everything is closed")

    def process_audio_from_active_mic(self):

        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            text = ""
            print("Microphone is active. Speak now!")
            while True:  # Infinite loop to keep the microphone on
                try:
                    audio = recognizer.listen(source)  # Continuously listen
                    print("Recognizing...")
                    new_text = recognizer.recognize_google(audio)
                    text = text + " " + new_text  # Convert speech to text
                    print(f"You said: {text}")
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand that.")
                except sr.RequestError as e:
                    print(f"Speech service error: {e}")

    def wake_up(self):
        print(self.Mic)

        try:
            while self.Mic == True:
                print("Voice Assistant is Activated say the wake word")

                pcm = self.audio_stream.read(handle.frame_length)
                pcm = struct.unpack_from("h" * handle.frame_length, pcm)

                # Process audio frame with Porcupine
                keyword_index = handle.process(pcm)

                if keyword_index >= 0:
                    print("detected")
                    self.process_audio_from_active_mic()
                    return
                else:
                    print(self.Mic)
        except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
                print(f"Speech service error: {e}")
        if self.Mic==False:
            print("Turning_off_streaming")
            self.audio_stream_off()


    def start(self):
        self.Mic=True
        self.audio_stream_on()
        self.wake_up()

    def stop(self):
        self.Mic=False
        self.audio_stream_off()




