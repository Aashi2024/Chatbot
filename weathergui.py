import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
from api import get_weather
from wiki_chatbot import fetch_summary
import pyrebase

# ---------------- Firebase Configuration ----------------
config = {
    "apiKey": "AIzaSyDXobsjqjHPq_QbYSlIb7q7H-ap09Ru9AQ",
    "authDomain": "first-dbproject.firebaseapp.com",
    "databaseURL": "https://first-dbproject-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "first-dbproject.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# ---------------- Chat Bubble Class ----------------
class ChatBubble(tk.Frame):
    def __init__(self, parent, message, is_user=False, **kwargs):
        super().__init__(parent, **kwargs)

        bubble_color = "#DCF8C6" if is_user else "#FFFFFF"
        align = "e" if is_user else "w"
        text_color = "#000000"

        bubble = tk.Label(
            self,
            text=message,
            bg=bubble_color,
            fg=text_color,
            font=("Arial", 12),
            wraplength=400,
            justify=tk.LEFT,
            padx=10,
            pady=6,
            bd=0,
            relief=tk.FLAT
        )

        bubble.pack(anchor=align, padx=10, pady=2)

# ---------------- Main Chatbot Class ----------------
class WeatherChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather ChatBot")

        self.weather_mode = False
        self.wiki_mode = False

        self.chat_frame = Frame(root, bg="#f0f0f0")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = Canvas(self.chat_frame, bg="#f0f0f0")
        self.scrollbar = Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.message_frame = Frame(self.canvas, bg="#f0f0f0")

        self.message_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.input_frame = Frame(root)
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.user_input = tk.Entry(self.input_frame, font=("Arial", 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
        self.user_input.bind("<Return>", self.process_input)

        self.send_button = tk.Button(self.input_frame, text="SEND", command=self.process_input)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

        self.button_panel = Frame(root, bg="#e0e0e0")
        self.button_panel.pack(fill=tk.X)

        self.create_main_buttons()

        self.bot_says("Welcome!")
        self.bot_says("Choose an option:")

    def create_main_buttons(self):
        self.clear_buttons()

        weather_btn = tk.Button(self.button_panel, text="WEATHER", width=12, command=self.enter_weather_mode)
        weather_btn.pack(side=tk.LEFT, padx=10, pady=5)

        wiki_btn = tk.Button(self.button_panel, text="WIKIPEDIA", width=12, command=self.enter_wiki_mode)
        wiki_btn.pack(side=tk.LEFT, padx=10, pady=5)

        exit_btn = tk.Button(self.button_panel, text="EXIT", width=12, command=self.exit_chat)
        exit_btn.pack(side=tk.LEFT, padx=10, pady=5)

    def create_back_button(self):
        self.clear_buttons()

        back_btn = tk.Button(self.button_panel, text="BACK", width=12, command=self.exit_mode)
        back_btn.pack(side=tk.LEFT, padx=10, pady=5)

        exit_btn = tk.Button(self.button_panel, text="EXIT", width=12, command=self.exit_chat)
        exit_btn.pack(side=tk.LEFT, padx=10, pady=5)

    def clear_buttons(self):
        for widget in self.button_panel.winfo_children():
            widget.destroy()

    def bot_says(self, message):
        bubble = ChatBubble(self.message_frame, message, is_user=False, bg="#f0f0f0")
        bubble.pack(anchor="w", fill=tk.X, padx=10, pady=2)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def user_says(self, message):
        bubble = ChatBubble(self.message_frame, message, is_user=True, bg="#f0f0f0")
        bubble.pack(anchor="e", fill=tk.X, padx=10, pady=2)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def enter_weather_mode(self):
        self.weather_mode = True
        self.wiki_mode = False
        self.bot_says("Please enter the city for weather info:")
        self.create_back_button()

    def enter_wiki_mode(self):
        self.wiki_mode = True
        self.weather_mode = False
        self.bot_says("What topic would you like to search on Wikipedia?")
        self.create_back_button()

    def exit_mode(self):
        self.weather_mode = False
        self.wiki_mode = False
        self.bot_says("You are back to the main menu. Choose an option:")
        self.create_main_buttons()

    def exit_chat(self):
        self.bot_says("Goodbye! Stay safe.")
        self.root.after(1500, self.root.destroy)

    # Save Wikipedia topic and answer to local file
    def save_to_file(self, topic, summary):
        try:
            with open("__pycache__/example.txt", "a", encoding="utf-8") as file:
                file.write(f"Q: {topic}\n")
                file.write(f"A: {summary}\n")
                file.write("-" * 50 + "\n")
        except Exception as e:
            self.bot_says(f"Error saving to file: {e}")

    # Save weather data to Firebase
    def save_weather_to_firebase(self, city, weather_info):
        try:
            data = {
                "city": city,
                "weather": weather_info
            }
            db.child("weather_queries").push(data)
        except Exception as e:
            self.bot_says(f"Error saving to database: {e}")

    def process_input(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.user_says(user_text)
        self.user_input.delete(0, tk.END)

        if self.weather_mode:
            city = user_text
            try:
                weather_info = get_weather(city)
                self.bot_says(weather_info)
                self.save_weather_to_firebase(city, weather_info)
            except Exception:
                self.bot_says(f"Sorry, I couldn't get the weather for {city}.")
            return

        if self.wiki_mode:
            topic = user_text
            summary = fetch_summary(topic)
            self.bot_says(summary)
            self.save_to_file(topic, summary)
            return

        self.bot_says("Please choose one of the options using the buttons below.")

# ---------------- Run the App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = WeatherChatbotGUI(root)
    root.mainloop()
