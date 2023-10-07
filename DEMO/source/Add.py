from tkinter import simpledialog
from tkinter import messagebox
import re
import threading
import random
import pygame
import pyttsx3
import tkinter as tk
from translate import Translator
from gtts import gTTS
from tkinter import ttk
from customtkinter import *
import datetime

class Close:
    try:
        def __init__(self, root, mark, wrongs):
            self.root = root
            self.root.title("END GAME")
            self.root.geometry("1000x700+300+50")
            self.score = mark
            self.wron = wrongs
            # print(self.score.txt)
            # print(wrongs)
            # self.root.attributes('-topmost', True)
            # self.root.config(bg="#B1DDC6")
            self.labels = CTkLabel(root, text="Kiểm Tra Đã Kết Thúc! Tạm Biệt !!!", text_color="#66B2FF",
                                   font=("Helvetica", 52))
            self.labels.pack(pady=20)
            self.labelss = CTkLabel(root, text="ヾ(＠⌒ー⌒＠)ノ             (●'◡'●)", text_color="#66B2FF",
                                    font=("Helvetica", 52))
            self.labelss.pack(pady=20)
            self.label = CTkLabel(root, text="", font=("Helvetica", 70))
            self.label.pack(pady=43)
            max_score = self.wron + self.score
            # if max_score == self.
            self.progress = ttk.Progressbar(root, orient="horizontal", length=700, mode="determinate")
            self.progress["maximum"] = max_score
            self.progress["value"] = mark
            self.progress.pack(pady=43)
            #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.update_label()
            self.ok_button = CTkButton(root, text="Tạm biệt", font=("Helvetica", 61), command=self.exit)
            self.ok_button.bind("<Return>", lambda event: self.exit)
            self.ok_button.pack(pady=52)
            for i in range(9):
                self.root.grid_rowconfigure(i, weight=1)
            for i in range(6):
                self.root.grid_columnconfigure(i, weight=1)

        def exit(self):
            self.root.destroy()


        def update_label(self):
            self.label.configure(text=f"Kết Quả: {self.score}/{self.progress['maximum']} Câu")
    except Exception as e:
        print(e)

class Choose:
    try:
        def __init__(self, root, vocabulary, sc, wron):
            self.root = root
            self.root.title("Choose Right")
            self.root.geometry("1000x700+300+50")
            self.vocabulary = vocabulary
            self.sc = sc
            self.wr = wron
            self.buttons = []
            self.check = []
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            pygame.init()
            self.create_buttons()

        def on_closing(self):
            if messagebox.askokcancel("Warning", "Bạn thực sự muốn tạm dừng việc học tại đây ?"):
                # os.system('shutdown -s')
                self.root.destroy()
                # print("tắt máy")

        def create_buttons(self):
            self.labels = CTkLabel(self.root, text="Hãy Chọn 2 nút là TỪ và NGHĨA của nhau !", text_color="#66B2FF",
                                   font=("Helvetica", 43))
            self.labels.pack(padx=10, pady=10)
            random.shuffle(self.vocabulary)
            sides = ["left", "bottom", "right", "top"]

            for word, meaning in self.vocabulary:
                word_button = CTkButton(self.root, text=word, font=("Helvetica", 34),
                                        command=lambda w=word: self.display_word(w))
                word_button.pack(pady=10, padx=10, side=random.choice(sides))

                meaning_button = CTkButton(self.root, text=meaning, font=("Helvetica", 34),
                                           command=lambda m=meaning: self.display_word(m))
                meaning_button.pack(pady=10, padx=10, side=random.choice(sides))

                self.buttons.append((word_button, meaning_button))

        def display_word(self, word):
            # print(f"Word: {word}")
            if len(self.check) < 2:
                self.check.append(word)
                # print(self.vocabulary)
                if len(self.check) == 2:
                    if (self.check[0], self.check[1]) in self.vocabulary or (
                    self.check[1], self.check[0]) in self.vocabulary:
                        # print("1")
                        self.update_buttons()
                        pygame.mixer.init()
                        sound = pygame.mixer.Sound("song/right.mp3")
                        sound.play()
                    else:
                        pygame.mixer.init()
                        sound = pygame.mixer.Sound("song/wrong.mp3")
                        sound.play()
                        # print("1")
                    self.check = []
            # print(self.check)

        def update_buttons(self):
            if (self.check[0], self.check[1]) in self.vocabulary:
                self.vocabulary.remove((self.check[0], self.check[1]))
            elif (self.check[1], self.check[0]) in self.vocabulary:
                self.vocabulary.remove((self.check[1], self.check[0]))

            print(self.vocabulary)
            delb = []
            for word_button, meaning_button in self.buttons:
                if word_button.cget("text") in self.check:
                    word_button.destroy()
                    delb.append(word_button)
                if meaning_button.cget("text") in self.check:
                    meaning_button.destroy()
                    delb.append(meaning_button)

            if (delb[0], delb[1]) in self.buttons:
                self.buttons.remove((delb[0], delb[1]))
            elif (delb[1], delb[0]) in self.buttons:
                self.buttons.remove((delb[1], delb[0]))

            for word_button, meaning_button in self.buttons:
                word_button.destroy()
                meaning_button.destroy()
            self.labels.destroy()
            self.create_buttons()
            self.checkend()

        def checkend(self):
            if len(self.buttons) == 0 or len(self.vocabulary) == 0:
                self.root.destroy()
                r_root = CTk()
                reviseapp = Close(r_root, self.sc, self.wr)
                r_root.mainloop()
    except Exception as e:
        print(e)

