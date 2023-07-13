from tkinter import *
import random
import math
from tkinter import messagebox

PROMPTS = [
    "When her father was drunk, he'd say 'I used to have a brother, you know,' and get a faraway look in his eyes ",
    "He kept absolutely still as the footsteps got louder ",
    "The girl shouldn't have been sacked but if he said anything ",
    "After five years, he just happened to be walking down her street? ",
    "It started with a chance meeting on a film-set ",
    "She turned and nearly fell over the bonnet of his car, which was crawling quietly along the street. ",
    "Reluctantly, he handed over the key ",
    "She went to the toilet and on her way back, opened the wrong door ",
    "He had enjoyed ten years of being totally irresponsible "]

INSTRUCTIONS = "Select how many minutes you would like to write for.\n" \
               "You can choose to write based on a random prompt generated or without a prompt.\n" \
               "If you don't write anything for 5 seconds, all the text you've typed will be deleted."

OVERALL_TIME_LIST = [3, 5, 10, 20, 30, 60]

TITLE_FONT = ("Times New Roman", 18, "bold")
BUTTON_FONT = ("Times New Roman", 14, "bold")
FONT = ("Times New Roman", 14, "normal")


class Screen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Disappearing Text Writing App")
        self.config(padx=10, pady=10)
        self.app_name = Label(master=self, text="Disappearing Text Writing App", font=TITLE_FONT, padx=5, pady=5)
        self.instructions_label = Label(master=self, text="Instructions", font=TITLE_FONT, padx=5, pady=5)
        self.instructions = Label(master=self, text=INSTRUCTIONS, font=FONT, padx=5, pady=5)
        self.user_entry = Text(master=self, wrap=WORD, font=FONT, padx=5, pady=5, height=10)
        self.timer_five_sec = None
        self.timer_overall = None
        self.timer_five_sec_label = Label(master=self, text="Text will disappear in: 5", font=FONT, padx=5, pady=5)
        self.timer_overall_label = Label(master=self, text="Overall Timer: ", font=FONT, padx=5, pady=5)
        self.start_writing_button = Button(master=self, text="Start Writing", command=self.start_writing,
                                           font=BUTTON_FONT, padx=5, pady=5)
        self.generate_random_prompt_button = Button(master=self, text="Generate Random Prompt",
                                                    command=self.set_up_prompt_screen, font=BUTTON_FONT, padx=5, pady=5)
        self.new_prompt_button = Button(master=self, text="New Prompt", command=self.generate_random_prompt,
                                        font=BUTTON_FONT, padx=5, pady=5)
        self.prompt_label = Label(master=self, text="Random Prompt", font=TITLE_FONT, padx=5, pady=5)
        self.random_prompt = ""
        self.time_chosen_var = StringVar(master=self)
        self.time_chosen_var.set("Select Writing Time (min)")
        self.time_chosen = OptionMenu(self, self.time_chosen_var, *OVERALL_TIME_LIST)
        self.time_chosen.config(font=FONT)
        self.word_count = 0
        self.word_count_label = Label(master=self, text=f"Word Count: {self.word_count}", font=FONT, padx=5, pady=5)
        self.is_typing = False
        self.idle_time = 0
        self.random_prompt_chosen = False
        self.set_up_instruction_screen()
        self.mainloop()

    def set_up_instruction_screen(self):
        self.instructions_label.grid(row=0, column=0, columnspan=2)
        self.instructions.grid(row=1, column=0, columnspan=2)
        self.time_chosen.grid(row=2, column=0, columnspan=2)
        self.generate_random_prompt_button.grid(row=3, column=0)
        self.start_writing_button.grid(row=3, column=1)

    def generate_random_prompt(self):
        self.random_prompt = random.choice(PROMPTS)
        self.user_entry.delete("1.0", END)
        self.user_entry.insert(INSERT, self.random_prompt)
        self.random_prompt_chosen = True

    def set_up_prompt_screen(self):
        if self.time_chosen_var.get() == "Select Writing Time (min)":
            messagebox.showwarning(title="Select Time", message="Please select how long you'd like to write for.")
            self.set_up_instruction_screen()
        else:
            self.instructions_label.destroy()
            self.instructions.destroy()
            self.generate_random_prompt_button.destroy()
            self.time_chosen.destroy()
            self.prompt_label.grid(row=0, column=0, columnspan=2)
            self.generate_random_prompt()
            self.user_entry.grid(row=1, column=0, columnspan=2)
            self.new_prompt_button.grid(row=2, column=0)
            self.start_writing_button.grid(row=2, column=1)

    def start_writing(self):
        if self.time_chosen_var.get() == "Select Writing Time (min)":
            messagebox.showwarning(title="Select Time", message="Please select how long you'd like to write for.")
            self.set_up_instruction_screen()
        else:
            self.instructions_label.destroy()
            self.instructions.destroy()
            self.generate_random_prompt_button.destroy()
            self.start_writing_button.destroy()
            self.new_prompt_button.destroy()
            self.prompt_label.destroy()
            time_chosen = int(self.time_chosen_var.get()) * 60
            self.time_chosen.destroy()
            self.timer_countdown(time_chosen)
            self.app_name.grid(row=0, column=0, columnspan=3)
            self.user_entry.grid(row=1, column=0, columnspan=3)
            self.timer_five_sec_label.grid(row=2, column=1)
            self.timer_overall_label.grid(row=3, column=0)
            self.word_count_label.grid(row=3, column=2)
            self.check_word_count()
            self.timer_five_sec = self.after(5000, self.erase_text)
            self.user_entry.bind("<Key>", self.check_typing)

    def timer_countdown(self, seconds):
        count_min = math.floor(seconds / 60)
        count_sec = seconds % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count_min < 10:
            count_min = f"0{count_min}"
        self.timer_overall_label.configure(text=f"Overall Timer: {count_min}:{count_sec}")
        if seconds > 0:
            self.timer_overall = self.after(1000, self.timer_countdown, seconds - 1)
        else:
            self.save_writing_text()

    def start_five_sec_timer(self):
        if self.idle_time == 5:
            self.erase_text()
        else:
            remaining_time = 5 - self.idle_time
            self.timer_five_sec_label.configure(text=f"Text will disappear in: {remaining_time}")
            self.idle_time += 1
            self.after_cancel(self.timer_five_sec)
            self.timer_five_sec = self.after(1000, self.start_five_sec_timer)

    def reset_timer(self):
        if self.timer_five_sec:
            self.after_cancel(self.timer_five_sec)
        self.idle_time = 0
        self.start_five_sec_timer()

    def check_word_count(self):
        user_entry_text = self.user_entry.get("1.0", END)
        spaces = user_entry_text.count(" ")
        self.word_count_label.configure(text=f"Word Count: {self.word_count}")
        self.word_count = spaces + 1

    def erase_text(self):
        if self.random_prompt_chosen:
            last_char = len(self.random_prompt) - 1
            self.user_entry.delete(f"1.{last_char}", END)
        else:
            self.user_entry.delete("1.0", END)
        self.is_typing = False
        self.idle_time = 0
        self.word_count = 0
        self.word_count_label.configure(text="Word Count: 0")
        self.timer_five_sec_label.configure(text="Text will disappear in: 0")

    def check_typing(self, event):
        # Checks to see if there is any visible content/the user is actively typing and returns True if so
        self.is_typing = bool(self.user_entry.get("1.0", "end-1c").strip())
        if not self.is_typing:
            self.start_five_sec_timer()
        else:
            self.after_cancel(self.timer_five_sec)
            self.idle_time = 0
            self.timer_five_sec_label.configure(text="Text will disappear in: 5")
        self.reset_timer()
        self.check_word_count()

    def save_writing_text(self):
        user_entry_text = self.user_entry.get("1.0", END)
        try:
            with open("writing/written_texts.txt", "a") as file:
                file.write(f"{user_entry_text}\n\n\n")
        except FileNotFoundError:
            with open("writing/written_texts.txt", "w") as file:
                file.write(user_entry_text)
        finally:
            messagebox.showinfo(title="Timer Up!", message="Your selected writing time is up! Your writing has been "
                                                           "saved to a text file.")
