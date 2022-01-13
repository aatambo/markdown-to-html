import tkinter as tk
from tkinter import filedialog, messagebox, font
import ttkbootstrap as ttk
import markdown
import os


class MarkDownEngine(ttk.Labelframe):
    """makes a tkinter frame"""

    def __init__(self, *args, **kwargs):
        """initializes super class and attributes"""
        super().__init__(*args, **kwargs)
        self.config(text='Open File')
        self.btn = {}
        self.text = {}

        # make frame responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # open md button
        self.btn['open'] = ttk.Button(
            self,
            text='Open Markdown',
            command=lambda: self.open_markdown()
        )
        self.btn['open'].grid(row=0, column=0)

        # convert button
        self.btn['convert'] = ttk.Button(
            self,
            text='Convert',
            command=lambda: self.convert_html()
        )
        self.btn['convert'].grid(row=0, column=2)

        # separator
        ttk.Separator(self, orient='vertical').\
            grid(row=0, column=1, rowspan=4, sticky='ns')

        # opened md textbox and clear button
        self.text['opened'] = tk.Text(
            self,
            wrap='word',
            state='disabled')
        self.text['opened'].grid(row=1, column=0)
        self.btn['clear0'] = ttk.Button(
            self,
            text='clear',
            command=lambda: self.clear0())
        self.btn['clear0'].grid(row=2, column=0)

        # converted md textbox,clear and save button
        self.text['converted'] = tk.Text(
            self,
            wrap='word',
            state='disabled')
        self.text['converted'].grid(row=1, column=2)
        self.btn['clear1'] = ttk.Button(
            self,
            text='clear',
            command=lambda: self.clear1())
        self.btn['clear1'].grid(row=3, column=2)
        self.btn['save'] = ttk.Button(
            self,
            text='save',
            command=lambda: self.save_html())
        self.btn['save'].grid(row=2, column=2)

    def open_markdown(self):
        file = filedialog.askopenfilename(
            title='Open a file',
            filetypes=(("markdown files", "*.md*"),)
        )
        if file:
            self.file = file
            self.text['opened'].config(state='normal')
            self.text['opened'].delete(1.0, 'end')
            with open(self.file, 'r') as f:
                self.text['opened'].\
                    insert(tk.INSERT, f.read())
            self.text['opened'].config(state='disabled')

    def convert_html(self):
        try:
            file = self.file
            response = True
        except:
            response = False

        if response == True:
            self.text['converted'].config(state='normal')
            self.text['converted'].delete(1.0, 'end')
            with open(file, 'r') as f:
                text = f.read()
                self.html = markdown.\
                    markdown(text, extensions=['md_in_html'])

                self.text['converted'].\
                    insert(tk.INSERT, self.html)

            self.text['converted'].config(state='disabled')
        else:
            tk.messagebox.showinfo(
                'Info',
                'Please open a file first before proceeding!'
            )

    def save_html(self):
        c_file = filedialog.asksaveasfilename(
            title='Enter name of new file',
            defaultextension='.html',
            filetypes=(("Html files", "*.html*"),)
        )

        if c_file:
            try:
                with open(c_file, 'w') as f:
                    f.write(self.html)
            except:
                tk.messagebox.showinfo(
                    'Info',
                    'Make sure you have converted the file first!'
                )
                os.remove(c_file)

    def clear0(self):
        self.text['opened'].config(state='normal')
        self.text['opened'].delete(1.0, 'end')
        self.text['opened'].config(state='disabled')

    def clear1(self):
        self.text['converted'].config(state='normal')
        self.text['converted'].delete(1.0, 'end')
        self.text['converted'].config(state='disabled')


class App(tk.Tk):
    """creates window"""

    def __init__(self, *args, **kwargs):
        """initializes super class and attributes"""
        super().__init__(*args, **kwargs)

        self.style = ttk.Style()
        self.style.theme_use('superhero')
        self.style.configure('TEntry', foreground='white')
        d_font = tk.font.nametofont('TkDefaultFont')
        d_font.configure(size=11, family='Helvetica')

        self.title('Markdown To Html')
        self.geometry('720x640')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = MarkDownEngine(self)
        self.frame.grid(column=0, row=0, sticky='nsew')


if __name__ == "__main__":
    app = App()
    app.mainloop()