class VocabularyQuizApp:
    try:
        def __init__(self, root, vocabulary, mark, w):
            self.root = root
            self.root.title("Game Đoán Từ")
            self.khen = ['Exellent', 'Joy wha', 'Good job bro', 'Joy wha', 'Significant', 'Yes', 'Joy wha', 'Fantastic']
            self.che = ['No', 'Sorry']
            self.root.geometry("1000x700+300+50")
            # self.root.attributes('-topmost', True)
            self.sc = mark
            self.wr = w
            self.vocabulary = list(set(vocabulary))
            self.quiz_index = 0
            self.quiz_word = ""
            self.wrong = []
            self.off = False
            pygame.init()
            self.correct_sound = pygame.mixer.Sound("song/right.mp3")
            self.wrong_sound = pygame.mixer.Sound("song/wrong.mp3")
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.current_word = None
            self.chin = []
            self.vocabulary = self.check_and_remove_chinese_words(self.vocabulary)
            print(self.chin)
            self.create_ui()

        def check_and_remove_chinese_words(self, vocab):
            chinese_words = [(word, translation) for word, translation in vocab if re.search('[\u4e00-\u9fff]', word)]
            self.chin.extend(chinese_words)
            return [(word, translation) for word, translation in vocab if not re.search('[\u4e00-\u9fff]', word)]

        def on_closing(self):
            if messagebox.askokcancel("Warning", "Bạn thực sự muốn tạm dừng việc học tại đây ?"):
                # os.system('shutdown -s')
                self.root.destroy()
                # print("tắt máy")

        def create_ui(self):
            # self.root.config(bg="#B1DDC6")
            self.word_label = CTkLabel(self.root, text="", font=("Arial", 70))
            self.word_label.pack(pady=20)

            self.okentry = CTkEntry(self.root, font=("Arial", 52), width=700)
            self.okentry.pack(pady=70)
            self.okentry.bind("<Return>", lambda event: self.check_answer())

            self.check_button = CTkButton(self.root, text="Kiểm Tra", font=("Arial", 52), command=self.check_answer)
            self.check_button.pack(pady=10)

            self.result_label = CTkLabel(self.root, text="", font=("Arial", 52))
            self.result_label.pack(pady=52)

            self.next_button = CTkButton(self.root, text="BỎ QUA", font=("Arial", 52), command=self.unknown)
            self.next_button.pack(pady=10)

            self.quiz_word = self.get_random_quiz_word()
            self.update_word_label()
            for i in range(9):
                self.root.grid_rowconfigure(i, weight=1)
            for i in range(6):
                self.root.grid_columnconfigure(i, weight=1)

        def get_random_quiz_word(self):
            # print(self.wrong)
            if self.quiz_index < len(self.vocabulary):
                self.current_word, meaning = self.vocabulary[self.quiz_index]
                self.current_word = self.process(self.current_word)
                self.quiz_index += 1
                return self.create_quiz_word(self.current_word)
            elif self.wrong != []:
                self.current_word = self.wrong[0]
                self.current_word = self.process(self.current_word)
                self.wrong.pop(0)
                return self.create_quiz_word(self.current_word)
            else:
                return None

        def unknown(self):
            if self.current_word not in self.wrong:
                self.wrong.append(self.current_word)
            self.quiz_word = self.get_random_quiz_word()
            self.update_word_label()
            self.result_label.configure(text="")
            self.okentry.delete(0, tk.END)

        def create_quiz_word(self, word):
            if len(word) <= 2:
                split = 2
            else:
                split = 3
            if '.' in word:
                so, word = word.split('.')
                word = word.strip()
            word_list = list(word)
            # random.shuffle(word_list)
            num_blanks = len(word) // split
            blanks_indices = random.sample(range(len(word)), num_blanks)
            for i in blanks_indices:
                word_list[i] = "_"
            return " ".join(word_list)

        def update_word_label(self):
            if self.quiz_word is not None:
                self.word_label.configure(text=self.quiz_word)
            else:
                if len(self.chin) > 0:
                    self.root.destroy()
                    r_root = CTk()
                    reviseapp = Choose(r_root, self.chin, self.sc, self.wr)
                    r_root.mainloop()
                else:
                    self.root.destroy()
                    r_root = CTk()
                    reviseapp = Close(r_root, self.sc, self.wr)
                    r_root.mainloop()

        def process(self, word):
            if '(' in word:
                word = re.sub(r'\(.*\)', '', word)
            if '.' in word:
                so, word = word.split('.')
                word = word.strip()
            return word

        def check_answer(self):
            if self.quiz_word is not None:
                user_answer = self.okentry.get().strip()
                original_word = self.current_word
                word = self.process(original_word)
                if user_answer.lower() == word.lower():
                    self.correct_sound.play()
                    self.result_label.configure(text="|✔| Correct! (≧▽≦)")
                    self.quiz_word = self.get_random_quiz_word()
                    self.okentry.delete(0, tk.END)
                    self.update_word_label()
                else:
                    self.wrong_sound.play()
                    self.result_label.configure(text="|✘| Incorrect! (┬┬﹏┬┬)")
                    self.okentry.delete(0, tk.END)
    except Exception as e:
        print(e)

class Listen:
    try:
        def __init__(self, root, vocabulary, mark, w):
            self.root = root
            self.root.title("Nghe")
            self.root.geometry("1000x700+300+50")
            self.cscore = mark
            self.w = w
            # self.root.attributes('-topmost', True)
            self.vocabulary = list(set(vocabulary))
            self.items = list(set(vocabulary))
            random.shuffle(self.items)
            # print(self.items[0][1])
            self.current_word = None
            self.current_meaning = None
            self.curpos = 0
            self.pos = 0
            pygame.init()
            self.off = False
            # self.correct_sound = pygame.mixer.Sound("song/right.mp3")
            # self.wrong_sound = pygame.mixer.Sound("song/wrong.mp3")
            self.wrong = []
            self.correct_answers = 0
            self.total_questions = 0
            self.create_ui()
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            # self.update_sscore_label()
            self.next_question()

        def on_closing(self):
            if messagebox.askokcancel("Warning", "Bạn thực sự muốn tạm dừng việc học tại đây ?"):
                # os.system('shutdown -s')
                self.root.destroy()
                # print("tắt máy")

        def create_ui(self):
            # self.root.config(bg="#B1DDC6")
            self.question_label = CTkLabel(self.root, text="Hãy Nhấn vào nút start để bắt đầu", font=("Helvetica", 61))
            self.question_label.pack(pady=20)
            self.read_button = CTkButton(self.root, text="Speak Again", font=("Helvetica", 34),
                                         command=lambda: self.read_word(self.current_word))
            self.read_button.pack(pady=20)
            self.start_button = CTkButton(self.root, text="Start", font=("Haelvetica", 34),
                                          command=self.start_reading_vocabulary)
            self.start_button.pack()
            self.nlabel = CTkLabel(self.root, text="Hãy nhấn vào nút START để bắt đầu nghe !!!", font=("Helvetica", 43))
            self.nlabel.pack(pady=20)

            entry_font = ("Helvetica", 43)
            self.answer = CTkEntry(self.root, font=entry_font, width=700, state=tk.DISABLED)
            self.answer.pack(pady=30)
            self.score_label = CTkLabel(self.root, text=f"Điểm số: 0/{len(self.items)}", font=("Helvetica", 52))
            self.score_label.pack(pady=10, side=BOTTOM)
            self.ok = CTkButton(self.root, text="OK", font=("Helvetica", 52), command=self.check_answer)
            self.ok.pack(pady=10)
            self.answer.bind("<Return>", lambda event: self.check_answer())

            self.label = CTkLabel(self.root, text="", font=("Helvetica", 43))
            self.label.pack(pady=20)
            for i in range(9):
                self.root.grid_rowconfigure(i, weight=1)
            for i in range(6):
                self.root.grid_columnconfigure(i, weight=1)

        def start_reading_vocabulary(self):
            self.start_button.destroy()
            self.answer.configure(state=tk.NORMAL)
            self.nlabel.configure(text='Nhập đáp án dưới đây:')
            self.read_word(self.current_word)

        def next_question(self):
            # self.root.after(1000)
            self.answer.delete(0, tk.END)
            # print(type(self.items))
            if self.curpos < len(self.items):
                self.current_word, self.current_meaning = self.items[self.curpos]
                self.current_word = self.current_word.lstrip('- ')
                if re.search('[\u4e00-\u9fff]', self.current_word):
                    self.question_label.configure(text=f"Listen And Write The MEANING!")
                else:
                    self.question_label.configure(text=f"Listen And Write The WORD!")
                if self.curpos > 0:
                    self.root.after(2500, self.read_word, self.current_word)
                self.curpos += 1
            elif self.pos < len(self.wrong):
                # self.items = self.wrong.copy()
                # self.wrong = []
                self.current_word, self.current_meaning = self.wrong[self.pos]
                self.current_word = self.current_word.lstrip('- ')
                if re.search('[\u4e00-\u9fff]', self.current_word):
                    self.question_label.configure(text=f"Listen And Write The MEANING!")
                else:
                    self.question_label.configure(text=f"Listen And Write The WORD!")
                self.root.after(2500, self.read_word, self.current_word)
                self.pos += 1
            else:
                self.off = False
                vocabs = self.check_and_remove_chinese_words(self.vocabulary)
                if len(vocabs) > 0:
                    self.root.destroy()
                    rd_root = CTk()
                    # print("-----------------------------")
                    # print(self.cscore+self.correct_answers)
                    # print(self.total_questions-self.cscore+self.w)
                    flard_app = VocabularyQuizApp(rd_root, self.vocabulary, (self.cscore + self.correct_answers),
                                                  (self.total_questions - self.correct_answers + self.w))
                    rd_root.mainloop()
                else:
                    self.root.destroy()
                    rd_root = CTk()
                    # print("-----------------------------")
                    # print(self.cscore+self.correct_answers)
                    # print(self.total_questions-self.cscore+self.w)
                    flard_app = Choose(rd_root, self.vocabulary, (self.cscore + self.correct_answers),
                                       (self.total_questions - self.correct_answers + self.w))
                    rd_root.mainloop()
            # self.read_word(self.current_word)

        def check_and_remove_chinese_words(self, vocab):
            return [(word, translation) for word, translation in vocab if not re.search('[\u4e00-\u9fff]', word)]

        def read_enword_thread(self, word):
            try:
                self.label.configure(text="")
                self.label.configure(text_color="white")
                engine = pyttsx3.init()
                engine.setProperty('rate', 106)
                engine.setProperty('volume', 2)
                engine.say(word)
                engine.runAndWait()
                return
            except Exception as e:
                print(e)

        def read_cnword_thread(self, word):
            try:
                self.label.configure(text="")
                self.label.configure(text_color="white")
                tts = gTTS(word, lang='zh-cn')
                temp_file = "temp.mp3"
                tts.save(temp_file)
                pygame.mixer.init()
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
                os.remove(temp_file)
            except Exception as e:
                print(e)

        def read_word(self, word):
            try:
                if re.search('[\u4e00-\u9fff]', self.current_word):
                    thread = threading.Thread(target=self.read_cnword_thread, args=(word,))
                    thread.start()
                else:
                    thread = threading.Thread(target=self.read_enword_thread, args=(word,))
                    thread.start()
            except Exception as e:
                print(e)

        def check_answer(self):
            selected_ans = self.answer.get().lower().strip()
            if selected_ans == "" or selected_ans == " " or selected_ans == "  " or selected_ans == "   ":
                return
            if re.search('[\u4e00-\u9fff]', self.current_word):
                rightword = self.current_meaning.lower()
                # word = self.current_meaning
            else:
                rightword = self.current_word.lower()
                # word = self.current_word
            # if '(' in word:
            #    word = re.sub(r'\(.*\)', '', word)
            if '(' in rightword:
                rightword = re.sub(r'\(.*\)', '', rightword)
            if selected_ans in rightword:
                self.label.configure(text=f"|✔| Correct! (≧▽≦)\nKết quả=> |{rightword}|")
                self.label.configure(text_color="green")
                self.correct_answers += 1
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/right.mp3")
                sound.play()
            else:
                self.label.configure(text=f"|✘| Incorrect! (┬┬﹏┬┬)\nĐáp án=> |{rightword}|")
                self.label.configure(text_color="red")
                self.wrong.append((self.current_word, self.current_meaning))
                # messagebox.showinfo("Kết quả", f"Sai! Đáp án đúng là '{rightword}'")
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/wrong.mp3")
                sound.play()

            self.total_questions += 1
            self.update_score_label()
            self.next_question()

        def update_score_label(self):
            score_text = f"Điểm: {self.correct_answers}/{self.total_questions}"
            self.score_label.configure(text=score_text)
    except Exception as e:
        print(e)

