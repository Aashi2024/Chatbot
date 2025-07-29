import tkinter as tk
from weathergui import WeatherChatbotGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherChatbotGUI(root)
    root.mainloop()