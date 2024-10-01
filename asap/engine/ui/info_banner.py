# info_banner.py
import tkinter as tk


class InfoBanner(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.money_label = tk.Label(self, text="Money: 0", font=('Helvetica', 18), bg="white")
        self.money_label.grid(row=0, column=0, padx=20)

        self.health_label = tk.Label(self, text="Health: 0", font=('Helvetica', 18), bg="white")
        self.health_label.grid(row=0, column=1, padx=20)

        self.turn_label = tk.Label(self, text="Turn: 0", font=('Helvetica', 18), bg="white")
        self.turn_label.grid(row=0, column=2, padx=20)

    def update(self, money, health, turn):
        self.money_label.config(text=f"Money: {money}")
        self.health_label.config(text=f"Health: {health}")
        self.turn_label.config(text=f"Turn: {turn}")