class TL:
    try:
        def __init__(self, root, vocabulary, mark, w):
            self.root = root
            self.root.title("Tự luận")
            self.root.geometry("1000x700+300+50")
            self.cscore = mark
            self.w = w
            self.khen = ['Good', 'Triple kill', 'Exellent', 'Mega kill', 'Ace', 'Fantastic']
            self.che = ['No', 'Sorry']
            # self.root.attributes('-topmost', True)
            self.vocab = list(set(vocabulary))
            self.items = list(set(vocabulary))
            random.shuffle(self.items)
            # print(self.items[0][1])
            self.current_word = None
            self.current_meaning = None
            self.curpos = 0
            self.wrong = []
            self.correct_answers = 0
            self.total_questions = 0
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.off = False
            pygame.init()
            self.correct_sound = pygame.mixer.Sound("song/right.mp3")
            self.create_ui()
            self.update_score_label()
            self.next_question()

        def on_closing(self):
            if messagebox.askokcancel("Warning", "Bạn thực sự muốn tạm dừng việc học tại đây ?"):
                # os.system('shutdown -s')
                self.root.destroy()
                # print("tắt máy")

        def create_ui(self):
            # self.root.config(bg="#B1DDC6")
            self.question_label = CTkLabel(self.root, text="", font=("Helvetica", 52))
            self.question_label.pack(pady=20)
            # self.nlabel = CTkLabel(self.root, text="Nhập đáp án dưới đây:", font=("Helvetica", 43))
            # self.nlabel.pack(pady=30)
            entry_font = ("Helvetica", 52)
            self.answer = CTkEntry(self.root, font=entry_font, width=700, placeholder_text="Nhập đáp án ở đây ...")
            self.answer.pack(pady=70)

            self.ok = CTkButton(self.root, text="OK", font=("Helvetica", 43), command=self.check_answer)
            self.ok.pack(pady=10)
            self.answer.bind("<Return>", lambda event: self.check_answer())

            self.label = CTkLabel(self.root, text="", font=("Helvetica", 43))
            self.label.pack(pady=20)

            self.score_label = CTkLabel(self.root, text="", font=("Helvetica", 52))
            self.score_label.pack(pady=10, side=BOTTOM)
            for i in range(9):
                self.root.grid_rowconfigure(i, weight=1)
            for i in range(6):
                self.root.grid_columnconfigure(i, weight=1)

        def next_question(self):
            # print(type(self.items))
            if self.curpos < len(self.items):
                self.current_word, self.current_meaning = self.items[self.curpos]
                self.current_word = self.current_word.lstrip('- ')
                if re.search('[\u4e00-\u9fff]', self.current_word):
                    self.question_label.configure(text=f"What is the meaning of '{self.current_word}'?")
                else:
                    self.question_label.configure(text=f"What is the meaning of '{self.current_meaning}'?")
                self.curpos += 1
            elif self.wrong:
                self.items = self.wrong.copy()
                self.wrong = []
                self.curpos = 0
            else:
                self.off = True
                self.root.destroy()
                l_root = CTk()
                # print("------------------")
                # print(self.cscore+self.correct_answers)
                # print(self.total_questions-self.cscore+self.w)
                l = Listen(l_root, self.vocab, (self.cscore + self.correct_answers),
                           (self.total_questions - self.correct_answers + self.w))
                l_root.mainloop()

        def hide_label(self):
            self.label.configure(text="")
            self.label.configure(text_color="white")

        def check_answer(self):
            selected_ans = self.answer.get().lower().strip()
            # print(len(selected_ans))
            # print(len(self.current_meaning)/2)
            if selected_ans == "" or selected_ans == " " or selected_ans == "  " or selected_ans == "   ":
                return
            if re.search('[\u4e00-\u9fff]', self.current_word):
                rightword = self.current_meaning.lower()
                # word = self.current_meaning
            else:
                rightword = self.current_word.lower()
                # word = self.current_word
            if '(' in rightword:
                rightword = re.sub(r'\(.*\)', '', rightword)
            if selected_ans in rightword:
                # self.read_word()
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/right.mp3")
                sound.play()
                self.read_word(f"{self.current_word}")
                self.label.configure(text=f"|✔| Correct! (≧▽≦) \nKết quả => |{rightword}| ")
                self.label.configure(text_color="green")
                self.correct_answers += 1

                self.answer.delete(0, tk.END)
            else:
                # self.read_word(random.choice(self.che))
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/wrong.mp3")
                sound.play()
                # self.read_word(f"{word}")
                self.label.configure(text=f"|✘| Incorrect! (┬┬﹏┬┬) \nĐáp án => |{rightword}| ")
                # messagebox.showinfo("Kết quả", f"Sai!(┬┬﹏┬┬) \n Đáp án đúng là '{self.current_word}'")
                self.label.configure(text_color="red")
                self.wrong.append((self.current_word, self.current_meaning))
                # self.root.after(2500, self.hide_label)
                self.answer.delete(0, tk.END)
            self.root.after(2500, self.hide_label)
            self.total_questions += 1
            self.update_score_label()

            self.next_question()

        def update_score_label(self):
            score_text = f"Điểm: {self.correct_answers}/{self.total_questions}"
            self.score_label.configure(text=score_text)

        def read_enword_thread(self, word):
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 124)
                engine.setProperty('volume', 2)
                engine.say(word)
                engine.runAndWait()

                return
            except Exception as e:
                print(e)

        def read_cnword_thread(self, word):
            try:
                self.label.configure(text="")
                self.label.configure(text_color="white")
                tts = gTTS(word, lang='zh-cn')
                temp_file = "temp.mp3"
                tts.save(temp_file)
                pygame.mixer.init()
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
                os.remove(temp_file)
            except Exception as e:
                print(e)

        def read_word(self, word):
            try:
                if re.search('[\u4e00-\u9fff]', word):
                    thread = threading.Thread(target=self.read_cnword_thread, args=(word,))
                    thread.start()
                else:
                    thread = threading.Thread(target=self.read_enword_thread, args=(word,))
                    thread.start()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

