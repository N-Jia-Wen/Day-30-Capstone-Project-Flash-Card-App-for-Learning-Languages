import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# Generate vocab words on flashcard (tries to access someone's saved progress).
# If saved progress not found, uses default vocab bank:
try:
    vocab_data = pandas.read_csv(filepath_or_buffer="./data/words_to_learn.csv")
    vocab_data_list = vocab_data.to_dict(orient="records")
except FileNotFoundError:
    vocab_data = pandas.read_csv(filepath_or_buffer="./data/french_words.csv")
    vocab_data_list = vocab_data.to_dict(orient="records")

# This saves the most recent entry:
latest_entry = {"Key": "Value (Placeholder)"}


def next_entry():
    global latest_entry, flip_timer

    canvas.itemconfig(card, image=card_front)
    # (new_entry is a dictionary)
    new_entry = random.choice(vocab_data_list)
    if new_entry == latest_entry:
        next_entry()
    else:

        # (after.cancel() prevents card from flipping too quickly if user clicks through multiple cards quickly:)
        window.after_cancel(flip_timer)

        fr_word = new_entry.get("French")
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=fr_word, fill="black")

        # Removes the previous entry from the list and adds back the most recent entry
        latest_entry = new_entry
        flip_timer = window.after(3000, func=flip_card)


def flip_card():
    en_word = latest_entry.get("English")
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=en_word, fill="white")
    canvas.itemconfig(card, image=card_back)


# Has same functionality as remove_entry() but removes entry from generated list and saves it to new csv file.
# This saves the user's progress and ensures they are not tested words they already know the meaning of.
def remove_entry():
    vocab_data_list.remove(latest_entry)
    updated_vocab_data = pandas.DataFrame(vocab_data_list)
    updated_vocab_data.to_csv(path_or_buf="./data/words_to_learn.csv", index=False)
    # next_entry is ordered last so that the entry is removed from the list
    # before latest_entry variable is assigned to the next entry
    next_entry()


# Creating UI:
window = tkinter.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Creating photos (does not work within functions):
card_front = tkinter.PhotoImage(file="./images/card_front.png")
card_back = tkinter.PhotoImage(file="./images/card_back.png")

# Setting up canvas:
canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="Placeholder", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Placeholder", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Creating buttons:
wrong_symbol = tkinter.PhotoImage(file="./images/wrong.png")
wrong_button = tkinter.Button(image=wrong_symbol, command=next_entry, highlightthickness=0)
wrong_button.grid(row=1, column=0)

right_symbol = tkinter.PhotoImage(file="./images/right.png")
right_button = tkinter.Button(image=right_symbol, command=remove_entry, highlightthickness=0)
right_button.grid(row=1, column=1)

next_entry()

window.mainloop()
