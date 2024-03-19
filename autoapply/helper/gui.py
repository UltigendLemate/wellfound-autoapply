from tkinter import Tk, Frame, Label, Checkbutton, Button, Scrollbar, StringVar, Canvas, RIGHT, BOTH, VERTICAL

class GUI:
    def __init__(self, data):
        self.root = Tk()
        self.root.title("Job Listings")

        self.canvas = Canvas(self.root)
        self.canvas.pack(side="left", fill=BOTH, expand=True)
        self.vscrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.vscrollbar.pack(side=RIGHT, fill='y')
        self.canvas.configure(yscrollcommand=self.vscrollbar.set)
        self.frame = Frame(self.canvas)
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
        for i, item in enumerate(data):
            var = StringVar(self.frame, value="0")
            self.checkbox_vars.append(var)

            checkbutton = Checkbutton(self.frame, text=f"", variable=var)
            checkbutton.grid(row=i, column=0, sticky="w")

            for j, (key, value) in enumerate(item.items()):
                if key not in ["checked", "link"]:
                    label = Label(self.frame, text=f"{value}", padx=0, pady=0, wraplength=200, justify='left')
                    label.grid(row=i, column=j + 1, sticky="w")

        submit_frame = Frame(self.root)
        submit_frame.pack(side="bottom", fill="x")

        submit_button = Button(submit_frame, text="Submit", command=lambda: self.submit(data))
        submit_button.pack(side=RIGHT, padx=10, pady=10)
        self.root.mainloop()
