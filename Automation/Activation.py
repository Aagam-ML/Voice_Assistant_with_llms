import pvporcupine
import pyaudio
import struct
import tkinter as tk
from tkinter import ttk
import ast
from New_Activation import add_reminder
from langchain_community.llms import Cohere
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import speech_recognition as sr


load_dotenv()
access_key = os.getenv("pvporcupine_APi_KEY")
keywords = ["jarvis", "computer"]
handle = pvporcupine.create(access_key=access_key, keywords=keywords)
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")
## Langsmith
os.environ["LANGCHAIN_TRACING_V2"]="True"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="Chatbot"

# Set up audio stream from microphone
task=[]
class Voice_Assistant():
    def __init__(self,task):
        self.pa = pyaudio.PyAudio()
        self.Mic = False
        self.task = task

    def clear_memory(self):
        self.task = []
        print(self.task)
    def toggle_stream_on(self):
        audio_stream = self.pa.open(rate=handle.sample_rate, channels=1, format=pyaudio.paInt16,
                               input=True, frames_per_buffer=handle.frame_length)
        return self.pa, audio_stream  # R

    def toggle_stream_off(self, pa, audio_stream):
        print("triggered2")
        audio_stream.stop_stream()
        pa.close(audio_stream)

    def process_audio_from_active_mic(self):
        global Mic
        if Mic:
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
                        text = text + " , " + new_text  # Convert speech to text
                        print(f"You said: {text}")
                        if new_text == "stop":
                            self.MyLLM(text)
                        elif new_text=="done":
                            for taski in self.task:
                                add_reminder("Personal",taski)
                            break
                        elif new_text == "clean":
                            self.clear_memory()

                    except sr.UnknownValueError:
                        print("Sorry, I couldn't understand that.")
                    except sr.RequestError as e:
                        print(f"Speech service error: {e}")
        self.wake_up()

    def wake_up(self):
            pa, audio_stream = self.toggle_stream_on()
            if Mic:

                while True:
                    # Read audio frame from microphone

                    pcm = audio_stream.read(handle.frame_length)
                    pcm = struct.unpack_from("h" * handle.frame_length, pcm)

                    # Process audio frame with Porcupine
                    keyword_index = handle.process(pcm)

                    if keyword_index >= 0:
                        print("detected")
                        self.toggle_stream_off(pa, audio_stream)
                        self. process_audio_from_active_mic()
            else:
                self.toggle_stream_off(pa, audio_stream)
                print("triggered")

    def start(self):
        global Mic
        Mic = True
        self.toggle_stream_on()
        self.wake_up()

    def stop(self):
        global Mic
        Mic = False
        self.wake_up()
        self.process_audio_from_active_mic()

    def generate(self):


        root = tk.Tk()
        root.title("Array Display in Table")

        # Create the Treeview widget (table)
        tree = ttk.Treeview(root, columns=("Value"), show="headings")

        # Define the column heading
        tree.heading("Value", text="Array Values")

        # Insert each element from the array into the table
        for item in self.task:
            tree.insert("", "end", values=(item,))

        # Pack the Treeview widget
        tree.pack(padx=20, pady=20)

        # Run the application
        root.mainloop()

    def MyLLM(self,text):
        # Initialize Cohere LLM

        LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
        LANGCHAIN_PROJECT = "Chatbot"


        ##Prompt Template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "just afind the task and written python array no extra information"),
                ("user", "Question:{question}")
            ]
        )


        llm = ChatCohere()
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        new_tasks =  chain.invoke({"question": text + "find the task and give and return it in the form of python array ex. ['a', 'b'], if there more than one question in it append the items do not make dictioniary"+ str(self.task) +" these are previous task and you update in them"})
        print(new_tasks)
        new_tasks = ast.literal_eval(new_tasks)
        self.task = new_tasks



Alexa = Voice_Assistant(task)
Alexa.start()


