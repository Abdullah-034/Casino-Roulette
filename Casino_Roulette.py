import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time


class User:
    def __init__(self, username):
        self.username = username
        self.data_file = f"{username}_data.json"
        self.history_file = f"{username}_history.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.currency = json.load(file).get("currency", 2000)
        else:
            self.currency = 2000
            self.save_data()

        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                self.history = json.load(file)
        else:
            self.history = []
            self.save_history()

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump({"currency": self.currency}, file)

    def save_history(self):
        with open(self.history_file, "w") as file:
            json.dump(self.history, file)


class LoginScreen:
    def __init__(self, app):
        self.app = app
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("400x250")
        self.window.configure(bg="#121212")

        tk.Label(self.window, text="Username", bg="#121212", fg="white").pack(pady=5)
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password", bg="#121212", fg="white").pack(pady=5)
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.window, text="Login", command=self.login).pack(pady=20)

        self.window.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        credentials = {"Noman": "1111", "Abdullah": "2222"}

        if username in credentials and credentials[username] == password:
            self.window.destroy()
            self.app.start_game(User(username))
        else:
            messagebox.showerror("Login Error", "Invalid username or password!")


class RouletteApp:
    def __init__(self):
        self.user = None
        self.window = None
        LoginScreen(self)

    def start_game(self, user):
        self.user = user
        if self.window:
            self.window.destroy()

        self.window = tk.Tk()
        self.window.title("Roulette Game")
        self.window.geometry("700x800")
        self.window.configure(bg="#121212")

        self.numbers = self.generate_numbers()
        self.bet = 0
        self.choice = None

        self.create_widgets()
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.window.mainloop()

    def generate_numbers(self):
        return [("green", 0)] + [("red", i) for i in range(1, 19)] + [("black", i) for i in range(19, 37)]

    def create_widgets(self):
        tk.Label(
            self.window, text="Roulette", font=("Brush Script", 28, "bold"), fg="#FFD700", bg="#121212"
        ).pack(fill="x", pady=5)

        self.currency_label = tk.Label(
            self.window,
            text=f"Currency: ${self.user.currency if self.user else 'N/A'}",
            font=("Brush Script", 16),
            bg="#121212",
            fg="white",
        )
        self.currency_label.pack(pady=10)

        bet_frame = tk.Frame(self.window, bg="#121212")
        bet_frame.pack(pady=10)

        tk.Label(bet_frame, text="Enter Bet Amount ($10-$500):", font=("Brush Script", 14), bg="#121212", fg="white").grid(row=0, column=0, padx=10)
        self.bet_entry = tk.Entry(bet_frame, font=("Brush Script", 14), width=10)
        self.bet_entry.grid(row=0, column=1)

        tk.Label(bet_frame, text="Enter Bet Choice (Black, Red, Green / 1-18 / 19-36):", font=("Brush Script", 14), bg="#121212", fg="white").grid(row=1, column=0, padx=10)
        self.choice_entry = tk.Entry(bet_frame, font=("Brush Script", 14), width=15)
        self.choice_entry.grid(row=1, column=1)

        btn_frame = tk.Frame(self.window, bg="#121212")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="SPIN",
            font=("Brush Script", 16),
            bg="#FF4500",
            fg="white",
            command=self.spin_wheel,
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            btn_frame,
            text="History",
            font=("Brush Script", 16),
            bg="#FFA500",
            fg="white",
            command=self.show_history,
        ).grid(row=0, column=1, padx=20)

        tk.Button(
            btn_frame,
            text="Quit",
            font=("Brush Script", 16),
            bg="#FFD700",
            fg="black",
            command=self.on_exit,
        ).grid(row=0, column=2, padx=20)

        self.wheel_canvas = tk.Canvas(self.window, width=350, height=350, bg="#121212", highlightthickness=0)
        self.wheel_canvas.pack(pady=20)

        self.message_label = tk.Label(self.window, text="", font=("Brush Script", 16), bg="#121212", fg="white")
        self.message_label.pack(pady=10)

    def spin_wheel(self):
        try:
            bet_amount = int(self.bet_entry.get())
            bet_choice = self.choice_entry.get().strip().lower()

            if bet_amount < 10 or bet_amount > 500 or self.user.currency < bet_amount:
                self.message_label.config(text="Invalid bet!", fg="red")
                return

            self.bet = bet_amount
            self.choice = bet_choice

            spin_time = 3
            start_time = time.time()
            while time.time() - start_time < spin_time:
                temp_result = random.choice(self.numbers)
                temp_color, temp_number = temp_result
                self.display_result(temp_number, temp_color, animating=True)
                self.window.update()
                time.sleep(0.05)

            result = random.choice(self.numbers)
            color, number = result
            self.display_result(number, color, animating=False)

        except ValueError:
            self.message_label.config(text="Enter a valid bet!", fg="red")

    def display_result(self, number, color, animating):
        self.wheel_canvas.delete("all")
        self.wheel_canvas.create_oval(25, 25, 325, 325, fill=color, outline="white")
        self.wheel_canvas.create_text(175, 175, text=str(number), font=("Brush Script", 48), fill="white")

        if not animating:
            win = False
            if self.choice in [color, "1-18", "19-36"]:
                if color == self.choice or (self.choice == "1-18" and 1 <= number <= 18) or (self.choice == "19-36" and 19 <= number <= 36):
                    win = True

            if win:
                self.user.currency += self.bet * 2
                self.message_label.config(text=f"WIN! Result: {number} ({color.upper()})", fg="green")
            else:
                self.user.currency -= self.bet
                self.message_label.config(text=f"LOSS! Result: {number} ({color.upper()})", fg="red")

            self.user.history.append({"bet": self.bet, "choice": self.choice, "result": number, "color": color, "win": win})
            self.user.save_history()

            if self.user.currency <= 0:
                self.user.currency = 2000
                messagebox.showinfo("Bankruptcy", "Your currency is reset to $2000!")

            self.currency_label.config(text=f"Currency: ${self.user.currency}")
            self.user.save_data()

    def show_history(self):
        history_window = tk.Toplevel(self.window)
        history_window.title("History")
        history_window.geometry("400x300")
        history_window.configure(bg="#121212")

        tk.Label(history_window, text=f"History for {self.user.username}", font=("Brush Script", 16), bg="#121212", fg="white").pack(pady=10)

        if not self.user.history:
            tk.Label(history_window, text="No history found!", font=("Brush Script", 14), bg="#121212", fg="white").pack()
        else:
            for entry in self.user.history:
                result = f"{entry['result']} ({entry['color'].upper()})"
                outcome = "WIN" if entry["win"] else "LOSS"
                tk.Label(
                    history_window,
                    text=f"Bet: ${entry['bet']} | Choice: {entry['choice']} | Result: {result} | {outcome}",
                    font=("Brush Script", 14),
                    bg="#121212",
                    fg="white",
                ).pack(anchor="w", padx=10)

    def on_exit(self):
        if self.user:
            self.user.save_data()
        self.window.destroy()


if __name__ == "__main__":
    app = RouletteApp()
