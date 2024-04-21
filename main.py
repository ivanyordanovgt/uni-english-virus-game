import random
import time

import winsound
from PIL import Image, ImageTk
from customtkinter import *
from punishments.draw_paint import punish_draw
from punishments.browse_history import punish_browse_history
from punishments.remove_wallpaper import punish_remove_wallpaper
from punishments.fill_up_pc import create_full_1gb_file
from utils import load_images_from_folder, reveal_random_letters, load_toml_file
import winsound

toml_settings = load_toml_file("./settings.toml")
master = CTk()
master.geometry("700x700")
master.configure(fg_color="black")
master.title("Maglish")

difficulty_config = {
    "nightmare": {
        "prepare_message": "Big mistake... Prepare for the worst..."
    }
}

words = load_images_from_folder("./images")
loaded_punishments = {
    "browse_history": punish_browse_history,
    "draw_paint": punish_draw,
    "remove_wallpaper": punish_remove_wallpaper,
    "pop_up": lambda: True,
    "fill_up_pc": create_full_1gb_file
}
class StartPage:
    def __init__(self):
        self.difficulty = None
        self.test = True
        self.start_frame = CTkFrame(master, fg_color="black", width=1000, height=500)
        self.current_opened_frame = None

    def start_game(self, difficituly):
        self.start_frame.place_forget()
        self.PrepareMessage()
        self.difficulty = difficituly
        self.punishments = toml_settings['difficulties'][difficituly.lower()]
    def animate_text(self, label, text, func, index=0):
        if index < len(text):
            label.configure(text=text[:index + 1])
            label.after(1, self.animate_text, label, text, func, index + 1)
        else:
            label.place_forget()
            func()

    def StartPage(self):
        CTkLabel(self.start_frame, text="Play on your own risk", font=("Arial MS", 40), text_color="#cd5c5c").place(
            x=160, y=50)

        for i in range(len(toml_settings["difficulties"]["buttons"])):
            CTkButton(
                self.start_frame, text=toml_settings["difficulties"]["buttons"][i], font=("Arial MS", 30), width=250, fg_color="#690101",
                hover_color="#a30303",
                command=lambda i=i: self.start_game(toml_settings["difficulties"]["buttons"][i])
            ).place(x=210, y=200 + (70 * i))

        self.start_frame.place(x=0, y=0)

    def PrepareMessage(self):
        if self.current_opened_frame:
            self.current_opened_frame.place_forget()

        prepare_label = CTkLabel(master, text="", font=("Arial MS", 30), text_color="#690101")
        prepare_label.place(x=50, y=50)
        text = difficulty_config['nightmare']["prepare_message"]
        self.animate_text(prepare_label, text, self.WordGame)


class Punishment:

    def __init__(self):
        self.last_message_coords = [-100, 100]
        self.last_message_coords_start = [-100, 100]

    def show_error_message(self, x, y):
        error_window = CTkToplevel(master)
        error_window.title("Error Message")
        error_window.geometry(f"300x150+{x}+{y}")
        error_window.attributes("-topmost", True)

        # Error message label
        label = CTkLabel(error_window, text="An error has occurred!", font=("Roboto Medium", 16))
        label.pack(pady=20)

        # Dismiss button to close the error message
        dismiss_button = CTkButton(error_window, text="OK", command=error_window.destroy)
        dismiss_button.pack(pady=10)

        def edit_bg():
            error_window.configure(fg_color="#{:06x}".format(random.randint(0, 0xFFFFFF)))
            error_window.after(500, edit_bg)

        edit_bg()

    def pop_up(self):
        c = 0
        for i in range(300):
            if c == 15:
                x, y = self.last_message_coords_start
                self.last_message_coords_start = [x + 100, y]
                self.last_message_coords = [self.last_message_coords_start[0], 50]
                c = 0
            x, y = self.last_message_coords
            self.show_error_message(x, y)
            self.last_message_coords = [x + 50, y + 50]
            c += 1


