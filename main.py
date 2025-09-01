import tkinter as tk
from tkinter import messagebox


class FlatButton(tk.Canvas):
    """Кнопка без градиента, с анимацией нажатия (iOS6-like)."""
    def __init__(self, parent, text, command=None,
                 color="#333333", text_color="white",
                 **kwargs):
        super().__init__(parent, width=70, height=60,
                         highlightthickness=0, bd=0, relief="flat", **kwargs)

        self.command = command
        self.text = text
        self.base_color = color
        self.pressed_color = "#111111"
        self.text_color = text_color

        # фон
        self.rect = self.create_rectangle(0, 0, 70, 60,
                                          fill=self.base_color, outline="#000000")

        # текст
        self.label = self.create_text(35, 30, text=text,
                                      fill=text_color,
                                      font=("Helvetica", 18, "bold"))

        # события
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        """Анимация при нажатии"""
        self.itemconfig(self.rect, fill=self.pressed_color)
        self.move(self.label, 0, 2)  # текст опускается чуть ниже

    def on_release(self, event):
        """Возврат после нажатия"""
        self.itemconfig(self.rect, fill=self.base_color)
        self.move(self.label, 0, -2)  # текст возвращается
        if self.command:
            self.command(self.text)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("iOS6 Calculator")
        self.configure(bg="#000000")
        self.geometry("320x480")
        self.resizable(False, False)

        self.expression = ""

        # экран
        self.entry = tk.Entry(self, font=("Helvetica", 28, "bold"),
                              borderwidth=0, relief="flat", justify="right",
                              bg="#fef9e7", fg="black")
        self.entry.pack(fill="x", padx=10, pady=10, ipady=15)

        frame = tk.Frame(self, bg="#000000")
        frame.pack(expand=True, fill="both")

        # цвета кнопок
        button_styles = {
            "memory": "#555555",
            "function": "#666666",
            "digit": "#333333",
            "op": "#666666",
            "equal": "#ff9500",
        }

        buttons = [
            [("mc", "memory"), ("m+", "memory"), ("m-", "memory"), ("mr", "memory")],
            [("AC", "function"), ("±", "function"), ("÷", "function"), ("×", "function")],
            [("7", "digit"), ("8", "digit"), ("9", "digit"), ("-", "op")],
            [("4", "digit"), ("5", "digit"), ("6", "digit"), ("+", "op")],
            [("1", "digit"), ("2", "digit"), ("3", "digit"), ("=", "equal")],
            [("0", "digit"), (".", "digit")]
        ]

        for r, row in enumerate(buttons):
            for c, (text, style) in enumerate(row):
                btn = FlatButton(frame, text=text,
                                 color=button_styles[style],
                                 command=self.on_click)

                if text == "0":
                    btn.grid(row=r, column=c, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif text == "=":
                    btn.grid(row=r, column=c, rowspan=2, sticky="nsew", padx=2, pady=2)
                else:
                    btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # растягиваем сетку
        for i in range(6):
            frame.rowconfigure(i, weight=1)
        for j in range(4):
            frame.columnconfigure(j, weight=1)

    def on_click(self, char):
        if char == "AC":
            self.expression = ""
            self.update_entry()
        elif char == "=":
            self.calculate()
        elif char == "±":
            if self.expression and self.expression[0] == "-":
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.update_entry()
        elif char in {"×"}:
            self.expression += "*"
            self.update_entry()
        elif char in {"÷"}:
            self.expression += "/"
            self.update_entry()
        elif char in {"mc", "m+", "m-", "mr"}:
            messagebox.showinfo("Память", f"Функция {char} не реализована :)")
        else:
            self.expression += str(char)
            self.update_entry()

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.expression = result
            self.update_entry()
        except Exception:
            messagebox.showerror("Ошибка", "Неверное выражение")
            self.expression = ""
            self.update_entry()


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