class Multichoice:
    try:
        def __init__(self, root, vocabulary):
            vocabulary = list(set(vocabulary))
            self.root = root
            self.root.title("Multiple Choice Quiz")
            self.root.geometry("1000x700+300+50")
            # self.vocabulary = vocabulary
            self.items = list(set(vocabulary))
            random.shuffle(self.items)
            self.items = list(set(self.items))
            self.current_word = None
            self.current_meaning = None
            self.options = []
            self.curpos = 0
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.khen = ['Exellent', 'Joy wha', 'Good job bro', 'Joy wha', 'Significant', 'Yes', 'Joy wha',
                         'Fantastic']
            # self.khen = ['Good','Yes','Wow','Join Wa', 'Triple kill', 'Exellent', 'Mega kill', 'Ace', 'Fantastic']
            self.che = ['No', 'Sorry']
            self.wrong = []
            # pygame.init()
            # self.correct_sound = pygame.mixer.Sound("song/right.mp3")
            # self.wrong_sound = pygame.mixer.Sound("song/wrong.mp3")
            self.score = 0
            self.total_questions = 0
            self.create_ui()
            self.off = False
            self.next_question()

        def on_closing(self):
            if messagebox.askokcancel("Warning", "Bạn thực sự muốn tạm dừng việc học tại đây ?"):
                # os.system('shutdown -s')
                self.root.destroy()
                # print("tắt máy")

        def create_ui(self):
            self.question_label = CTkLabel(self.root, text="", font=("Helvetica", 52))
            self.question_label.pack(pady=20)
            # self.root.config(bg="#B1DDC6")
            self.option_buttons = []
            for i in range(4):
                button = CTkButton(self.root, text="", font=("Helvetica", 52),
                                   command=lambda i=i: self.check_answer(i))
                button.pack(pady=16)
                self.option_buttons.append(button)
            self.label = CTkLabel(self.root, text="", font=("Helvetica", 43))
            self.label.pack(pady=20)
            self.score_label = CTkLabel(self.root, text=f"Điểm số: 0/{len(self.items)}", font=("Helvetica", 52))
            self.score_label.pack(pady=16, side=BOTTOM)
            for i in range(9):
                self.root.grid_rowconfigure(i, weight=1)
            for i in range(6):
                self.root.grid_columnconfigure(i, weight=1)

        def next_question(self):
            if self.curpos < len(self.items):
                self.current_word, self.current_meaning = self.items[self.curpos]
                self.curpos += 1
                self.question_label.configure(text=f"What is the meaning of '{self.current_word}'?")
                self.options = [self.current_meaning]
                while len(self.options) < 4:
                    option = random.choice([pair[1] for pair in self.items])
                    if option not in self.options:
                        self.options.append(option)
                random.shuffle(self.options)
                for i, option in enumerate(self.options):
                    self.option_buttons[i].configure(text=option)
            elif self.wrong:
                self.current_word, self.current_meaning = self.wrong.pop(0)
                self.question_label.configure(text=f"What is the meaning of '{self.current_word.lstrip('- ')}'?")
                self.options = [self.current_meaning]
                while len(self.options) < 4:
                    option = random.choice([pair[1] for pair in self.items])
                    if option not in self.options:
                        self.options.append(option)
                random.shuffle(self.options)
                for i, option in enumerate(self.options):
                    self.option_buttons[i].configure(text=option)
            else:
                self.off = True
                self.root.destroy()
                Tl_root = CTk()
                # print(self.score.txt)
                # print(self.total_questions-self.score.txt)
                Tl = TL(Tl_root, self.items, self.score, (self.total_questions - self.score))
                Tl_root.mainloop()

        def read_word_thread(self, word):
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 124)
                engine.setProperty('volume', 2)
                engine.say(word)
                engine.runAndWait()
                return
            except Exception as e:
                print(e)

        def read_word(self, word):
            try:
                thread = threading.Thread(target=self.read_word_thread, args=(word,))
                thread.start()
            except Exception as e:
                print(e)

        def check_answer(self, selected_option):
            selected_meaning = self.options[selected_option]
            if selected_meaning == self.current_meaning:
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/right.mp3")
                sound.play()
                # self.read_word(f"{random.choice(self.khen)}")
                self.label.configure(text="|✔| Correct! (≧▽≦)")
                self.label.configure(text_color="green")
                # messagebox.showinfo("Kết quả", f"Đúng! Là {self.current_word}")
                self.score += 1  # Tăng điểm số nếu đúng
                self.total_questions += 1
                # self.root.after(1501, self.hide_label)
            else:
                # self.read_word(random.choice(self.che))
                pygame.mixer.init()
                sound = pygame.mixer.Sound("song/wrong.mp3")
                sound.play()
                self.label.configure(text="|✘| Incorrect! (┬┬﹏┬┬)")
                self.label.configure(text_color="red")
                self.wrong.append((self.current_word, self.current_meaning))
                # messagebox.showinfo("Kết quả", f"Sai! Đáp án đúng là '{self.current_meaning}'")
                self.total_questions += 1
            self.root.after(2500, self.hide_label)
            self.update_score_label()
            self.next_question()

        def hide_label(self):
            self.label.configure(text="")
            self.label.configure(text_color="white")

        def update_score_label(self):
            score_text = f"Điểm số: {self.score} / {self.total_questions}"
            self.score_label.configure(text=score_text)
    except Exception as e:
        print(e)
