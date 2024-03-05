from tkinter import Tk, Frame, Label, Checkbutton, Button,Scrollbar,W, RIGHT, StringVar, Canvas,ALL, BOTH, VERTICAL

# Sample data (replace with your actual array)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def update_canvas_size(event):
    # Update the scroll region to encompass the frame
    canvas.configure(scrollregion=canvas.bbox("all"))

def submit(data):
    for i in range(len(checkbox_vars)):
        data[i]["checked"] = checkbox_vars[i].get()
    # for item in data:
    #     print(item)
    root.destroy()

# Initialize the main window
root = Tk()
root.title("Job Listings")

def openGUI(data):

    for i, item in enumerate(data):
        # Create checkbox variable
        var = StringVar(frame, value="0")  # Initial value set to checked
        checkbox_vars.append(var)  # Add the StringVar to the list

        # Create checkbutton
        checkbutton = Checkbutton(frame, text=f"", variable=var )
        checkbutton.grid(row=i, column=0, sticky="w")

        # Display other job details
        for j, (key, value) in enumerate(item.items()):
            if key not in ["checked","link"]:  # Exclude "checked" property
                label = Label(frame, text=f"{value}", padx=0, pady=0, wraplength=200, justify='left')
                label.grid(row=i, column=j+1, sticky="w")

    submit_frame = Frame(root)
    submit_frame.pack(side="bottom", fill="x")


    submit_button = Button(submit_frame, text="Submit", command=lambda:submit(data))
    submit_button.pack(side=RIGHT, padx=10, pady=10)
    root.mainloop()


canvas = Canvas(root)
canvas.pack(side="left",fill=BOTH, expand=True)
vscrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
vscrollbar.pack(side=RIGHT, fill='y')
canvas.configure(yscrollcommand=vscrollbar.set)
frame = Frame(canvas)
frame.pack(fill=BOTH, expand=True)
canvas.create_window((0, 0), window=frame, anchor="nw")
# Bind the event to update the canvas size when the frame's size changes
frame.bind("<Configure>", update_canvas_size)
# Set a fixed height for the canvas
canvas.config(height=300, width=750)
canvas.bind_all("<MouseWheel>", on_mousewheel)

checkbox_vars = []