class Game(StartPage):
    def __init__(self):
        super().__init__()
        self.c = 0
        self.time_per_word = 20
        self.time_left = self.time_per_word
        self.timer_geometry = (800, 100)
        self.punish = Punishment()
        self.wrong_count = 0
        self.difficulties = toml_settings['difficulties']

    def generate_word(self):
        if len(words) < 1:
            return None, None, None
        word = random.choice(list(words.keys()))
        image = ImageTk.PhotoImage(words[word])
        words.pop(word)

        hint_word = []
        for w in word.split(" "):
            c_word = ""
            c_word += w[0].upper()
            w = w[1::]
            for letter in w:
                c_word += " _ "
            hint_word.append(c_word)
        return word, image, hint_word

    def cancel_timer(self):
        master.after_cancel(self.timer_job)
        if self.difficulties[self.difficulty]["move_timer"]:
            master.after_cancel(self.update_timer_pos_job)
            master.after_cancel(self.update_timer_pos_job)
        self.timer_window.destroy()

    def refresh_word(self):
        self.word_game_frame.destroy()
        self.cancel_timer()
        self.wrong_count = 0
        self.WordGame()

    def submit_word(self, event):
        print(self.word_entry.get())
        if self.word_entry.get() == self.correct_word:
            self.refresh_word()
        else:

            self.wrong_count += 1
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
            self.hint_word = []
            for word in self.correct_word.split(" "):
                if self.wrong_count+1 >= len(word):
                    self.wrong_count = 5
                    break
                self.hint_word.append(reveal_random_letters(word, self.wrong_count + 1))
            for i in range(len(self.hint_word)):
                c_label = self.word_labels[i]
                c_label.configure(text=self.hint_word[i])

            if self.wrong_count >= 4:
                self.cancel_timer()
                self.punishment()
                self.refresh_word()

    def punishment(self):
        self.cancel_timer()
        self.punish.pop_up()

    def update_timer_pos(self):
        self.timer_window.geometry(f"500x100+{random.randint(100, 1600)}+{random.randint(100, 900)}")
        self.timer_window.configure(fg_color="#{:06x}".format(random.randint(0, 0xFFFFFF)))
        speed_type = self.difficulties[self.difficulty]["move_timer_speed"]
        speed_value = toml_settings['move_timer_speed_types'][speed_type]
        self.update_timer_pos_job = master.after(speed_value, self.update_timer_pos)

    def start_timer(self):
        self.timer_label.configure(text=f"You lose in {self.time_left}")
        self.time_left -= 1

        if self.time_left < 1:
            self.punishment()
            self.cancel_timer()
            print("WTF?")
            return

        self.timer_job = master.after(1000, self.start_timer)

    def timer(self):
        self.timer_window = CTkToplevel(master, fg_color="black")
        self.timer_window.attributes("-topmost", True)
        self.timer_label = CTkLabel(
            self.timer_window, text=f"You lose in {self.time_per_word}", text_color="red", font=("Arial", 50)
        )
        self.difficulty = self.difficulty.lower()
        self.time_left = self.difficulties[self.difficulty]["time_per_word"]
        self.timer_label.pack()
        self.start_timer()
        if self.difficulties[self.difficulty]["move_timer"]:
            self.update_timer_pos()

    def WordGame(self):
        self.word_game_frame = CTkFrame(master, width=1000, height=500, fg_color="black")
        word, image, hint_word = self.generate_word()

        if not word:
            for i in range(20):
                CTkLabel(self.word_game_frame, text="YOU WON", font=("Arial MS", 50), text_color="red").pack()
            master.after(3000, self.punish.pop_up)

        self.correct_word = word
        self.hint_word = hint_word
        self.word_game_frame.place(x=0, y=0)
        self.word_image_label = CTkLabel(self.word_game_frame, image=image, text="").pack(padx=150, pady=25)
        self.word_labels = []
        for i in range(len(hint_word)):
            c_label = CTkLabel(self.word_game_frame, text=hint_word[i], font=("Arial ", 30), text_color="red")
            self.word_labels.append(c_label)
            c_label.pack(padx=150)

        self.word_entry = CTkEntry(
            self.word_game_frame, text_color="#cd5c5c", font=("Arial", 20), width=300, fg_color="#262626"
        )
        self.word_entry.bind("<Return>", self.submit_word)
        self.word_entry.pack(pady=20)
        self.timer()
        pass


game = Game()
game.StartPage()
master.mainloop()