class Transl:
    try:
        def __init__(self, troot):
            self.troot = troot
            self.translated_text = ""
            troot.title("TRANSLATOR")
            self.troot.configure(bg="black")
            # self.troot.geometry("300x400")
            self.troot.attributes('-topmost', True)
            self.language_frame = tk.Frame(troot, bg="black")
            self.language_frame.pack(pady=5, padx=10, side=tk.TOP)
            self.from_lang_var = tk.StringVar()
            self.to_lang_var = tk.StringVar()
            self.from_lang_var.set("vi")
            self.to_lang_var.set("en")
            self.from_lang_menu = tk.OptionMenu(self.language_frame, self.from_lang_var, "vi", "en")
            self.from_lang_menu.pack(padx=5, side=tk.LEFT)
            self.to_lang_menu = tk.OptionMenu(self.language_frame, self.to_lang_var, "vi", "en")
            self.to_lang_menu.pack(padx=5, side=tk.RIGHT)
            self.input_text_widget = tk.Text(troot, height=10, width=30)
            self.input_text_widget.pack(pady=5, padx=10, side=tk.LEFT)
            self.translate_button = tk.Button(troot, text="Translate ➠", command=self.translate_text, bg="green",
                                              fg="white", font=("Arial", 16))
            self.translate_button.pack(side=tk.LEFT)
            self.read_en_button = tk.Button(troot, text="Đọc", command=self.read_word, bg="red",
                                            fg="white", font=("Arial", 16))
            self.read_en_button.pack(side=tk.LEFT)
            # self.slabel = tk.Label(text='➠', bg="black", fg="white", font=("Arial", 25))
            # self.slabel.pack(side=tk.LEFT)
            self.output_text_widget = tk.Text(troot, height=10, width=30)
            self.output_text_widget.pack(pady=5, padx=10, side=tk.LEFT)

        def read_word(self):
            engine = pyttsx3.init()
            engine.setProperty('rate', 106)
            engine.setProperty('volume', 2)
            engine.say(self.translated_text)
            engine.runAndWait()

        def translate_text(self):
            input_text = self.input_text_widget.get("1.0", "end-1c")
            from_lang = self.from_lang_var.get()
            to_lang = self.to_lang_var.get()
            if from_lang != to_lang:
                translator = Translator(to_lang=to_lang, from_lang=from_lang)
                self.translated_text = translator.translate(input_text)
                self.output_text_widget.delete("1.0", "end")
                self.output_text_widget.insert("1.0", self.translated_text)
            else:
                self.output_text_widget.delete("1.0", "end")
                self.output_text_widget.insert("1.0", f"{input_text}\n Hãy chọn ngôn ngữ khác.")
    except Exception as e:
        print(e)

