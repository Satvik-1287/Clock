import tkinter as tk
from tkinter import messagebox
import time
import requests

class DigitalClock(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Digital Clock")
        self.geometry("700x500")
        self.configure(bg="black")

        self.time_label = tk.Label(self, font=("cascadia code", 70), fg="white", bg="black")
        self.time_label.pack(expand=True, fill='both')

        self.date_label = tk.Label(self, font=("cascadia code", 24), fg="white", bg="black")
        self.date_label.pack()

        self.weather_label = tk.Label(self, font=("cascadia code", 20), fg="white", bg="black")
        self.weather_label.pack(pady=10)

        self.alarm_time = None

        self.create_controls()

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%A, %B %d, %Y")

        self.time_label.config(text=current_time, font=("cascadia code", 70), bg="black")
        self.date_label.config(text=current_date)

        if self.alarm_time and current_time == self.alarm_time:
            self.trigger_alarm()

        self.after(1000, self.update_clock)

    def create_controls(self):
        control_frame = tk.Frame(self, bg="black")
        control_frame.pack(fill='x')

        button_style = {
            "font": ("cascadia code", 12, "bold"),
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#555555",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "highlightthickness": 0,
            "padx": 10,
            "pady": 5,
        }

        toggle_fullscreen_button = tk.Button(control_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen, **button_style)
        toggle_fullscreen_button.pack(side='right', padx=5, pady=5)

        set_alarm_button = tk.Button(control_frame, text="Set Alarm", command=self.set_alarm, **button_style)
        set_alarm_button.pack(side='left', padx=5, pady=5)

        weather_button = tk.Button(control_frame, text="Show Weather", command=self.show_weather, **button_style)
        weather_button.pack(side='left', padx=5, pady=5)

    def toggle_fullscreen(self):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def set_alarm(self):
        self.alarm_window = tk.Toplevel(self)
        self.alarm_window.title("Set Alarm")
        self.alarm_window.geometry("300x150")
        self.alarm_window.configure(bg="black")

        label = tk.Label(self.alarm_window, text="Enter time (HH:MM:SS):", font=("cascadia code", 14), fg="white", bg="black")
        label.pack(pady=10)

        self.alarm_entry = tk.Entry(self.alarm_window, font=("cascadia code", 14))
        self.alarm_entry.pack(pady=5)

        button_style = {
            "font": ("cascadia code", 12, "bold"),
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#555555",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "highlightthickness": 0,
            "padx": 10,
            "pady": 5,
        }

        set_button = tk.Button(self.alarm_window, text="Set Alarm", command=self.confirm_alarm, **button_style)
        set_button.pack(pady=10)

    def confirm_alarm(self):
        alarm_time = self.alarm_entry.get()
        if alarm_time:
            self.alarm_time = alarm_time
            messagebox.showinfo("Alarm Set", f"Alarm set for {self.alarm_time}")
        self.alarm_window.destroy()

    def trigger_alarm(self):
        self.alarm_time = None
        messagebox.showinfo("Alarm", "Time to wake up!")

    def show_weather(self):
        self.weather_window = tk.Toplevel(self)
        self.weather_window.title("Show Weather")
        self.weather_window.geometry("300x150")
        self.weather_window.configure(bg="black")

        label = tk.Label(self.weather_window, text="Enter city:", font=("cascadia code", 14), fg="white", bg="black")
        label.pack(pady=10)

        self.weather_entry = tk.Entry(self.weather_window, font=("cascadia code", 14))
        self.weather_entry.pack(pady=5)

        button_style = {
            "font": ("cascadia code", 12, "bold"),
            "bg": "#333333",
            "fg": "white",
            "activebackground": "#555555",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "highlightthickness": 0,
            "padx": 10,
            "pady": 5,
        }

        get_button = tk.Button(self.weather_window, text="Get Weather", command=self.display_weather, **button_style)
        get_button.pack(pady=10)

    def display_weather(self):
        city = self.weather_entry.get()
        if city:
            api_key = "c4f817c5f697a7db66b52c6712bc375b"  # Replace with your OpenWeatherMap API key
            weather_data = self.get_weather_data(city, api_key)
            if weather_data:
                self.weather_label.config(text=weather_data)
        self.weather_window.destroy()

    def get_weather_data(self, city, api_key):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather = response.json()
            temp = weather['main']['temp']
            description = weather['weather'][0]['description']
            return f"{city.title()}: {temp}°C, {description}"
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Failed to retrieve weather data.")
            return None

if __name__ == "__main__":
    app = DigitalClock()
    app.mainloop()
