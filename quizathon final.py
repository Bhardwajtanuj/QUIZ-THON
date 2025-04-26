from tkinter import *
from tkinter import messagebox as mb
import json
from PIL import Image, ImageTk

class Quiz:
    def __init__(self, level_data):
        self.level_data = level_data
        self.q_no = 0
        self.question = level_data['question']
        self.options = level_data['options']
        self.answer = level_data['answer']
        self.data_size = len(self.question)
        self.correct = 0

        self.bg_image = Image.open("background1.png")
        self.bg_image = self.bg_image.resize((800, 450))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(gui, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.display_title()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()

    def display_result(self):
        
        for widget in gui.winfo_children():
            widget.destroy()

        wrong_count = self.data_size - self.correct
        correct = f"✅ Correct: {self.correct}"
        wrong = f"❌ Wrong: {wrong_count}"
        score = int(self.correct / self.data_size * 100)
        result = f"🎯 Score: {score}%"

        result_frame = Frame(gui, width=800, height=450, bg="black")
        result_frame.place(x=0, y=0)

        
        bg_label = Label(result_frame, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        
        Label(result_frame, text="Quiz Results", font=("ariel", 28, "bold"),
              bg="black", fg="white").place(relx=0.5, rely=0.1, anchor="center")

        Label(result_frame, text=result, font=("ariel", 22, "bold"),
              bg="black", fg="yellow").place(relx=0.5, rely=0.3, anchor="center")

        Label(result_frame, text=correct, font=("ariel", 18),
              bg="black", fg="lightgreen").place(relx=0.5, rely=0.42, anchor="center")

        Label(result_frame, text=wrong, font=("ariel", 18),
              bg="black", fg="red").place(relx=0.5, rely=0.50, anchor="center")

        Button(result_frame, text="Restart Quiz", command=lambda: self.restart_quiz(),
               font=("ariel", 16, "bold"), bg="blue", fg="white", padx=10, pady=5).place(relx=0.5, rely=0.65, anchor="center")

        Button(result_frame, text="Exit", command=exit,
               font=("ariel", 16, "bold"), bg="red", fg="white", padx=10, pady=5).place(relx=0.5, rely=0.75, anchor="center")

    def restart_quiz(self):
        for widget in gui.winfo_children():
            widget.destroy()
        Quiz(self.level_data)

    def check_ans(self, q_no):
        return self.opt_selected.get() == self.answer[q_no]

    def next_btn(self):
        if self.check_ans(self.q_no):
            self.correct += 1
        self.q_no += 1
        if self.q_no == self.data_size:
            self.display_result()
        else:
            self.display_question()
            self.display_options()

    def buttons(self):
        Button(gui, text="Next", command=self.next_btn,
               width=10, bg="green", fg="white", font=("ariel", 16, "bold")).place(x=350, y=380)

        Button(gui, text="Quit", command=gui.destroy,
               width=5, bg="red", fg="white", font=("ariel", 16, "bold")).place(x=700, y=50)

    def display_options(self):
        self.opt_selected.set(0)
        for i, option in enumerate(self.options[self.q_no]):
            self.opts[i]['text'] = option

    def display_question(self):
        Label(gui, text=self.question[self.q_no], width=50,
              font=('ariel', 16, 'bold'), anchor='w', bg="black", fg="white").place(x=70, y=100)

    def display_title(self):
        Label(gui, text="Quizathon", width=50,
              bg="black", fg="white", font=("ariel", 20, "bold")).place(x=0, y=2)

    def radio_buttons(self):
        btns = []
        y_pos = 150
        for i in range(4):
            btn = Radiobutton(gui, text=" ", variable=self.opt_selected,
                              value=i+1, font=("ariel", 14), bg="black", fg="red")
            btn.place(x=100, y=y_pos)
            btns.append(btn)
            y_pos += 40
        return btns


gui = Tk()
gui.geometry("800x450")
gui.title("Quizathon")

with open('data.json') as f:
    all_data = json.load(f)

start_frame = Frame(gui, width=800, height=450)
start_frame.place(x=0, y=0)

welcome_img = Image.open("background1.png")
welcome_img = welcome_img.resize((800, 450))
welcome_photo = ImageTk.PhotoImage(welcome_img)
bg_label = Label(start_frame, image=welcome_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

Label(start_frame, text="Welcome to Quizathon!", font=("ariel", 24, "bold"),
      bg="black", fg="white").place(relx=0.5, rely=0.25, anchor="center")

level_var = StringVar()
level_var.set("easy")
levels = ["easy", "medium", "hard"]

level_menu = OptionMenu(start_frame, level_var, *levels)
level_menu.config(font=("ariel", 14), bg="red", fg="white")
level_menu.place(relx=0.5, rely=0.4, anchor="center")

def start_quiz():
    selected_level = level_var.get()
    level_data = all_data[selected_level]
    start_frame.destroy()
    Quiz(level_data)

Button(start_frame, text="Start Quiz", command=start_quiz,
       font=("ariel", 18, "bold"), bg="green", fg="white", padx=20, pady=10).place(relx=0.5, rely=0.6, anchor="center")

gui.mainloop()