class Ask:
    def __init__(self, root):
        self.root = root
        self.root.title("Ask")
        self.root.geometry("600x300+200+100")
        #self.root.config(bg="#B1DDC6")
        self.label = CTkLabel(root, text="Bạn hãy nhập vị trí bắt đầu và vị trí kết thúc của sổ từ vựng bạn muốn học:",
                              font=("Helvetica", 14))
        self.label.pack(pady=20)
        self.start_position_label = CTkLabel(root, text="Vị trí bắt đầu:")
        self.start_position_label.pack()
        self.start_position_entry = CTkEntry(root)
        self.start_position_entry.pack()
        self.end_position_label = CTkLabel(root, text="Vị trí kết thúc:")
        self.end_position_label.pack()
        self.end_position_entry = CTkEntry(root)
        self.end_position_entry.pack()
        self.ok_button = CTkButton(root, text="OK", command=self.load_flashcard)
        self.ok_button.pack(pady=10)
        self.glabel = CTkLabel(self.root, text="!!!Lưu Ý: Danh sách phải có 4 Từ Trở Lên!!!", font=("Helvetica", 14),
                               wraplength=400)
        self.glabel.pack(pady=20)

    def validate_selected_vocabulary(self, en, st):
        if (en - st) < 4 or st > en:
            messagebox.showerror("Lỗi", "Bạn hãy nhập lại từ vựng bắt đầu hoặc từ vựng kết thúc")
            return False
        return True

    def load_flashcard(self):
        try:
            start_position = int(self.start_position_entry.get())
            end_position = int(self.end_position_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số từ vựng và vị trí bắt đầu là số nguyên.")
            return
        if not self.validate_selected_vocabulary(end_position, start_position):
            return
        try:
            with open("datastorage/learn.txt", "r", encoding="utf-8") as file:
                line = file.readlines()
            with open("datastorage/tempv.txt", "r", encoding="utf-8") as file:
                lines1 = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Không tìm thấy file 'learn.txt'.")
            return
        lines = line + lines1

        s = max(start_position-1, 0)
        e = min(end_position-1, len(lines))
        lines = lines[s:e+1]
        print(lines)
        #print(lines)
        vocabulary = []
        for line in lines:
            if line and ':' in line:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    word, meaning = parts
                    vocabulary.append((word.strip(), meaning.strip()))
        #print(vocabulary)
        with open("datastorage/relearn.txt", "w", encoding="utf-8") as file:
            for word, meaning in vocabulary:
                file.write(f"{word}:{meaning}\n")

        self.root.destroy()
        multiplechoice_root = CTk()
        multiplechoice = Multichoice(multiplechoice_root, vocabulary)
        multiplechoice_root.mainloop()
class Asknew:
    def __init__(self, root,data):
        self.root = root
        self.root.title("Ask")
        self.root.geometry("600x300+200+100")
        self.vocab = data
        # self.root.config(bg="#B1DDC6")
        self.label = CTkLabel(root, text="Bạn hãy nhập vị trí bắt đầu và vị trí kết thúc của sổ từ vựng bạn muốn học:",
                              font=("Helvetica", 14))
        self.label.pack(pady=20)
        self.start_position_label = CTkLabel(root, text="Vị trí bắt đầu:")
        self.start_position_label.pack()
        self.start_position_entry = CTkEntry(root)
        self.start_position_entry.pack()
        self.end_position_label = CTkLabel(root, text="Vị trí kết thúc:")
        self.end_position_label.pack()
        self.end_position_entry = CTkEntry(root)
        self.end_position_entry.pack()
        self.ok_button = CTkButton(root, text="OK", command=self.load_flashcard)
        self.ok_button.pack(pady=10)
        self.glabel = CTkLabel(self.root, text="!!!Lưu Ý: Danh sách phải có 4 Từ Trở Lên!!!", font=("Helvetica", 14),
                               wraplength=400)
        self.glabel.pack(pady=20)

    def validate_selected_vocabulary(self, en, st):
        if (en - st) < 4 or st > en:
            messagebox.showerror("Lỗi", "Bạn hãy nhập lại từ vựng bắt đầu hoặc từ vựng kết thúc")
            return False
        return True

    def findse(self,lines,word):
        en = len(lines)
        for idx, line in enumerate(lines):
            if word.strip() in line.strip() and "##*###**" in line.strip():
                st = idx
                break
        for idx, line in enumerate(lines[st+1:]):
            if "##*###**" in line.strip():
                en = idx
                break
        #print(f"{st}")
        #print(f"{en}")
        en = en + st
        #print(f"//{en}")
        return st,en

    def load_flashcard(self):
        try:
            start_position = int(self.start_position_entry.get())
            end_position = int(self.end_position_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số từ vựng và vị trí bắt đầu là số nguyên.")
            return
        if not self.validate_selected_vocabulary(end_position, start_position):
            return
        lines = self.vocab
        #print(lines)
        s = min(start_position, len(lines)-1)
        e = min(end_position, len(lines)-1)
        lines = lines[s:e+1]
        print(lines)
        #print(lines)
        with open("datastorage/tempv.txt", "w", encoding="utf-8") as file:
            for word, meaning in lines:
                file.write(f"{word}:{meaning}\n")

        self.root.destroy()
        multiplechoice_root = CTk()
        multiplechoice = Multichoice(multiplechoice_root, lines)
        multiplechoice_root.mainloop()
class AutoOpenNewApp(CTkToplevel):
    def __init__(self, vocabulary,word):
        super().__init__()
        self.title("Add vocab")
        self.geometry("800x710+300+50")
        #self.config(bg="red")
        self.vocabulary = vocabulary
        self.title = word
        #print(self.start)
        #print(self.end)
        #print(self.vocabulary)
        try:
            icon_path = "images/icon.ico"
            self.iconbitmap(default=icon_path)
        except Exception as e:
            print(e)
        self.items = []
        self.create_widgets()
    def create_widgets(self):
        CTkLabel(self, text="Word:", font=("Helvetica", 34)).grid(row=0, column=0, sticky="w")
        self.program_name_var = tk.StringVar()
        self.program_name_entry = CTkEntry(self, width=480, textvariable=self.program_name_var)
        self.program_name_entry.grid(row=0, column=1, columnspan=3)
        CTkLabel(self, text="Meaning:", font=("Helvetica", 34)).grid(row=1, column=0, sticky="w")
        self.file_path_var = tk.StringVar()
        self.file_path_entry = CTkEntry(self, width=480, textvariable=self.file_path_var)
        self.file_path_entry.grid(row=1, column=1, columnspan=3)
        CTkButton(self, text="+", command=self.add_to_listbox, corner_radius=50, font=("Helvetica", 34)).grid(row=0,
                                                                                                              column=6,
                                                                                                              padx=10,
                                                                                                              pady=10)
        CTkButton(self, text="Quick Add+", command=self.quick_add, corner_radius=34, border_color="#0080FF",
                  border_width=2, fg_color="transparent", font=("Helvetica", 14)).grid(row=2, column=6)
        CTkButton(self, text="Learn", command=self.set, corner_radius=34, border_color="#F92E2E", text_color="#F92E2E",
                  border_width=2, fg_color="transparent", font=("Helvetica", 14)).grid(row=2, column=0, padx=10)
        self.listbox = tk.Listbox(self, width=50, height=20, font=("Helvetica", 20))
        self.listbox.grid(row=3, column=0, columnspan=7, padx=10, pady=5)
        CTkButton(self, text="Delete", command=self.delete_file, corner_radius=34, border_color="#0080FF",
                  border_width=2, fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=0, pady=5)
        CTkButton(self, text="Refresh", command=self.refresh_app, corner_radius=34, border_color="#0080FF",
                  border_width=2, fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=6, pady=5)
        CTkButton(self, text="Translate", command=self.tranlate, corner_radius=34, border_color="#0080FF",
                  border_width=2, fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=3, pady=5)
        CTkButton(self, text="Edit", command=self.edit_vocabulary, corner_radius=34, border_color="#0080FF",
                  border_width=2, fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=1, pady=5)
        try:
            self.load_data()
        except Exception as e:
            pass
    def load(self):
        self.listbox.delete(0, tk.END)
        for index, item in enumerate(self.vocabulary, start=0):
            #print(len(self.vocabulary))
            #print(self.vocabulary)
            if ':' in item:
                word, meaning = item.split(":")
                self.listbox.insert(tk.END, f"{index}. {word.strip()} : {meaning.strip()}")
            else:
                print(item)
    def quick_add(self):
        quick_add_window = tk.Toplevel(self)
        quick_add_window.title("Quick Add")
        initial_content = "Word1:Mean1\nWord2:Mean2\nWord3:Mean3"
        text_area = tk.Text(quick_add_window, height=10, width=40)
        text_area.insert(tk.END, initial_content)
        text_area.pack()
        def add_text():
            text = text_area.get("1.0", "end-1c")
            if text:
                # print(text)
                with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
                st, en = self.findse(lines, self.title)
                if lines[en].strip():
                    lines.insert(en, text)
                else:
                    lines.insert(en - 1, text)
                with open("datastorage/vlist.txt", "w", encoding="utf-8") as file:
                    file.writelines(lines)
                self.load_data()
                quick_add_window.destroy()
        ok_button = tk.Button(quick_add_window, text="OK", command=add_text, font=("Helvetica", 14))
        ok_button.pack()

    def set(self):
        print("----------")
        print(self.data())
        print("----------")
        askr = CTk()
        ask = Asknew(askr,self.data())
        askr.mainloop()
        #pass
    def findse(self,lines,word):
        en = len(lines)
        for idx, line in enumerate(lines):
            if word.strip() in line.strip() and "##*###**" in line.strip():
                st = idx
                break
        for idx, line in enumerate(lines[st+1:]):
            if "##*###**" in line.strip():
                en = idx
                break
        #print(f"{st}")
        #print(f"{en}")
        en = en + st
        #print(f"//{en}")
        return st,en
    def add_to_listbox(self):
        #print("1")
        word = self.program_name_var.get()
        print(word)
        mean = self.file_path_var.get()
        print(mean)
        #print(f"{word} and {mean}")
        #self.load_data()
        if word and mean:
            new_line =f"{word}:{mean}\n"
            # le = f"{word} : {mean}"
            self.listbox.insert(tk.END, new_line)
            self.vocabulary.append((word, mean))
            with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            #print(self.end)
            #print(self.start)
            st,en = self.findse(lines,self.title)
            print(st)
            print(en)
            if lines[en].strip():
                lines.insert(en, new_line)
            else:
                lines.insert(en-1, new_line)
            with open("datastorage/vlist.txt", "w", encoding="utf-8") as file:
                file.writelines(lines)
            self.program_name_var.set('')
            self.file_path_var.set('')
            self.load_data()
        #self.load_data()
    def tranlate(self):
        self.transl_window = tk.Toplevel(self)
        trans = Transl(self.transl_window)
    def edit_vocabulary(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            selected_item_index = selected_item[0]
            selected_item_text = self.listbox.get(selected_item_index)
            selected_word = selected_item_text.split(":")[0].strip()
            if '.' in selected_word:
                selected_word = selected_word.split('.')[1].strip()
            current_meaning = selected_item_text.split(":")[1].strip()
            new_word = simpledialog.askstring("Chỉnh sửa", f"Chỉnh sửa từ '{selected_word}':",initialvalue=selected_word)
            new_meaning = simpledialog.askstring("Chỉnh sửa", f"Chỉnh sửa nghĩa cho '{current_meaning}':",initialvalue=current_meaning)
            if new_word is not None and new_meaning is not None:
                with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
                st, en = self.findse(lines, self.title)
                new = lines[st:en]
                # print(new)
                for idx, line in enumerate(new, start=0):
                    if current_meaning in line:
                        new[idx] = f"{new_word}:{new_meaning}\n"
                        # print(line)
                        break
                newlin = lines[:st] + new + lines[en:]
                # lines[selected_item_index + 1] = f"{new_word}:{new_meaning}\n"
                with open("datastorage/vlist.txt", "w", encoding="utf-8") as file:
                    file.writelines(newlin)
                # new_item_text = f"{new_word} : {new_meaning}"
                # self.listbox.delete(selected_item_index)
                # self.listbox.insert(selected_item_index, new_item_text)
                self.load_data()
    def delete_file(self):
        selected_index = self.listbox.curselection()
        #print(selected_index)
        if selected_index:
            #self.load_data()
            selected_item_index = selected_index[0]
            selected_item_text = self.listbox.get(selected_item_index)
            #print(selected_item_text)
            selected_word = selected_item_text.split(":")[1].strip()
            #print(selected_word)
            file_path = 'datastorage/vlist.txt'
            self.listbox.delete(selected_index)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                st,en = self.findse(lines,self.title)
                new = lines[st:en]
                #print(new)
                for idx,line in enumerate(new,start=0):
                    if selected_word in line:
                        del new[idx]
                        #print(line)
                        break
                #print(new)
                newlin = lines[:st]+new+lines[en:]
                #print(newlin)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(newlin)
                #print(f"Đã xóa dòng: {deleted_line.strip()} từ tệp {file_path}")
            except FileNotFoundError:
                print(f"Tệp {file_path} không tồn tại.")
            except Exception as e:
                print(f"Lỗi: {e}")
            self.load_data()
    def refresh_app(self):
        pass
        #self.load_data()
    def findse(self,lines,word):
        en = len(lines)
        for idx, line in enumerate(lines):
            if word in line and "##*###**" in line:
                st = idx
                break
        for idx, line in enumerate(lines[st+1:]):
            if "##*###**" in line:
                en = idx
                break
        #print(f"{st}")
        #print(f"{en}")
        en = en + st
        #print(f"//{en}")
        return st,en
    def load_data(self):
        self.listbox.delete(0, tk.END)
        try:
            with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            st,en = self.findse(lines,self.title)
            newlines = lines[st:en]
            for index,line in enumerate(newlines, start=1):
                if ":" in line:
                    name, file_path = line.split(":")
                    file_path = file_path.strip()
                    name = name.strip()
                    self.vocabulary.append((name, file_path))
                    self.listbox.insert(tk.END, f"{index}. {name} : {file_path}")  # Add index
        except FileNotFoundError:
            pass
    def data(self):
        try:
            vo = []
            with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            st,en = self.findse(lines,self.title)
            newlines = lines[st:en]
            #print(newlines)
            for index,line in enumerate(newlines, start=1):
                if ":" in line:
                    name, file_path = line.split(":")
                    file_path = file_path.strip()
                    name = name.strip()
                    vo.append((name, file_path))
            return vo
        except FileNotFoundError:
            pass

    def run(self):
        self.mainloop()
class Changelist(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Change Vocab List")
        self.geometry("400x330+700+560")
        self.attributes('-topmost', True)
        self.listbox = tk.Listbox(self, width=25, height=7, font=("Helvetica", 20))
        self.listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.load()

        study_button = tk.Button(self, text="Open", command=self.study_action, font=("Helvetica", 14))
        open_button = tk.Button(self, text="Add new", command=self.open_action, font=("Helvetica", 14))
        edit_button = tk.Button(self, text="Edit", command=self.edit_action, font=("Helvetica", 14))
        delete_button = tk.Button(self, text="Delete", command=self.delete_action, font=("Helvetica", 14))

        study_button.grid(row=1, column=0, padx=10, pady=10)
        open_button.grid(row=1, column=1, padx=10, pady=10)
        edit_button.grid(row=1, column=2, padx=10, pady=10)
        delete_button.grid(row=1, column=3, padx=10, pady=10)

    def load(self):
        self.listbox.delete(0, tk.END)
        with open("datastorage/nlist.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            self.listbox.insert(tk.END, line.strip())

    def study_action(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            selected_item_index = selected_item[0]
            selected_item_text = self.listbox.get(selected_item_index)
            with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                lin = file.readlines()
            st,en = self.findse(lin, selected_item_text)
            vocab = lin[st+1:en]
            #print(vocab)
            app = AutoOpenNewApp(vocab,selected_item_text)
            app.run()

    def open_action(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            name = simpledialog.askstring("Add Name", "Enter a name:")
            if name:
                self.listbox.insert(tk.END, name)
                with open("datastorage/nlist.txt", "a", encoding="utf-8") as file:
                    file.write(name+"\n")
                with open(file_path, "r", encoding="utf-8") as source_file:
                    lines = source_file.readlines()
                data = [line for line in lines if line.strip() and line.count(":") <= 1]
                with open("datastorage/vlist.txt", "a", encoding="utf-8") as target_file:
                    target_file.write("##*###**" + name + "\n")
                    target_file.writelines(data)
                    target_file.write("\n\n\n")
                with open("datastorage/pos.txt", "a", encoding="utf-8") as file:
                    file.write("0\n")
    def edit_action(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            selected_item_index = selected_item[0]
            selected_item_text = self.listbox.get(selected_item_index)
            new_word = simpledialog.askstring("Chỉnh sửa", f"Chỉnh sửa tên '{selected_item_text}':",
                                              initialvalue=selected_item_text)
            if new_word is not None:
                with open("datastorage/nlist.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
                lines[selected_item_index] = f"{new_word}\n"
                with open("datastorage/nlist.txt", "w", encoding="utf-8") as file:
                    file.writelines(lines)
                with open("datastorage/vlist.txt", "r", encoding="utf-8") as f:
                    lin = f.readlines()
                for index, line in enumerate(lin):
                    if selected_item_text.strip() in line.strip() and "##*###**" in line.strip():
                        lin[index]=f"##*###**{new_word}\n"
                        break
                with open("datastorage/vlist.txt", "w", encoding="utf-8") as f:
                    f.writelines(lin)
                self.load()
    def findse(self,lines,word):
        en = len(lines)
        for idx, line in enumerate(lines):
            if word.strip() in line.strip() and "##*###**" in line.strip():
                st = idx
                break
        for idx, line in enumerate(lines[st+1:]):
            if "##*###**" in line.strip():
                en = idx
                break
        #print(f"{st}")
        #print(f"{en}")
        en = en + st
        #print(f"//{en}")
        return st,en
    def delete_action(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            selected_item_index = selected_item[0]
            selected_item_text = self.listbox.get(selected_item_index)
            with open("datastorage/nlist.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            new_lines = lines[:selected_item_index] + lines[selected_item_index + 1:]
            with open("datastorage/nlist.txt", "w", encoding="utf-8") as file:
                file.writelines(new_lines)
            with open("datastorage/pos.txt", "r", encoding="utf-8") as file:
                lin = file.readlines()
            new_lines = lin[:selected_item_index] + lin[selected_item_index + 1:]
            with open("datastorage/pos.txt", "w", encoding="utf-8") as file:
                file.writelines(new_lines)
            with open("datastorage/vlist.txt", "r", encoding="utf-8") as file:
                lin = file.readlines()
            st,en = self.findse(lin, selected_item_text)
            new_lines = lin[:st] + lin[en + 1:]
            with open("datastorage/vlist.txt", "w", encoding="utf-8") as file:
                file.writelines(new_lines)
            self.load()
class AutoOpenApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Add vocab")
        self.geometry("800x710+400+50")
        #self.config(bg="grey")
        try:
            icon_path = "images/icon.ico"
            self.iconbitmap(default=icon_path)
        except Exception as e:
            print(e)
        self.items = []
        self.create_widgets()
    def create_widgets(self):
        CTkLabel(self, text="Word:", font=("Helvetica", 34)).grid(row=0, column=0, sticky="w")
        self.program_name_var = tk.StringVar()
        self.program_name_entry = CTkEntry(self, width=480, textvariable=self.program_name_var)
        self.program_name_entry.grid(row=0, column=1, columnspan=3)
        CTkLabel(self, text="Meaning:", font=("Helvetica", 34)).grid(row=1, column=0, sticky="w")
        self.file_path_var = tk.StringVar()
        self.file_path_entry = CTkEntry(self, width=480, textvariable=self.file_path_var)
        self.file_path_entry.grid(row=1, column=1, columnspan=3)
        CTkButton(self, text="+", command=self.add_to_listbox,corner_radius=50, font=("Helvetica", 34)).grid(row=0, column=6,padx=10,pady=10)
        CTkButton(self, text="Quick Add+", command=self.quick_add,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 14)).grid(row=2, column=6)
        CTkButton(self, text="Train", command=self.set,corner_radius=34,border_color="#F92E2E",text_color="#F92E2E",border_width=2,fg_color="transparent", font=("Helvetica", 14)).grid(row=2, column=0, padx=10)
        self.listbox = tk.Listbox(self, width=50, height=20, font=("Helvetica", 20))
        self.listbox.grid(row=3, column=0, columnspan=7,padx= 10,pady = 5)
        CTkButton(self, text="Delete", command=self.delete_file,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=0,pady=5)
        CTkButton(self, text="Change List", command=self.changevocablist,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=2)
        CTkButton(self, text="Refresh", command=self.refresh_app,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=6,pady=5)
        CTkButton(self, text="Translate", command=self.tranlate,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=3,pady=5)
        CTkButton(self, text="Edit", command=self.edit_vocabulary,corner_radius=34,border_color="#0080FF",border_width=2,fg_color="transparent", font=("Helvetica", 25)).grid(row=8, column=1,pady=5)
        try:
            self.load_data()
        except Exception as e:
            pass
        self.checkok()
        print(self.items)
    def checkok(self):
        if int(datetime.datetime.now().weekday()) != 6:
            with open("datastorage/checkchange.txt", "w", encoding="utf-8") as file:
                pass
    def checkend(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if int(datetime.datetime.now().weekday()) == 6:
            with open('datastorage/checkchange.txt', "r") as log_file:
                logged_dates = log_file.read().splitlines()
            if current_date not in logged_dates:
                with open("datastorage/tempv.txt", "r", encoding="utf-8") as file:
                    temp = file.readlines()
                with open("datastorage/learn.txt", "a", encoding="utf-8") as file1:
                    file1.writelines(temp)
                with open("datastorage/tempv.txt", "w", encoding="utf-8") as filen:
                    pass
                with open("datastorage/checkchange.txt", "w", encoding="utf-8") as file:
                    file.write(datetime.datetime.now().strftime("%Y-%m-%d"))
    def changevocablist(self):
        cl = Changelist()
        cl.mainloop()

    def quick_add(self):
        quick_add_window = tk.Toplevel(self)
        quick_add_window.title("Quick Add")
        quick_add_window.geometry("400x250+1000+50")
        initial_content = "Word1:Mean1\nWord2:Mean2\nWord3:Mean3"
        text_area = tk.Text(quick_add_window, height=10, width=40)
        text_area.insert(tk.END, initial_content)
        text_area.pack()
        def add_text():
            text = text_area.get("1.0", "end-1c")
            if text:
                #print(text)
                with open("datastorage/tempv.txt", "a", encoding="utf-8") as file:
                    file.write(text + "\n")
                self.load_data()
                quick_add_window.destroy()
        ok_button = tk.Button(quick_add_window, text="OK", command=add_text, font=("Helvetica", 14))
        ok_button.pack()

    def set(self):
        if self.items != []:
            # print(self.items)
            askr = CTk()
            ask = Ask(askr)
            askr.mainloop()
        else:
            return
    def add_to_listbox(self):
        word = self.program_name_var.get()
        mean = self.file_path_var.get()
        #print(f"{word} and {mean}")
        #print(type(word))
        self.load_data()
        if word and mean:
            entry = f"{word}:{mean}"
            # le = f"{word} : {mean}"
            self.listbox.insert(tk.END, entry)
            self.items.append((word, mean))  # Thêm mục vào danh sách
            with open("datastorage/tempv.txt", "a", encoding="utf-8") as file:
                file.write(f"{entry}\n")
            self.program_name_var.set('')
            self.file_path_var.set('')
        self.load_data()
    def tranlate(self):
        self.transl_window = tk.Toplevel(self)
        trans = Transl(self.transl_window)
    def edit_vocabulary(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            selected_item_index = selected_item[0]
            selected_item_text = self.listbox.get(selected_item_index)
            selected_word = selected_item_text.split(":")[0].strip()
            if '.' in selected_word:
                selected_word = selected_word.split('.')[1].strip()
            current_meaning = selected_item_text.split(":")[1].strip()
            new_word = simpledialog.askstring("Chỉnh sửa", f"Chỉnh sửa từ '{selected_word}':",initialvalue=selected_word)
            new_meaning = simpledialog.askstring("Chỉnh sửa", f"Chỉnh sửa nghĩa cho '{selected_word}':",initialvalue=current_meaning)
            if new_word is not None and new_meaning is not None:
                with open("datastorage/learn.txt", "r", encoding="utf-8") as file:
                    lines = file.readlines()
                with open("datastorage/tempv.txt", "r", encoding="utf-8") as file1:
                    lines1 = file1.readlines()
                try:
                    lines[selected_item_index] = f"{new_word}:{new_meaning}\n"
                    with open("datastorage/learn.txt", "w", encoding="utf-8") as file:
                        file.writelines(lines)
                except Exception as e:
                    lines1[selected_item_index- len(lines)] = f"{new_word}:{new_meaning}\n"
                    with open("datastorage/tempv.txt", "w", encoding="utf-8") as file1:
                        file1.writelines(lines1)
                new_item_text = f"{new_word} : {new_meaning}"
                self.listbox.delete(selected_item_index)
                self.listbox.insert(selected_item_index, new_item_text)
                self.load_data()
    def delete_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.load_data()
            if selected_index:
                self.listbox.delete(selected_index)
            file_path = 'datastorage/learn.txt'
            line_number = selected_index[0]
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            with open("datastorage/tempv.txt", "r", encoding="utf-8") as file1:
                lines1 = file1.readlines()
            #print(lines[line_number + 1])
            #print(line_number)
            #print(line_number - len(lines))
            try:
                deleted_line = lines.pop(line_number)
            except Exception as e:
                deleted_line = lines1.pop(line_number - len(lines))
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            with open("datastorage/tempv.txt", "w", encoding="utf-8") as file1:
                file1.writelines(lines1)
            print(f"Đã xóa dòng: {deleted_line.strip()} từ tệp {file_path}")
            self.load_data()
    def refresh_app(self):
        self.load_data()
    def load_data(self):
        self.checkend()
        self.listbox.delete(0, tk.END)
        try:
            with open("datastorage/learn.txt", "r", encoding="utf-8") as file:
                line = file.readlines()
            with open("datastorage/tempv.txt", "r", encoding="utf-8") as file:
                lines1 = file.readlines()
            lines = line + lines1
            for index, line in enumerate(lines, start=1):
                #print(line)
                if ':' in line:
                    name, file_path = line.strip().split(":")
                    file_path = file_path.strip()
                    self.items.append((name, file_path))
                    self.listbox.insert(tk.END, f"{index}. {name} : {file_path}")

        except FileNotFoundError:
            pass


    def run(self):
        self.mainloop()
if __name__ == "__main__":
    #vocabulary = [('tasty', 'ngon'), ('爸爸', 'father (bàba)'), ('北京', 'Beijing (běijīng)'), ('上', 'upper, up side (shàng)'), ('fizzy', 'có ga')]
    #multiplechoice_root = CTk()
    #multiplechoice = Listen(multiplechoice_root, vocabulary,10,5)
    #multiplechoice_root.mainloop()
    app = AutoOpenApp()
    app.mainloop()