from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
translation_dict = {}


try:
    translation_words = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    translation_dict = original_data.to_dict(orient="records")
else:
    translation_dict = translation_words.to_dict(orient="records")

updated_list = []


windows = Tk()
windows.title("Flashy")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
random_french = {}


def next_card():
    global random_french, timer
    windows.after_cancel(timer)
    random_french = random.choice(translation_dict)
    canvas.itemconfig(title_label, text="French", fill="black")
    canvas.itemconfig(french_words, text=f"{random_french['French']}", fill="black")
    canvas.itemconfig(card_images, image=card_front)
    timer = windows.after(3000, func=flip_card)


def flip_card():
    global translation_dict, updated_list
    canvas.itemconfig(card_images, image=card_back)
    canvas.itemconfig(title_label, text="English", fill="white")
    canvas.itemconfig(french_words, text=f"{random_french['English']}", fill="white")


def is_known():
    translation_dict.remove(random_french)
    print(len(translation_dict))
    data = pandas.DataFrame(translation_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


timer = windows.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

check_image = PhotoImage(file="images/right.png")
cross_image = PhotoImage(file="images/wrong.png")
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

card_images = canvas.create_image(400, 263, image=card_front)

title_label = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
french_words = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

wrong_button = Button(image=cross_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()
windows.mainloop()
