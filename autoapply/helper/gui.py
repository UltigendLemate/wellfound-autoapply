from tkinter import Tk, Frame, Label, Checkbutton, Button, Scrollbar, StringVar, Canvas, RIGHT, BOTH, VERTICAL, font

class GUI:
    def __init__(self, data):
        self.root = Tk()
        self.root.title("Job Listings")

        self.canvas = Canvas(self.root)
        self.canvas.pack(side="left", fill=BOTH, expand=True)
        self.vscrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.vscrollbar.pack(side=RIGHT, fill='y')
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)
        self.frame = Frame(self.canvas, bg="#f0f0f0")  # Set background color to light gray
        self.frame.pack(fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.update_canvas_size)
        self.canvas.config(height=300, width=750)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.checkbox_vars = []

        self.openGUI(data)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_canvas_size(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def submit(self, data):
        for i in range(len(self.checkbox_vars)):
            data[i]["checked"] = self.checkbox_vars[i].get()
        self.root.destroy()

    def openGUI(self, data):
        bold_font = font.Font(weight="bold")  # Bold font for labels

        for i, item in enumerate(data):
            var = StringVar(self.frame, value="0")
            self.checkbox_vars.append(var)

            checkbutton = Checkbutton(self.frame, variable=var, bg="#f0f0f0", height=2, width=5)  # Increase checkbox size
            checkbutton.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="w")

            for j, (key, value) in enumerate(item.items()):
                if key not in ["checked", "link"]:
                    label = Label(self.frame, text=f"{value}", font=bold_font if j == 0 else None,
                                  padx=5, pady=5, wraplength=200, justify='left', bg="#f0f0f0")  # Set background color to light gray
                    label.grid(row=i, column=j + 1, padx=5, pady=5, sticky="w")

        submit_frame = Frame(self.root, bg="#f0f0f0")  # Set background color to light gray
        submit_frame.pack(side="bottom", fill="x")

        submit_button = Button(submit_frame, text="Submit", command=lambda: self.submit(data), bg="#4CAF50", fg="white")  # Set button color to green and text color to white
        submit_button.pack(side=RIGHT, padx=10, pady=10)
        self.root.mainloop()
