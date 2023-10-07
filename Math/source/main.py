from tkinter import PhotoImage
from customtkinter import *
import tkinter as tk
import math
import time
import threading

class App:
    try:
        def __init__(self, root):
            self.root = root
            self.root.title("PHT")
            self.root.geometry("800x600+430+90")
            self.canvas = CTkCanvas(self.root, width=1300, height=900)
            self.canvas.pack()

            self.background_image = PhotoImage(file="img/wall.png")

            self.canvas.create_image(0, 0, anchor=NW, image=self.background_image)

            self.ok_button = CTkButton(self.canvas, text="OK", font=("Ariel", 24, "italic"),
                                       command=self.on_ok_button_click)
            self.ok_button.place(relx=0.5, rely=0.8, anchor=CENTER)

        def on_ok_button_click(self):
            self.root.destroy()
            root = CTk()
            app = NApp(root)
            root.mainloop()
    except Exception as e:
        print(e)


class NApp:
    try:
        def __init__(self, root):
            self.root = root
            # self.root.config(bg="#B1DDC6")
            self.root.title("PHT")
            self.root.geometry("1330x550+100+100")
            self.frame = CTkFrame(root)
            self.frame.pack()
            self.image_label = tk.Label(self.frame)
            self.image_label.grid(row=1, column=0, padx=10, pady=10)
            self.image_path = "img/1.png"
            self.image = PhotoImage(file=self.image_path)
            self.image_label.configure(image=self.image)
            self.text_label = CTkLabel(self.frame, text="Đề bài:", font=("Arial", 25))
            self.text_label.grid(row=0, column=1)
            self.initial_text = "Bài toán:\nMột vị khách du lịch đến một ngọn núi thì từ xa thấy một ngọn núi cao hùng vĩ có độ cao A km. Từ vị trí cách tâm núi B km ông thấy được một ngôi chùa cổ.Ông rất tò \nmò về chiều cao của ngôi chùa đó và đã hỏi rất nhiều \nngười dẫn nhưng vẫn chưa tìm được câu trả lời. Biết \ngóc nhìn tạo bởi ánh mắt của ông đến đỉnh ngôi chùa \nvà chân ngôi chùa là C°. Hãy tìm giúp ông chiều cao \ncủa ngôi chùa đó mà không cần dùng đến nhiều thiết bị đo, chỉ dùng máy tính là đủ."
            self.text_area2 = CTkTextbox(self.frame, height=430, width=650, font=("Arial", 25),
                                         scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70",
                                         border_width=2)
            self.text_area2.grid(row=1, column=1)
            self.text_area2.insert(tk.END, self.initial_text)
            self.text_area2.configure(state=DISABLED)
            self.entry1 = CTkEntry(self.root, width=120, height=50, font=("Arial", 17),
                                   placeholder_text="Chiều cao núi", text_color="#FFFF00")
            self.entry2 = CTkEntry(self.root, width=120, height=50, font=("Arial", 17), placeholder_text="Khoảng cách",
                                   text_color="#FFFF00")
            self.entry3 = CTkEntry(self.root, width=120, height=50, font=("Arial", 17), placeholder_text="Góc nhìn",
                                   text_color="#FFFF00")
            self.entry1.pack(side=tk.LEFT, padx=30, pady=10)
            self.entry2.pack(side=tk.LEFT, padx=30, pady=10)
            self.entry3.pack(side=tk.LEFT, padx=30, pady=10)
            self.ok_button = CTkButton(self.root, corner_radius=34, fg_color="transparent", hover_color="#4158D0",
                                       border_color="#FF3333", border_width=2, text="OK", font=("Arial", 25),
                                       command=self.calculate)
            self.ok_button.pack(padx=30, pady=20)

        def is_numeric(self, value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        def calculate(self):
            self.ok_button.configure(state=DISABLED)
            self.entry1.configure(state=DISABLED)
            self.entry2.configure(state=DISABLED)
            self.entry3.configure(state=DISABLED)
            ccn = self.entry1.get()
            kc = self.entry2.get()
            gn = self.entry3.get()
            if not self.entry3.get() and not self.entry1.get() and not self.entry2.get():
                self.ok_button.configure(state=NORMAL)
                self.entry1.configure(state=NORMAL)
                self.entry2.configure(state=NORMAL)
                self.entry3.configure(state=NORMAL)
                return
            if not self.is_numeric(ccn) or not self.is_numeric(kc) or not self.is_numeric(gn):
                self.ok_button.configure(state=NORMAL)
                self.entry1.configure(state=NORMAL)
                self.entry2.configure(state=NORMAL)
                self.entry3.configure(state=NORMAL)
                return
            self.text_area2.configure(state=NORMAL)
            self.text_area2.delete("1.0", tk.END)
            # print(f"ccn:{ccn},kc:{kc},gn:{gn}")
            ccn = int(ccn)
            kc = int(kc)
            gn = int(gn)
            self.text_label.configure(text="Bài giải:")
            angle_radian = math.radians(gn)
            tan_30_degree = math.tan(angle_radian)
            result = round(((ccn / kc) + tan_30_degree) / (1 - (ccn / kc) * tan_30_degree), 2)
            result1 = abs(round((kc * result), 2))
            BG = f" ▶  Xét △BCD vuông tại C có:\n\n         tan(CDB) = " + str(ccn) + " / " + str(
                kc) + f"\n\n=> tan(CDA) = tan(CDB + BAD) = tan(CDB + " + str(gn) + f"°)\n\n = (tan(CDB) + tan(" + str(
                gn) + f"°)) / (1 - tan(CDB).tan(" + str(gn) + f"°))\n = " + str(
                result) + f"\n\nXét △ACD vuông tại C có:\n   AC = CD.tan(CDA) = " + str(
                result1) + f" km\n\n=> AB = AC - BC = " + str(result1) + f" - " + str(ccn) + f" = " + str(
                round((result1 - ccn), 2)) + f" km.\n   Vậy chiều cao của ngôi chùa là: " + str(
                abs(round((result1 - ccn), 2))) + " km"
            threading.Thread(target=self.append_text_slowly, args=(self.text_area2, BG)).start()
            #self.text_area2.insert(tk.END, BG)

        def append_text_slowly(self, widget, text, delay=0.05):
            try:
                for char in text:
                    widget.insert(tk.END, char)
                    widget.update_idletasks()
                    time.sleep(delay)
                widget.configure(state=DISABLED)
                self.entry1.configure(state=NORMAL)
                self.entry2.configure(state=NORMAL)
                self.entry3.configure(state=NORMAL)
                self.ok_button.configure(state=NORMAL)
                return
            except Exception:
                return
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        root = CTk()
        app = App(root)
        root.mainloop()
    except Exception as e:
        print(e)
