import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.current_file = None

        # Create Text Widget
        self.text_area = tk.Text(root, wrap='none', undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        # Create Scrollbars
        self.scroll_y = tk.Scrollbar(self.text_area, orient=tk.VERTICAL, command=self.text_area.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_x = tk.Scrollbar(self.text_area, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.config(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Create Menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.edit_menu.add_command(label="Select All", command=lambda: self.text_area.event_generate("<<SelectAll>>"))

        self.format_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.choose_font)
        self.format_menu.add_command(label="Color Scheme", command=self.choose_color_scheme)

        self.view_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Line Numbers", command=self.toggle_line_numbers)
        self.view_menu.add_command(label="Syntax Highlighting", command=self.syntax_highlighting)

        self.line_numbers = tk.Text(root, width=4, padx=4, takefocus=0, border=0, background='lightgrey', state='disabled')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area.bind("<KeyRelease>", self.update_line_numbers)

        self.font_family = "Courier"
        self.font_size = 12
        self.text_area.config(font=(self.font_family, self.font_size))

    def new_file(self):
        self.current_file = None
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        self.current_file = filedialog.askopenfilename(defaultextension=".txt",
                                                       filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.current_file:
            self.text_area.delete(1.0, tk.END)
            with open(self.current_file, "r") as file:
                self.text_area.insert(1.0, file.read())
            self.root.title(os.path.basename(self.current_file) + " - Text Editor")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        self.current_file = filedialog.asksaveasfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(os.path.basename(self.current_file) + " - Text Editor")

    def exit_app(self):
        self.root.quit()

    def choose_font(self):
        font_choice = font.Font(font=self.text_area['font'])
        font_window = tk.Toplevel(self.root)
        font_window.title("Choose Font")
        
        tk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=10, pady=5)
        font_family_var = tk.StringVar(value=self.font_family)
        tk.OptionMenu(font_window, font_family_var, *font.families()).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=5)
        font_size_var = tk.IntVar(value=self.font_size)
        tk.Spinbox(font_window, from_=8, to=72, textvariable=font_size_var).grid(row=1, column=1, padx=10, pady=5)
        
        def apply_font():
            self.font_family = font_family_var.get()
            self.font_size = font_size_var.get()
            self.text_area.config(font=(self.font_family, self.font_size))
            font_window.destroy()
        
        tk.Button(font_window, text="Apply", command=apply_font).grid(row=2, column=0, columnspan=2, pady=10)

    def choose_color_scheme(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(bg=color)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        row, col = self.text_area.index("end").split('.')
        for i in range(1, int(row)):
            self.line_numbers.insert(tk.END, f"{i}\n")
        
        self.line_numbers.config(state='disabled')

    def toggle_line_numbers(self):
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    def syntax_highlighting(self):
        keywords = ["def", "import", "from", "class", "if", "else", "elif", "return"]
        for keyword in keywords:
            self.highlight_pattern(keyword, "keyword", "blue")

    def highlight_pattern(self, pattern, tag, color):
        start = 1.0
        while True:
            start = self.text_area.search(pattern, start, tk.END)
            if not start:
                break
            end = f"{start}+{len(pattern)}c"
            self.text_area.tag_add(tag, start, end)
            start = end
        self.text_area.tag_config(tag, foreground=color)

if __name__ == "__main__":
    root = tk.Tk()
    te = TextEditor(root)
    root.mainloop()

