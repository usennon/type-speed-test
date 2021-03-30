from tkinter import *
import random

wpm = 0
cpm = 0


def reset():
    global wpm
    global cpm
    wpm = 0
    cpm = 0
    canvas.itemconfig(word_text, text=f"There will be a word")
    start_button['state'] = 'active'
    clear_button['state'] = 'disabled'


def read_file(file):
    with open(file, encoding='utf-8') as file:
        words = file.readlines()
        words = [word.split(' ')[0] for word in words if len(word.split(' ')[0]) >= 6][:300]
        return words


words = read_file('cs.txt')


def core_game(old_random):
    global wpm
    global cpm
    old_random_word = old_random
    random_word = random.choice(words)
    canvas.itemconfig(word_text, text=f'{random_word}')
    user_input = text.get()
    if old_random_word == user_input:
        wpm += 1
        cpm += len(old_random_word)
    print(user_input + ' user')
    print(old_random_word + ' random')
    game_button['command'] = lambda: core_game(old_random=random_word)
    text.delete(0, 'end')
    print(wpm)


def count_down(count):
    canvas.itemconfig(timer_text, text=f"{count}")
    if count > 0:
        window.after(1000, count_down, count - 1)
    if count == 0:
        global wpm
        global cpm
        game_button['state'] = 'disabled'
        canvas.itemconfig(word_text, text=f"Wpm: {wpm}, Cpm: {cpm}")
        clear_button['state'] = 'active'


def start_game():
    text['state'] = 'normal'
    start_button['state'] = 'disabled'
    game_button['state'] = 'active'
    count_down(60)
    random_word = random.choice(words)
    canvas.itemconfig(word_text, text=f'{random_word}')
    core_game(old_random=random_word)


window = Tk()
window.title('Typing speed')
window.config(padx=50, pady=50)
window.bind('<Return>', lambda event=None: game_button.invoke())

canvas = Canvas(width=200, height=200)
timer_text = canvas.create_text(100, 138, text="00:00")
word_text = canvas.create_text(100, 100, text="There will be a word")
canvas.pack()

text_label = Label(text='Input your text')
text_label.pack()
text = Entry(width=26)
text.pack()
game_button = Button(text='Ok')
game_button.pack()

game_button['state'] = 'disabled'

text['state'] = 'disabled'

start_button = Button(text='Start', command=start_game)
start_button.pack()

clear_button = Button(text='Reset', command=reset)
clear_button.pack()
clear_button['state'] = 'disabled'
window.mainloop()
