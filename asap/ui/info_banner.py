# info_banner.py
import tkinter as tk

class InfoBanner(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        banner_font = ('Helvetica', 24, 'bold')

        self.money_label = tk.Label(self, text="Money: 0", font=banner_font, bg='white', fg='black', relief="solid", bd=1)
        self.money_label.pack(side=tk.LEFT, padx=10)

        self.health_label = tk.Label(self, text="Health: 0", font=banner_font, bg='white', fg='black', relief="solid", bd=1)
        self.health_label.pack(side=tk.LEFT, padx=10)

        self.turn_label = tk.Label(self, text="Turn: 0", font=banner_font, bg='white', fg='black', relief="solid", bd=1)
        self.turn_label.pack(side=tk.LEFT, padx=10)

    def update(self, money, health, turn):
        self.money_label.config(text=f"Money: {money}")
        self.health_label.config(text=f"Health: {health}")
        self.turn_label.config(text=f"Turn: {turn}")
