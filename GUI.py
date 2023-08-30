import os
import asyncio
import edge_tts
import tkinter as tk
from tkinter import filedialog, messagebox

AVAILABLE_VOICES = ["en-US-RogerNeural", "en-US-AriaNeural"]  # Add more voices if needed

class TextToAudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Audio Converter")

        self.voice_var = tk.StringVar()
        self.voice_var.set(AVAILABLE_VOICES[0])  # Set default voice

        self.conversion_status_var = tk.StringVar()
        self.conversion_status_var.set("")  # Initialize with an empty message

        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("400x300")  # Set the initial size of the main window

        frame = tk.Frame(self.root, width=400, height=300)  # Set the size of the frame
        frame.pack()

        tk.Label(frame, text="Select Voice:").pack()
        voice_dropdown = tk.OptionMenu(frame, self.voice_var, *AVAILABLE_VOICES)
        voice_dropdown.pack()

        tk.Button(frame, text="Select Text File and Convert", command=self.convert_text_to_audio).pack()

        self.conversion_status_label = tk.Label(frame, textvariable=self.conversion_status_var)
        self.conversion_status_label.pack()

    def set_conversion_status(self, status):
        self.conversion_status_var.set(status)
        if status == "File converted successfully!":
            self.root.after(2000, self.clear_conversion_status)

    def clear_conversion_status(self):
        self.conversion_status_var.set("")

    def convert_text_to_audio(self):
        voice = self.voice_var.get()

        input_filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        if input_filepath:
            output_filename = os.path.splitext(os.path.basename(input_filepath))[0] + ".mp3"
            output_filepath = os.path.join(os.path.dirname(input_filepath), output_filename)

            with open(input_filepath, "r") as file:
                text = file.read().strip()

            self.convert_text_to_audio_async(text, voice, output_filepath)

    async def save_audio(self, communicate, output_filename):
        await communicate.save(output_filename)

    def convert_text_to_audio_async(self, text, voice, output_filename):
        communicate = edge_tts.Communicate(text, voice)
        try:
            asyncio.run(self.save_audio(communicate, output_filename))
            self.set_conversion_status("File converted successfully!")
        except Exception as e:
            self.set_conversion_status("An error occurred during conversion.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToAudioConverterApp(root)
    root.mainloop()
