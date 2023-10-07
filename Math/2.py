from tkinter import PhotoImage
from customtkinter import *
import tkinter as tk
import math
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PHT")
        self.root.geometry("800x600+430+90")

        self.canvas = CTkCanvas(self.root, width=1300, height=900)
        self.canvas.pack()

        self.background_image = PhotoImage(file="wall.png")

        self.canvas.create_image(0, 0, anchor=NW, image=self.background_image)

        self.ok_button = CTkButton(self.canvas, text="OK", font=("Ariel", 24, "italic"), command=self.on_ok_button_click)
        self.ok_button.place(relx=0.5, rely=0.8, anchor=CENTER)

    def on_ok_button_click(self):
        print("Nút OK đã được nhấn!")


class NApp:
    def __init__(self, root):
        self.root = root
        #self.root.config(bg="#B1DDC6")
        self.root.title("Writing")
        self.root.geometry("1330x550+100+100")

        self.frame = CTkFrame(root)
        self.frame.pack()

        self.image_label = tk.Label(self.frame)
        self.image_label.grid(row=1, column=0, padx=10, pady=10)

        self.image_path = "C:/Users/ADMIN/Downloads/1.png"
        self.image = PhotoImage(file=self.image_path)
        self.image_label.configure(image=self.image)

        self.text_label = CTkLabel(self.frame, text="Đề bài:",font=("Arial",25))
        self.text_label.grid(row=0, column=1)

        initial_text = "Bài toán:\nMột vị khách du lịch đến một ngọn núi thì từ xa thấy một ngọn núi cao hùng vĩ có độ cao A km. Từ vị trí cách tâm núi B km ông thấy được một ngôi chùa cổ.Ông rất tò mò về chiều cao của ngôi chùa đó và đã hỏi rất nhiều người dẫn nhưng vẫn chưa tìm được câu trả lời. Biết góc nhìn    tạo  bởi  ánh mắt của ông đến đỉnh ngôi  chùa và chân ngôi chùa là C độ.Hãy tìm giúp ông chiều cao của ngôi  chùa đó mà không cần dùng đến nhiều thiết bị đo,chỉ     dùng máy tính là đủ."
        BG = f"Bài giải:\n▶  Xét △BCD vuông tại C có:\n\n tan(CDB) = BC / BD\n\n=> tan(CDA) = tan(CDB + BAD) = tan(CDB + BAD)\n\n = (tan(CDB) + tan(BAD)) / (1 - tan(CDB).tan(BAD)) = x\n\nXét △ACD vuông tại C:\n\nAC = CD.tan(CDA) = x1\n\n=> AB = AC - BC = x1 - BC = KQ"
        self.text_area2 = tk.Text(self.frame, height=14, width=45,font=("Arial",25))
        self.text_area2.grid(row=1, column=1)
        self.text_area2.insert(tk.END, initial_text)
        self.text_area2.configure(state=DISABLED)

        self.entry1 = CTkEntry(self.root, width=100,placeholder_text="Chiều cao núi")
        self.entry2 = CTkEntry(self.root, width=100,placeholder_text="Khoảng cách")
        self.entry3 = CTkEntry(self.root, width=100,placeholder_text="Góc nhìn")

        self.entry1.pack(side=tk.LEFT,padx=30, pady=10)
        self.entry2.pack(side=tk.LEFT,padx=30, pady=10)
        self.entry3.pack(side=tk.LEFT,padx=30, pady=10)

        self.ok_button = CTkButton(self.root, text="OK", command=self.calculate)
        self.ok_button.pack(padx=30, pady=30)

    def is_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def calculate(self):
        ccn = self.entry1.get()
        kc = self.entry2.get()
        gn = self.entry3.get()
        if not self.entry3.get() and not self.entry1.get() and not self.entry2.get():
            return
        if not self.is_numeric(ccn) or not self.is_numeric(kc) or not self.is_numeric(gn):
            #print("Các giá trị phải là số.")
            return
        self.text_area2.configure(state=NORMAL)
        self.text_area2.delete("1.0", tk.END)
        #print(f"ccn:{ccn},kc:{kc},gn:{gn}")
        ccn = float(ccn)
        kc = float(kc)
        gn = float(gn)
        self.text_label.configure(text="Bài giải:")
        angle_radian = math.radians(gn)

        # Tính giá trị tan(30 độ)
        tan_30_degree = math.tan(angle_radian)

        # Tính giá trị của biểu thức
        result = round(((ccn / kc) + tan_30_degree) / (1 - (ccn / kc) * tan_30_degree), 2)
        result1 = round((kc*result),2)

        BG = f" ▶  Xét △BCD vuông tại C có:\n\n tan(CDB) = ",str(ccn)," / ",{str(kc)},f"\n\n=> tan(CDA) = tan(CDB + BAD) = tan(CDB + ",{str(gn)},f"°)\n\n = (tan(CDB) + tan(",{str(gn)},f"°)) / (1 - tan(CDB).tan(",{str(gn)},f"°))\n = ",{str(result)},f"\n\nXét △ACD vuông tại C:\n\nAC = CD.tan(CDA) = ",{str(result1)},f"\n\n=> AB = AC - BC = ",{str(result1)},f" - ",{str(ccn)},f" = ",{str(round((result1-ccn), 2))}
        self.append_text_slowly(self.text_area2, BG)
        self.text_area2.configure(state=DISABLED)

    def append_text_slowly(widget, text, delay=0.1):
        for char in text:
            widget.configure(state=tk.NORMAL)
            widget.insert(tk.END, char)
            widget.configure(state=tk.DISABLED)
            widget.update()
            time.sleep(delay)


if __name__ == "__main__":
    root = CTk()
    app = NApp(root)
    root.mainloop()
