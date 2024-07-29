import tkinter as tk

BG_COLOR = "#2f2e2a"
FG_COLOR = "#ffffff"

root = tk.Tk()
root.configure(bg=BG_COLOR)
root.minsize(800, 480)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

rect_width = 80
rect_height = 100
gap = 20

width = 8 * rect_width + 7 * gap
height = 3* rect_height + 2 * gap
canvas = tk.Canvas(root, width=width, height=height, bg=BG_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0)

# x, y = 0, 0
# for col in range(8):
#     canvas.create_rectangle(x, y, x + rect_width, y + rect_height, fill=BG_COLOR, width=1, outline=FG_COLOR, dash=(10, 5))
#     x += rect_width + gap
    # canvas.create_text(col * width + width // 2, height + height // 2, text="1", font="Helvetica 20 bold", fill="#fff")

x, y = 0, rect_height
for row in range(2):
    for col in range(8):
        canvas.create_rectangle(x, y, x + rect_width, y + rect_height, fill="#800020", width=0)
        canvas.create_text(x + rect_width // 2, y + rect_height // 2, text="1", font="Helvetica 24 bold", fill="#fff")
        x += rect_width + gap
    y += rect_height + gap
    x = 0

root.mainloop()